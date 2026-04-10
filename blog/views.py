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
from .serializers import PostSerializer, CommentSerializer
from .forms import NewUserForm, PostForm, CommentForm, UserProfileForm
from .models import Post, Comment

# 博客列表视图（原有代码，无修改）
class PostList(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    queryset = Post.objects.filter(status=1).order_by('-created_date')
    context_object_name = 'posts'

# 博客详情视图（原有代码，无修改）
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

# API视图 - 博客（原有代码，无修改）
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# API视图 - 评论（原有代码，无修改）
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# ---------------------- 核心修改：登录视图（改为邮箱登录） ----------------------
def login_request(request):
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
                return redirect("homepage")  # 修复：main:homepage → homepage
            else:
                # 密码错误提示
                messages.error(request, "Incorrect password!")
        except User.DoesNotExist:
            # 邮箱未注册提示
            messages.error(request, "Email not registered!")

    # GET请求：返回登录页面
    return render(request, "blog/login.html")

# 注册视图（修复main:前缀）
def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("homepage")  # 修复：main:homepage → homepage
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "blog/register.html", {"register_form": form})

# 登出视图（修复main:前缀）
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("homepage")  # 修复：main:homepage → homepage

# 创建博客视图（修复main:前缀）
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('homepage')  # 修复：main:homepage → homepage
        else:
            messages.error(request, 'Failed to create post: ' + ', '.join(form.errors))
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

# 添加评论视图（修复main:前缀）
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', slug=post.slug)  # 修复：main:post_detail → post_detail
        else:
            messages.error(request, 'Failed to add comment: ' + ', '.join(form.errors))
    return redirect('post_detail', slug=post.slug)  # 修复：main:post_detail → post_detail

# 点赞评论视图（修复main:前缀）
@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_slug = comment.post.slug
    
    if request.user not in comment.likes.all():
        comment.likes.add(request.user)
        messages.success(request, 'Liked comment!')
    else:
        messages.error(request, 'You already liked this comment!')
    
    return redirect('post_detail', slug=post_slug)  # 修复：main:post_detail → post_detail

# ---------------------- 老师原版：密码重置4个视图（修复main:前缀） ----------------------
# 1. 第一步：用户输入邮箱，发送重置链接
class CustomPasswordResetView(PasswordResetView):
    # 模板路径
    template_name = "blog/password_reset.html"
    # 提交后跳转页面（修复main:前缀）
    success_url = reverse_lazy("password_reset_done")  # 修复：main:password_reset_done → password_reset_done

# 2. 第二步：重置链接发送成功提示页
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "blog/password_reset_done.html"

# 3. 第三步：用户点击链接，设置新密码
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    # 重置成功后跳转页面（修复main:前缀）
    success_url = reverse_lazy("password_reset_complete")  # 修复：main:password_reset_complete → password_reset_complete
    template_name = "blog/password_reset_confirm.html"

# 4. 第四步：密码重置完成提示页
class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "blog/password_reset_complete.html"

    # ---------------------- 新增：用户个人资料视图 ----------------------
@login_required  # 必须登录才能访问
def profile(request):
    # 处理个人资料更新
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Failed to update profile: ' + ', '.join(form.errors))
    else:
        form = UserProfileForm(instance=request.user)
    
    # 渲染个人资料页面
    return render(request, 'blog/profile.html', {
        'user': request.user,
        'profile_form': form
    })