#!/usr/bin/env python3
"""
验证仪表盘URL修复
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_template_fixes():
    """验证模板文件中的URL修复"""
    template_files = [
        'app/templates/talent_management/employee_management/smart_goals_dashboard.html',
        'app/templates/talent_management/employee_management/projects_dashboard.html',
        'app/templates/talent_management/employee_management/feedback_dashboard.html',
        'app/templates/talent_management/employee_management/profile_dashboard.html',
        'app/templates/talent_management/employee_management/performance_dashboard.html',
        'app/templates/talent_management/employee_management/learning_dashboard.html',
        'app/templates/talent_management/employee_management/compensation_dashboard.html'
    ]

    print("=== 验证模板文件URL修复 ===")

    all_correct = True

    for template_file in template_files:
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查是否还有错误的URL
            if 'talent_management.employee_auth.employee_dashboard' in content:
                print(f"❌ {template_file}: 仍然包含错误URL")
                all_correct = False
            else:
                print(f"✅ {template_file}: URL修复正确")

            # 检查是否包含正确的URL
            if 'talent_management.employee_management.employee_dashboard' in content:
                print(f"   包含正确URL: ✅")
            else:
                print(f"   缺少正确URL: ⚠️")
        else:
            print(f"❌ {template_file}: 文件不存在")

    # 检查认证文件中的URL
    auth_file = 'talent_management_system/employee_manager_module/employee_auth.py'
    if os.path.exists(auth_file):
        with open(auth_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'talent_management.employee_management.employee_dashboard' in content:
            print(f"✅ {auth_file}: 认证重定向URL正确")
        else:
            print(f"❌ {auth_file}: 认证重定向URL可能有问题")
            all_correct = False

    if all_correct:
        print("\n🎉 所有URL修复验证通过！")
        print("现在所有返回仪表盘的链接都指向正确的路由。")
    else:
        print("\n❌ 还有URL需要修复。")

    return all_correct

if __name__ == "__main__":
    verify_template_fixes()

