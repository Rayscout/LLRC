#!/bin/bash

# 自动部署脚本
echo "🚀 开始自动部署..."

# 服务器信息
SERVER_IP="60.205.251.52"
SERVER_USER="root"
PROJECT_DIR="/var/www/llrc"

# 上传配置文件
echo "📤 上传配置文件..."
scp gunicorn.conf.py $SERVER_USER@$SERVER_IP:$PROJECT_DIR/
scp llrc.service $SERVER_USER@$SERVER_IP:$PROJECT_DIR/
scp nginx.conf $SERVER_USER@$SERVER_IP:$PROJECT_DIR/
scp init_db.py $SERVER_USER@$SERVER_IP:$PROJECT_DIR/

# 在服务器上执行部署
ssh $SERVER_USER@$SERVER_IP << 'EOF'
cd /var/www/llrc

# 设置Git仓库
if [ ! -d ".git" ]; then
    git init
    git config --global --add safe.directory /var/www/llrc
    git remote add origin https://github.com/Rayscout/LLRC.git
fi

# 拉取最新代码
echo "📥 拉取最新代码..."
git fetch origin
git reset --hard origin/main

# 设置权限
chown -R www-data:www-data /var/www/llrc

# 配置systemd服务
cp llrc.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable llrc

# 配置Nginx
cp nginx.conf /etc/nginx/sites-available/llrc
ln -sf /etc/nginx/sites-available/llrc /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# 测试Nginx配置
nginx -t

# 初始化数据库
source venv/bin/activate
python3 init_db.py

# 启动服务
systemctl start llrc
systemctl restart nginx

# 检查服务状态
echo "📊 检查服务状态..."
systemctl status llrc --no-pager
systemctl status nginx --no-pager

echo "✅ 自动部署完成！"
EOF

echo "✅ 部署脚本执行完成！"
echo "🌐 访问地址: http://$SERVER_IP"
