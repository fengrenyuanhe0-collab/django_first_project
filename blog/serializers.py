from rest_framework import serializers
from .models import Post, Comment

# 博客文章序列化器
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'author', 'created_date', 'slug']

# 评论序列化器（可选）
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'name', 'body', 'created_on', 'active']