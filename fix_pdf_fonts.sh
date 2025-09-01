#!/bin/bash

# PDF字体修复脚本
# 用于在云服务器上安装中文字体，解决PDF导出中文显示问题

echo "=== PDF字体修复脚本 ==="
echo "正在检测系统环境..."

# 检测操作系统
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
    echo "操作系统: $OS $VER"
else
    echo "无法检测操作系统"
    exit 1
fi

# 检测是否为Ubuntu/Debian系统
if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
    echo "检测到Ubuntu/Debian系统，开始安装中文字体..."
    
    # 更新包列表
    sudo apt-get update
    
    # 安装中文字体包
    echo "正在安装中文字体包..."
    sudo apt-get install -y \
        fonts-noto-cjk \
        fonts-wqy-microhei \
        fonts-wqy-zenhei \
        fonts-arphic-uming \
        fonts-arphic-ukai \
        fonts-liberation \
        fonts-dejavu \
        fontconfig
    
    # 刷新字体缓存
    echo "正在刷新字体缓存..."
    sudo fc-cache -fv
    
    echo "Ubuntu/Debian字体安装完成"

# 检测是否为CentOS/RHEL系统
elif [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]] || [[ "$OS" == *"RHEL"* ]]; then
    echo "检测到CentOS/RHEL系统，开始安装中文字体..."
    
    # 安装中文字体包
    echo "正在安装中文字体包..."
    sudo yum install -y \
        google-noto-sans-cjk-fonts \
        google-noto-serif-cjk-fonts \
        wqy-microhei-fonts \
        wqy-zenhei-fonts \
        liberation-fonts \
        dejavu-fonts \
        fontconfig
    
    # 刷新字体缓存
    echo "正在刷新字体缓存..."
    sudo fc-cache -fv
    
    echo "CentOS/RHEL字体安装完成"

else
    echo "未知的操作系统: $OS"
    echo "请手动安装中文字体包"
fi

# 创建项目字体目录
echo "正在创建项目字体目录..."
FONT_DIR="$(dirname "$0")/fonts"
mkdir -p "$FONT_DIR"

# 下载字体文件
echo "正在下载字体文件..."
cd "$FONT_DIR"

# 下载Noto Sans CJK字体
if [ ! -f "NotoSansCJK-Regular.otf" ]; then
    echo "下载 NotoSansCJK-Regular.otf..."
    wget -O NotoSansCJK-Regular.otf \
        "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Chinese/NotoSansCJKsc-Regular.otf"
fi

if [ ! -f "NotoSansCJK-Medium.otf" ]; then
    echo "下载 NotoSansCJK-Medium.otf..."
    wget -O NotoSansCJK-Medium.otf \
        "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Chinese/NotoSansCJKsc-Medium.otf"
fi

if [ ! -f "NotoSansCJK-Bold.otf" ]; then
    echo "下载 NotoSansCJK-Bold.otf..."
    wget -O NotoSansCJK-Bold.otf \
        "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Chinese/NotoSansCJKsc-Bold.otf"
fi

# 检查字体文件是否下载成功
echo "检查字体文件..."
if [ -f "NotoSansCJK-Regular.otf" ]; then
    echo "✓ NotoSansCJK-Regular.otf 下载成功"
else
    echo "✗ NotoSansCJK-Regular.otf 下载失败"
fi

if [ -f "NotoSansCJK-Medium.otf" ]; then
    echo "✓ NotoSansCJK-Medium.otf 下载成功"
else
    echo "✗ NotoSansCJK-Medium.otf 下载失败"
fi

if [ -f "NotoSansCJK-Bold.otf" ]; then
    echo "✓ NotoSansCJK-Bold.otf 下载成功"
else
    echo "✗ NotoSansCJK-Bold.otf 下载失败"
fi

# 设置字体文件权限
echo "设置字体文件权限..."
chmod 644 *.otf

# 测试字体可用性
echo "测试字体可用性..."
python3 "$(dirname "$0")/test_pdf_fonts.py"

echo "=== 字体修复完成 ==="
echo "字体目录: $FONT_DIR"
echo "请重启应用程序以使字体生效"
