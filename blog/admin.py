"""
Registers the Post model with the Django admin interface.
This file allows administrators to manage blog articles via the admin panel.
将 Post 模型注册到 Django 后台，使管理员可以在后台创建、编辑、删除博客文章。
"""
from django.contrib import admin
from .models import Post
from .models import Comment

admin.site.register(Comment)
class PostAdmin(admin.ModelAdmin):
    # 关键：把 created_on 改成 created_date（和模型一致）
    list_display = ('title', 'slug', 'status', 'created_date')
    list_filter = ("status",)
    search_fields = ['title', 'text']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)
    