# Django First Project

A complete Django blog system with user, post, comment, API and Docker support.

---

# Project Info
- GitHub Repository: https://github.com/fengrenyuanhe0-collab/django_first_project.git
- Docker Image Hash: `903dbc605536f0edf35afea4eb5a8bf7c4ebf06c2f0c5df0e13d0501565868bf`
- Local Address: http://localhost:8008


---

# All Page Links (Chinese/English)
Base URL: http://localhost:8008

## 1. General Pages | 通用页面
1. Homepage | 网站首页：http://localhost:8008
2. User Login | 用户登录：http://localhost:8008/login/
3. User Register | 用户注册：http://localhost:8008/register/
4. User Logout | 退出登录：http://localhost:8008/logout/
5. User Profile | 个人中心：http://localhost:8008/profile/

## 2. Blog Post Pages | 博客文章页面
6. Create Post | 发布文章：http://localhost:8008/post/create/
7. Post Detail | 文章详情：http://localhost:8008/post/[slug]/
8. Post Comment | 文章评论：http://localhost:8008/post/[id]/comment/
9. Comment Like | 评论点赞：http://localhost:8008/comment/[id]/like/

## 3. Password Reset Pages | 密码重置页面
10. Password Reset Apply | 重置申请：http://localhost:8008/password-reset/
11. Reset Submitted | 申请提交成功：http://localhost:8008/password-reset/done/
12. Reset Confirm | 重置验证：http://localhost:8008/password-reset-confirm/[uid]/[token]/
13. Reset Complete | 重置完成：http://localhost:8008/password-reset-complete/

## 4. Admin Pages | 管理员后台
14. Admin Dashboard | 后台首页：http://localhost:8008/admin/
15. Admin Login | 后台登录：http://localhost:8008/admin/login/
16. Admin Logout | 后台退出：http://localhost:8008/admin/logout/
17. Admin Change Password | 后台修改密码：http://localhost:8008/admin/password_change/

## 5. API Pages | API接口
18. API Index | API总入口：http://localhost:8008/api/
19. Posts API | 文章接口：http://localhost:8008/api/posts/
20. Comments API | 评论接口：http://localhost:8008/api/comments/

------

# Test Accounts | 测试账户
**Admin Account | 管理员账户**
- Username: le
- Email: 3558927029@qq.com
- Password: Cc1002

**User Account | 用户账户**
- Email: 3558927029@qq.com
- Password: Cc031002


# Docker Deployment | Docker部署
```bash
docker run -d -p 8008:8000 sha256:903dbc605536f0edf35afea4eb5a8bf7c4ebf06c2f0c5df0e13d0501565868bf

# Docker Deployment | Docker部署
```bash
docker run -d -p 8008:8000 sha256:903dbc605536f0edf35afea4eb5a8bf7c4ebf06c2f0c5df0e13d0501565868bf

git clone https://github.com/fengrenyuanhe0-collab/django_first_project.git
cd django_first_project
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

