from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings  # 确保导入MEDIA_ROOT

# 导入API相关
from rest_framework.routers import DefaultRouter
from blog.views import register, PostViewSet, CommentViewSet

# 1. 初始化API路由器
router = DefaultRouter()

# 2. 注册API视图集 ✅ 注意：这里不要加前缀 api/！
router.register(r'posts', PostViewSet, basename='api-posts')
router.register(r'comments', CommentViewSet, basename='api-comments')

# 3. 主路由列表（顺序绝对不能错！）
urlpatterns = [
    path('admin/', admin.site.urls),

    # 登录/登出/注册
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', register, name='register'),

    # ✅ 正确：API 路由前缀是 /api/，里面的视图集不用再加 api/
    path('api/', include(router.urls)),

    # ✅ 博客首页：必须放在最后！
    path('', include('blog.urls')),
]

# 4. 媒体文件路由（开发环境）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)