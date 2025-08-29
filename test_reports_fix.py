#!/usr/bin/env python3
"""
测试报表和AI洞察模块修复的脚本
"""

import requests
import time
from flask import Flask
import threading
import sys

def test_reports_access():
    """测试报表和AI洞察模块的访问"""
    print("开始测试报表和AI洞察模块...")

    # 等待应用程序启动
    time.sleep(3)

    try:
        # 测试报表页面
        print("测试报表页面...")
        response = requests.get('http://127.0.0.1:5000/smartrecruit/hr/dashboard/reports', timeout=10)

        if response.status_code == 200:
            print("✅ 报表页面访问成功")
            if 'report_data' in response.text:
                print("✅ 报表数据正确传递")
            else:
                print("⚠️ 报表页面访问成功，但未找到report_data")
                print(f"页面内容预览: {response.text[:200]}...")
        elif response.status_code == 302:
            print("ℹ️ 报表页面重定向（需要登录）- 这是正常的")
            print(f"重定向到: {response.headers.get('Location', '未知')}")
        else:
            print(f"❌ 报表页面访问失败，状态码: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")

        # 测试AI洞察页面
        print("测试AI洞察页面...")
        response = requests.get('http://127.0.0.1:5000/smartrecruit/hr/dashboard/insights', timeout=10)

        if response.status_code == 200:
            print("✅ AI洞察页面访问成功")
            if 'insights' in response.text:
                print("✅ AI洞察数据正确传递")
            else:
                print("⚠️ AI洞察页面访问成功，但未找到insights数据")
        elif response.status_code == 302:
            print("ℹ️ AI洞察页面重定向（需要登录）- 这是正常的")
        else:
            print(f"❌ AI洞察页面访问失败，状态码: {response.status_code}")

        print("测试完成！")

    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
        print("请确保Flask应用程序正在运行")

if __name__ == "__main__":
    test_reports_access()
