# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm

from rest_framework import viewsets
from .serializers import PostSerializer
from .models import Post
# 首页：显示所有已发布的博客
class PostList(ListView):
    model = Post
    template_name = 'index.html'
    queryset = Post.objects.filter(status=1).order_by('-created_date')
    context_object_name = 'post_list'

# 发布新博客（需要登录）
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = form.instance.title.lower().replace(" ", "-").replace("_", "-")
        return super().form_valid(form)

# 博客详情页
class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'

    def get_context_data(self,** kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(active=True).order_by('-likes', '-created_on')
        context['comment_form'] = CommentForm()
        return context

# 添加评论（需要登录，自动关联用户）
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user  # 自动关联登录用户
            comment.save()
            return redirect('post_detail', slug=post.slug)
    return redirect('post_detail', slug=post.slug)

# 评论点赞
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.likes += 1
    comment.save()
    return redirect('post_detail', slug=comment.post.slug)

    # API VIEWSET
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()