# 智慧采购管理系统 - 部署指南

## 🚀 部署概述

本文档详细介绍了智慧采购管理系统的部署方法，包括开发环境和生产环境的配置。

## 📋 系统要求

### 最低配置要求
- **操作系统**: Linux (Ubuntu 18.04+, CentOS 7+) / macOS / Windows 10+
- **Python**: 3.8 或更高版本
- **内存**: 2GB RAM
- **存储**: 10GB 可用空间
- **网络**: 稳定的互联网连接

### 推荐配置
- **操作系统**: Ubuntu 20.04 LTS
- **Python**: 3.9+
- **内存**: 4GB RAM 或更多
- **存储**: 50GB SSD
- **CPU**: 2核心或更多

## 🛠️ 开发环境部署

### 1. 环境准备

#### 安装 Python
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# CentOS/RHEL
sudo yum install python3 python3-pip

# macOS (使用 Homebrew)
brew install python

# Windows
# 从 https://python.org 下载并安装 Python
```

#### 安装 Git
```bash
# Ubuntu/Debian
sudo apt install git

# CentOS/RHEL
sudo yum install git

# macOS
brew install git

# Windows
# 从 https://git-scm.com 下载并安装
```

### 2. 克隆项目

```bash
git clone https://github.com/your-username/intelligent-procurement-system.git
cd intelligent-procurement-system
```

### 3. 创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 4. 安装依赖

```bash
# 升级 pip
pip install --upgrade pip

# 安装项目依赖
pip install -r requirements.txt
```

### 5. 配置环境

```bash
# 复制配置文件模板
cp config.py.example config.py

# 编辑配置文件
nano config.py  # 或使用其他编辑器
```

在 `config.py` 中配置以下关键信息：

```python
# 阿里巴巴 API 配置
API_KEY = "your_actual_api_key"
API_SECRET = "your_actual_api_secret"
API_TOKEN = "your_actual_api_token"

# 数据库配置
SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"

# 邮件配置
MAIL_CONFIG = {
    'MAIL_USERNAME': 'your_email@qq.com',
    'MAIL_PASSWORD': 'your_smtp_password'
}
```

### 6. 初始化数据库

```bash
# 设置环境变量
export FLASK_APP=main.py
export FLASK_ENV=development

# 初始化数据库
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. 运行应用

```bash
# 启动开发服务器
python main.py

# 或使用 Flask 命令
flask run --host=0.0.0.0 --port=5000
```

访问 `http://localhost:5000` 即可使用系统。

## 🏭 生产环境部署

### 1. 服务器准备

#### 更新系统
```bash
sudo apt update && sudo apt upgrade -y
```

#### 安装必要软件
```bash
sudo apt install -y python3 python3-pip python3-venv nginx supervisor git
```

### 2. 创建应用用户

```bash
sudo adduser procurement
sudo usermod -aG sudo procurement
su - procurement
```

### 3. 部署应用

```bash
# 克隆项目到生产目录
cd /home/procurement
git clone https://github.com/your-username/intelligent-procurement-system.git
cd intelligent-procurement-system

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

### 4. 配置生产环境

```bash
# 复制并编辑配置文件
cp config.py.example config.py
nano config.py
```

生产环境配置示例：
```python
import os

class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-production-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///production.db'
    SESSION_COOKIE_SECURE = True
```

### 5. 初始化生产数据库

```bash
export FLASK_ENV=production
export FLASK_APP=main.py

flask db upgrade
```

### 6. 配置 Gunicorn

创建 Gunicorn 配置文件：
```bash
nano gunicorn.conf.py
```

```python
# gunicorn.conf.py
bind = "127.0.0.1:8000"
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

### 7. 配置 Supervisor

创建 Supervisor 配置：
```bash
sudo nano /etc/supervisor/conf.d/procurement.conf
```

```ini
[program:procurement]
command=/home/procurement/intelligent-procurement-system/venv/bin/gunicorn -c gunicorn.conf.py main:app
directory=/home/procurement/intelligent-procurement-system
user=procurement
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/procurement.log
environment=FLASK_ENV=production
```

启动 Supervisor：
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start procurement
```

### 8. 配置 Nginx

创建 Nginx 配置：
```bash
sudo nano /etc/nginx/sites-available/procurement
```

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为您的域名

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /home/procurement/intelligent-procurement-system/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    client_max_body_size 16M;
}
```

启用站点：
```bash
sudo ln -s /etc/nginx/sites-available/procurement /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. 配置 SSL (可选但推荐)

使用 Let's Encrypt 免费 SSL 证书：
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 🐳 Docker 部署

### 1. 创建 Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN useradd -m -u 1000 procurement && chown -R procurement:procurement /app
USER procurement

# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]
```

### 2. 创建 docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=sqlite:///app.db
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped
```

### 3. 构建和运行

```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f
```

## 🔧 维护和监控

### 日志管理

```bash
# 查看应用日志
sudo tail -f /var/log/procurement.log

# 查看 Nginx 日志
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### 备份数据库

```bash
# 创建备份脚本
nano backup.sh
```

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/procurement/backups"
DB_FILE="/home/procurement/intelligent-procurement-system/app.db"

mkdir -p $BACKUP_DIR
cp $DB_FILE $BACKUP_DIR/app_$DATE.db

# 保留最近 30 天的备份
find $BACKUP_DIR -name "app_*.db" -mtime +30 -delete
```

```bash
chmod +x backup.sh

# 添加到定时任务
crontab -e
# 添加：0 2 * * * /home/procurement/backup.sh
```

### 更新应用

```bash
# 切换到应用目录
cd /home/procurement/intelligent-procurement-system

# 拉取最新代码
git pull origin main

# 激活虚拟环境
source venv/bin/activate

# 更新依赖
pip install -r requirements.txt

# 运行数据库迁移
flask db upgrade

# 重启应用
sudo supervisorctl restart procurement
```

## 🔍 故障排除

### 常见问题

1. **端口被占用**
```bash
# 查看端口占用
sudo netstat -tlnp | grep :5000
# 杀死占用进程
sudo kill -9 <PID>
```

2. **权限问题**
```bash
# 修复文件权限
sudo chown -R procurement:procurement /home/procurement/intelligent-procurement-system
```

3. **数据库连接失败**
```bash
# 检查数据库文件权限
ls -la app.db
# 重新初始化数据库
flask db upgrade
```

4. **API 调用失败**
- 检查阿里巴巴 API 配置
- 验证网络连接
- 查看 API 调用日志

### 性能优化

1. **数据库优化**
```bash
# SQLite 优化
echo "PRAGMA optimize;" | sqlite3 app.db
```

2. **Nginx 缓存配置**
```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

3. **Gunicorn 工作进程调优**
```python
# 根据 CPU 核心数调整 workers
workers = multiprocessing.cpu_count() * 2 + 1
```

## 📞 技术支持

如果在部署过程中遇到问题，请：

1. 查看日志文件获取详细错误信息
2. 检查配置文件是否正确
3. 确认所有依赖已正确安装
4. 联系技术支持团队

---

部署完成后，您的智慧采购管理系统就可以正常运行了！记得定期备份数据和更新系统。