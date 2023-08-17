from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Post, Comment, PostLike, Category, PostImage
from .permissions import IsAuthorOrReadonly, IsAuthorUpdateOrReadOnly
from .serializers import PostSerializer, CommentSerializer, CategorySerializer, BoardOnlySerializer, PostImageSerializer
from rest_framework import viewsets, status, permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import UpdateAPIView
from rest_framework import generics
from rest_framework.views import APIView
import os


# Post의 목록, detail 보여주기, 수정하기, 삭제하기
class PostViewSet(viewsets.ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)

    def list(self, request, *args, **kwargs):

        posts = Post.objects.all()

        # 마이페이지 - 작성한글 / 댓글 단 글 / 좋아요한 글
        mypage = request.query_params.get('mypage')
        if mypage == 'posts':
            if request.user.is_authenticated:
                nickname = request.user.username
                posts = posts.filter(writer__username=nickname)
        elif mypage == 'comments':
            if request.user.is_authenticated:
                nickname = request.user.username
                posts = posts.filter(comments__writer__username=nickname).distinct()
        elif mypage == 'likes':
            if request.user.is_authenticated:
                nickname = request.user.username
                posts = posts.filter(postlikes__user__username=nickname)
        else:
            posts


        #카테고리 별 아이디 값으로 해당 게시글 보이기
        categoryId = request.query_params.get('categoryId', '')
        if categoryId != '':
            category = Category.objects.filter(pk=categoryId).first()
            posts = posts.filter(category=category)


        # 좋아요 순 / 최신 순 정렬
        order = request.query_params.get('order')
        if order == 'popular':
            posts = posts.order_by('-like_count')
        else:
            posts = posts.order_by('-created_at')
        
        
        serializer = PostSerializer(posts, many=True)
        
        return Response(serializer.data)


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
            permission_classes = [IsAuthorOrReadonly]
        elif action == 'retrieve':
            permission_classes = [AllowAny]
        elif action == 'update':
            permission_classes = [IsAuthorOrReadonly]
        elif action == 'partial_update':
            permission_classes = [IsAuthorOrReadonly]
        elif action == 'distory':
            permission_classes = [IsAuthorOrReadonly]
        return [permission() for permission in permission_classes]
    
    def update(self, request, *args, **kwargs):
        post = self.get_object()
        old_images = set(post.images.all())
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            new_images = set(post.images.all())
            unused_images = old_images - new_images
            for img in unused_images:
                img.file.delete(save=True)
                img.delete()
        return response

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        images = post.images.all()

        response = super().destroy(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            for img in images:
                img.file.delete(save=True)
                img.delete()
        return response
    def get_serializer_class(self):
        if self.action == 'create':
            return PostImageSerializer
        return super().get_serializer_class()
    


# 이미지
class PostImageViewSet(viewsets.ModelViewSet):
    queryset = PostImage.objects.all()
    serializer_class = PostImageSerializer
    parser_classes = [MultiPartParser]
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        file_obj = request.data['image']
        image = PostImage.objects.create(image=file_obj, owner=request.user)
        data = {'url': settings.BASE_URL + image.image.url, 'id': image.pk}
        return Response(data, status=201)





# Post 한 게시물에 댓글 목록 보기, 작성, 수정, 삭제
class CommentViewSet(viewsets.ModelViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    
    def list(self ,request, *args, **kwargs):
        comments = Comment.objects.all()

        postId = request.query_params.get('postId', '')

        # 현재 게시물 id값 받아와서 해당 게시물의 댓글 보여주기
        if postId != '':
            post = Post.objects.filter(pk=postId).first()
            comments = Comment.objects.filter(post=post)


        # 댓글 등록 순 / 최신 순 정렬
        order = request.query_params.get('order')
        if order == 'newest':
            comments = comments.order_by('-created_at')
        elif order == 'registration':
            comments
        else:
            comments
        
        serializer = self.get_serializer(comments, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

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
            permission_classes = [IsAuthorOrReadonly] # 인증된 요청에서만 veiw 호출
        elif action == 'retrieve':
            permission_classes = [AllowAny]
        elif action == 'update':
            permission_classes = [IsAuthorOrReadonly] # Staff User에 대해서만 요청 허용
        elif action == 'partial_update':
            permission_classes = [IsAuthorOrReadonly]
        elif action == 'distory':
            permission_classes = [IsAuthorOrReadonly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)



## Post 한 게시물 좋아요 / 좋아요 수
class PostlikeViewSet(APIView):

    #authentication_classes = []
    permission_classes = [IsAuthenticated]

    def post(self, request, id, format=None):
        post = Post.objects.get(id=id)
        if post.like_users.values().filter(username=request.user.username):
            recommanded = PostLike.objects.filter(post=post, user=request.user)
            recommanded.delete()
        else:
            PostLike.objects.create(post=post, user=request.user)

        post.like_count = PostLike.objects.values().filter(post=post).count()
        post.save()

        return Response(post.like_count)


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


# 대댓글 보여주기
class CommentOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all()
    serializer_class = BoardOnlySerializer
    permission_classes = [AllowAny]
