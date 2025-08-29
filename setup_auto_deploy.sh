#!/bin/bash

# 一键设置自动部署
echo "🚀 设置自动部署..."

# 服务器信息
SERVER_IP="60.205.251.52"
SERVER_USER="root"
PROJECT_DIR="/var/www/llrc"

# 上传自动启动脚本
echo "📤 上传自动启动脚本..."
scp server_auto_start.sh $SERVER_USER@$SERVER_IP:/root/
scp server_hooks/post-receive $SERVER_USER@$SERVER_IP:/root/

# 在服务器上设置
ssh $SERVER_USER@$SERVER_IP << 'EOF'
# 设置自动启动脚本权限
chmod +x /root/server_auto_start.sh

# 设置Git钩子
mkdir -p /var/www/llrc/.git/hooks
cp /root/post-receive /var/www/llrc/.git/hooks/
chmod +x /var/www/llrc/.git/hooks/post-receive

# 初始化Git仓库（如果不存在）
cd /var/www/llrc
if [ ! -d ".git" ]; then
    git init
    git remote add origin https://github.com/YOUR_USERNAME/llrc-project.git
fi

echo "✅ 自动部署设置完成！"
echo "📝 请记得在GitHub仓库设置中配置Secrets"
EOF

echo "✅ 设置完成！"
echo "📝 下一步："
echo "1. 将代码推送到GitHub"
echo "2. 在GitHub仓库设置中配置Secrets"
echo "3. 运行自动启动脚本"
