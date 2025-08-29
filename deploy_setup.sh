#!/bin/bash

# 服务器环境准备脚本
echo "🚀 开始准备服务器环境..."

# 更新系统
echo "📦 更新系统包..."
apt update && apt upgrade -y

# 安装必要的软件包
echo "🔧 安装Python和必要工具..."
apt install -y python3 python3-pip python3-venv nginx git curl wget unzip

# 安装Python依赖
echo "🐍 安装Python依赖..."
apt install -y python3-dev build-essential libssl-dev libffi-dev

# 创建项目目录
echo "📁 创建项目目录..."
mkdir -p /var/www/llrc
chown -R $USER:$USER /var/www/llrc

# 安装Node.js（如果需要前端构建）
echo "📦 安装Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# 安装PM2（进程管理）
echo "⚙️ 安装PM2..."
npm install -g pm2

echo "✅ 服务器环境准备完成！"
