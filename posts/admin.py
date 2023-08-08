from django.contrib import admin

from .models import Post, Comment

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    pass