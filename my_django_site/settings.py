"""
Django settings for my_django_site project.
网页显示保持英文，代码注释中文
"""

from pathlib import Path
import os  # 日志需要
from dotenv import load_dotenv  # 新增：加载.env

# 加载.env环境变量（容器化核心：从外部配置读取敏感信息）
load_dotenv()

# 项目根目录（适配你的my_django_site结构）
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全密钥（从.env读取，容器化时不用改代码）
SECRET_KEY = os.getenv("SECRET_KEY", 'django-insecure-REPLACE_THIS_WITH_YOUR_OWN_SECRET_KEY')

# 开发模式（从.env读取，容器内默认关闭DEBUG）
DEBUG = os.getenv("DEBUG", "True") == "True"

# 允许访问的主机（从.env读取，容器化时允许所有主机）
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []

# 已安装应用（保留你原有，新增的功能依赖已包含）
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',  # Session 功能核心
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',  # 你的blog app，必须保留！
]

# 中间件（核心修改：加全站缓存中间件+自定义日志中间件）
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # 1. 全站缓存中间件（第一个加载，自动缓存所有页面）
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session 中间件
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 2. 全站缓存中间件（最后一个加载）
    'django.middleware.cache.FetchFromCacheMiddleware',
    # 3. 自定义日志中间件（自动记录所有页面访问日志）
    'my_django_site.middleware.AllPageLoggingMiddleware',
]

# 根路由配置（适配你的my_django_site）
ROOT_URLCONF = 'my_django_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 关键修改：添加根目录的templates路径，解决模板找不到的问题
        'DIRS': [BASE_DIR / 'templates'],  
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI配置（适配你的my_django_site）
WSGI_APPLICATION = 'my_django_site.wsgi.application'

# 数据库（容器化核心：优先从.env读取PostgreSQL配置，本地开发用sqlite）
DATABASES = {
    'default': {
        # 容器化用PostgreSQL，本地开发用sqlite
        'ENGINE': os.getenv("DATABASE_ENGINE", 'django.db.backends.sqlite3'),
        'NAME': os.getenv("DATABASE_NAME", BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv("DATABASE_USER", ''),
        'PASSWORD': os.getenv("DATABASE_PASSWORD", ''),
        'HOST': os.getenv("DATABASE_HOST", ''),
        'PORT': os.getenv("DATABASE_PORT", ''),
    }
}

# 密码验证（保留原有）
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 国际化（网页保持英文，不改动）
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 静态文件（容器化核心：添加STATIC_ROOT，让collectstatic收集静态文件）
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # 容器化必须：收集静态文件到static目录
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==================================================
# 1. SESSION 配置（标准网站必备，适配你的项目）
# ==================================================
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 存在数据库
SESSION_COOKIE_AGE = 14 * 24 * 60 * 60  # 14天有效期
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 关闭浏览器不失效
SESSION_SAVE_EVERY_REQUEST = True  # 每次请求刷新过期时间

# ==================================================
# 2. 全站CACHING 缓存配置（自动覆盖所有页面）
# ==================================================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'my_django_site_cache',  # 适配你的项目名
    }
}
# 全站缓存有效期：300秒（5分钟，可自行调整）
CACHE_MIDDLEWARE_SECONDS = 300
# 缓存前缀（避免和其他项目冲突）
CACHE_MIDDLEWARE_KEY_PREFIX = 'my_django_site'
# 缓存使用的别名（对应上面的default缓存）
CACHE_MIDDLEWARE_ALIAS = 'default'

# ==================================================
# 3. LOGGING 日志配置（自动写入logs目录，记录所有页面访问）
# ==================================================
# 先创建logs目录（避免报错）
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOG_DIR, 'django.log'),  # 日志存在logs目录
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'blog': {  # 单独记录blog app的日志
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


CSRF_TRUSTED_ORIGINS = [
    'http://localhost:81',
    'http://127.0.0.1:81',
]