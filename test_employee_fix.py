#!/usr/bin/env python3
import requests
import time

def test_employee_modules():
    print("等待应用程序启动...")
    time.sleep(5)

    base_url = "http://127.0.0.1:5000"

    try:
        # 测试员工仪表盘
        print("测试员工仪表盘...")
        response = requests.get(f"{base_url}/talent/employee_management/employee_dashboard", timeout=10)
        print(f"员工仪表盘状态码: {response.status_code}")

        # 测试SMART目标页面
        print("测试SMART目标页面...")
        response = requests.get(f"{base_url}/talent/employee_management/smart_goals/", timeout=10)
        print(f"SMART目标页面状态码: {response.status_code}")

        print("✅ 员工模块测试完成！")

    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_employee_modules()
