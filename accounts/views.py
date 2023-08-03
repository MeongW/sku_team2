from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter, KakaoProvider
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter

from django.conf import settings

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.utils import user_username


from dj_rest_auth.registration.views import SocialLoginView


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def get_signup_form_initial_data(self, sociallogin):
        user = sociallogin.user
        initial = {
            "username": user_username(user) or "",
        }
        return initial