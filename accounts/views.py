from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter, KakaoProvider
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_username
from allauth.account.utils import user_email
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.views import ConnectionsView
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect

from json.decoder import JSONDecodeError

from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.views import PasswordChangeView
from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from dj_rest_auth.views import sensitive_post_parameters_m, UserDetailsView
from dj_rest_auth.app_settings import api_settings

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

import requests

from .serializers import SMSSendSerializer, SMSAuthConfirmSerializer, FindUserNameSerializer
from .models import SMSAuthentication
from .permissions import IsUserInfoMatched, IsSMSAuthenticated


CustomUser = get_user_model()

class CustomPasswordResetView(generics.GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.

    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = api_settings.PASSWORD_CHANGE_SERIALIZER
    permission_classes = (IsUserInfoMatched,)
    throttle_scope = 'dj_rest_auth'

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('New password has been saved.')})

class SMSAuthSendView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SMSSendSerializer
    
    def post(self, request):
        data = request.data
        
        serializer = SMSSendSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        sms_auth = SMSAuthentication.objects.filter(phone_number=serializer.validated_data['phone_number'])
        
        if sms_auth:
            sms_auth.delete()
        SMSAuthentication.objects.create(phone_number=serializer.validated_data['phone_number'], is_authenticated = False)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        
        result = CustomUser.objects.filter(phone_number=phone_number)
        
        if result:
            result = result[0].username
            return Response({'success': True, 'username': result, 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

BASE_URL = "http://localhost:8000/"

KAKAO_CALLBACK_URI = "http://localhost:8000/api/accounts/social/kakao/callback/"  # 프론트 로그인 URI 입력

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
    id = "kakao_" + uid
    
    try:
        social_account = SocialAccount.objects.filter(uid=uid, provider='Kakao')
        
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}api/accounts/social/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signin"}, status=accept_status)
        accept_json = accept.json()
        
        #print(accept_json)
        print(accept.headers['Set-Cookie'])
        
        accept_json.pop('user', None)
        
        return Response(accept_json, status=status.HTTP_200_OK)
    
    except social_account.DoesNotExist:
        # 기존에 가입된 유저가 없으면 새로 가입
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}api/accounts/social/kakao/login/finish/", data=data)
        accept_status = accept.status_code
        if accept_status != 200:
            return JsonResponse({"err_msg": "failed to signup"}, status=accept_status)

        accept_json = accept.json()
        accept_json.pop('user', None)
        print(accept.headers['Set-Cookie'])
        return Response(accept_json, status=status.HTTP_201_CREATED)



class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    client_class = OAuth2Client
    callback_url = KAKAO_CALLBACK_URI

def kakao_login(request):
    rest_api_key = getattr(settings, 'KAKAO_REST_API_KEY')
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={rest_api_key}&redirect_uri={KAKAO_CALLBACK_URI}&response_type=code"
    )