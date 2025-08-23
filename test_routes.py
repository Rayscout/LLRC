#!/usr/bin/env python3
"""
测试所有路由是否正常工作
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_creation():
    """测试应用创建"""
    try:
        from app import create_app
        app = create_app()
        print("✅ 应用创建成功")
        return app
    except Exception as e:
        print(f"❌ 应用创建失败: {e}")
        return None

def test_blueprint_registration(app):
    """测试蓝图注册"""
    try:
        # 检查蓝图是否已注册
        registered_blueprints = list(app.blueprints.keys())
        print(f"✅ 已注册的蓝图: {registered_blueprints}")
        
        # 检查特定蓝图
        expected_blueprints = ['common', 'smartrecruit', 'talent_management']
        for bp in expected_blueprints:
            if bp in registered_blueprints:
                print(f"✅ {bp} 蓝图已注册")
            else:
                print(f"❌ {bp} 蓝图未注册")
        
        return True
    except Exception as e:
        print(f"❌ 蓝图注册测试失败: {e}")
        return False

def test_route_registration(app):
    """测试路由注册"""
    try:
        # 获取所有路由
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{rule.endpoint}: {rule.rule}")
        
        print(f"✅ 共找到 {len(routes)} 个路由")
        
        # 检查关键路由
        key_routes = [
            'common.auth.sign',
            'talent_management.supervisor_auth.supervisor_auth',
            'talent_management.employee_auth.employee_auth',
            'talent_management.supervisor_auth.supervisor_dashboard',
            'talent_management.employee_auth.employee_dashboard'
        ]
        
        for route in key_routes:
            try:
                app.url_map.bind('localhost').build(route)
                print(f"✅ 路由 {route} 可用")
            except Exception:
                print(f"❌ 路由 {route} 不可用")
        
        return True
    except Exception as e:
        print(f"❌ 路由注册测试失败: {e}")
        return False

def test_database_connection(app):
    """测试数据库连接"""
    try:
        with app.app_context():
            from app.models import db
            # 尝试执行一个简单的查询
            db.session.execute('SELECT 1')
            print("✅ 数据库连接正常")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试应用...")
    print("=" * 50)
    
    # 测试应用创建
    app = test_app_creation()
    if not app:
        return
    
    print("\n" + "=" * 50)
    
    # 测试蓝图注册
    test_blueprint_registration(app)
    
    print("\n" + "=" * 50)
    
    # 测试路由注册
    test_route_registration(app)
    
    print("\n" + "=" * 50)
    
    # 测试数据库连接
    test_database_connection(app)
    
    print("\n" + "=" * 50)
    print("🎉 测试完成！")

if __name__ == '__main__':
    main()
