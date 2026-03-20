"""
Defines the views for the blog application.
This file contains the home view, which displays a list of all blog posts.
blog 应用的视图文件，定义了首页视图，用于查询所有博客文章并传递给模板展示。
"""
from django.views.generic import ListView, DetailView
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post, Comment
from .forms import CommentForm

# 首页文章列表
class PostList(ListView):
    model = Post
    template_name = 'index.html'
    queryset = Post.objects.filter(status=1).order_by('-created_date')
    context_object_name = 'post_list'

# 文章详情 + 评论提交（修复跳转逻辑）
class PostDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(** kwargs)
        # 传入评论列表和表单
        context['comments'] = self.object.comments.filter(active=True)
        context['comment_form'] = CommentForm()
        return context

    # 处理评论提交（用更简单的方式）
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.save()
            # 修复跳转：直接拼 URL，避免依赖 get_absolute_url 出错
            return HttpResponseRedirect(reverse('post_detail', args=[self.object.slug]))
        
        # 表单验证失败时返回原页面
        context = self.get_context_data(object=self.object)
        context['comment_form'] = form
        return self.render_to_response(context)