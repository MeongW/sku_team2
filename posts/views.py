from django.shortcuts import redirect
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from .permissions import IsAuthorOrReadonly, IsAuthorUpdateOrReadOnly

# Post의 목록, detail 보여주기, 수정하기, 삭제하기
class PostViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorUpdateOrReadOnly,]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

# Post 한 게시물에 댓글 작성하기
class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = []
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorUpdateOrReadOnly,]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)
        
# Post 한 게시물 좋아요