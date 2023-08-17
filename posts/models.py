from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()

def blog_image_upload_path(instance, filename):
    return f'media/{instance.post.pk}/iamges/{filename}'


class Category(models.Model):
    name = models.CharField(verbose_name='카테고리', max_length=20, null=False)

    def __str__(self) -> str:
        return f"Category Name: {self.name}"

class PostImage(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/tmp/', null=True, blank=True)

class Post(models.Model):
    title = models.CharField(verbose_name='제목', max_length=50)
    images = models.ManyToManyField(PostImage, blank=True)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    content = RichTextUploadingField(blank=True,null=True) # ckeditor
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    like_users = models.ManyToManyField(CustomUser, through='PostLike', related_name='liked_posts')
    like_count = models.PositiveBigIntegerField(default=0)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Title: {self.title}"

class Comment(models.Model):
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(verbose_name='작성일', auto_now_add=True)
    post = models.ForeignKey(to='Post', related_name='comments', on_delete=models.CASCADE)
    writer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='reply', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"Content: {self.content}"


class PostLike(models.Model):
    post = models.ForeignKey(to='Post', related_name='postlikes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=False)
    like_at = models.DateTimeField(verbose_name='생성일', auto_now_add=True)

    def __str__(self) -> str:
        return f"Like_At: {self.like_at}"
