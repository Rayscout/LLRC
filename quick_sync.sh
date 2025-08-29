#!/bin/bash

# 快速同步脚本 - 从GitHub拉取最新代码并重启服务
echo "⚡ 快速同步..."

# 服务器信息
SERVER_IP="60.205.251.52"
SERVER_USER="root"
PROJECT_DIR="/var/www/llrc"

# 在服务器上执行同步
ssh $SERVER_USER@$SERVER_IP << 'EOF'
cd /var/www/llrc

echo "📥 拉取最新代码..."
git fetch origin
git reset --hard origin/main

echo "📦 安装新依赖..."
source venv/bin/activate
pip install -r requirements.txt

echo "🔄 重启服务..."
systemctl restart llrc

echo "📊 检查服务状态..."
systemctl status llrc --no-pager

echo "✅ 同步完成！"
EOF

echo "✅ 快速同步完成！"
echo "🌐 访问地址: http://$SERVER_IP"
