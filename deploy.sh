#!/bin/bash

# LLRC项目部署脚本
echo "🚀 开始部署LLRC项目..."

# 设置变量
PROJECT_DIR="/var/www/llrc"
SERVICE_NAME="llrc"

# 检查是否以root权限运行
if [ "$EUID" -ne 0 ]; then
    echo "❌ 请以root权限运行此脚本"
    exit 1
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p $PROJECT_DIR
mkdir -p /var/log/llrc
mkdir -p /etc/nginx/sites-available
mkdir -p /etc/nginx/sites-enabled

# 设置权限
chown -R www-data:www-data $PROJECT_DIR
chown -R www-data:www-data /var/log/llrc

# 复制项目文件（假设项目文件在当前目录）
echo "📋 复制项目文件..."
cp -r . $PROJECT_DIR/
chown -R www-data:www-data $PROJECT_DIR

# 创建虚拟环境
echo "🐍 创建Python虚拟环境..."
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate

# 安装依赖
echo "📦 安装Python依赖..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# 创建生产环境配置文件
echo "⚙️ 创建生产环境配置..."
cat > $PROJECT_DIR/.env << EOF
SECRET_KEY=your_production_secret_key_$(date +%s)
DATABASE_URL=sqlite:////var/www/llrc/instance/site.db
FLASK_ENV=production
FLASK_DEBUG=False
MONGO_URI=mongodb://localhost:27017/applications
API_TOKEN=your_api_token_here
API_URL=https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct
EOF

# 设置环境变量权限
chown www-data:www-data $PROJECT_DIR/.env
chmod 600 $PROJECT_DIR/.env

# 复制服务文件
echo "🔧 配置系统服务..."
cp llrc.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable $SERVICE_NAME

# 配置Nginx
echo "🌐 配置Nginx..."
cp nginx.conf /etc/nginx/sites-available/llrc
ln -sf /etc/nginx/sites-available/llrc /etc/nginx/sites-enabled/

# 删除默认站点
rm -f /etc/nginx/sites-enabled/default

# 测试Nginx配置
nginx -t
if [ $? -eq 0 ]; then
    echo "✅ Nginx配置测试通过"
else
    echo "❌ Nginx配置测试失败"
    exit 1
fi

# 初始化数据库
echo "🗄️ 初始化数据库..."
cd $PROJECT_DIR
source venv/bin/activate
python3 -c "
from app import create_app
from app.models import db
app = create_app()
with app.app_context():
    db.create_all()
    print('数据库初始化完成')
"

# 启动服务
echo "🚀 启动服务..."
systemctl start $SERVICE_NAME
systemctl restart nginx

# 检查服务状态
echo "📊 检查服务状态..."
systemctl status $SERVICE_NAME --no-pager
systemctl status nginx --no-pager

# 配置防火墙
echo "🔥 配置防火墙..."
ufw allow 22
ufw allow 80
ufw allow 443
ufw --force enable

echo "✅ 部署完成！"
echo "🌐 访问地址: http://60.205.251.52"
echo "📝 查看日志: journalctl -u llrc -f"
echo "🔄 重启服务: systemctl restart llrc"
