FROM python:3.11-slim

WORKDIR /app

COPY . /app

# 安装依赖
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]FROM python:3.11-slim

WORKDIR /app

COPY . /app

# 安装依赖
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# ✅ 只加这一句！收集静态文件，让 admin 样式正常！
RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]