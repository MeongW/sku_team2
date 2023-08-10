from .models import Post, Comment, PostLike, Category
from rest_framework.serializers import ModelSerializer, ReadOnlyField, SerializerMethodField


class CommentSerializer(ModelSerializer):
    # 작성자를 서버에 자동으로 넘겨준다.
    writer = ReadOnlyField(source='wirter.nickname')

    class Meta:
        model = Comment
        fields = ['post', 'content', 'created_at', 'writer']


class CategorySerializer(ModelSerializer):
    count = SerializerMethodField() # serializer에만 존재하는 필드

    class Meta:
        model = Category
        fields = ['name', 'count', 'id',]

    def get_count(self, obj):
        return Post.objects.filter(category__name=obj.name).count()


class PostLikeSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['like_count']


class PostSerializer(ModelSerializer):
    # 작성자를 서버에 자동으로 넘겨준다.
    writer = ReadOnlyField(source='wirter.nickname')
    # 댓글 추가
    comments = CommentSerializer(many=True, read_only=True)

    # 카테고리 추가
    category = CategorySerializer(many=False, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'image', 'content', 'created_at', 'view_count', 'like_users', 'like_count', 'writer', 'comments', 'category']