#!/bin/bash
# 云服务器部署脚本

set -e

echo "🚀 开始部署LLRC应用..."

# 项目配置
PROJECT_DIR="/var/www/llrc"
SERVICE_NAME="llrc"

# 1. 拉取最新代码
echo "📥 拉取最新代码..."
cd $PROJECT_DIR
git fetch origin
git reset --hard origin/pxy

# 2. 更新依赖
echo "📦 更新Python依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. 检查表情识别模块
echo "🤖 检查表情识别模块..."
python3 -c "
from smartrecruit_system.candidate_module.emotion_recognition import get_emotion_recognition_ai
ai = get_emotion_recognition_ai()
print('✅ 表情识别模块正常')
"

# 4. 重启服务
echo "🔄 重启服务..."
sudo systemctl restart $SERVICE_NAME

# 5. 检查服务状态
echo "📊 检查服务状态..."
sudo systemctl status $SERVICE_NAME --no-pager

echo "✅ 部署完成！"
