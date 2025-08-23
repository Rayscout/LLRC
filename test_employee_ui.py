#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试新的员工界面
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_employee_ui():
    """测试新的员工界面"""
    print("🔍 测试新的员工界面...")
    print("=" * 50)
    
    try:
        from app import create_app, db
        from app.models import User
        
        print("✅ 成功导入所需模块")
        
        app = create_app()
        print("✅ 成功创建Flask应用")
        
        with app.app_context():
            # 测试1: 检查数据库连接
            print("\n1. 检查数据库连接...")
            try:
                from sqlalchemy import text
                db.session.execute(text("SELECT 1"))
                print("   ✅ 数据库连接正常")
            except Exception as e:
                print(f"   ❌ 数据库连接失败: {e}")
                return False
            
            # 测试2: 查询员工用户
            print("\n2. 查询员工用户...")
            try:
                employees = User.query.filter_by(user_type='employee').all()
                print(f"   ✅ 成功查询到 {len(employees)} 个员工")
                
                if employees:
                    employee = employees[0]
                    print(f"   📋 第一个员工: {employee.first_name} {employee.last_name}")
                    print(f"      邮箱: {employee.email}")
                    print(f"      员工编号: {getattr(employee, 'employee_id', '未设置')}")
                    print(f"      部门: {getattr(employee, 'department', '未设置')}")
                    print(f"      职位: {getattr(employee, 'position', '未设置')}")
                else:
                    print("   ⚠️ 没有员工数据")
                    return False
                    
            except Exception as e:
                print(f"   ❌ 查询员工失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试3: 测试员工仪表板函数
            print("\n3. 测试员工仪表板函数...")
            try:
                from talent_management_system.employee_manager_module.employee_auth import employee_dashboard
                from flask import session
                
                # 模拟用户登录
                with app.test_request_context('/talent/employee_auth/dashboard'):
                    session['user_id'] = employee.id
                    session['user_type'] = 'employee'
                    
                    # 测试函数
                    result = employee_dashboard()
                    print("   ✅ 员工仪表板函数执行成功")
                    print(f"   📋 返回类型: {type(result)}")
                    
            except Exception as e:
                print(f"   ❌ 员工仪表板函数执行失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            print("\n✅ 员工界面测试完成")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_employee_ui()
