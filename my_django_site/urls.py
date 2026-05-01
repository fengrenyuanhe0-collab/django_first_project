"""
URL路由配置
全站缓存和日志由中间件自动处理，无需在此加装饰器
"""
from django.contrib import admin
from django.urls import path, include

# 完全保留你的原有路由，无需任何修改
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # 所有blog页面自动被缓存+日志覆盖
]