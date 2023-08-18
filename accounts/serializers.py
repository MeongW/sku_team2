import bcrypt

from .models import SMSAuthentication

from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.conf import settings

from rest_framework import serializers

from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

UserModel = get_user_model()

class CustomPasswordResetSerializer(serializers.Serializer):
    auth_answer = serializers.CharField(max_length=100)
    phone_number = serializers.CharField(max_length=11, validators=[
        RegexValidator(regex=r"^01([0|1|6|7|8|9])?\d{3,4}?\d{4}$", message='전화번호 형식이 잘못되었습니다.')
    ], required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    username = serializers.CharField()

class CustomUserDetailsSerializer(UserDetailsSerializer):

    nickname = serializers.CharField(max_length=32)
    introduce = serializers.CharField(max_length=50)
    profile_image = serializers.ImageField(use_url=True)
    class Meta:
        extra_fields = ['username', 'email', 'profile_image', 'phone_number', 'nickname', 'introduce', ]
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email', 'username', 'phone_number')

class CustomRegisterSerializer(RegisterSerializer):
    profile_image = serializers.ImageField(use_url=True, required=False)
    phone_number = serializers.CharField(max_length=11, validators=[
        RegexValidator(regex=r"^01([0|1|6|7|8|9])?\d{3,4}?\d{4}$", message='전화번호 형식이 잘못되었습니다.')
    ])
    nickname = serializers.CharField()
    introduce = serializers.CharField()
    auth_answer = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True)
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        
        data['profile_image'] = self.validated_data.get('profile_image', '')
        data['phone_number'] = self.validated_data.get('phone_number', '')
        data['nickname'] = self.validated_data.get('nickname', '')
        data['introduce'] = self.validated_data.get('introduce', '')
        data['auth_answer'] = bcrypt.hashpw(self.validated_data.get('auth_answer', '').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
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
    auth_number = serializers.IntegerField()
    class Meta:
        model = SMSAuthentication
        fields = ['phone_number', 'auth_number']

class FindUserNameSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, validators=[
        RegexValidator(regex=r"^01([0|1|6|7|8|9])?\d{3,4}?\d{4}$", message='전화번호 형식이 잘못되었습니다.')
    ])

class SendUserNameSerializer(serializers.Serializer):
    email = serializers.EmailField()
