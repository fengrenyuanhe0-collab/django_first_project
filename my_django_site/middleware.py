"""
自定义中间件：给所有页面自动加访问日志，不影响页面显示
"""
import logging
from django.utils.deprecation import MiddlewareMixin

# 初始化日志器
logger = logging.getLogger('django')

class AllPageLoggingMiddleware(MiddlewareMixin):
    """
    给所有页面添加访问日志，自动记录：访问路径、IP、请求方法、用户
    """
    def process_request(self, request):
        # 记录所有页面的访问日志（后台日志，不显示在网页）
        log_info = {
            'path': request.path,  # 访问的页面路径（如/、/post/1/）
            'ip': request.META.get('REMOTE_ADDR', 'unknown'),  # 访问IP
            'method': request.method,  # 请求方法（GET/POST）
            'user': request.user.username or 'anonymous'  # 访问用户（匿名/登录用户）
        }
        # 写入日志（格式：时间 级别 模块 信息）
        logger.info(f"Page accessed - path:{log_info['path']} | ip:{log_info['ip']} | method:{log_info['method']} | user:{log_info['user']}")