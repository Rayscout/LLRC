#!/usr/bin/env python3
"""
测试视频下载功能的脚本
"""

import os
from app import create_app

def test_video_download():
    """测试视频下载功能"""
    app = create_app()
    
    with app.test_client() as client:
        # 模拟用户登录
        with client.session_transaction() as sess:
            sess['user_id'] = 1  # 假设用户ID为1
        
        # 测试文件 - 使用实际存在的文件
        test_filename = "Amina_El-Bakali_Resume.pdf"  # 使用实际存在的PDF文件
        
        print(f"测试文件: {test_filename}")
        print("=" * 50)
        
        # 测试1: 专用下载路由
        print("1. 测试专用下载路由 /download/video/<filename>")
        response = client.get(f'/download/video/{test_filename}')
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"   响应头: {dict(response.headers)}")
        else:
            print(f"   错误响应: {response.get_json()}")
        print()
        
        # 测试2: 简单下载路由
        print("2. 测试简单下载路由 /simple/video/<filename>")
        response = client.get(f'/simple/video/{test_filename}')
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"   响应头: {dict(response.headers)}")
        else:
            print(f"   错误响应: {response.get_json()}")
        print()
        
        # 测试3: 静态文件路由
        print("3. 测试静态文件路由 /static/uploads/cv/<filename>")
        response = client.get(f'/static/uploads/cv/{test_filename}')
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            print(f"   响应头: {dict(response.headers)}")
        else:
            print(f"   错误响应: {response.get_data(as_text=True)[:200]}")
        print()
        
        # 测试4: 检查文件是否存在
        print("4. 检查文件是否存在")
        file_path = os.path.join(app.config['UPLOAD_FOLDER_CV'], test_filename)
        print(f"   文件路径: {file_path}")
        print(f"   文件存在: {os.path.exists(file_path)}")
        if os.path.exists(file_path):
            print(f"   文件大小: {os.path.getsize(file_path)} 字节")
            print(f"   文件可读: {os.access(file_path, os.R_OK)}")
        print()

if __name__ == '__main__':
    test_video_download()
