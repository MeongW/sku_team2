from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Post, Comment, PostLike, Category
from .serializers import PostSerializer, CommentSerializer, PostLikeSerializer, CategorySerializer
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from .permissions import IsAuthorOrReadonly, IsAuthorUpdateOrReadOnly
from rest_framework.generics import UpdateAPIView
from rest_framework import generics
from rest_framework.views import APIView



# Post의 목록, detail 보여주기, 수정하기, 삭제하기
class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

    def get_authentications(self):
        authentication_classes = list()
        action = self.action

        if action == 'list':
            authentication_classes = []
        elif action == 'create':
            authentication_classes = [TokenAuthentication]
        elif action == 'retrieve':
            authentication_classes = []
        elif action == 'update':
            authentication_classes = [TokenAuthentication]
        elif action == 'partial_update':
            authentication_classes = [TokenAuthentication]
        elif action == 'distory':
            authentication_classes = [TokenAuthentication]
        return [authentication() for authentication in authentication_classes]

    
    def get_permissions(self):
        permission_classes = list()
        action = self.action
        
        if action == 'list':
            permission_classes = [AllowAny] # 인증 / 비인증 모두 허용
        elif action == 'create':
            permission_classes = [IsAuthenticated] # 인증된 요청에서만 veiw 호출
        elif action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif action == 'update':
            permission_classes = [IsAdminUser] # Staff User에 대해서만 요청 허용
        elif action == 'partial_update':
            permission_classes = [IsAdminUser]
        elif action == 'distory':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
        


# Post 한 게시물에 댓글 목록 보기, 작성, 수정, 삭제
class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_authentications(self):
        authentication_classes = list()
        action = self.action    
        if action == 'list':
            authentication_classes = []
        elif action == 'create':
            authentication_classes = [TokenAuthentication]
        elif action == 'retrieve':
            authentication_classes = []
        elif action == 'update':
            authentication_classes = [TokenAuthentication]
        elif action == 'partial_update':
            authentication_classes = [TokenAuthentication]
        elif action == 'distory':
            authentication_classes = [TokenAuthentication]
        return [authentication() for authentication in authentication_classes]

    
    def get_permissions(self):
        permission_classes = list()
        action = self.action

        if action == 'list':
            permission_classes = [AllowAny] # 인증 / 비인증 모두 허용
        elif action == 'create':
            permission_classes = [IsAuthenticated] # 인증된 요청에서만 veiw 호출
        elif action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif action == 'update':
            permission_classes = [IsAdminUser] # Staff User에 대해서만 요청 허용
        elif action == 'partial_update':
            permission_classes = [IsAdminUser]
        elif action == 'distory':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)



# Post 한 게시물 좋아요
class PostLikeAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostLikeSerializer

    # update 메서드 오버라이딩
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # 내부에 like + 1 로직 추가 (이후 serializer의 data변수에 dict 형태로 넣어줌)
        data = {'like_count' : instance.like_count + 1}
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    


# Category
class CategoryViewSet(APIView):
    def get(self, request, format=None):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

# Category ID 값 당 게시글 찾기
class CategorySearchViewSet(APIView):
    def get(self, request, id, format=None):
        queryset = Post.objects.filter(category__id=id)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)