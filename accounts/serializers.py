from django.contrib.auth import get_user_model

from rest_framework import serializers


from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer

UserModel = get_user_model()

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
        if hasattr(UserModel, 'nickname'):
            extra_fields.append('nickname')
        if hasattr(UserModel, 'introduce'):
            extra_fields.append('introduce')
            
        model = UserModel
        fields = ('pk', *extra_fields)
        read_only_fields = ('email',)

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField()
    profile_image = serializers.ImageField(use_url=True, required=False)
    nickname = serializers.CharField()
    introduce = serializers.CharField()
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        
        data['email'] = self.validated_data.get('email', '')
        data['profile_image'] = self.validated_data.get('profile_image', '')
        data['nickname'] = self.validated_data.get('nickname', '')
        data['introduce'] = self.validated_data.get('introduce', '')
        
        return data