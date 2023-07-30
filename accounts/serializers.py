from django.contrib.auth import get_user_model

from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as JwtTokenObtainPairSerializer

class CustomUserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password',
        ]

class CustomUserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password',
            'name',
            'age',
        ]

class TokenObtainPairSerializer(JwtTokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD
