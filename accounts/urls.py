from django.urls import path, include
from .views import (
    SMSAuthSendView, 
    SMSAuthConfirmView, 
    CustomPasswordResetView, 
    FindUserNameView,
    SendUserNameView,
    DeleteAccount,
    kakao_callback,
    kakao_login,
    KakaoLogin,
    naver_callback,
    naver_login,
    NaverLogin,
)

from dj_rest_auth.views import (
    UserDetailsView,
    PasswordChangeView,
    PasswordResetConfirmView,
    LoginView,
    LogoutView,
)
from dj_rest_auth.registration.views import RegisterView

from dj_rest_auth.jwt_auth import get_refresh_view
from rest_framework_simplejwt.views import TokenVerifyView


urlpatterns = [
    path('dj-rest-auth/login', LoginView.as_view(), name='rest_login'),
    path('dj-rest-auth/logout', LogoutView.as_view(), name='rest_logout'),
    path('dj-rest-auth/user', UserDetailsView.as_view(), name='rest_user_details'),
    path('dj_rest_auth/user/destroy', DeleteAccount.as_view(), name='rest_user_destroy'),
    path('dj-rest-auth/password/change', PasswordChangeView.as_view(), name='rest_password_change'),
    path('dj-rest-auth/password/reset', CustomPasswordResetView.as_view(), name='rest_password_reset'),
    path('dj-rest-auth/password/reset/confirm', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('dj-rest-auth/registration', RegisterView.as_view(), name='rest_register'),
    
    path('dj-rest-auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('dj-rest-auth/token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    
    path('social/kakao/callback', kakao_callback),
    path('social/kakao/login', kakao_login),
    path('social/kakao/login/finish', KakaoLogin.as_view()),
    
    path('social/naver/callback', naver_callback),
    path('social/naver/login', naver_login),
    path('social/naver/login/finish', NaverLogin.as_view()),

    path('smsauth/send', SMSAuthSendView.as_view(), name='sms_auth_send'),
    path('smsauth/confirm', SMSAuthConfirmView.as_view(), name="sms_auth_confirm"),

    path('finduser', FindUserNameView.as_view(), name='find_user'),
    path('finduser/send', SendUserNameView.as_view(), name='send_user'),
]
