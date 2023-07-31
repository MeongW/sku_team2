from django.urls import path, include
from rest_framework import routers

from .views import PostModelViewSet

router = routers.DefaultRouter()
router.register(r'', PostModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
]