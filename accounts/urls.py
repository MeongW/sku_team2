from django.urls import path, include
from .views import SMSAuthSendView, SMSAuthConfirmView, CustomPasswordResetView

from dj_rest_auth.views import (
    UserDetailsView,
    PasswordChangeView,
    PasswordResetConfirmView,
    LoginView,
    LogoutView,
)
from dj_rest_auth.registration.views import RegisterView

urlpatterns = [
    path('dj-rest-auth/login/', LoginView.as_view(), name='rest_login'),
    path('dj-rest-auth/logout/', LogoutView.as_view(), name='rest_logout'),
    path('dj-rest-auth/user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('dj-rest-auth/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('dj-rest-auth/password/reset/', CustomPasswordResetView.as_view(), name='rest_password_reset'),
    path('dj-rest-auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    
    
    path('dj-rest-auth/registration/', RegisterView.as_view(), name='rest_register'),
    
    path('social/', include('allauth.urls')),
    
    path('smsauth/send', SMSAuthSendView.as_view(), name='sms_auth_send'),
    path('smsauth/confirm', SMSAuthConfirmView.as_view(), name="sms_auth_confirm"),
    #path('social/kakao/', KakaoLogin.as_view(), name="kakao_login"),
    #path('social/kakao/callback', KakaoCallBackView.as_view(), name="kakao_callback"),
]