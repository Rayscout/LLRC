#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试个人资料逻辑
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_profile_logic():
    """测试个人资料逻辑"""
    print("🔍 测试个人资料逻辑...")
    print("=" * 50)
    
    try:
        from app import create_app, db
        from app.models import User
        from talent_management_system.employee_manager_module.profile import extract_skills_from_text
        
        print("✅ 成功导入所需模块")
        
        app = create_app()
        print("✅ 成功创建Flask应用")
        
        with app.app_context():
            # 测试1: 数据库连接
            print("\n1. 测试数据库连接...")
            try:
                from sqlalchemy import text
                db.session.execute(text("SELECT 1"))
                print("   ✅ 数据库连接正常")
            except Exception as e:
                print(f"   ❌ 数据库连接失败: {e}")
                return False
            
            # 测试2: 查询员工用户
            print("\n2. 测试查询员工用户...")
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
            
            # 测试3: 测试技能提取函数
            print("\n3. 测试技能提取函数...")
            try:
                test_text = "我是一名Python开发工程师，有3年Django和Flask开发经验，熟悉MySQL和Redis数据库。"
                skills = extract_skills_from_text(test_text)
                print(f"   ✅ 技能提取成功")
                print(f"   📋 提取的技能: {skills}")
                
            except Exception as e:
                print(f"   ❌ 技能提取失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试4: 测试工作年限计算
            print("\n4. 测试工作年限计算...")
            try:
                from datetime import datetime
                
                if employee.hire_date:
                    hire_date = employee.hire_date
                    if isinstance(hire_date, str):
                        hire_date = datetime.strptime(hire_date, '%Y-%m-%d').date()
                    
                    work_years = (datetime.now().date() - hire_date).days // 365
                    print(f"   ✅ 工作年限计算成功")
                    print(f"   📋 入职日期: {employee.hire_date}")
                    print(f"   📋 工作年限: {work_years} 年")
                else:
                    print("   ⚠️ 员工没有入职日期")
                    
            except Exception as e:
                print(f"   ❌ 工作年限计算失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            print("\n✅ 个人资料逻辑测试完成")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_profile_logic()
