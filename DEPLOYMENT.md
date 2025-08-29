# 🚀 LLRC 部署指南

## 📋 概述

本文档详细说明了如何将 LLRC 应用部署到生产环境，实现 GitHub 自动同步部署。

## 🎯 部署目标

- ✅ 云服务器自动运行应用
- ✅ GitHub 推送后自动同步
- ✅ 其他同学可通过链接访问
- ✅ 生产环境稳定运行

## 🏗️ 系统架构

```
用户请求 → Nginx → Gunicorn → Flask应用
                ↓
            静态文件服务
```

## 📦 前置要求

### 服务器要求
- Ubuntu 18.04+ 或 CentOS 7+
- 至少 1GB RAM
- 至少 10GB 存储空间
- 公网IP地址

### 软件要求
- Python 3.8+
- Git
- Nginx
- Supervisor (可选)

## 🔧 部署步骤

### 第一步：服务器环境准备

```bash
# 1. 更新系统
sudo apt update && sudo apt upgrade -y

# 2. 安装基础软件
sudo apt install -y python3 python3-pip python3-venv git nginx supervisor curl

# 3. 创建项目目录
sudo mkdir -p /var/www/llrc
sudo chown $USER:$USER /var/www/llrc
```

### 第二步：克隆项目代码

```bash
cd /var/www/llrc
git clone https://github.com/Rayscout/LLRC.git .
```

### 第三步：运行自动部署脚本

```bash
# 给脚本执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

### 第四步：配置GitHub Secrets

在GitHub仓库中设置以下secrets：

1. 进入 `Settings` → `Secrets and variables` → `Actions`
2. 点击 `New repository secret`
3. 添加以下secrets：

| Secret名称 | 说明 | 示例值 |
|-----------|------|--------|
| `HOST` | 服务器IP地址 | `123.456.789.123` |
| `USERNAME` | 服务器用户名 | `ubuntu` |
| `SSH_KEY` | SSH私钥内容 | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `PORT` | SSH端口 | `22` |

## 🔍 验证部署

### 检查服务状态

```bash
# 检查LLRC服务
sudo systemctl status llrc

# 检查Nginx服务
sudo systemctl status nginx

# 检查端口监听
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :5000
```

### 访问应用

- 本地访问: `http://localhost`
- 外部访问: `http://你的服务器IP`
- 健康检查: `http://你的服务器IP/health`

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

# 拉取最新代码
git fetch origin
git reset --hard origin/main

# 更新依赖
source venv/bin/activate
pip install -r requirements.txt

# 重启服务
sudo systemctl restart llrc
```

## 🚨 故障排除

### 常见问题

#### 1. 服务启动失败

```bash
# 查看详细错误信息
sudo journalctl -u llrc -n 50

# 检查配置文件
sudo nginx -t

# 检查端口占用
sudo netstat -tlnp | grep :5000
```

#### 2. 权限问题

```bash
# 重新设置权限
sudo chown -R www-data:www-data /var/www/llrc
sudo chmod -R 755 /var/www/llrc
```

#### 3. 数据库问题

```bash
# 初始化数据库
cd /var/www/llrc
source venv/bin/activate
flask db init
flask db migrate
flask db upgrade
```

#### 4. 防火墙问题

```bash
# 检查防火墙状态
sudo ufw status

# 开放必要端口
sudo ufw allow 80
sudo ufw allow 443
```

## 🔒 安全建议

### 1. 防火墙配置
```bash
# 只开放必要端口
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### 2. SSH安全
```bash
# 禁用root登录
sudo nano /etc/ssh/sshd_config
# 设置 PermitRootLogin no

# 重启SSH服务
sudo systemctl restart ssh
```

### 3. 定期更新
```bash
# 系统更新
sudo apt update && sudo apt upgrade -y

# 依赖更新
cd /var/www/llrc
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## 📞 技术支持

如果遇到问题，请：

1. 查看日志文件获取错误信息
2. 检查服务状态
3. 验证配置文件
4. 联系技术支持

## 🎉 部署完成

恭喜！现在你的LLRC应用已经成功部署到生产环境，并且：

- ✅ 支持GitHub自动同步
- ✅ 其他同学可通过链接访问
- ✅ 生产环境稳定运行
- ✅ 自动服务管理

每次推送代码到GitHub的main分支时，应用会自动更新并重启！
