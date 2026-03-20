#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
"""
Django's command-line utility for administrative tasks.
This file is used to run commands like startserver, makemigrations, migrate, etc.
Django 命令行工具，用于启动服务器、数据库迁移、创建管理员等操作。
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_django_site.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
