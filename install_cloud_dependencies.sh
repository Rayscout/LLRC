#!/bin/bash

# 云服务器依赖安装脚本
# 用于安装Excel导出和数据处理所需的Python库

echo "开始安装云服务器依赖..."

# 更新包管理器
if command -v apt-get &> /dev/null; then
    echo "检测到Ubuntu/Debian系统，使用apt-get..."
    sudo apt-get update
    sudo apt-get install -y python3-pip python3-dev build-essential
elif command -v yum &> /dev/null; then
    echo "检测到CentOS/RHEL系统，使用yum..."
    sudo yum update -y
    sudo yum install -y python3-pip python3-devel gcc
else
    echo "未知的包管理器，请手动安装Python3和pip"
    exit 1
fi

# 升级pip
echo "升级pip..."
python3 -m pip install --upgrade pip

# 安装Excel处理依赖
echo "安装Excel处理依赖..."
python3 -m pip install pandas==2.1.4 openpyxl==3.1.2 xlrd==2.0.1 xlwt==1.3.0

# 安装其他必要依赖
echo "安装其他必要依赖..."
python3 -m pip install numpy matplotlib reportlab

# 验证安装
echo "验证安装..."
python3 -c "
try:
    import pandas as pd
    print('✓ pandas 安装成功:', pd.__version__)
except ImportError as e:
    print('✗ pandas 安装失败:', e)

try:
    import openpyxl
    print('✓ openpyxl 安装成功:', openpyxl.__version__)
except ImportError as e:
    print('✗ openpyxl 安装失败:', e)

try:
    import numpy as np
    print('✓ numpy 安装成功:', np.__version__)
except ImportError as e:
    print('✗ numpy 安装失败:', e)

try:
    import matplotlib
    print('✓ matplotlib 安装成功:', matplotlib.__version__)
except ImportError as e:
    print('✗ matplotlib 安装失败:', e)

try:
    from reportlab.pdfbase import pdfmetrics
    print('✓ reportlab 安装成功')
except ImportError as e:
    print('✗ reportlab 安装失败:', e)
"

echo "依赖安装完成！"
echo "如果看到任何 ✗ 标记，请手动安装相应的包"
echo "重启Web服务以使更改生效"
