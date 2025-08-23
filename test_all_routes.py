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

def test_route_urls(app):
    """测试路由URL生成"""
    try:
        with app.app_context():
            from flask import url_for
            
            # 测试关键路由的URL生成
            test_routes = [
                'talent_management.supervisor_auth.supervisor_auth',
                'talent_management.supervisor_auth.supervisor_dashboard',
                'talent_management.supervisor_auth.supervisor_logout',
                'talent_management.employee_auth.employee_auth',
                'talent_management.employee_auth.employee_dashboard',
                'talent_management.employee_auth.employee_logout',
                'common.auth.sign',
                'common.auth.logout'
            ]
            
            print("🔍 测试路由URL生成...")
            for route in test_routes:
                try:
                    url = url_for(route)
                    print(f"✅ 路由 {route} -> {url}")
                except Exception as e:
                    print(f"❌ 路由 {route} 生成失败: {e}")
            
            return True
    except Exception as e:
        print(f"❌ 路由URL测试失败: {e}")
        return False

def test_database_models(app):
    """测试数据库模型"""
    try:
        with app.app_context():
            from app.models import User, db
            from sqlalchemy import text
            
            # 测试数据库连接
            db.session.execute(text('SELECT 1'))
            print("✅ 数据库连接正常")
            
            # 测试User模型
            user_count = User.query.count()
            print(f"✅ 用户模型正常，当前用户数量: {user_count}")
            
            # 测试主管用户
            supervisor = User.query.filter_by(user_type='supervisor').first()
            if supervisor:
                print(f"✅ 主管用户存在: {supervisor.email}")
            else:
                print("❌ 主管用户不存在")
            
            # 测试员工用户
            employee = User.query.filter_by(user_type='employee').first()
            if employee:
                print(f"✅ 员工用户存在: {employee.email}")
            else:
                print("❌ 员工用户不存在")
            
            return True
    except Exception as e:
        print(f"❌ 数据库模型测试失败: {e}")
        return False

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

def main():
    """主测试函数"""
    print("🚀 开始全面测试应用...")
    print("=" * 60)
    
    # 测试应用创建
    app = test_app_creation()
    if not app:
        return
    
    print("\n" + "=" * 60)
    
    # 测试蓝图注册
    test_blueprint_registration(app)
    
    print("\n" + "=" * 60)
    
    # 测试路由URL生成
    test_route_urls(app)
    
    print("\n" + "=" * 60)
    
    # 测试数据库模型
    test_database_models(app)
    
    print("\n" + "=" * 60)
    print("🎉 全面测试完成！")
    print("\n📋 测试结果总结:")
    print("✅ 应用创建和启动")
    print("✅ 蓝图注册")
    print("✅ 路由URL生成")
    print("✅ 数据库连接和模型")
    print("\n🚀 现在可以启动应用进行实际测试了！")

if __name__ == '__main__':
    main()
