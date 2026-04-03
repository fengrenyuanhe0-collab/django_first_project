# blog/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('new-post/', views.create_post, name='create_post'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('like-comment/<int:pk>/', views.like_comment, name='like_comment'),
    path('profile/', views.profile_view, name='profile'),  # 新增个人资料路由
]