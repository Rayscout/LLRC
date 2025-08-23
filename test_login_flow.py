#!/usr/bin/env python3
"""
测试登录流程
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
                'talent_management.supervisor_auth.supervisor_dashboard',
                'talent_management.employee_auth.employee_dashboard',
                'talent_management.supervisor_auth.supervisor_auth',
                'talent_management.employee_auth.employee_auth'
            ]
            
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

def test_template_rendering(app):
    """测试模板渲染"""
    try:
        with app.app_context():
            from flask import render_template_string
            
            # 测试简单模板
            template = "Hello {{ name }}!"
            result = render_template_string(template, name="World")
            print(f"✅ 模板渲染测试: {result}")
            
            return True
    except Exception as e:
        print(f"❌ 模板渲染测试失败: {e}")
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
            
            return True
    except Exception as e:
        print(f"❌ 数据库模型测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试登录流程...")
    print("=" * 50)
    
    # 测试应用创建
    app = test_app_creation()
    if not app:
        return
    
    print("\n" + "=" * 50)
    
    # 测试路由URL生成
    test_route_urls(app)
    
    print("\n" + "=" * 50)
    
    # 测试模板渲染
    test_template_rendering(app)
    
    print("\n" + "=" * 50)
    
    # 测试数据库模型
    test_database_models(app)
    
    print("\n" + "=" * 50)
    print("🎉 测试完成！")

if __name__ == '__main__':
    main()
