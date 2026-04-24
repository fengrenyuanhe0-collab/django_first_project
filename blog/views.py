from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import reverse_lazy
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import logging
from .serializers import PostSerializer, CommentSerializer
from .forms import NewUserForm, PostForm, CommentForm, UserProfileForm
from .models import Post, Comment

# 日志器（按文档）
logger = logging.getLogger('blog')

# 首页：缓存 + 日志 + Session
class PostList(ListView):
    model = Post
    template_name = 'blog/home.html'
    queryset = Post.objects.filter(status=1).order_by('-created_date')
    context_object_name = 'posts'

    def get(self, request, *args, **kwargs):
        # 日志：记录访问
        logger.warning("Homepage was accessed!")
        
        # Session：记录访问次数
        if 'visit_count' not in request.session:
            request.session['visit_count'] = 0
        request.session['visit_count'] += 1

        return super().get(request, *args, **kwargs)

# 文章详情：手动缓存 + 日志
class PostDetail(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self,** kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        cache_key = f'post_{post.slug}'

        # 先从缓存取
        cached_post = cache.get(cache_key)
        if not cached_post:
            cache.set(cache_key, post, 300)
            logger.info(f"Post {post.slug} loaded from DB and cached")
        else:
            logger.info(f"Post {post.slug} loaded from cache")

        context['comments'] = post.comments.all().order_by('-created_on')
        context['comment_form'] = CommentForm()
        return context

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# 登录视图：Session + 日志
def login_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user:
                login(request, authenticated_user)
                request.session['last_login'] = str(user.last_login)
                logger.info(f"User {email} logged in successfully")
                messages.success(request, "Login successful!")
                return redirect("homepage")
            else:
                messages.error(request, "Incorrect password!")
        except User.DoesNotExist:
            messages.error(request, "Email not registered!")
    return render(request, "blog/login.html")

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            logger.info(f"New user registered: {user.email}")
            messages.success(request, "Registration successful!")
            return redirect("homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "blog/register.html", {"register_form": form})

def logout_request(request):
    logger.info(f"User {request.user.email} logged out")
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("homepage")

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            logger.info(f"New post created: {post.title}")
            messages.success(request, 'Post created successfully!')
            return redirect('homepage')
        else:
            logger.error(f"Post creation failed: {form.errors}")
            messages.error(request, 'Failed to create post')
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

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
    return redirect('post_detail', slug=post.slug)

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user not in comment.likes.all():
        comment.likes.add(request.user)
        messages.success(request, 'Liked comment!')
    else:
        messages.error(request, 'You already liked this comment!')
    return redirect('post_detail', slug=comment.post.slug)

class CustomPasswordResetView(PasswordResetView):
    template_name = "blog/password_reset.html"
    success_url = reverse_lazy("password_reset_done")

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "blog/password_reset_done.html"

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy("password_reset_complete")
    template_name = "blog/password_reset_confirm.html"

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "blog/password_reset_complete.html"

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            logger.info(f"Profile updated: {request.user.username}")
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            logger.warning(f"Profile update failed: {form.errors}")
            messages.error(request, 'Failed to update profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'blog/profile.html', {
        'user': request.user,
        'profile_form': form
    })