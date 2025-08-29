#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试公开岗位功能
"""

import requests
import json

def test_public_jobs():
    """测试公开岗位页面"""
    base_url = "http://localhost:5000"
    
    print("🧪 测试公开岗位功能...")
    
    # 测试首页
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ 首页访问成功")
            if "查看岗位" in response.text:
                print("✅ 首页包含'查看岗位'链接")
            else:
                print("❌ 首页缺少'查看岗位'链接")
        else:
            print(f"❌ 首页访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 首页访问异常: {e}")
    
    # 测试公开岗位页面
    try:
        response = requests.get(f"{base_url}/jobs")
        if response.status_code == 200:
            print("✅ 公开岗位页面访问成功")
            if "最新岗位" in response.text:
                print("✅ 公开岗位页面内容正确")
            else:
                print("❌ 公开岗位页面内容异常")
        else:
            print(f"❌ 公开岗位页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 公开岗位页面访问异常: {e}")
    
    # 测试岗位数据
    try:
        response = requests.get(f"{base_url}/jobs")
        if response.status_code == 200:
            # 检查是否包含岗位相关的HTML结构
            if 'job-card' in response.text:
                print("✅ 页面包含岗位卡片结构")
            else:
                print("⚠️  页面可能没有岗位数据")
        else:
            print(f"❌ 无法获取岗位数据: {response.status_code}")
    except Exception as e:
        print(f"❌ 岗位数据测试异常: {e}")

if __name__ == "__main__":
    test_public_jobs()
