#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试员工仪表板错误
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_employee_dashboard_error():
    """测试员工仪表板错误"""
    print("🔍 检查员工仪表板错误...")
    print("=" * 50)
    
    try:
        from app import create_app, db
        from app.models import User
        from talent_management_system.employee_manager_module.employee_auth import employee_dashboard
        
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
            
            # 查询员工用户
            print("\n2. 查询员工用户...")
            try:
                employees = User.query.filter_by(user_type='employee').all()
                print(f"   ✅ 成功查询到 {len(employees)} 个员工")
                
                if employees:
                    employee = employees[0]
                    print(f"   📋 员工信息: {employee.first_name} {employee.last_name}")
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
            
            # 测试员工仪表板函数
            print("\n3. 测试员工仪表板函数...")
            try:
                from flask import session
                
                # 模拟用户登录
                with app.test_request_context('/talent/employee_auth/dashboard'):
                    session['user_id'] = employee.id
                    session['user_type'] = 'employee'
                    
                    # 测试函数
                    result = employee_dashboard()
                    print("   ✅ 员工仪表板函数执行成功")
                    print(f"   📋 返回类型: {type(result)}")
                    
                    # 检查返回的内容
                    if isinstance(result, str):
                        print("   📋 返回HTML内容长度: {} 字符".format(len(result)))
                        if "error" in result.lower() or "exception" in result.lower():
                            print("   ⚠️ HTML内容中可能包含错误信息")
                    else:
                        print("   📋 返回对象: {}".format(result))
                    
            except Exception as e:
                print(f"   ❌ 员工仪表板函数执行失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 检查模板文件
            print("\n4. 检查模板文件...")
            template_path = "app/templates/talent_management/employee_management/employee_dashboard.html"
            if os.path.exists(template_path):
                print(f"   ✅ 模板文件存在: {template_path}")
                
                # 检查模板文件大小
                file_size = os.path.getsize(template_path)
                print(f"   📋 文件大小: {file_size} 字节")
                
                # 检查模板文件内容
                try:
                    with open(template_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        print(f"   📋 文件内容长度: {len(content)} 字符")
                        
                        # 检查是否有语法错误
                        if "{{" in content and "}}" in content:
                            print("   ✅ 模板语法标记正常")
                        else:
                            print("   ⚠️ 未找到模板语法标记")
                            
                except Exception as e:
                    print(f"   ❌ 读取模板文件失败: {e}")
                    return False
            else:
                print(f"   ❌ 模板文件不存在: {template_path}")
                return False
            
            # 检查路由注册
            print("\n5. 检查路由注册...")
            try:
                with app.test_client() as client:
                    # 测试路由是否存在
                    response = client.get('/talent/employee_auth/dashboard')
                    print(f"   📋 路由响应状态: {response.status_code}")
                    
                    if response.status_code == 200:
                        print("   ✅ 路由访问正常")
                    elif response.status_code == 302:
                        print("   ⚠️ 路由重定向 (可能需要登录)")
                    else:
                        print(f"   ❌ 路由访问失败: {response.status_code}")
                        
            except Exception as e:
                print(f"   ❌ 路由测试失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            print("\n✅ 员工仪表板检查完成")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_employee_dashboard_error()
