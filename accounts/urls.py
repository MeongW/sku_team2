from django.urls import path, include
from .views import SMSAuthSendView, SMSAuthConfirmView

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('social/', include('allauth.urls')),
    
    path('smsauth/send', SMSAuthSendView.as_view(), name='sms_auth_send'),
    path('smsauth/confirm', SMSAuthConfirmView.as_view(), name="sms_auth_confirm")
    #path('social/kakao/', KakaoLogin.as_view(), name="kakao_login"),
    #path('social/kakao/callback', KakaoCallBackView.as_view(), name="kakao_callback"),
]