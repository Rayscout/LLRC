#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文字体安装脚本
用于在云服务器上安装中文字体，解决PDF导出中文显示问题
"""

import os
import sys
import platform
import urllib.request
import zipfile
import subprocess
import shutil

def install_fonts_ubuntu():
    """在Ubuntu/Debian系统上安装中文字体"""
    print("正在Ubuntu/Debian系统上安装中文字体...")
    
    try:
        # 更新包列表
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        
        # 安装中文字体包
        font_packages = [
            'fonts-noto-cjk',
            'fonts-wqy-microhei',
            'fonts-wqy-zenhei',
            'fonts-arphic-uming',
            'fonts-arphic-ukai',
            'fonts-liberation',
            'fonts-dejavu'
        ]
        
        for package in font_packages:
            try:
                print(f"正在安装 {package}...")
                subprocess.run(['sudo', 'apt-get', 'install', '-y', package], check=True)
                print(f"{package} 安装成功")
            except subprocess.CalledProcessError as e:
                print(f"{package} 安装失败: {e}")
        
        # 刷新字体缓存
        subprocess.run(['sudo', 'fc-cache', '-fv'], check=True)
        print("字体缓存已刷新")
        
        return True
        
    except Exception as e:
        print(f"Ubuntu字体安装失败: {e}")
        return False

def install_fonts_centos():
    """在CentOS/RHEL系统上安装中文字体"""
    print("正在CentOS/RHEL系统上安装中文字体...")
    
    try:
        # 安装中文字体包
        font_packages = [
            'google-noto-sans-cjk-fonts',
            'google-noto-serif-cjk-fonts',
            'wqy-microhei-fonts',
            'wqy-zenhei-fonts',
            'liberation-fonts',
            'dejavu-fonts'
        ]
        
        for package in font_packages:
            try:
                print(f"正在安装 {package}...")
                subprocess.run(['sudo', 'yum', 'install', '-y', package], check=True)
                print(f"{package} 安装成功")
            except subprocess.CalledProcessError as e:
                print(f"{package} 安装失败: {e}")
        
        # 刷新字体缓存
        subprocess.run(['sudo', 'fc-cache', '-fv'], check=True)
        print("字体缓存已刷新")
        
        return True
        
    except Exception as e:
        print(f"CentOS字体安装失败: {e}")
        return False

def download_fonts_manually():
    """手动下载字体文件到项目目录"""
    print("正在手动下载字体文件...")
    
    # 创建字体目录
    font_dir = os.path.join(os.path.dirname(__file__), 'fonts')
    os.makedirs(font_dir, exist_ok=True)
    
    # 字体下载链接
    font_urls = {
        'NotoSansCJK-Regular.otf': 'https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Chinese/NotoSansCJKsc-Regular.otf',
        'NotoSansCJK-Medium.otf': 'https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Chinese/NotoSansCJKsc-Medium.otf',
        'NotoSansCJK-Bold.otf': 'https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Chinese/NotoSansCJKsc-Bold.otf',
    }
    
    for font_name, font_url in font_urls.items():
        font_path = os.path.join(font_dir, font_name)
        if not os.path.exists(font_path):
            try:
                print(f"正在下载 {font_name}...")
                urllib.request.urlretrieve(font_url, font_path)
                print(f"{font_name} 下载完成")
            except Exception as e:
                print(f"{font_name} 下载失败: {e}")
        else:
            print(f"{font_name} 已存在")
    
    return font_dir

def test_font_availability():
    """测试字体可用性"""
    print("正在测试字体可用性...")
    
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        
        # 测试系统字体
        system_fonts = [
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Medium.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
        ]
        
        for font_path in system_fonts:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('TestFont', font_path))
                    print(f"✓ 字体可用: {font_path}")
                    return True
                except Exception as e:
                    print(f"✗ 字体不可用: {font_path} - {e}")
        
        # 测试项目内字体
        font_dir = os.path.join(os.path.dirname(__file__), 'fonts')
        project_fonts = [
            os.path.join(font_dir, 'NotoSansCJK-Regular.otf'),
            os.path.join(font_dir, 'NotoSansCJK-Medium.otf'),
        ]
        
        for font_path in project_fonts:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('TestFont', font_path))
                    print(f"✓ 项目字体可用: {font_path}")
                    return True
                except Exception as e:
                    print(f"✗ 项目字体不可用: {font_path} - {e}")
        
        print("✗ 没有可用的中文字体")
        return False
        
    except Exception as e:
        print(f"字体测试失败: {e}")
        return False

def main():
    """主函数"""
    print("=== 中文字体安装脚本 ===")
    print(f"操作系统: {platform.system()}")
    print(f"系统版本: {platform.release()}")
    
    # 检查是否为Linux系统
    if platform.system() != 'Linux':
        print("此脚本仅适用于Linux系统")
        return
    
    # 检测Linux发行版
    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read().lower()
            if 'ubuntu' in content or 'debian' in content:
                distro = 'ubuntu'
            elif 'centos' in content or 'rhel' in content or 'redhat' in content:
                distro = 'centos'
            else:
                distro = 'unknown'
    except:
        distro = 'unknown'
    
    print(f"Linux发行版: {distro}")
    
    # 安装系统字体
    if distro == 'ubuntu':
        install_fonts_ubuntu()
    elif distro == 'centos':
        install_fonts_centos()
    else:
        print("未知的Linux发行版，跳过系统字体安装")
    
    # 手动下载字体
    font_dir = download_fonts_manually()
    
    # 测试字体可用性
    if test_font_availability():
        print("✓ 中文字体安装成功！")
        print(f"字体文件位置: {font_dir}")
    else:
        print("✗ 中文字体安装失败")
        print("请手动安装中文字体或检查网络连接")

if __name__ == '__main__':
    main()
