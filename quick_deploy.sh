#!/bin/bash

# LLRC 快速部署脚本
echo "🚀 LLRC 快速部署开始..."

# 检查是否为root用户
if [[ $EUID -eq 0 ]]; then
   echo "❌ 请不要使用root用户运行此脚本"
   exit 1
fi

# 项目配置
PROJECT_DIR="/var/www/llrc"

echo "📋 部署配置:"
echo "项目目录: $PROJECT_DIR"

# 1. 创建目录并设置权限
echo "📁 创建目录..."
sudo mkdir -p /var/log/llrc /var/run/llrc
sudo chown -R www-data:www-data /var/log/llrc /var/run/llrc

# 2. 安装依赖
echo "📦 安装系统依赖..."
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git nginx

# 3. 设置项目权限
echo "🔐 设置权限..."
sudo chown -R www-data:www-data $PROJECT_DIR

# 4. 创建虚拟环境
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo "🐍 创建虚拟环境..."
    cd $PROJECT_DIR
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "🐍 更新依赖..."
    cd $PROJECT_DIR
    source venv/bin/activate
    pip install -r requirements.txt
fi

# 5. 配置服务
echo "⚙️ 配置服务..."
sudo cp $PROJECT_DIR/llrc.service /etc/systemd/system/
sudo systemctl daemon-reload

# 6. 配置Nginx
echo "🌐 配置Nginx..."
sudo cp $PROJECT_DIR/nginx.conf /etc/nginx/sites-available/llrc
sudo ln -sf /etc/nginx/sites-available/llrc /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 7. 启动服务
echo "🚀 启动服务..."
sudo systemctl enable llrc
sudo systemctl start llrc
sudo systemctl restart nginx

# 8. 配置防火墙
echo "🔥 配置防火墙..."
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# 9. 显示结果
echo "✅ 部署完成！"
echo ""
echo "📱 访问信息:"
echo "本地访问: http://localhost"
echo "外部访问: http://$(curl -s ifconfig.me)"
echo "健康检查: http://$(curl -s ifconfig.me)/health"
echo ""
echo "🔧 常用命令:"
echo "查看服务状态: sudo systemctl status llrc"
echo "重启服务: sudo systemctl restart llrc"
echo "查看日志: sudo journalctl -u llrc -f"
echo ""
echo "🎉 现在你的同学可以通过服务器IP访问你的应用了！"
