#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试个人资料函数在Flask请求上下文中的表现
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_profile_with_context():
    """测试个人资料函数在Flask请求上下文中的表现"""
    print("🔍 测试个人资料函数在Flask请求上下文中的表现...")
    print("=" * 50)
    
    try:
        from app import create_app, db
        from app.models import User
        from talent_management_system.employee_manager_module.profile import profile_dashboard
        
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
                    print(f"      部门: {getattr(employee, 'employee_id', '未设置')}")
                    print(f"      职位: {getattr(employee, 'position', '未设置')}")
                    print(f"      入职日期: {getattr(employee, 'hire_date', '未设置')}")
                    print(f"      个人简介: {getattr(employee, 'bio', '未设置')}")
                    print(f"      工作经验: {getattr(employee, 'experience', '未设置')}")
                    print(f"      教育背景: {getattr(employee, 'education', '未设置')}")
                    print(f"      技能: {getattr(employee, 'skills', '未设置')}")
                else:
                    print("   ⚠️ 没有员工数据")
                    return False
                    
            except Exception as e:
                print(f"   ❌ 查询员工失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试3: 模拟Flask请求上下文
            print("\n3. 模拟Flask请求上下文...")
            try:
                from flask import request, session, g
                
                # 创建一个测试请求上下文
                with app.test_request_context('/talent/employee_manager/profile/'):
                    # 模拟用户登录
                    session['user_id'] = employee.id
                    
                    # 手动设置g.user（模拟before_request钩子）
                    g.user = employee
                    
                    print("   ✅ 成功创建测试请求上下文")
                    print(f"   📋 模拟用户ID: {session['user_id']}")
                    print(f"   📋 g.user已设置: {g.user.first_name} {g.user.last_name}")
                    
                    # 测试个人资料函数
                    print("\n4. 测试个人资料函数...")
                    try:
                        result = profile_dashboard()
                        print("   ✅ 个人资料函数执行成功")
                        print(f"   📋 返回类型: {type(result)}")
                        
                        if hasattr(result, 'status_code'):
                            print(f"   📋 状态码: {result.status_code}")
                        
                    except Exception as e:
                        print(f"   ❌ 个人资料函数执行失败: {e}")
                        import traceback
                        traceback.print_exc()
                        return False
                        
            except Exception as e:
                print(f"   ❌ 创建测试请求上下文失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            print("\n✅ 个人资料函数测试完成")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_profile_with_context()
