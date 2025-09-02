#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有模块的导出功能
"""

import requests
import json
from datetime import datetime

def test_all_exports():
    """测试所有模块的导出功能"""
    print("🧪 测试所有模块的导出功能...")
    
    # 测试端点列表
    endpoints = [
        {
            "name": "薪酬分析导出",
            "url": "http://localhost:5000/talent/hr_admin/salary_analysis/api/export_data",
            "method": "POST"
        },
        {
            "name": "组织健康度导出",
            "url": "http://localhost:5000/talent/hr_admin/org_health/api/export_report",
            "method": "POST"
        },
        {
            "name": "职业发展追踪导出",
            "url": "http://localhost:5000/talent/hr_admin/career_tracking/api/export_report",
            "method": "POST"
        },
        {
            "name": "人才流失预警导出",
            "url": "http://localhost:5000/talent/hr_admin/turnover_alert/api/export_data",
            "method": "POST"
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n📋 测试 {endpoint['name']}...")
        
        try:
            response = requests.post(endpoint['url'], timeout=30)
            
            print(f"状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("✅ 导出成功！")
                print(f"文件大小: {len(response.content)} bytes")
                
                # 保存文件
                filename = f"{endpoint['name'].replace('导出', '')}_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
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
    
    print("\n🎉 所有模块导出功能测试完成！")

if __name__ == "__main__":
    test_all_exports()
