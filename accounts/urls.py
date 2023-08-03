from django.urls import path, include

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),

    path('social/', include('allauth.urls')),
    
    #path('social/kakao/', KakaoLogin.as_view(), name="kakao_login"),
    #path('social/kakao/callback', KakaoCallBackView.as_view(), name="kakao_callback"),
]