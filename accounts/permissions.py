import bcrypt

from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import ValidationError

from .models import SMSAuthentication

from django.contrib.auth import get_user_model


class IsSMSAuthenticated(BasePermission):
    def has_permission(self, request, view):
        phone_number = request.data.get('phone_number')
        if phone_number == '':
            raise ValidationError("[phone_number]Invalid value.", code=status.HTTP_400_BAD_REQUEST)

        query_set = SMSAuthentication.objects.filter(phone_number=phone_number)
        if query_set:
            if query_set[0].is_authenticated:
                return True
        return False

class IsUserInfoMatched(BasePermission):
    def has_permission(self, request, view):
        User = get_user_model()
        
        username = request.data.get('username', '')
        auth_answer = request.data.get('auth_answer', '')
        phone_number = request.data.get('phone_number', '')
        email = request.data.get('email', '')
        
        if username == '':
            raise ValidationError("[auth_answer]Invalid value.", code=status.HTTP_400_BAD_REQUEST)
        if auth_answer == '':
            raise ValidationError("[auth_answer]Invalid value.", code=status.HTTP_400_BAD_REQUEST)

        if phone_number == '' and email == '':
            raise ValidationError("[phone_number or email]Invalid value.", code=status.HTTP_400_BAD_REQUEST)
        
        user_query_set = User.objects.filter(username=username, phone_number=phone_number, email=email).first()
        
        if not user_query_set:
            if phone_number == '':
                user_query_set = User.objects.filter(username=username, email=email).first()
            if email == '':
                user_query_set = User.objects.filter(username=username, phone_number=phone_number).first()
        
        
        if user_query_set:
            print(user_query_set.auth_answer)
            if bcrypt.checkpw(auth_answer.encode('utf-8'), (user_query_set.auth_answer).encode('utf-8')):
                return True
        return False