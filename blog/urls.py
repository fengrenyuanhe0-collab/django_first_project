from django.urls import path
from . import views

# 核心：精准匹配的路由必须放在模糊匹配前面！
urlpatterns = [
    # 1. 首页
    path('', views.PostList.as_view(), name='homepage'),
    
    # 2. 认证相关
    path('login/', views.login_request, name='login'),
    path('register/', views.register_request, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # 3. 密码重置
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # 4. 博客操作（精准匹配，关键！）
    path('post/create/', views.create_post, name='create_post'),  # 创建博客路由（必须有！）
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/like/', views.like_comment, name='like_comment'),
    
    # 5. 博客详情（模糊匹配，必须放最后！）
    path('post/<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]