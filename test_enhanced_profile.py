#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试增强的个人资料功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_enhanced_profile():
    """测试增强的个人资料功能"""
    print("🔍 测试增强的个人资料功能...")
    print("=" * 60)
    
    try:
        from app import create_app, db
        from app.models import User
        from talent_management_system.employee_manager_module.profile import (
            profile_dashboard, parse_education_history, parse_work_history, 
            get_performance_history, extract_skills_from_text
        )
        
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
            
            # 测试3: 测试技能提取功能
            print("\n3. 测试技能提取功能...")
            try:
                test_text = "我是一名Python开发工程师，有3年Django和Flask开发经验，熟悉MySQL和Redis数据库，会使用Docker和Git。"
                skills = extract_skills_from_text(test_text)
                print(f"   ✅ 技能提取成功")
                print(f"   📋 提取的技能: {skills}")
                
            except Exception as e:
                print(f"   ❌ 技能提取失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试4: 测试教育经历解析
            print("\n4. 测试教育经历解析...")
            try:
                education_text = "清华大学 - 计算机科学与技术 - 学士学位 - 2018-2022\n北京大学 - 软件工程 - 硕士学位 - 2022-2024"
                education_history = parse_education_history(education_text)
                print(f"   ✅ 教育经历解析成功")
                print(f"   📋 解析结果: {len(education_history)} 条记录")
                for edu in education_history:
                    print(f"      - {edu['school']} - {edu['major']} - {edu['degree']}")
                
            except Exception as e:
                print(f"   ❌ 教育经历解析失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试5: 测试工作经历解析
            print("\n5. 测试工作经历解析...")
            try:
                experience_text = "腾讯科技 - 高级开发工程师 - 2022-2024 - 负责微信支付系统的开发和维护\n阿里巴巴 - 开发工程师 - 2020-2022 - 参与电商平台的开发"
                work_history = parse_work_history(experience_text)
                print(f"   ✅ 工作经历解析成功")
                print(f"   📋 解析结果: {len(work_history)} 条记录")
                for work in work_history:
                    print(f"      - {work['company']} - {work['position']}")
                
            except Exception as e:
                print(f"   ❌ 工作经历解析失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试6: 测试绩效历史获取
            print("\n6. 测试绩效历史获取...")
            try:
                performance_history = get_performance_history(employee.id)
                print(f"   ✅ 绩效历史获取成功")
                print(f"   📋 获取结果: {len(performance_history)} 条记录")
                for perf in performance_history:
                    print(f"      - {perf['period']}: {perf['score']}分 ({perf['level']})")
                
            except Exception as e:
                print(f"   ❌ 绩效历史获取失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试7: 测试个人资料仪表板函数
            print("\n7. 测试个人资料仪表板函数...")
            try:
                from flask import session
                
                # 模拟用户登录
                with app.test_request_context('/talent/employee_manager/profile/'):
                    session['user_id'] = employee.id
                    session['user_type'] = 'employee'
                    
                    # 测试函数
                    result = profile_dashboard()
                    print("   ✅ 个人资料仪表板函数执行成功")
                    print(f"   📋 返回类型: {type(result)}")
                    
            except Exception as e:
                print(f"   ❌ 个人资料仪表板函数执行失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            print("\n✅ 增强的个人资料功能测试完成")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_enhanced_profile()
