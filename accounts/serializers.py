from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer

class CustomRegisterSerializer(RegisterSerializer):
    profile_image = serializers.ImageField()
    nickname = serializers.CharField()
    introduce = serializers.CharField()
    
    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        
        data['profile_image'] = self.validated_data.get('profile_image', '')
        data['nickname'] = self.validated_data.get('nickname', '')
        data['introduce'] = self.validated_data.get('introduce', '')
        
        return data