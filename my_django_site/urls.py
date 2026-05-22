"""
URL路由配置
全站缓存和日志由中间件自动处理，无需在此加装饰器
"""
from django.contrib import admin
from django.urls import path, include
# 👇 新增：DRF API 路由配置（不影响你原有博客）
from rest_framework.routers import DefaultRouter
from blog.views import PostViewSet, CommentViewSet
# 这里定义 router，必须写！
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # 所有blog页面自动被缓存+日志覆盖
    # 👇 新增：统一 API 入口（一个链接看所有 API）
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),  # API 登录功能

]  