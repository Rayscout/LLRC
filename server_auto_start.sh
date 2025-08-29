#!/bin/bash

# 服务器自动启动脚本
echo "🚀 服务器自动启动脚本..."

# 项目目录
PROJECT_DIR="/var/www/llrc"

# 检查Git仓库是否存在
if [ ! -d "$PROJECT_DIR/.git" ]; then
    echo "❌ Git仓库不存在，正在初始化..."
    cd $PROJECT_DIR
    git init
    git remote add origin https://github.com/YOUR_USERNAME/llrc-project.git
fi

# 拉取最新代码
echo "📥 拉取最新代码..."
cd $PROJECT_DIR
git fetch origin
git reset --hard origin/main

# 检查虚拟环境
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo "🐍 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境并安装依赖
echo "📦 安装依赖..."
source venv/bin/activate
pip install -r requirements.txt

# 初始化数据库
echo "🗄️ 初始化数据库..."
python3 init_db.py

# 启动服务
echo "🔧 启动服务..."
systemctl start llrc
systemctl start nginx

# 检查服务状态
echo "📊 检查服务状态..."
systemctl status llrc --no-pager
systemctl status nginx --no-pager

echo "✅ 服务器启动完成！"
echo "🌐 访问地址: http://$(curl -s ifconfig.me)"
