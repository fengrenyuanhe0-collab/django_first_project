"""
URL configuration for my_django_site project.
This file maps URLs to views, including the admin panel and blog homepage.
Django 项目总路由文件，配置网址与视图的对应关系，包含 admin 和博客首页。
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # 博客应用路由
    path('', include('blog.urls')),
    # Django自带登录/注销路由
    path('accounts/', include('django.contrib.auth.urls')),
]