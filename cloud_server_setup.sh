#!/bin/bash

# 云服务器Gemini API配置脚本
# 使用方法: bash cloud_server_setup.sh

echo "🚀 云服务器Gemini API配置脚本"
echo "=================================="

# 检查是否为root用户
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  检测到root用户，建议使用普通用户运行"
fi

# 设置API密钥（请替换为你的实际密钥）
GOOGLE_API_KEY="AIzaSyDdOylv0bq8q1UypVG-r4m2yHxHNf_CsMo"
GEMINI_API_KEY="AIzaSyDdOylv0bq8q1UypVG-r4m2yHxHNf_CsMo"
GEMINI_MODEL="gemini-1.5-flash"

echo "📝 设置环境变量..."

# 方法1: 设置当前会话环境变量
export GOOGLE_API_KEY="$GOOGLE_API_KEY"
export GEMINI_API_KEY="$GEMINI_API_KEY"
export GEMINI_MODEL="$GEMINI_MODEL"

# 方法2: 添加到.bashrc文件
echo "" >> ~/.bashrc
echo "# Gemini API配置" >> ~/.bashrc
echo "export GOOGLE_API_KEY=\"$GOOGLE_API_KEY\"" >> ~/.bashrc
echo "export GEMINI_API_KEY=\"$GEMINI_API_KEY\"" >> ~/.bashrc
echo "export GEMINI_MODEL=\"$GEMINI_MODEL\"" >> ~/.bashrc

# 方法3: 创建.env文件
cat > .env << EOF
GOOGLE_API_KEY=$GOOGLE_API_KEY
GEMINI_API_KEY=$GEMINI_API_KEY
GEMINI_MODEL=$GEMINI_MODEL
EOF

# 方法4: 设置系统级环境变量
sudo tee /etc/environment.d/gemini.conf > /dev/null << EOF
GOOGLE_API_KEY=$GOOGLE_API_KEY
GEMINI_API_KEY=$GEMINI_API_KEY
GEMINI_MODEL=$GEMINI_MODEL
EOF

echo "✅ 环境变量设置完成"
echo ""

# 验证环境变量
echo "🔍 验证环境变量设置..."
echo "GOOGLE_API_KEY: ${GOOGLE_API_KEY:0:10}..."
echo "GEMINI_API_KEY: ${GEMINI_API_KEY:0:10}..."
echo "GEMINI_MODEL: $GEMINI_MODEL"
echo ""

# 测试网络连接
echo "🌐 测试网络连接..."
if ping -c 3 generativelanguage.googleapis.com > /dev/null 2>&1; then
    echo "✅ 网络连接正常"
else
    echo "❌ 网络连接失败，可能需要配置代理或防火墙"
fi
echo ""

# 测试API连接
echo "🧪 测试API连接..."
if command -v curl > /dev/null; then
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=$GOOGLE_API_KEY" \
        -X POST \
        -H "Content-Type: application/json" \
        -d '{"contents":[{"parts":[{"text":"Hello"}]}]}')
    
    if [ "$response" = "200" ]; then
        echo "✅ API连接测试成功"
    else
        echo "❌ API连接测试失败，状态码: $response"
    fi
else
    echo "⚠️  curl未安装，跳过API连接测试"
fi
echo ""

# 安装Python依赖
echo "📦 检查Python依赖..."
if command -v python3 > /dev/null; then
    echo "✅ Python3已安装"
    
    # 检查requests库
    if python3 -c "import requests" 2>/dev/null; then
        echo "✅ requests库已安装"
    else
        echo "📥 安装requests库..."
        pip3 install requests
    fi
else
    echo "❌ Python3未安装，请先安装Python3"
fi
echo ""

# 运行测试脚本
echo "🧪 运行API测试脚本..."
if [ -f "test_gemini_api.py" ]; then
    python3 test_gemini_api.py
else
    echo "⚠️  测试脚本不存在，跳过测试"
fi
echo ""

# 重启服务（如果使用systemd）
if systemctl is-active --quiet llrc 2>/dev/null; then
    echo "🔄 重启LLRC服务..."
    sudo systemctl restart llrc
    echo "✅ 服务重启完成"
elif systemctl is-active --quiet llrc_simple 2>/dev/null; then
    echo "🔄 重启LLRC简单服务..."
    sudo systemctl restart llrc_simple
    echo "✅ 服务重启完成"
else
    echo "ℹ️  未检测到运行中的LLRC服务"
fi
echo ""

echo "🎉 配置完成！"
echo ""
echo "📋 下一步操作："
echo "1. 重新加载环境变量: source ~/.bashrc"
echo "2. 或者重新登录服务器"
echo "3. 检查应用日志确认配置生效"
echo "4. 测试语音识别功能"
echo ""
echo "🔧 如果仍有问题，请检查："
echo "- 网络连接和防火墙设置"
echo "- API密钥是否正确"
echo "- 应用日志中的详细错误信息"
