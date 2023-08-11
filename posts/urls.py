from django.urls import path, include
from rest_framework import routers
from rest_framework import urls

from .views import PostViewSet, CommentViewSet, CommentOnlyViewSet


router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'reply/comments', CommentOnlyViewSet)


urlpatterns = [
    path('', include(router.urls)),
]