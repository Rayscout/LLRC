#!/bin/bash

# 快速同步脚本 - 只同步修改的文件
echo "⚡ 快速同步..."

# 服务器信息
SERVER_IP="60.205.251.52"
SERVER_USER="root"
PROJECT_DIR="/var/www/llrc"

# 同步特定文件或目录
echo "📤 同步文件..."
scp -r app/ $SERVER_USER@$SERVER_IP:$PROJECT_DIR/
scp -r smartrecruit_system/ $SERVER_USER@$SERVER_IP:$PROJECT_DIR/
scp -r talent_management_system/ $SERVER_USER@$SERVER_IP:$PROJECT_DIR/

# 重启服务
echo "🔄 重启服务..."
ssh $SERVER_USER@$SERVER_IP "systemctl restart llrc"

echo "✅ 同步完成！"
