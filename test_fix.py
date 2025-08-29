#!/usr/bin/env python3
import requests
import time

def test_pages():
    print("等待应用程序启动...")
    time.sleep(3)

    base_url = "http://127.0.0.1:5000"

    try:
        # 测试报表页面
        print("测试报表页面...")
        response = requests.get(f"{base_url}/smartrecruit/hr/dashboard/reports", timeout=10)
        print(f"报表页面状态码: {response.status_code}")

        # 测试洞察页面
        print("测试洞察页面...")
        response = requests.get(f"{base_url}/smartrecruit/hr/dashboard/insights", timeout=10)
        print(f"洞察页面状态码: {response.status_code}")

        print("测试完成")

    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_pages()
