#!/usr/bin/env python3
import requests
import time

def test_app():
    print("等待应用程序启动...")
    time.sleep(3)

    try:
        # 测试主页
        response = requests.get("http://127.0.0.1:5000/", timeout=10)
        print(f"主页状态码: {response.status_code}")

        # 测试报表页面
        response = requests.get("http://127.0.0.1:5000/smartrecruit/hr/dashboard/reports", timeout=10)
        print(f"报表页面状态码: {response.status_code}")

        # 测试洞察页面
        response = requests.get("http://127.0.0.1:5000/smartrecruit/hr/dashboard/insights", timeout=10)
        print(f"洞察页面状态码: {response.status_code}")

        print("✅ 应用程序启动成功，所有页面可访问！")

    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_app()
