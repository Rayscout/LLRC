#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试人才流失预警导出功能
"""

import requests
import json

def test_turnover_export():
    """测试人才流失预警导出功能"""
    print("🧪 测试人才流失预警导出功能...")
    
    # 测试导出端点
    url = "http://localhost:5000/talent/hr_admin/turnover_alert/api/export_data"
    
    try:
        response = requests.post(url, timeout=30)
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ 导出成功！")
            print(f"文件大小: {len(response.content)} bytes")
            
            # 保存文件
            filename = f"turnover_alert_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"✅ 文件已保存为: {filename}")
            
        elif response.status_code == 401:
            print("⚠️ 需要登录")
        elif response.status_code == 403:
            print("⚠️ 权限不足")
        else:
            print(f"❌ 导出失败: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败: {e}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    from datetime import datetime
    test_turnover_export()
