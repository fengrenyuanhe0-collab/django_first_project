# blog/views.py 完整修复版
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# 导入模型和表单（统一放在顶部，避免重复）
from .models import Post, Comment, UserProfile
from .forms import PostForm, CommentForm, UserProfileForm

from rest_framework import viewsets
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
# 1. 首页博客列表
class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    queryset = Post.objects.filter(status=1).order_by('-created_date')
    context_object_name = 'posts'

# 2. 博客详情
class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        context['comments'] = self.object.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        return context

# 3. 创建博客（修复后保留）
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # 关联登录用户为作者
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})

# 4. 注册视图（修复后保留）
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # 创建新用户
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')  # 注册成功跳登录页
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 5. 个人资料视图（修复后保留）
@login_required
def profile_view(request):
    # 获取或创建当前用户的个人资料
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form})

# 6. 添加评论（合并两个版本，用Form验证，修复重复定义问题）
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        # 用CommentForm验证数据，更规范
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user  # 关联评论用户
            comment.active = True
            comment.name = request.user.username  # 填充评论者名称
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', slug=post.slug)
        else:
            # 表单验证失败时提示错误
            messages.error(request, 'Failed to add comment: Please check your input!')
    # GET请求或表单验证失败，返回文章详情页
    return redirect('post_detail', slug=post.slug)

# 7. 点赞评论（修复缺少return的问题）
@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # 优化：避免重复点赞（可选，增强体验）
    if request.user not in comment.likes.all():
        comment.likes.add(request.user)  # 用ManyToMany的add方法（你的原代码用+=是错的！）
        messages.success(request, 'Liked comment!')
    else:
        messages.error(request, 'You already liked this comment!')
    comment.save()
    # 核心修复：添加return
    return redirect('post_detail', slug=comment.post.slug)

# 博客文章API视图集
class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.filter(status=1).order_by('-created_date')
    serializer_class = PostSerializer

# 评论API视图集（可选）
class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Comment.objects.filter(active=True).order_by('-created_on')
    serializer_class = CommentSerializer