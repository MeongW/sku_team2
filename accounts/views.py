from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView

from dj_rest_auth.registration.views import RegisterView


'''
@permission_classes([AllowAny])
class SignUpView(generics.CreateAPIView):
    serializer_class = CustomUserSignUpSerializer
    
    def create(self, request):
        email = request.POST['email']
        password = request.POST['password']
        
        pa

@permission_classes([AllowAny])
class LoginView(APIView):
    serializer_class = CustomUserLoginSerializer
    
    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(
            request,
            email=email,
            password=password,
        )
        
        if user is not None:
            serializer = CustomUserLoginSerializer(user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            return res
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            
'''