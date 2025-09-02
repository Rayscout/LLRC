#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
调试登录错误
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def debug_login_error():
    """调试登录错误"""
    print("🔍 调试登录错误...")
    print("=" * 50)
    
    try:
        from app import create_app, db
        from app.models import User
        from app.common.auth import sign
        
        print("✅ 成功导入所需模块")
        
        app = create_app()
        print("✅ 成功创建Flask应用")
        
        with app.app_context():
            # 检查数据库连接
            print("\n1. 检查数据库连接...")
            try:
                from sqlalchemy import text
                db.session.execute(text("SELECT 1"))
                print("   ✅ 数据库连接正常")
            except Exception as e:
                print(f"   ❌ 数据库连接失败: {e}")
                return False
            
            # 检查员工用户
            print("\n2. 检查员工用户...")
            try:
                employees = User.query.filter_by(user_type='employee').all()
                print(f"   ✅ 成功查询到 {len(employees)} 个员工")
                
                if employees:
                    employee = employees[0]
                    print(f"   📋 员工信息: {employee.first_name} {employee.last_name}")
                    print(f"      邮箱: {employee.email}")
                    print(f"      密码: {employee.password}")
                    print(f"      用户类型: {employee.user_type}")
                    
                    # 测试密码验证
                    test_password = '123456'
                    if employee.password == test_password:
                        print("   ✅ 密码验证正确")
                    else:
                        print(f"   ❌ 密码验证失败，期望: {test_password}，实际: {employee.password}")
                else:
                    print("   ⚠️ 没有员工数据")
                    return False
                    
            except Exception as e:
                print(f"   ❌ 查询员工失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试登录函数
            print("\n3. 测试登录函数...")
            try:
                from flask import request, session
                from werkzeug.test import EnvironBuilder
                from werkzeug.wrappers import Request
                
                # 创建模拟请求
                with app.test_request_context('/auth/sign', method='POST'):
                    # 设置表单数据
                    from flask import request
                    request.form = {
                        'action': 'signin',
                        'email': employee.email,
                        'password': '123456',
                        'role': 'employee'
                    }
                    # 测试登录
                    result = sign()
                    print("   ✅ 登录函数执行成功")
                    print(f"   📋 返回类型: {type(result)}")
                    
                    if hasattr(result, 'status_code'):
                        print(f"   📋 响应状态: {result.status_code}")
                    
            except Exception as e:
                print(f"   ❌ 登录函数执行失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            print("\n✅ 登录错误调试完成")
            return True
            
    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_login_error()
