#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云服务器权限和配置检查脚本
检查文件存储路径、权限、字体文件等配置
"""

import os
import sys
import tempfile
import platform
from pathlib import Path

def check_system_info():
    """检查系统信息"""
    print("=== 系统信息 ===")
    print(f"操作系统: {platform.system()}")
    print(f"Python版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"用户ID: {os.getuid() if hasattr(os, 'getuid') else 'Windows'}")
    print()

def check_temp_directories():
    """检查临时目录权限"""
    print("=== 临时目录检查 ===")
    
    temp_dirs = [
        tempfile.gettempdir(),
        '/tmp',
        '/var/tmp',
        os.path.join(os.getcwd(), 'temp'),
        os.path.join(os.getcwd(), 'uploads')
    ]
    
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            try:
                # 测试写入权限
                test_file = os.path.join(temp_dir, 'test_write.tmp')
                with open(test_file, 'w') as f:
                    f.write('test')
                os.remove(test_file)
                print(f"✓ {temp_dir} - 可写")
            except Exception as e:
                print(f"✗ {temp_dir} - 不可写: {e}")
        else:
            print(f"- {temp_dir} - 不存在")
    print()

def check_font_files():
    """检查字体文件"""
    print("=== 字体文件检查 ===")
    
    font_paths = []
    
    if platform.system() == "Windows":
        font_paths = [
            "C:/Windows/Fonts/simsun.ttc",
            "C:/Windows/Fonts/simhei.ttf",
            "C:/Windows/Fonts/msyh.ttc"
        ]
    elif platform.system() == "Linux":
        font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
        ]
    else:  # macOS
        font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc"
        ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            print(f"✓ {font_path}")
        else:
            print(f"✗ {font_path} - 不存在")
    
    # 检查项目本地字体目录
    local_font_dir = os.path.join(os.getcwd(), 'fonts')
    if os.path.exists(local_font_dir):
        print(f"✓ 本地字体目录: {local_font_dir}")
        fonts = os.listdir(local_font_dir)
        for font in fonts:
            if font.endswith(('.ttf', '.ttc', '.otf')):
                print(f"  - {font}")
    else:
        print(f"✗ 本地字体目录不存在: {local_font_dir}")
    print()

def check_python_dependencies():
    """检查Python依赖"""
    print("=== Python依赖检查 ===")
    
    dependencies = [
        'pandas',
        'openpyxl',
        'reportlab',
        'matplotlib',
        'numpy',
        'flask',
        'sqlalchemy'
    ]
    
    for dep in dependencies:
        try:
            module = __import__(dep)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {dep} - 版本: {version}")
        except ImportError:
            print(f"✗ {dep} - 未安装")
    print()

def check_file_permissions():
    """检查文件权限"""
    print("=== 文件权限检查 ===")
    
    test_paths = [
        os.getcwd(),
        tempfile.gettempdir(),
        os.path.join(os.getcwd(), 'logs'),
        os.path.join(os.getcwd(), 'reports')
    ]
    
    for path in test_paths:
        if os.path.exists(path):
            try:
                # 检查读取权限
                os.access(path, os.R_OK)
                read_ok = "✓"
            except:
                read_ok = "✗"
            
            try:
                # 检查写入权限
                os.access(path, os.W_OK)
                write_ok = "✓"
            except:
                write_ok = "✗"
            
            try:
                # 检查执行权限
                os.access(path, os.X_OK)
                exec_ok = "✓"
            except:
                exec_ok = "✗"
            
            print(f"{path}: 读{read_ok} 写{write_ok} 执行{exec_ok}")
        else:
            print(f"{path}: 不存在")
    print()

def create_test_files():
    """创建测试文件"""
    print("=== 测试文件创建 ===")
    
    test_files = [
        ('test_excel.xlsx', 'excel'),
        ('test_pdf.pdf', 'pdf'),
        ('test_txt.txt', 'text')
    ]
    
    for filename, file_type in test_files:
        try:
            if file_type == 'excel':
                # 测试Excel文件创建
                try:
                    import pandas as pd
                    df = pd.DataFrame({'测试': ['数据']})
                    df.to_excel(filename, index=False)
                    print(f"✓ {filename} - 创建成功")
                    os.remove(filename)
                except Exception as e:
                    print(f"✗ {filename} - 创建失败: {e}")
            
            elif file_type == 'pdf':
                # 测试PDF文件创建
                try:
                    from reportlab.pdfgen import canvas
                    c = canvas.Canvas(filename)
                    c.drawString(100, 100, "测试PDF")
                    c.save()
                    print(f"✓ {filename} - 创建成功")
                    os.remove(filename)
                except Exception as e:
                    print(f"✗ {filename} - 创建失败: {e}")
            
            elif file_type == 'text':
                # 测试文本文件创建
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write('测试文本文件')
                    print(f"✓ {filename} - 创建成功")
                    os.remove(filename)
                except Exception as e:
                    print(f"✗ {filename} - 创建失败: {e}")
        
        except Exception as e:
            print(f"✗ {filename} - 测试失败: {e}")
    
    print()

def main():
    """主函数"""
    print("云服务器权限和配置检查")
    print("=" * 50)
    
    check_system_info()
    check_temp_directories()
    check_font_files()
    check_python_dependencies()
    check_file_permissions()
    create_test_files()
    
    print("检查完成！")
    print("\n建议:")
    print("1. 如果看到 ✗ 标记，请根据错误信息进行修复")
    print("2. 确保临时目录有写入权限")
    print("3. 安装缺失的Python依赖")
    print("4. 配置中文字体文件")
    print("5. 检查Web服务用户权限")

if __name__ == "__main__":
    main()
