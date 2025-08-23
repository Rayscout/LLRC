#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def test_employee_profile():
    """测试员工个人资料功能"""
    print("🔧 测试员工个人资料功能...")
    
    # 创建会话
    session = requests.Session()
    
    try:
        # 1. 访问登录页面
        print("🔍 访问登录页面...")
        response = session.get('http://localhost:5000/auth/sign', timeout=10)
        
        if response.status_code == 200:
            print("✅ 登录页面访问成功")
            
            # 2. 尝试登录员工账号
            print("🔍 尝试登录员工账号...")
            login_data = {
                'action': 'signin',
                'email': 'employee@test.com',
                'password': '123456',
                'role': 'employee'
            }
            
            response = session.post('http://localhost:5000/auth/sign', data=login_data, timeout=10)
            
            if response.status_code == 302:
                print("✅ 员工登录成功")
                
                # 3. 访问员工仪表盘
                print("🔍 访问员工仪表盘...")
                response = session.get('http://localhost:5000/talent_management/employee_management/employee_dashboard', timeout=10)
                
                if response.status_code == 200:
                    print("✅ 员工仪表盘访问成功")
                    
                    # 4. 访问个人资料页面
                    print("🔍 访问个人资料页面...")
                    response = session.get('http://localhost:5000/talent_management/employee_manager/profile/', timeout=10)
                    
                    if response.status_code == 200:
                        content = response.text
                        print("✅ 个人资料页面访问成功")
                        
                        # 检查页面内容
                        checks = [
                            ('个人资料', '页面标题'),
                            ('基本信息', '基本信息区域'),
                            ('技能标签', '技能区域'),
                            ('教育经历', '教育经历区域'),
                            ('工作经历', '工作经历区域'),
                            ('绩效评分历史', '绩效历史区域'),
                            ('编辑资料', '编辑按钮'),
                            ('导出PDF简历', 'PDF导出功能')
                        ]
                        
                        for element, description in checks:
                            if element in content:
                                print(f"✅ {description}: 找到")
                            else:
                                print(f"❌ {description}: 未找到")
                        
                        # 5. 测试编辑个人资料页面
                        print("🔍 测试编辑个人资料页面...")
                        response = session.get('http://localhost:5000/talent_management/employee_manager/profile/edit', timeout=10)
                        
                        if response.status_code == 200:
                            content = response.text
                            print("✅ 编辑个人资料页面访问成功")
                            
                            # 检查编辑页面内容
                            edit_checks = [
                                ('编辑个人资料', '编辑页面标题'),
                                ('基本信息', '基本信息表单'),
                                ('专业信息', '专业信息表单'),
                                ('教育经历', '教育经历表单'),
                                ('工作经历', '工作经历表单'),
                                ('保存更改', '保存按钮')
                            ]
                            
                            for element, description in edit_checks:
                                if element in content:
                                    print(f"✅ {description}: 找到")
                                else:
                                    print(f"❌ {description}: 未找到")
                            
                            # 6. 测试编辑功能
                            print("🔍 测试编辑功能...")
                            edit_data = {
                                'first_name': '测试',
                                'last_name': '员工',
                                'phone_number': '13800138000',
                                'birthday': '1990-01-01',
                                'bio': '我是一名经验丰富的软件工程师，专注于Web开发和人工智能应用。',
                                'skills': 'Python, JavaScript, React, Node.js, 项目管理',
                                'education': '清华大学 - 计算机科学与技术 - 本科 - 2012年',
                                'experience': '阿里巴巴 - 高级软件工程师 - 2018-2023\n负责电商平台后端开发，参与过多个大型项目。'
                            }
                            
                            response = session.post('http://localhost:5000/talent_management/employee_manager/profile/edit', data=edit_data, timeout=10)
                            
                            if response.status_code == 302:
                                print("✅ 个人资料编辑成功")
                                
                                # 7. 验证编辑结果
                                print("🔍 验证编辑结果...")
                                response = session.get('http://localhost:5000/talent_management/employee_manager/profile/', timeout=10)
                                
                                if response.status_code == 200:
                                    content = response.text
                                    if '测试员工' in content and 'Python' in content:
                                        print("✅ 编辑结果验证成功")
                                    else:
                                        print("❌ 编辑结果验证失败")
                                else:
                                    print(f"❌ 验证页面访问失败: {response.status_code}")
                            else:
                                print(f"❌ 编辑提交失败: {response.status_code}")
                        else:
                            print(f"❌ 编辑页面访问失败: {response.status_code}")
                    else:
                        print(f"❌ 个人资料页面访问失败: {response.status_code}")
                else:
                    print(f"❌ 员工仪表盘访问失败: {response.status_code}")
            else:
                print(f"❌ 员工登录失败: {response.status_code}")
                print("可能需要先创建员工测试账号")
        else:
            print(f"❌ 登录页面访问失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试出错: {e}")
    
    return True

if __name__ == "__main__":
    test_employee_profile()
