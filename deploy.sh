#!/bin/bash

# LLRC 自动部署脚本
# 使用方法: ./deploy.sh

set -e  # 遇到错误立即退出

echo "🚀 开始部署 LLRC 应用..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查是否为root用户
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}错误: 请不要使用root用户运行此脚本${NC}"
   exit 1
fi

# 项目配置
PROJECT_NAME="llrc"
PROJECT_DIR="/var/www/llrc"
SERVICE_NAME="llrc"
NGINX_SITE="llrc"

echo -e "${YELLOW}📋 部署配置:${NC}"
echo "项目名称: $PROJECT_NAME"
echo "项目目录: $PROJECT_DIR"
echo "服务名称: $SERVICE_NAME"

# 1. 创建必要的目录
echo -e "\n${YELLOW}📁 创建必要的目录...${NC}"
sudo mkdir -p /var/log/llrc
sudo mkdir -p /var/run/llrc
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled

# 2. 设置目录权限
echo -e "\n${YELLOW}🔐 设置目录权限...${NC}"
sudo chown -R www-data:www-data /var/log/llrc
sudo chown -R www-data:www-data /var/run/llrc
sudo chown -R www-data:www-data $PROJECT_DIR

# 3. 安装系统依赖
echo -e "\n${YELLOW}📦 安装系统依赖...${NC}"
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git nginx supervisor

# 4. 创建虚拟环境（如果不存在）
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo -e "\n${YELLOW}🐍 创建Python虚拟环境...${NC}"
    cd $PROJECT_DIR
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo -e "\n${YELLOW}🐍 更新Python依赖...${NC}"
    cd $PROJECT_DIR
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# 5. 复制服务文件
echo -e "\n${YELLOW}⚙️ 配置系统服务...${NC}"
sudo cp $PROJECT_DIR/llrc.service /etc/systemd/system/
sudo systemctl daemon-reload

# 6. 配置Nginx
echo -e "\n${YELLOW}🌐 配置Nginx...${NC}"
sudo cp $PROJECT_DIR/nginx.conf /etc/nginx/sites-available/$NGINX_SITE
sudo ln -sf /etc/nginx/sites-available/$NGINX_SITE /etc/nginx/sites-enabled/

# 删除默认站点
sudo rm -f /etc/nginx/sites-enabled/default

# 测试Nginx配置
sudo nginx -t

# 7. 启动服务
echo -e "\n${YELLOW}🚀 启动服务...${NC}"
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME
sudo systemctl restart nginx

# 8. 检查服务状态
echo -e "\n${YELLOW}📊 检查服务状态...${NC}"
echo "LLRC服务状态:"
sudo systemctl status $SERVICE_NAME --no-pager

echo -e "\nNginx服务状态:"
sudo systemctl status nginx --no-pager

# 9. 配置防火墙
echo -e "\n${YELLOW}🔥 配置防火墙...${NC}"
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw --force enable

# 10. 显示访问信息
echo -e "\n${GREEN}✅ 部署完成！${NC}"
echo -e "\n${YELLOW}📱 访问信息:${NC}"
echo "本地访问: http://localhost"
echo "外部访问: http://$(curl -s ifconfig.me)"
echo "健康检查: http://$(curl -s ifconfig.me)/health"

echo -e "\n${YELLOW}🔧 常用命令:${NC}"
echo "查看服务状态: sudo systemctl status $SERVICE_NAME"
echo "重启服务: sudo systemctl restart $SERVICE_NAME"
echo "查看日志: sudo journalctl -u $SERVICE_NAME -f"
echo "查看Nginx日志: sudo tail -f /var/log/nginx/access.log"

echo -e "\n${GREEN}🎉 部署成功！你的同学现在可以通过服务器IP访问你的应用了！${NC}"
