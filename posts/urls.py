from django.urls import path, include
from rest_framework import routers
from rest_framework import urls

from .views import PostViewSet, CommentViewSet, CommentOnlyViewSet, PostImageViewSet


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'reply/comments', CommentOnlyViewSet)
router.register(r'images', PostImageViewSet)


urlpatterns = [
    path('', include(router.urls)),
]