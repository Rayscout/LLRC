#!/usr/bin/env python3
import requests

print("测试注销端点...")
try:
    response = requests.post("http://127.0.0.1:5000/talent/hr_admin/employee-management/deactivate/1", timeout=5)
    print(f"状态码: {response.status_code}")
    if response.status_code == 401:
        print("✅ 端点正常，需要认证")
    elif response.status_code == 404:
        print("❌ 端点不存在")
    else:
        print(f"⚠️  其他状态码: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")

print("测试重新激活端点...")
try:
    response = requests.post("http://127.0.0.1:5000/talent/hr_admin/employee-management/reactivate/1", timeout=5)
    print(f"状态码: {response.status_code}")
    if response.status_code == 401:
        print("✅ 端点正常，需要认证")
    elif response.status_code == 404:
        print("❌ 端点不存在")
    else:
        print(f"⚠️  其他状态码: {response.status_code}")
except Exception as e:
    print(f"❌ 错误: {e}")
