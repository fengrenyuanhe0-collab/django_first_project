from django.contrib import admin
from django.urls import path, include

# 根路由只做1件事：包含blog的所有路由
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # 所有blog路由交给子路由处理
]