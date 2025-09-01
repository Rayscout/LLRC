#!/bin/bash

# 中文字体安装脚本
# 用于解决PDF生成中中文显示为方框的问题

echo "=== 中文字体安装脚本 ==="
echo "正在检查和安装中文字体..."

# 检查系统类型
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "检测到Linux系统"
    
    # 检查是否以root权限运行
    if [[ $EUID -ne 0 ]]; then
        echo "请使用sudo运行此脚本以安装字体"
        echo "命令: sudo bash install_chinese_fonts.sh"
        exit 1
    fi
    
    # 更新包管理器
    echo "更新包管理器..."
    if command -v apt-get &> /dev/null; then
        apt-get update
        echo "安装中文字体包..."
        apt-get install -y fonts-noto-cjk fonts-wqy-microhei fonts-wqy-zenhei fonts-arphic-uming fonts-arphic-ukai
    elif command -v yum &> /dev/null; then
        yum update -y
        echo "安装中文字体包..."
        yum install -y google-noto-cjk-fonts wqy-microhei-fonts wqy-zenhei-fonts
    elif command -v dnf &> /dev/null; then
        dnf update -y
        echo "安装中文字体包..."
        dnf install -y google-noto-cjk-fonts wqy-microhei-fonts wqy-zenhei-fonts
    else
        echo "不支持的包管理器，请手动安装中文字体"
    fi
    
    # 刷新字体缓存
    echo "刷新字体缓存..."
    fc-cache -fv
    
    # 检查字体是否安装成功
    echo "检查字体安装情况..."
    echo "Noto CJK字体:"
    fc-list | grep -i "noto.*cjk" | head -5
    
    echo "文泉驿字体:"
    fc-list | grep -i "wqy" | head -5
    
    echo "AR PL字体:"
    fc-list | grep -i "ar pl" | head -5
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "检测到macOS系统"
    echo "macOS通常已包含中文字体，无需额外安装"
    
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    echo "检测到Windows系统"
    echo "Windows通常已包含中文字体，无需额外安装"
    
else
    echo "未知系统类型: $OSTYPE"
fi

echo ""
echo "=== 字体检查完成 ==="
echo "如果仍有字体问题，请检查以下路径是否存在中文字体文件："
echo "Linux: /usr/share/fonts/truetype/noto/"
echo "Linux: /usr/share/fonts/truetype/wqy/"
echo "Linux: /usr/share/fonts/truetype/arphic/"
echo ""
echo "您也可以手动下载字体文件并放置到相应目录"
