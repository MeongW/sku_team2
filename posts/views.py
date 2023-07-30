from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import api_view, APIView ,action
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsOwner

from .models import Post
from .serializers import (
    PostBaseModelSerializer, 
    PostListModelSerializer, 
    PostRetrieveModelSerializer, 
    CommentListModelSerializer,
    LikeModelSerializer,
)


# 게시글 목록 + 생성
class PostListCreateView(generics.ListAPIView, generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListModelSerializer
    
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_authenticated:
            serializer.save(writer=request.user)
        else:
            serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 게시글 상세, 수정, 삭제
class PostRetrieveUpdateView(generics.RetrieveAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostRetrieveModelSerializer

# 게시글 좋아요
class PostLikeView(APIView):
    serializer_class = LikeModelSerializer
    
    def post(self, request):
        data = request.data
        user = request.user
        post_id = data.get('post', None)
        
        
        post = Post.objects.get(id=post_id)
        
        if post.like_users.filter(id=user.id).exists():
            post.like_users.remove(user)
        else:
            post.like_users.add(user)

        like_count = post.liked_users.count()
        
        return Response({'like_count': like_count})

class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostListModelSerializer
    
    '''
    def get_serializer_class(self):
        if self.action == 'create':
            return PostBaseModelSerializer
        return super().get_serializer_class()
    '''
    '''
    def get_permissions(self):
        permission_classes = list()
        action = self.action
        if action == 'list':
            permission_classes = [AllowAny]
        elif action == 'create':
            permission_classes = [IsAuthenticated]
        elif action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif action == 'update':
            permission_classes = [IsOwner]
        elif action == 'partial_update':
            permission_classes = [IsOwner]
        elif action == 'destroy':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
    '''
    @action(detail=True, methods=['get'])
    def get_comment_all(self, request, pk=None):
        post = self.get_object()
        comment_all = post.comment_set.all()
        serializer = CommentListModelSerializer(comment_all, many=True)
        
        return Response(serializer.data)