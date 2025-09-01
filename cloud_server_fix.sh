#!/bin/bash
"""
云服务器一键修复脚本
解决登录Internal Server Error问题
"""

echo "🚀 LLRC云服务器一键修复工具"
echo "=================================="

# 检查是否在云服务器上
if [[ ! "$(hostname)" == *"iZ"* ]]; then
    echo "❌ 此脚本需要在云服务器上运行"
    exit 1
fi

echo "📁 切换到项目目录..."
cd /var/www/llrc

echo "🔧 修复文件权限..."
sudo chown -R llrcuser:llrcuser /var/www/llrc/instance
sudo chmod 755 /var/www/llrc/instance
sudo chmod 644 /var/www/llrc/instance/site.db 2>/dev/null || true

echo "🐍 激活虚拟环境..."
source venv/bin/activate

echo "🔧 修复SQLAlchemy语法..."
python3 fix_sqlalchemy_syntax.py

echo "🗄️ 初始化数据库..."
python3 init_database_final.py

echo "🔄 重启服务..."
sudo systemctl restart llrc

echo "⏳ 等待服务启动..."
sleep 5

echo "🧪 测试服务状态..."
sudo systemctl status llrc --no-pager

echo "🌐 测试访问..."
curl -s -o /dev/null -w "%{http_code}" http://60.205.251.52/auth/sign

echo ""
echo "🎉 修复完成！"
echo "📝 测试账号："
echo "   HR管理员: hr@test.com / 123456"
echo "   员工账号: employee@test.com / 123456"
echo "   高管账号: executive@test.com / 123456"
echo "   求职者账号: candidate@test.com / 123456"
echo ""
echo "🌐 访问地址: http://60.205.251.52/auth/sign"
