# 基础镜像：Python 3.11 轻量版
FROM python:3.11-slim

# 环境变量：避免Python编译生成pyc文件、保证输出实时打印
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 设置工作目录（容器内的目录）
WORKDIR /app

# 复制依赖文件，先装依赖（利用Docker缓存，改代码不用重装依赖）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目到容器
COPY . .

# 暴露端口（容器内Django运行的端口）
EXPOSE 8000