#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def test_simple_page():
    """简单测试页面加载"""
    print("🔍 简单测试页面加载...")
    
    try:
        # 测试求职者首页
        print("🔍 测试求职者首页...")
        response = requests.get('http://localhost:5000/smartrecruit/candidate/', timeout=10)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            print("✅ 页面加载成功")
            
            # 检查关键元素
            checks = [
                ('candidate_ios_style.css', 'CSS文件引用'),
                ('navbar', '导航栏'),
                ('智能推荐', '导航文本'),
                ('为您推荐', '页面内容'),
                ('快速操作', '页面内容')
            ]
            
            for element, description in checks:
                if element in content:
                    print(f"✅ {description}: 找到")
                else:
                    print(f"❌ {description}: 未找到")
            
            # 检查页面长度
            print(f"页面长度: {len(content)} 字符")
            
            # 显示页面前500字符
            print(f"页面开头: {content[:500]}...")
            
        else:
            print(f"❌ 页面加载失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试出错: {e}")

if __name__ == "__main__":
    test_simple_page()
