#!/usr/bin/env python3
"""
测试头像和简历上传功能
"""

import os
import sys
import tempfile
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_upload_folders():
    """测试上传文件夹是否存在"""
    print("=== 测试上传文件夹 ===")
    
    # 检查上传文件夹配置
    from app.config import Config
    
    cv_folder = Config.UPLOAD_FOLDER_CV
    photos_folder = Config.UPLOAD_FOLDER_PHOTOS
    
    print(f"CV上传文件夹: {cv_folder}")
    print(f"头像上传文件夹: {photos_folder}")
    
    # 检查文件夹是否存在
    cv_exists = os.path.exists(cv_folder)
    photos_exists = os.path.exists(photos_folder)
    
    print(f"CV文件夹存在: {cv_exists}")
    print(f"头像文件夹存在: {photos_exists}")
    
    if cv_exists:
        cv_files = os.listdir(cv_folder)
        print(f"CV文件夹中的文件数量: {len(cv_files)}")
    
    if photos_exists:
        photo_files = os.listdir(photos_folder)
        print(f"头像文件夹中的文件数量: {len(photo_files)}")
    
    return cv_exists and photos_exists

def test_upload_utils():
    """测试上传工具函数"""
    print("\n=== 测试上传工具函数 ===")
    
    from app.utils import allowed_file, get_allowed_cv_extensions
    
    # 测试文件格式检查
    test_files = [
        ('test.pdf', True),
        ('test.docx', True),
        ('test.png', True),
        ('test.jpg', True),
        ('test.mp4', True),
        ('test.txt', False),
        ('test.exe', False),
    ]
    
    allowed_extensions = get_allowed_cv_extensions()
    print(f"允许的CV文件扩展名: {allowed_extensions}")
    
    for filename, expected in test_files:
        result = allowed_file(filename, allowed_extensions)
        status = "✓" if result == expected else "✗"
        print(f"{status} {filename}: {result} (期望: {expected})")
    
    # 测试头像格式检查
    photo_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    photo_test_files = [
        ('avatar.png', True),
        ('avatar.jpg', True),
        ('avatar.jpeg', True),
        ('avatar.gif', True),
        ('avatar.pdf', False),
        ('avatar.txt', False),
    ]
    
    print(f"\n允许的头像文件扩展名: {photo_extensions}")
    
    for filename, expected in photo_test_files:
        result = allowed_file(filename, photo_extensions)
        status = "✓" if result == expected else "✗"
        print(f"{status} {filename}: {result} (期望: {expected})")

def test_profile_module():
    """测试profile模块"""
    print("\n=== 测试Profile模块 ===")
    
    try:
        from smartrecruit_system.candidate_module.profile import profile_bp
        print("✓ Profile蓝图导入成功")
        
        # 检查路由
        routes = []
        for rule in profile_bp.url_map.iter_rules():
            routes.append(f"{rule.rule} [{', '.join(rule.methods)}]")
        
        print(f"Profile模块路由:")
        for route in routes:
            print(f"  - {route}")
            
    except Exception as e:
        print(f"✗ Profile模块导入失败: {e}")

def test_files_module():
    """测试文件下载模块"""
    print("\n=== 测试文件下载模块 ===")
    
    try:
        from app.common.files import files_bp
        print("✓ Files蓝图导入成功")
        
        # 检查路由
        routes = []
        for rule in files_bp.url_map.iter_rules():
            routes.append(f"{rule.rule} [{', '.join(rule.methods)}]")
        
        print(f"Files模块路由:")
        for route in routes:
            print(f"  - {route}")
            
    except Exception as e:
        print(f"✗ Files模块导入失败: {e}")

def test_app_creation():
    """测试应用程序创建"""
    print("\n=== 测试应用程序创建 ===")
    
    try:
        from app import create_app
        app = create_app()
        print("✓ 应用程序创建成功")
        
        # 检查蓝图注册
        registered_blueprints = list(app.blueprints.keys())
        print(f"注册的蓝图: {registered_blueprints}")
        
        # 检查配置
        print(f"CV上传文件夹配置: {app.config.get('UPLOAD_FOLDER_CV')}")
        print(f"头像上传文件夹配置: {app.config.get('UPLOAD_FOLDER_PHOTOS')}")
        
        return True
        
    except Exception as e:
        print(f"✗ 应用程序创建失败: {e}")
        return False

def create_test_files():
    """创建测试文件"""
    print("\n=== 创建测试文件 ===")
    
    # 创建测试图片文件
    test_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x0cIDATx\x9cc```\x00\x00\x00\x04\x00\x01\xf5\x00\x01\x00\x00\x00\x00IEND\xaeB`\x82'
    
    # 创建测试PDF文件
    test_pdf_content = b'%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test PDF) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF'
    
    test_files = [
        ('test_image.png', test_image_content),
        ('test_document.pdf', test_pdf_content),
    ]
    
    for filename, content in test_files:
        with open(filename, 'wb') as f:
            f.write(content)
        print(f"✓ 创建测试文件: {filename}")

def main():
    """主测试函数"""
    print("开始测试上传功能...\n")
    
    # 测试上传文件夹
    folders_ok = test_upload_folders()
    
    # 测试工具函数
    test_upload_utils()
    
    # 测试模块导入
    test_profile_module()
    test_files_module()
    
    # 测试应用程序创建
    app_ok = test_app_creation()
    
    # 创建测试文件
    create_test_files()
    
    print("\n=== 测试总结 ===")
    print(f"上传文件夹: {'✓' if folders_ok else '✗'}")
    print(f"应用程序创建: {'✓' if app_ok else '✗'}")
    
    if folders_ok and app_ok:
        print("\n✓ 上传功能测试通过！")
        print("现在可以测试实际的文件上传功能了。")
    else:
        print("\n✗ 上传功能测试失败，请检查配置。")

if __name__ == '__main__':
    main()
