#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试public_jobs页面背景颜色更改
"""

import requests
from bs4 import BeautifulSoup
import re

def test_background_changes():
    """测试页面背景颜色是否已更改"""
    try:
        # 测试公开岗位页面
        response = requests.get('http://localhost:5000/jobs')
        if response.status_code == 200:
            print("✅ 公开岗位页面访问成功")
            
            # 检查页面内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 检查是否还有紫色背景
            purple_gradients = soup.find_all(string=re.compile(r'linear-gradient.*#667eea.*#764ba2'))
            if purple_gradients:
                print("❌ 页面仍包含紫色渐变背景")
                for gradient in purple_gradients:
                    print(f"   发现: {gradient.strip()}")
            else:
                print("✅ 页面已移除紫色渐变背景")
            
            # 检查是否使用了CSS变量
            css_vars = soup.find_all(string=re.compile(r'var\(--bg\)|var\(--fg\)|var\(--primary\)'))
            if css_vars:
                print("✅ 页面使用了CSS变量系统")
                for var in css_vars:
                    print(f"   使用变量: {var.strip()}")
            else:
                print("❌ 页面未使用CSS变量系统")
            
            # 检查背景颜色设置
            background_styles = soup.find_all(string=re.compile(r'background.*var\(--bg\)'))
            if background_styles:
                print("✅ 页面背景使用CSS变量")
            else:
                print("❌ 页面背景未使用CSS变量")
                
        else:
            print(f"❌ 公开岗位页面访问失败: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Flask应用正在运行")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

if __name__ == "__main__":
    print("🔍 测试public_jobs页面背景颜色更改...")
    test_background_changes()
