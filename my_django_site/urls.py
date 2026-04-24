"""
URL configuration for my_django_site project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 项目根路由：把所有博客相关路由分发给 blog 应用
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),  # 关键：引入 blog/urls.py
]

# 开发环境媒体文件访问配置
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)