"""
URL configuration for the blog application.
This file maps the homepage URL to the home view.
blog 应用的路由文件，配置首页 URL 与 home 视图的对应关系。
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]