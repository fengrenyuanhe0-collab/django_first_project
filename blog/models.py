# blog/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# 用户资料：昵称、头像
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.nickname or self.user.username
        
# 博客文章模型
class Post(models.Model):
    STATUS_CHOICES = (
        (0, 'Draft'),
        (1, 'Publish'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

# 评论模型
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField()
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-likes', '-created_on']

    def __str__(self):
        if self.user:
            return f'Comment by {self.user.username} on {self.post.title}'
        return f'Anonymous comment on {self.post.title}'