#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试员工界面路由注册情况
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_blueprint_registration():
    """测试蓝图注册情况"""
    try:
        from app import create_app
        print("✅ 成功导入create_app函数")
        
        app = create_app()
        print("✅ 成功创建Flask应用")
        
        # 检查注册的蓝图
        print("\n📋 已注册的蓝图:")
        for blueprint_name, blueprint in app.blueprints.items():
            print(f"  - {blueprint_name}: {blueprint}")
        
        # 检查员工相关的路由
        print("\n🔍 检查员工相关路由:")
        
        # 检查talent_management蓝图
        if 'talent_management' in app.blueprints:
            talent_bp = app.blueprints['talent_management']
            print(f"  ✅ talent_management蓝图已注册")
            
            # 检查子蓝图
            if hasattr(talent_bp, 'deferred_functions'):
                print(f"  📝 talent_management子蓝图数量: {len(talent_bp.deferred_functions)}")
            else:
                print(f"  ⚠️ 无法获取talent_management子蓝图信息")
        else:
            print(f"  ❌ talent_management蓝图未注册")
        
        # 检查具体路由
        print("\n🌐 可用的员工相关URL:")
        employee_urls = [
            '/talent/employee/auth',
            '/talent/employee/dashboard',
            '/talent/employee_manager/profile/',
            '/talent/employee_manager/performance/',
            '/talent/employee_manager/projects/',
            '/talent/employee_manager/learning_recommendation/dashboard'
        ]
        
        for url in employee_urls:
            try:
                with app.test_request_context(url):
                    # 尝试匹配路由
                    adapter = app.url_map.bind('localhost')
                    endpoint, values = adapter.match(url)
                    print(f"  ✅ {url} -> {endpoint}")
            except Exception as e:
                print(f"  ❌ {url} -> 错误: {e}")
        
        print("\n✅ 蓝图注册测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        from talent_management_system.employee_manager_module import employee_manager_bp
        print("✅ 成功导入employee_manager_bp")
    except Exception as e:
        print(f"❌ 导入employee_manager_bp失败: {e}")
        return False
    
    try:
        from talent_management_system.employee_manager_module.profile import profile_bp
        print("✅ 成功导入profile_bp")
    except Exception as e:
        print(f"❌ 导入profile_bp失败: {e}")
        return False
    
    try:
        from talent_management_system.employee_manager_module.performance import performance_bp
        print("✅ 成功导入performance_bp")
    except Exception as e:
        print(f"❌ 导入performance_bp失败: {e}")
        return False
    
    try:
        from talent_management_system.employee_manager_module.projects import projects_bp
        print("✅ 成功导入projects_bp")
    except Exception as e:
        print(f"❌ 导入projects_bp失败: {e}")
        return False
    
    try:
        from talent_management_system.employee_manager_module.learning_recommendation import learning_recommendation_bp
        print("✅ 成功导入learning_recommendation_bp")
    except Exception as e:
        print(f"❌ 导入learning_recommendation_bp失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 开始测试员工界面路由...")
    print("=" * 50)
    
    # 测试模块导入
    if test_imports():
        print("\n" + "=" * 50)
        # 测试蓝图注册
        test_blueprint_registration()
    else:
        print("\n❌ 模块导入测试失败，跳过蓝图注册测试")
    
    print("\n" + "=" * 50)
    print("🏁 测试完成")
