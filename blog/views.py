"""
blog应用视图
保留所有原有功能（登录/注册/评论/密码重置等），新增缓存和日志功能，页面显示英文
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
# 导入Django自带的密码重置视图（老师原版）
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import reverse_lazy
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# 新增：缓存装饰器（类视图/函数视图都适配）
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# 新增：日志模块
import logging

from .serializers import PostSerializer, CommentSerializer
from .forms import NewUserForm, PostForm, CommentForm, UserProfileForm
from .models import Post, Comment

# 新增：初始化日志器（记录blog所有操作）
logger = logging.getLogger('blog')

# ---------------------- 原有博客列表视图：新增缓存+日志 ----------------------
# @method_decorator(cache_page(60 * 5), name='dispatch')
class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    queryset = Post.objects.filter(status=1).order_by('-created_date')
    context_object_name = 'posts'

    # 新增：记录列表页访问日志
    def get(self, request, *args, **kwargs):
        logger.info(f'User accessed PostList | IP:{request.META.get("REMOTE_ADDR")} | User:{request.user.username or "anonymous"}')
        return super().get(request, *args, **kwargs)

# ---------------------- 原有博客详情视图：新增缓存+日志 ----------------------
#@method_decorator(cache_page(60 * 10), name='dispatch')  # 详情页缓存10分钟
class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self,** kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all().order_by('-created_on')
        context['comment_form'] = CommentForm()
        return context
    
    # 新增：记录详情页访问日志
    def get(self, request, *args, **kwargs):
        post_slug = kwargs.get('slug')
        logger.info(f'User accessed PostDetail | Slug:{post_slug} | IP:{request.META.get("REMOTE_ADDR")} | User:{request.user.username or "anonymous"}')
        return super().get(request, *args, **kwargs)

# ---------------------- 原有API视图：保留无修改（API一般不缓存） ----------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# ---------------------- 原有登录视图：新增日志 ----------------------
def login_request(request):
    # 新增：记录登录请求日志
    logger.info(f'Login attempt | IP:{request.META.get("REMOTE_ADDR")} | Method:{request.method}')
    
    # 处理POST请求（用户提交登录表单）
    if request.method == "POST":
        # 获取表单提交的邮箱和密码
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # 根据邮箱查询用户（Django默认用username登录，需转换）
            user = User.objects.get(email=email)
            # 验证密码是否正确
            authenticated_user = authenticate(username=user.username, password=password)

            if authenticated_user:
                # 登录成功，跳转到首页（删除main:前缀）
                login(request, authenticated_user)
                messages.success(request, "Login successful!")
                # 新增：记录登录成功日志
                logger.info(f'Login success | Email:{email} | User:{user.username} | IP:{request.META.get("REMOTE_ADDR")}')
                return redirect("homepage")  # 修复：main:homepage → homepage
            else:
                # 密码错误提示
                messages.error(request, "Incorrect password!")
                # 新增：记录登录失败日志
                logger.warning(f'Login failed | Email:{email} | Reason: Incorrect password | IP:{request.META.get("REMOTE_ADDR")}')
        except User.DoesNotExist:
            # 邮箱未注册提示
            messages.error(request, "Email not registered!")
            # 新增：记录登录失败日志
            logger.warning(f'Login failed | Email:{email} | Reason: Email not registered | IP:{request.META.get("REMOTE_ADDR")}')

    # GET请求：返回登录页面
    return render(request, "blog/login.html")

# ---------------------- 原有注册视图：新增日志 ----------------------
def register_request(request):
    # 新增：记录注册请求日志
    logger.info(f'Register attempt | IP:{request.META.get("REMOTE_ADDR")} | Method:{request.method}')
    
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            # 新增：记录注册成功日志
            logger.info(f'Register success | Username:{user.username} | Email:{user.email} | IP:{request.META.get("REMOTE_ADDR")}')
            return redirect("homepage")  # 修复：main:homepage → homepage
        messages.error(request, "Unsuccessful registration. Invalid information.")
        # 新增：记录注册失败日志
        logger.warning(f'Register failed | Reason: Invalid form | IP:{request.META.get("REMOTE_ADDR")}')
    form = NewUserForm()
    return render(request, "blog/register.html", {"register_form": form})

# ---------------------- 原有登出视图：新增日志 ----------------------
def logout_request(request):
    # 新增：记录登出日志（登出前获取用户名）
    username = request.user.username or "anonymous"
    logger.info(f'Logout | User:{username} | IP:{request.META.get("REMOTE_ADDR")}')
    
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("homepage")  # 修复：main:homepage → homepage

# ---------------------- 原有创建博客视图：新增日志 ----------------------
@login_required
def create_post(request):
    # 新增：记录创建博客请求日志
    logger.info(f'Create post attempt | User:{request.user.username} | IP:{request.META.get("REMOTE_ADDR")} | Method:{request.method}')
    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            # 新增：记录创建成功日志
            logger.info(f'Create post success | Post title:{post.title} | User:{request.user.username} | IP:{request.META.get("REMOTE_ADDR")}')
            return redirect('homepage')  # 修复：main:homepage → homepage
        else:
            error_msg = 'Failed to create post: ' + ', '.join(form.errors)
            messages.error(request, error_msg)
            # 新增：记录创建失败日志
            logger.warning(f'Create post failed | User:{request.user.username} | Reason:{error_msg} | IP:{request.META.get("REMOTE_ADDR")}')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

# ---------------------- 原有添加评论视图：新增日志 ----------------------
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 新增：记录添加评论请求日志
    logger.info(f'Add comment attempt | Post ID:{pk} | User:{request.user.username} | IP:{request.META.get("REMOTE_ADDR")} | Method:{request.method}')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            # 新增：记录添加成功日志
            logger.info(f'Add comment success | Post ID:{pk} | User:{request.user.username} | IP:{request.META.get("REMOTE_ADDR")}')
            return redirect('post_detail', slug=post.slug)  # 修复：main:post_detail → post_detail
        else:
            error_msg = 'Failed to add comment: ' + ', '.join(form.errors)
            messages.error(request, error_msg)
            # 新增：记录添加失败日志
            logger.warning(f'Add comment failed | Post ID:{pk} | User:{request.user.username} | Reason:{error_msg} | IP:{request.META.get("REMOTE_ADDR")}')
    return redirect('post_detail', slug=post.slug)  # 修复：main:post_detail → post_detail

# ---------------------- 原有点赞评论视图：新增日志 ----------------------
@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_slug = comment.post.slug
    # 新增：记录点赞请求日志
    logger.info(f'Like comment attempt | Comment ID:{pk} | User:{request.user.username} | IP:{request.META.get("REMOTE_ADDR")}')
    
    if request.user not in comment.likes.all():
        comment.likes.add(request.user)
        messages.success(request, 'Liked comment!')
        # 新增：记录点赞成功日志
        logger.info(f'Like comment success | Comment ID:{pk} | User:{request.user.username} | IP:{request.META.get("REMOTE_ADDR")}')
    else:
        messages.error(request, 'You already liked this comment!')
        # 新增：记录点赞失败日志
        logger.warning(f'Like comment failed | Comment ID:{pk} | User:{request.user.username} | Reason: Already liked | IP:{request.META.get("REMOTE_ADDR")}')
    
    return redirect('post_detail', slug=post_slug)  # 修复：main:post_detail → post_detail

# ---------------------- 原有密码重置视图：新增日志（类视图） ----------------------
# 1. 第一步：用户输入邮箱，发送重置链接
class CustomPasswordResetView(PasswordResetView):
    # 模板路径
    template_name = "blog/password_reset.html"
    # 提交后跳转页面（修复main:前缀）
    success_url = reverse_lazy("password_reset_done")  # 修复：main:password_reset_done → password_reset_done
    
    # 新增：记录密码重置请求日志
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        logger.info(f'Password reset request | Email:{email} | IP:{request.META.get("REMOTE_ADDR")}')
        return super().post(request, *args, **kwargs)

# 2. 第二步：重置链接发送成功提示页
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "blog/password_reset_done.html"
    
    # 新增：记录日志
    def get(self, request, *args, **kwargs):
        logger.info(f'Password reset done | IP:{request.META.get("REMOTE_ADDR")} | User:{request.user.username or "anonymous"}')
        return super().get(request, *args, **kwargs)

# 3. 第三步：用户点击链接，设置新密码
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    # 重置成功后跳转页面（修复main:前缀）
    success_url = reverse_lazy("password_reset_complete")  # 修复：main:password_reset_complete → password_reset_complete
    template_name = "blog/password_reset_confirm.html"
    
    # 新增：记录密码重置确认日志
    def post(self, request, *args, **kwargs):
        logger.info(f'Password reset confirm | IP:{request.META.get("REMOTE_ADDR")} | User:{request.user.username or "anonymous"}')
        return super().post(request, *args, **kwargs)

# 4. 第四步：密码重置完成提示页
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "blog/password_reset_complete.html"
    
    # 新增：记录日志
    def get(self, request, *args, **kwargs):
        logger.info(f'Password reset complete | IP:{request.META.get("REMOTE_ADDR")} | User:{request.user.username or "anonymous"}')
        return super().get(request, *args, **kwargs)

# ---------------------- 原有个人资料视图：新增日志 ----------------------
@login_required  # 必须登录才能访问
def profile(request):
    # 新增：记录个人资料访问/更新日志
    logger.info(f'Profile access | User:{request.user.username} | IP:{request.META.get("REMOTE_ADDR")} | Method:{request.method}')
    
    # 处理个人资料更新
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            # 新增：记录更新成功日志
            logger.info(f'Profile updated | User:{request.user.username} | IP:{request.META.get("REMOTE_ADDR")}')
            return redirect('profile')
        else:
            error_msg = 'Failed to update profile: ' + ', '.join(form.errors)
            messages.error(request, error_msg)
            # 新增：记录更新失败日志
            logger.warning(f'Profile update failed | User:{request.user.username} | Reason:{error_msg} | IP:{request.META.get("REMOTE_ADDR")}')
    else:
        form = UserProfileForm(instance=request.user)
    
    # 渲染个人资料页面
    return render(request, 'blog/profile.html', {
        'user': request.user,
        'profile_form': form
    })