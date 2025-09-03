#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试高管职业发展路径导出功能
"""

import requests
import json
import os
import sys

def test_executive_career_export():
    """测试高管职业发展路径导出功能"""
    
    # 服务器地址
    base_url = "http://localhost:5000"
    
    print("🧪 开始测试高管职业发展路径导出功能...")
    
    # 1. 测试高管登录
    print("\n1. 测试高管登录...")
    login_data = {
        'username': 'executive',
        'password': 'executive123',
        'user_type': 'executive'
    }
    
    try:
        login_response = requests.post(f"{base_url}/talent/executive_auth/login", data=login_data)
        print(f"登录响应状态: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("✅ 高管登录成功")
            
            # 获取session cookies
            cookies = login_response.cookies
            
            # 2. 测试高管仪表板访问
            print("\n2. 测试高管仪表板访问...")
            dashboard_response = requests.get(f"{base_url}/talent/hr_admin/executive_dashboard", cookies=cookies)
            print(f"仪表板响应状态: {dashboard_response.status_code}")
            
            if dashboard_response.status_code == 200:
                print("✅ 高管仪表板访问成功")
                
                # 3. 测试职业发展路径导出
                print("\n3. 测试职业发展路径导出...")
                export_response = requests.post(
                    f"{base_url}/talent/hr_admin/export_executive_career_path",
                    cookies=cookies,
                    headers={'Content-Type': 'application/json'}
                )
                
                print(f"导出响应状态: {export_response.status_code}")
                print(f"响应头: {dict(export_response.headers)}")
                
                if export_response.status_code == 200:
                    print("✅ 职业发展路径导出成功")
                    
                    # 检查是否是Excel文件
                    content_type = export_response.headers.get('Content-Type', '')
                    if 'spreadsheet' in content_type or 'excel' in content_type:
                        print("✅ 确认导出的是Excel文件")
                        
                        # 保存文件
                        filename = f"executive_career_path_test_{os.getpid()}.xlsx"
                        with open(filename, 'wb') as f:
                            f.write(export_response.content)
                        print(f"✅ 文件已保存为: {filename}")
                        
                        # 检查文件大小
                        file_size = len(export_response.content)
                        print(f"文件大小: {file_size} 字节")
                        
                        if file_size > 1000:  # 至少1KB
                            print("✅ 文件大小合理")
                        else:
                            print("⚠️ 文件可能太小，请检查内容")
                    else:
                        print("⚠️ 响应不是Excel文件")
                        print(f"内容类型: {content_type}")
                        
                elif export_response.status_code == 401:
                    print("❌ 导出失败: 未授权 (401)")
                elif export_response.status_code == 403:
                    print("❌ 导出失败: 权限不足 (403)")
                elif export_response.status_code == 500:
                    print("❌ 导出失败: 服务器内部错误 (500)")
                    try:
                        error_data = export_response.json()
                        print(f"错误详情: {error_data}")
                    except:
                        print(f"错误响应: {export_response.text}")
                else:
                    print(f"❌ 导出失败: 状态码 {export_response.status_code}")
                    print(f"响应内容: {export_response.text}")
            else:
                print("❌ 高管仪表板访问失败")
                print(f"响应内容: {dashboard_response.text}")
        else:
            print("❌ 高管登录失败")
            print(f"响应内容: {login_response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
    
    print("\n🏁 测试完成")

if __name__ == "__main__":
    test_executive_career_export()
