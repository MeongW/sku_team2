import random

from .models import SMSAuthentication

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

from rest_framework import serializers

from dj_rest_auth.serializers import UserDetailsSerializer, PasswordChangeSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

UserModel = get_user_model()

class CustomPasswordResetSerializer(PasswordChangeSerializer):
    auth_answer = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=11, validators=[
        RegexValidator(regex=r"^01([0|1|6|7|8|9])?\d{3,4}?\d{4}$", message='전화번호 형식이 잘못되었습니다.')
    ])
    username = serializers.CharField()

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        extra_fields = []
        if hasattr(UserModel, 'USERNAME_FIELD'):
            extra_fields.append(UserModel.USERNAME_FIELD)
        if hasattr(UserModel, 'EMAIL_FIELD'):
            extra_fields.append(UserModel.EMAIL_FIELD)
        if hasattr(UserModel, 'first_name'):
            extra_fields.append('first_name')
        if hasattr(UserModel, 'last_name'):
            extra_fields.append('last_name')
        if hasattr(UserModel, 'profile_image'):
            extra_fields.append('profile_image')
        if hasattr(UserModel, 'phone_number'):
            extra_fields.append('phone_number')
        if hasattr(UserModel, 'nickname'):
            extra_fields.append('nickname')
        if hasattr(UserModel, 'introduce'):
            extra_fields.append('introduce')
        
        
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)

class CustomRegisterSerializer(RegisterSerializer):
    profile_image = serializers.ImageField(use_url=True, required=False)
    phone_number = serializers.CharField(max_length=11, validators=[
        RegexValidator(regex=r"^01([0|1|6|7|8|9])?\d{3,4}?\d{4}$", message='전화번호 형식이 잘못되었습니다.')
    ])
    nickname = serializers.CharField()
    introduce = serializers.CharField()
    auth_answer = serializers.CharField()
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        
        data['profile_image'] = self.validated_data.get('profile_image', '')
        data['phone_number'] = self.validated_data.get('phone_number', '')
        data['nickname'] = self.validated_data.get('nickname', '')
        data['introduce'] = self.validated_data.get('introduce', '')
        data['auth_answer'] = self.validated_data.get('auth_answer', '')
        
        return data

class SMSSendSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=11, validators=[
        RegexValidator(regex=r"^01([0|1|6|7|8|9])?\d{3,4}?\d{4}$", message='전화번호 형식이 잘못되었습니다.')
    ])
    
    class Meta:
        model = SMSAuthentication
        fields = ['phone_number',]

class SMSAuthConfirmSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=11, validators=[
        RegexValidator(regex=r"^01([0|1|6|7|8|9])?\d{3,4}?\d{4}$", message='전화번호 형식이 잘못되었습니다.')
    ])
    auth_number = serializers.IntegerField(min_value=1000, max_value=9999)
    class Meta:
        model = SMSAuthentication
        fields = ['phone_number', 'auth_number',]