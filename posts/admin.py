from django.contrib import admin

from .models import Post, Comment, PostLike, Category

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    pass

@admin.register(PostLike)
class PostLikeModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass