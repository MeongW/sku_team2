from .models import Post, Comment, Category, PostImage
from rest_framework.serializers import ModelSerializer, ReadOnlyField, SerializerMethodField


class CommentSerializer(ModelSerializer):
    # 작성자를 서버에 자동으로 넘겨준다.
    writer = ReadOnlyField(source='writer.nickname')

    reply = SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'post', 'writer', 'content', 'created_at', 'parent', 'reply']

    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data
    
class BoardOnlySerializer(ModelSerializer):
    parent_comments = SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'parent_comments')

    def get_parent_comments(self, obj):
        parent_comments = obj.comments.filter(parent=None)
        serializer = CommentSerializer(parent_comments, many=True)
        return serializer.data


class CategorySerializer(ModelSerializer):

    count = SerializerMethodField() # serializer에만 존재하는 필드

    class Meta:
        model = Category
        fields = ['id', 'name', 'count']

    def get_count(self, obj):
        return Post.objects.filter(category__name=obj.name).count()


class PostImageSerializer(ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['image']


class PostSerializer(ModelSerializer):
    # 작성자를 서버에 자동으로 넘겨준다.
    writer = ReadOnlyField(source='writer.nickname')

    # 카테고리 추가
    #category = CategorySerializer(many=False, read_only=True)
    #images = PostImageSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'images', 'writer', 'content', 'created_at', 'like_users', 'like_count', 'category']

class GetPostSerializer(ModelSerializer):
    writer = ReadOnlyField(source='writer.nickname')
    images = PostImageSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'title', 'images', 'writer', 'content', 'created_at', 'like_users', 'like_count', 'category']
