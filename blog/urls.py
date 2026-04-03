from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 注册 API
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('new-post/', views.PostCreateView.as_view(), name='new_post'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('comment/<int:pk>/', views.add_comment, name='add_comment'),
    path('like-comment/<int:pk>/', views.like_comment, name='like_comment'),

    # API 路由
    path('api/v1/', include(router.urls)),
]