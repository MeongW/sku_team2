import bcrypt

from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import SMSAuthentication

from django.contrib.auth import get_user_model


class IsSMSAuthenticated(BasePermission):
    def has_permission(self, request, view):
        phone_number = request.data.get('phone_number')
        print(phone_number)
        query_set = SMSAuthentication.objects.filter(phone_number=phone_number)
        if query_set:
            if query_set[0].is_authenticated:
                return True
        return False

class IsUserInfoMatched(BasePermission):
    def has_permission(self, request, view):
        username = request.data.get('username')
        auth_answer = request.data.get('auth_answer')
        phone_number = request.data.get('phone_number')
        
        User = get_user_model()
        user_query_set = User.objects.filter(username=username, phone_number=phone_number)
        
        if user_query_set:
            print(user_query_set[0].auth_answer)
            if bcrypt.checkpw(auth_answer.encode('utf-8'), (user_query_set[0].auth_answer).encode('utf-8')):
                return True
        return False