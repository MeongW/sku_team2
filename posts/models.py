from django.db import models
from django.contrib.auth import get_user_model

from accounts.models import CustomUser

User = get_user_model()

def blog_image_upload_path(instance, filename):
    return f'media/{instance.post.pk}/iamges/{filename}'


class Category(models.Model):
    name = models.CharField(verbose_name='카테고리', max_length=20, null=True)

    def __str__(self):
        return self.name

class PostImage(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/tmp/', null=True, blank=True)

class Post(models.Model):
    title = models.CharField(verbose_name='제목', max_length=50)
    images = models.ManyToManyField(PostImage)
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    view_count = models.IntegerField(verbose_name='조회수', default=0)
    like_users = models.ManyToManyField(CustomUser, through='PostLike', related_name='liked_posts')
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    like_count = models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    post = models.ForeignKey(to='Post', related_name='comments', on_delete=models.CASCADE)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='reply', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.content

class PostLike(models.Model):
    post = models.ForeignKey(to='Post', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    like_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)

    def __str__(self):
        return self.like_at