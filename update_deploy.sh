#!/bin/bash

# 更新部署脚本
echo "🚀 开始更新部署..."

# 服务器信息
SERVER_IP="60.205.251.52"
SERVER_USER="root"
PROJECT_DIR="/var/www/llrc"

# 上传修改的文件
echo "📤 上传文件到服务器..."
scp -r app/* $SERVER_USER@$SERVER_IP:$PROJECT_DIR/app/
scp -r smartrecruit_system/* $SERVER_USER@$SERVER_IP:$PROJECT_DIR/smartrecruit_system/
scp -r talent_management_system/* $SERVER_USER@$SERVER_IP:$PROJECT_DIR/talent_management_system/

# 重启服务
echo "🔄 重启服务..."
ssh $SERVER_USER@$SERVER_IP "cd $PROJECT_DIR && systemctl restart llrc"

# 检查服务状态
echo "📊 检查服务状态..."
ssh $SERVER_USER@$SERVER_IP "systemctl status llrc --no-pager"

echo "✅ 更新部署完成！"
echo "🌐 访问地址: http://$SERVER_IP"
