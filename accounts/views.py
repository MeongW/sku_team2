from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.models import SocialAccount
from allauth.account.forms import EmailAwarePasswordResetTokenGenerator

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string

from json.decoder import JSONDecodeError

from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.app_settings import api_settings

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from dj_rest_auth.views import PasswordResetView

import requests

from .serializers import (
    SMSSendSerializer, 
    SMSAuthConfirmSerializer, 
    FindUserNameSerializer, 
    SendUserNameSerializer,
    CustomPasswordResetSerializer,
)
from .models import SMSAuthentication
from .permissions import IsUserInfoMatched, IsSMSAuthenticated


CustomUser = get_user_model()

class CustomPasswordResetView(generics.GenericAPIView):
    permission_classes = [IsUserInfoMatched, ]
    serializer_class = CustomPasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        
        default_token_generator = EmailAwarePasswordResetTokenGenerator()
        try:
            user = CustomUser.objects.get(username=username)
            
            try:
                temp_key = default_token_generator.make_token(user)
            except:
                return Response({'success': False, 'detail': 'Token generator error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({'uid': user.pk, 'token': temp_key}, status=status.HTTP_200_OK)
        
        except user.DoesNotExist:
            return Response({'success': False, 'detail': 'Cannot found user.'}, status=status.HTTP_400_BAD_REQUEST)
        

class SMSAuthSendView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SMSSendSerializer
    
    def post(self, request):
        data = request.data
        
        serializer = SMSSendSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        
        try:
            auth_user = CustomUser.objects.get(phone_number=phone_number)

            sms_auth = SMSAuthentication.objects.filter(phone_number=phone_number).first()
            
            if sms_auth:
                sms_auth.delete()
            SMSAuthentication.objects.create(phone_number=phone_number, is_authenticated = False)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except auth_user.DoesNotExist:
            return Response({'success':False, 'detail': 'User does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

class SMSAuthConfirmView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SMSAuthConfirmSerializer
    def post(self, request):
        data = request.data
        serializer = SMSAuthConfirmSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        auth_number = serializer.validated_data['auth_number']
        
        result = SMSAuthentication.check_auth_number(phone_number, auth_number)
        
        SMSAuthentication.objects.filter(phone_number=phone_number).update(is_authenticated=result)
        
        if result:
            return Response({'success': result, 'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'success': result, 'data': serializer.data}, status=status.HTTP_400_BAD_REQUEST)

class FindUserNameView(generics.GenericAPIView):
    permission_classes = [IsSMSAuthenticated, ]
    serializer_class = FindUserNameSerializer
    
    def post(self, request):
        data = request.data
        serializer = FindUserNameSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        phone_number = serializer.validated_data['phone_number']
        
        result = CustomUser.objects.filter(phone_number=phone_number).first()
        
        if SocialAccount.objects.filter(user=result).first():
            return Response({'success': False, 'detail': 'Social account user.'}, status=status.HTTP_400_BAD_REQUEST)

        if result:
            result = result.username
            SMSAuthentication.objects.filter(phone_number=phone_number).delete()
            return Response({'success': True, 'username': result, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

class SendUserNameView(generics.GenericAPIView):
    permission_classes = [AllowAny, ]
    serializer_class = SendUserNameSerializer
    
    def post(self, request):
        data = request.data
        serializer = SendUserNameSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        
        if serializer.is_valid():
            pass
        else:
            return Response({'success': False, 'detail': 'Email field error.'}, status=status.HTTP_400_BAD_REQUEST)
        
        result = CustomUser.objects.filter(email=email).first()
        
        if SocialAccount.objects.filter(user=result).first():
            return Response({'success': False, 'detail': 'Social account user.'}, status=status.HTTP_400_BAD_REQUEST)

        if result:
            result = result.username
            subject = "[토리] 계정 찾기 아이디 정보입니다."
            message = render_to_string('accounts/email/email_finduser.html', {'username': result})
            to = [email, ]
            try:
                send_mail(subject, "_", settings.DEFAULT_FROM_EMAIL, to, html_message=message)
                return Response({'success': True}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'success': False, 'detail': 'Email sending failed.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'success': False, 'detail': 'Cannot found account.'}, status=status.HTTP_400_BAD_REQUEST)

class DeleteAccount(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()

        return Response({"success": True}, status=status.HTTP_200_OK)

BASE_URL = settings.BASE_URL

KAKAO_CALLBACK_URI = f"{BASE_URL}/api/accounts/social/kakao/callback"

@api_view(["GET"])
@permission_classes([AllowAny])
def kakao_callback(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    client_secret = getattr(settings, 'KAKAO_CLIENT_SECRET')
    code = request.GET.get("code")
    redirect_uri = KAKAO_CALLBACK_URI
    
    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={rest_api_key}&redirect_uri={redirect_uri}&code={code}&client_secret={client_secret}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    
    profile_request = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    profile_json = profile_request.json()
    error = profile_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    uid = str(profile_json.get("id"))
    
    try:
        social_account = SocialAccount.objects.filter(uid=uid, provider='Kakao')
        
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}/api/accounts/social/kakao/login/finish", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        
        accept_json = accept.json()
        accept_json.pop('user', None)
        
        return Response(accept_json, status=status.HTTP_200_OK)
    
    except social_account.DoesNotExist:
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}/api/accounts/social/kakao/login/finish", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)

        return Response(accept_json, status=status.HTTP_201_CREATED)

class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI

def kakao_login(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri=https://servicetori.site/html/callback&response_type=code"
    )

NAVER_CALLBACK_URI = f"{BASE_URL}/api/accounts/social/naver/callback"

@api_view(["GET"])
@permission_classes([AllowAny])
def naver_callback(request):
    rest_api_key = getattr(settings, 'NAVER_CLIENT_ID')
    client_secret = getattr(settings, 'NAVER_CLIENT_SECRET')
    code = request.GET.get("code")
    state = request.GET.get("state")
    redirect_uri = NAVER_CALLBACK_URI
    
    token_req = requests.get(
        f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={rest_api_key}&client_secret={client_secret}&code={code}&state={state}"
    )
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get("access_token")
    
    profile_request = requests.post(
        "https://openapi.naver.com/v1/nid/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    
    profile_json = profile_request.json()
    print(profile_json)
    error = profile_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    uid = str(profile_json.get("response").get("id"))
    print(uid)

    try:
        social_account = SocialAccount.objects.filter(uid=uid, provider='Naver')
        
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}/api/accounts/social/naver/login/finish", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        
        accept_json = accept.json()
        accept_json.pop('user', None)
        
        return Response(accept_json, status=status.HTTP_200_OK)
    
    except social_account.DoesNotExist:
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}/api/accounts/social/naver/login/finish", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        
        return Response(accept_json, status=status.HTTP_201_CREATED)

class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    client_class = OAuth2Client
    callback_url = NAVER_CALLBACK_URI

def naver_login(request):
    rest_api_key = getattr(settings, 'NAVER_CLIENT_ID')
    return redirect(
        f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={rest_api_key}&redirect_uri={NAVER_CALLBACK_URI}&state=test"
    )
