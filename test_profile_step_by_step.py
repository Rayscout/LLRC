#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
逐步测试个人资料页面
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_profile_step_by_step():
    """逐步测试个人资料页面"""
    print("🔍 逐步测试个人资料页面...")
    print("=" * 50)
    
    try:
        from app import create_app, db
        from app.models import User
        from talent_management_system.employee_manager_module.profile import profile_dashboard
        
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
            
            # 测试2: 查询用户
            print("\n2. 测试查询用户...")
            try:
                users = User.query.all()
                print(f"   ✅ 成功查询到 {len(users)} 个用户")
                
                if users:
                    user = users[0]
                    print(f"   📋 第一个用户: {user.first_name} {user.last_name}")
                    print(f"      邮箱: {user.email}")
                    print(f"      类型: {getattr(user, 'user_type', '未设置')}")
                else:
                    print("   ⚠️ 没有用户数据")
                    return False
                    
            except Exception as e:
                print(f"   ❌ 查询用户失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 测试3: 测试个人资料函数
            print("\n3. 测试个人资料函数...")
            try:
                # 模拟session
                from flask import session
                session['user_id'] = user.id
                
                # 调用个人资料函数
                result = profile_dashboard()
                print("   ✅ 个人资料函数执行成功")
                print(f"   📄 返回类型: {type(result)}")
                
            except Exception as e:
                print(f"   ❌ 个人资料函数执行失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            print("\n✅ 逐步测试完成")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_profile_step_by_step()
