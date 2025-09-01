# 🚀 LLRC 云服务器部署指南

## 📋 概述

本指南详细说明如何将最新版本的LLRC应用（使用DeepFace表情识别）部署到云服务器，并解决同步问题。

## 🎯 解决的问题

- ✅ 修复表情识别功能（从YOLO切换到DeepFace）
- ✅ 解决本地与云端环境不一致问题
- ✅ 确保GitHub同步正常工作
- ✅ 提供自动化部署脚本

## 🏗️ 系统架构

```
用户请求 → Nginx → Gunicorn → Flask应用 → DeepFace表情识别
```

## 📦 前置要求

### 服务器要求
- Ubuntu 18.04+ 或 CentOS 7+
- 至少 2GB RAM（DeepFace需要更多内存）
- 至少 20GB 存储空间
- 公网IP地址

### 软件要求
- Python 3.8+
- Git
- Nginx
- MongoDB

## 🔧 部署步骤

### 第一步：服务器环境准备

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装基础软件
sudo apt install -y python3 python3-pip python3-venv git nginx supervisor curl

# 3. 安装MongoDB
sudo apt install -y mongodb

# 4. 启动MongoDB服务
sudo systemctl start mongodb
sudo systemctl enable mongodb

# 5. 创建项目目录
sudo mkdir -p /var/www/llrc
sudo chown $USER:$USER /var/www/llrc
```

### 第二步：克隆项目代码

```bash
cd /var/www/llrc
git clone https://github.com/Rayscout/LLRC.git .
git checkout pxy  # 切换到pxy分支
```

### 第三步：创建虚拟环境

```bash
# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 升级pip
pip install --upgrade pip

# 安装依赖
pip install -r requirements.txt
```

### 第四步：运行自动部署脚本

```bash
# 给脚本执行权限
chmod +x deploy.sh
chmod +x cloud_deploy.sh

# 运行部署脚本
./deploy.sh
```

### 第五步：验证部署

```bash
# 运行环境检查
python3 cloud_check.py

# 检查服务状态
sudo systemctl status llrc
sudo systemctl status nginx

# 检查端口监听
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :5000
```

## 🔍 环境检查

### 运行环境检查脚本

```bash
python3 cloud_check.py
```

预期输出：
```
🔍 云服务器环境检查
==============================
✅ DeepFace导入成功
✅ 表情识别模块正常

🎉 环境检查通过！
```

### 手动检查关键功能

```bash
# 1. 检查DeepFace
python3 -c "from deepface import DeepFace; print('DeepFace正常')"

# 2. 检查表情识别模块
python3 -c "
from smartrecruit_system.candidate_module.emotion_recognition import get_emotion_recognition_ai
ai = get_emotion_recognition_ai()
print('表情识别模块正常')
"

# 3. 检查MongoDB连接
python3 -c "
import pymongo
client = pymongo.MongoClient('mongodb://localhost:27017/')
client.server_info()
print('MongoDB连接正常')
"
```

## 📝 常用管理命令

### 服务管理

```bash
# 启动服务
sudo systemctl start llrc

# 停止服务
sudo systemctl stop llrc

# 重启服务
sudo systemctl restart llrc

# 查看服务状态
sudo systemctl status llrc

# 启用开机自启
sudo systemctl enable llrc
```

### 日志查看

```bash
# 查看应用日志
sudo journalctl -u llrc -f

# 查看Nginx访问日志
sudo tail -f /var/log/nginx/access.log

# 查看Nginx错误日志
sudo tail -f /var/log/nginx/error.log

# 查看应用日志文件
tail -f /var/www/llrc/app.log
```

### 代码更新

```bash
cd /var/www/llrc

# 方法1：使用自动部署脚本
./cloud_deploy.sh

# 方法2：手动更新
git fetch origin
git reset --hard origin/pxy
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart llrc
```

## 🚨 故障排除

### 常见问题及解决方案

#### 1. DeepFace安装失败

```bash
# 安装系统依赖
sudo apt install -y libgl1-mesa-glx libglib2.0-0

# 重新安装DeepFace
pip uninstall deepface
pip install deepface==0.0.79
```

#### 2. 表情识别模块导入失败

```bash
# 检查Python路径
python3 -c "import sys; print(sys.path)"

# 检查模块文件是否存在
ls -la smartrecruit_system/candidate_module/

# 重新安装依赖
pip install -r requirements.txt
```

#### 3. MongoDB连接失败

```bash
# 检查MongoDB服务状态
sudo systemctl status mongodb

# 启动MongoDB服务
sudo systemctl start mongodb

# 检查端口监听
sudo netstat -tlnp | grep :27017
```

#### 4. 服务启动失败

```bash
# 查看详细错误信息
sudo journalctl -u llrc -n 50

# 检查配置文件
sudo nginx -t

# 检查端口占用
sudo netstat -tlnp | grep :5000
```

#### 5. 内存不足

```bash
# 检查内存使用
free -h

# 增加swap空间
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 性能优化

#### 1. 系统优化

```bash
# 优化系统参数
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

#### 2. Nginx优化

```bash
# 编辑Nginx配置
sudo nano /etc/nginx/nginx.conf

# 添加以下配置到http块
worker_processes auto;
worker_connections 1024;
keepalive_timeout 65;
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

#### 3. Gunicorn优化

```bash
# 编辑Gunicorn配置
sudo nano /var/www/llrc/gunicorn.conf.py

# 优化配置
workers = 4
worker_class = 'gevent'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
```

## 🔒 安全配置

### 1. 防火墙配置

```bash
# 配置防火墙
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. SSH安全

```bash
# 编辑SSH配置
sudo nano /etc/ssh/sshd_config

# 设置安全参数
PermitRootLogin no
PasswordAuthentication no
Port 22
```

### 3. 定期更新

```bash
# 创建自动更新脚本
sudo nano /usr/local/bin/update-system.sh

#!/bin/bash
sudo apt update && sudo apt upgrade -y
cd /var/www/llrc
./cloud_deploy.sh

# 设置执行权限
sudo chmod +x /usr/local/bin/update-system.sh

# 添加到crontab
sudo crontab -e
# 添加：0 2 * * 0 /usr/local/bin/update-system.sh
```

## 📞 技术支持

### 获取帮助

1. **查看日志**：`sudo journalctl -u llrc -f`
2. **检查状态**：`sudo systemctl status llrc`
3. **运行诊断**：`python3 cloud_check.py`
4. **查看错误**：`tail -f /var/www/llrc/app.log`

### 联系信息

- 项目仓库：https://github.com/Rayscout/LLRC
- 问题反馈：通过GitHub Issues

## 🎉 部署完成

恭喜！现在你的LLRC应用已经成功部署到云服务器，并且：

- ✅ 使用DeepFace进行表情识别
- ✅ 支持GitHub自动同步
- ✅ 其他同学可通过链接访问
- ✅ 生产环境稳定运行
- ✅ 自动服务管理

### 访问信息

- 本地访问: `http://localhost`
- 外部访问: `http://你的服务器IP`
- 健康检查: `http://你的服务器IP/health`
- 表情识别测试: `http://你的服务器IP/smartrecruit/candidate/applications/emotion_demo`

每次推送代码到GitHub的pxy分支时，应用会自动更新并重启！
