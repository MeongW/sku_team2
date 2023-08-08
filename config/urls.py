from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="http://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),   
    
    path('api/accounts/', include('accounts.urls')),
    path('api/posts/', include('posts.urls')),

    path('api_auth/', include('rest_framework.urls')),

    path('jwt-token-auth/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('jwt-token-auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt-token-auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
