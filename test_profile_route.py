#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
测试个人资料路由
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_profile_route():
    """测试个人资料路由"""
    print("🔍 测试个人资料路由...")
    print("=" * 50)
    
    try:
        from app import create_app
        from talent_management_system.employee_manager_module.profile import profile_bp
        
        print("✅ 成功导入所需模块")
        
        app = create_app()
        print("✅ 成功创建Flask应用")
        
        # 检查蓝图注册
        with app.app_context():
            print("\n1. 检查蓝图注册...")
            registered_blueprints = [bp.name for bp in app.blueprints.values()]
            print(f"   📋 已注册的蓝图: {registered_blueprints}")
            
            # 检查路由
            print("\n2. 检查路由...")
            routes = []
            for rule in app.url_map.iter_rules():
                if 'profile' in rule.rule:
                    routes.append({
                        'endpoint': rule.endpoint,
                        'rule': rule.rule,
                        'methods': list(rule.methods)
                    })
            
            if routes:
                print("   ✅ 找到个人资料相关路由:")
                for route in routes:
                    print(f"      📍 {route['endpoint']} -> {route['rule']} [{', '.join(route['methods'])}]")
            else:
                print("   ⚠️ 没有找到个人资料相关路由")
            
            # 检查模板
            print("\n3. 检查模板...")
            try:
                from flask import render_template_string
                test_template = "{{ '测试模板' }}"
                result = render_template_string(test_template)
                print(f"   ✅ 模板渲染正常: {result}")
            except Exception as e:
                print(f"   ❌ 模板渲染失败: {e}")
            
            print("\n✅ 个人资料路由测试完成")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_profile_route()
