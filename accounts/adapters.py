import random

from django.core.exceptions import ObjectDoesNotExist

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import user_email
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        
        user = super().save_user(request, user, form, False)

        profile_image = data.get("profile_image")
        nickname = data.get("nickname")
        introduce = data.get("introduce")
        auth_answer = data.get("auth_answer")
        phone_number = data.get("phone_number")
        
        if profile_image:
            user.profile_image = profile_image

        if nickname:
            user.nickname = nickname
        
        if introduce:
            user.introduce = introduce
        
        if auth_answer:
            user.auth_answer = auth_answer
        
        if phone_number:
            user.phone_number = phone_number
        
        user.save()
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_signup_form_initial_data(self, sociallogin):
        user = sociallogin.user
        initial = {
            "username": user_email(user) or "",
        }
        return initial
    def pre_social_login(self, request, sociallogin):
        if sociallogin.is_existing:
            return Response({'detail': 'Social account is exist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        email = sociallogin.user.email
        if email:
            try:
                email_address = EmailAddress.objects.get(email=email)
                sociallogin.connect(request, email_address.user)
            except EmailAddress.DoesNotExist:
                pass
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        
        provider = sociallogin.account.provider
        uid = sociallogin.account.uid

        #if provider == 'kakao':
            #email = sociallogin.account.extra_data.get('kakao_account', {}).get('email', '')
            #nickname = sociallogin.account.extra_data.get('properties', {}).get('nickname', '')
        #if provider == 'naver':
            #email = sociallogin.account.extra_data.get('email', '')
            #nickname = sociallogin.account.extra_data.get('nickname','')
            #phone_number = sociallogin.account.extra_data.get('mobile', '').replace('-', '')


        while True:
            username = provider + '_' + str(random.randint(10000000, 100000000))
            try:
                CustomUser.objects.get(username=username)
            except ObjectDoesNotExist:
                user.username = username
                break

        while True:
            nickname = provider + '_' + str(random.randint(10000000, 100000000))
            try:
                CustomUser.objects.get(nickname=nickname)
            except ObjectDoesNotExist:
                user.nickname = nickname
                break
        
        user.save()
        
        return user
