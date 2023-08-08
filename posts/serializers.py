from .models import Post, Comment, PostLike
from rest_framework.serializers import ModelSerializer, ReadOnlyField

class PostSerializer(ModelSerializer):
    # 작성자를 서버에 자동으로 넘겨준다.
    writer = ReadOnlyField(source='wirter.nickname')

    class Meta:
        model = Post
        fields = ['title', 'image', 'content', 'created_at', 'view_count', 'like_users', 'writer']

class CommentSerializer(ModelSerializer):
    # 작성자를 서버에 자동으로 넘겨준다.
    writer = ReadOnlyField(source='wirter.nickname')

    class Meta:
        model = Comment
        fields = ['post', 'content', 'created_at', 'writer']