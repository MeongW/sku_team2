from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from posts.views import CategoryViewSet, CategorySearchViewSet, PostlikeViewSet, SearchPostList


schema_view = get_schema_view(
    openapi.Info(
        title="Service Tori API",
        default_version='v1',
        description="Test description",
        terms_of_service="http://www.google.com/policies/terms/",
        contact=openapi.Contact(email="servicetori@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    url=f'{settings.BASE_URL}/swagger/',
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ckeditor/', include('ckeditor_uploader.urls')), # ckeditor
    
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),   
    
    path('api/accounts/', include('accounts.urls')),
    path('api/posts/', include('posts.urls'), name='post-list'),

    path('api/posts/posts/<int:id>/like/', PostlikeViewSet.as_view(), name='post-like'),
    path('api/category/', CategoryViewSet.as_view(), name='post-category'),
    path('api/category/<int:id>', CategorySearchViewSet.as_view(), name='post-category-search'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
