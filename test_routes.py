#!/usr/bin/env python3
"""
测试路由注册的脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_route_registration():
    """测试路由是否正确注册"""
    try:
        from app import create_app

        app = create_app()

        with app.app_context():
            print("=== 路由注册测试 ===")

            # 获取所有注册的路由
            routes = []
            for rule in app.url_map.iter_rules():
                routes.append({
                    'endpoint': rule.endpoint,
                    'methods': list(rule.methods),
                    'rule': str(rule)
                })

            # 查找我们关心的路由
            target_routes = [
                'smartrecruit.hr.dashboard.reports',
                'smartrecruit.hr.dashboard.insights',
                'smartrecruit.hr.dashboard.hr_dashboard'
            ]

            print("查找目标路由:")
            for target in target_routes:
                found = False
                for route in routes:
                    if route['endpoint'] == target:
                        print(f"✅ 找到路由: {target}")
                        print(f"   路径: {route['rule']}")
                        print(f"   方法: {route['methods']}")
                        found = True
                        break
                if not found:
                    print(f"❌ 未找到路由: {target}")

            print(f"\n总共注册的路由数量: {len(routes)}")

            # 显示所有smartrecruit相关的路由
            print("\n=== SmartRecruit相关路由 ===")
            smartrecruit_routes = [r for r in routes if r['endpoint'].startswith('smartrecruit')]
            for route in smartrecruit_routes[:20]:  # 只显示前20个
                print(f"  {route['endpoint']}: {route['rule']} [{', '.join(route['methods'])}]")

            if len(smartrecruit_routes) > 20:
                print(f"  ... 还有 {len(smartrecruit_routes) - 20} 个路由")

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_route_registration()
