#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF导出修复测试脚本
用于测试员工模块的PDF导出功能是否正常工作
"""

import os
import sys
import tempfile
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'talent_management_system'))

def test_pdf_export():
    """测试PDF导出功能"""
    print("=== PDF导出修复测试 ===")
    
    try:
        # 导入必要的模块
        from talent_management_system.employee_manager_module.profile import generate_pdf_resume, force_setup_chinese_font
        
        # 测试字体设置
        print("1. 测试字体设置...")
        font_name = force_setup_chinese_font()
        print(f"✓ 字体设置成功: {font_name}")
        
        # 创建模拟用户数据
        print("2. 创建模拟用户数据...")
        class MockUser:
            def __init__(self):
                self.first_name = "Ray"
                self.last_name = "Scout"
                self.employee_id = "001"
                self.department = "Tech"
                self.position = "team-member"
                self.email = "ray4@gmail.com"
                self.phone_number = "1234"
                self.hire_date = datetime(2025, 8, 14).date()
                self.bio = "Experienced software developer with strong problem-solving skills."
                self.experience = "Tech Company - Software Engineer - 2020-2023 - Developed web applications"
                self.education = "University - Computer Science - Bachelor - 2016-2020"
                self.skills = None
        
        user = MockUser()
        
        # 模拟其他数据
        skills = ["Python", "JavaScript", "React", "Node.js"]
        work_years = 3
        education_history = [
            {
                'school': 'University',
                'major': 'Computer Science',
                'degree': 'Bachelor',
                'period': '2016-2020'
            }
        ]
        work_history = [
            {
                'company': 'Tech Company',
                'position': 'Software Engineer',
                'period': '2020-2023',
                'description': 'Developed web applications'
            }
        ]
        performance_history = [
            {
                'period': '2024Q1',
                'score': 92,
                'level': 'Excellent',
                'evaluator': 'Manager',
                'comments': 'Outstanding performance and technical skills.'
            }
        ]
        
        print("3. 生成PDF...")
        pdf_path = generate_pdf_resume(user, skills, work_years, education_history, work_history, performance_history)
        
        if os.path.exists(pdf_path):
            print(f"✓ PDF生成成功: {pdf_path}")
            print(f"✓ 文件大小: {os.path.getsize(pdf_path)} bytes")
            
            # 检查文件内容
            with open(pdf_path, 'rb') as f:
                content = f.read()
                if b'%PDF' in content:
                    print("✓ PDF文件格式正确")
                else:
                    print("⚠️ PDF文件格式可能有问题")
            
            return True
        else:
            print("❌ PDF文件未生成")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_export()
    if success:
        print("\n🎉 PDF导出修复测试成功！")
    else:
        print("\n❌ PDF导出修复测试失败！")
