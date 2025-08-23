#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试SMART目标功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_smart_goals():
    """测试SMART目标功能"""
    print("🎯 测试SMART目标功能...")
    print("=" * 60)
    
    try:
        from app import create_app, db
        from app.models import User
        from talent_management_system.employee_manager_module.smart_goals import (
            analyze_skill_gaps, generate_recommended_goals, calculate_goal_stats,
            get_user_goals, SMART_GOAL_TEMPLATES
        )
        
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
                    print(f"      职位: {getattr(employee, 'position', '未设置')}")
                    print(f"      部门: {getattr(employee, 'department', '未设置')}")
                else:
                    print("   ⚠️ 没有员工数据")
                    return False
                    
            except Exception as e:
                print(f"   ❌ 查询员工失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试技能差距分析
            print("\n3. 测试技能差距分析...")
            try:
                skill_gaps = analyze_skill_gaps(employee)
                print(f"   ✅ 成功分析技能差距，发现 {len(skill_gaps)} 个差距")
                
                if skill_gaps:
                    print("   📋 技能差距详情:")
                    for i, gap in enumerate(skill_gaps[:3], 1):
                        print(f"      {i}. {gap['skill']} - {gap['estimated_learning_hours']}小时 ({gap['priority']}优先级)")
                else:
                    print("   📋 暂无技能差距")
                    
            except Exception as e:
                print(f"   ❌ 技能差距分析失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试推荐目标生成
            print("\n4. 测试推荐目标生成...")
            try:
                recommended_goals = generate_recommended_goals(employee, skill_gaps)
                print(f"   ✅ 成功生成 {len(recommended_goals)} 个推荐目标")
                
                if recommended_goals:
                    print("   📋 推荐目标详情:")
                    for i, goal in enumerate(recommended_goals[:3], 1):
                        print(f"      {i}. {goal['title']}")
                        print(f"         类别: {goal['category']}, 优先级: {goal['priority']}")
                        print(f"         预计时间: {goal['estimated_hours']}小时")
                else:
                    print("   📋 暂无推荐目标")
                    
            except Exception as e:
                print(f"   ❌ 推荐目标生成失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试用户目标获取
            print("\n5. 测试用户目标获取...")
            try:
                user_goals = get_user_goals(employee.id)
                print(f"   ✅ 成功获取 {len(user_goals)} 个用户目标")
                
                if user_goals:
                    print("   📋 用户目标详情:")
                    for i, goal in enumerate(user_goals, 1):
                        print(f"      {i}. {goal['title']}")
                        print(f"         进度: {goal['progress']}%, 状态: {goal['status']}")
                        print(f"         预计时间: {goal['estimated_hours']}小时, 已完成: {goal['completed_hours']}小时")
                else:
                    print("   📋 暂无用户目标")
                    
            except Exception as e:
                print(f"   ❌ 用户目标获取失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试目标统计计算
            print("\n6. 测试目标统计计算...")
            try:
                goal_stats = calculate_goal_stats(user_goals)
                print("   ✅ 成功计算目标统计")
                print(f"   📋 统计结果:")
                print(f"      总目标数: {goal_stats['total_goals']}")
                print(f"      进行中: {goal_stats['active_goals']}")
                print(f"      已完成: {goal_stats['completed_goals']}")
                print(f"      平均进度: {goal_stats['avg_progress']}%")
                print(f"      完成率: {goal_stats['completion_rate']}%")
                print(f"      总时间: {goal_stats['total_hours']}小时")
                print(f"      已完成时间: {goal_stats['completed_hours']}小时")
                    
            except Exception as e:
                print(f"   ❌ 目标统计计算失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试SMART目标模板
            print("\n7. 测试SMART目标模板...")
            try:
                print("   ✅ SMART目标模板加载成功")
                print(f"   📋 模板统计:")
                
                total_templates = 0
                for category, templates in SMART_GOAL_TEMPLATES.items():
                    if isinstance(templates, dict):
                        for subcategory, goals in templates.items():
                            if isinstance(goals, list):
                                total_templates += len(goals)
                                print(f"      {category}.{subcategory}: {len(goals)} 个模板")
                    elif isinstance(templates, list):
                        total_templates += len(templates)
                        print(f"      {category}: {len(templates)} 个模板")
                
                print(f"      总计: {total_templates} 个目标模板")
                    
            except Exception as e:
                print(f"   ❌ SMART目标模板测试失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试路由访问
            print("\n8. 测试路由访问...")
            try:
                from flask import session
                
                with app.test_request_context('/talent/employee_manager/smart_goals/'):
                    session['user_id'] = employee.id
                    session['user_type'] = 'employee'
                    
                    from talent_management_system.employee_manager_module.smart_goals import goals_dashboard
                    result = goals_dashboard()
                    print("   ✅ SMART目标仪表板路由访问成功")
                    print(f"   📋 返回类型: {type(result)}")
                    
            except Exception as e:
                print(f"   ❌ 路由访问失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            print("\n✅ SMART目标功能测试完成")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_smart_goals()
