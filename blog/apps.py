"""
Configuration for the blog application.
This file registers the blog app with Django, defining the app's name and config class.
blog 应用的配置文件，用于在 Django 中注册应用，定义应用名称和配置类。
"""
from django.apps import AppConfig


class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
