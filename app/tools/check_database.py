"""
LLRC Header Start
文件功能: 应用后端 Python 模块：app/tools/check_database.py
创建时间: 2025-08-24 09:20
创建人: 张宇成
更新记录:
- 2025-08-24 09:50 by 侯东杨
LLRC Header End
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILE-HEADER-AUTO-ADDED
文件: app/tools/check_database.py
功能: 通用模块
创建时间: 2025-08-21 11:08
创建人: 谢佳悦
更新记录:
- 2025-08-25 09:16 by 张宇成
- 2025-08-30 13:21 by 李雨梦
"""

"""
检查数据库中的用户数据
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def check_database():
    """检查数据库中的用户数据"""
    try:
        from app import create_app, db
        from app.models import User
        
        print("🔍 开始检查数据库...")
        print("=" * 50)
        
        app = create_app()
        
        with app.app_context():
            # 检查数据库连接
            try:
                from sqlalchemy import text
                db.session.execute(text("SELECT 1"))
                print("✅ 数据库连接正常")
            except Exception as e:
                print(f"❌ 数据库连接失败: {e}")
                return False
            
            # 检查用户表
            try:
                users = User.query.all()
                print(f"✅ 用户表查询成功，共有 {len(users)} 个用户")
                
                if users:
                    print("\n📋 用户列表:")
                    for user in users:
                        print(f"  - ID: {user.id}")
                        print(f"    姓名: {user.first_name} {user.last_name}")
                        print(f"    邮箱: {user.email}")
                        print(f"    类型: {user.user_type}")
                        print(f"    员工编号: {getattr(user, 'employee_id', '未设置')}")
                        print(f"    部门: {getattr(user, 'department', '未设置')}")
                        print(f"    职位: {getattr(user, 'position', '未设置')}")
                        print(f"    入职日期: {getattr(user, 'hire_date', '未设置')}")
                        bio = getattr(user, 'bio', '未设置')
                        if bio and bio != '未设置':
                            print(f"    个人简介: {bio[:50]}...")
                        else:
                            print(f"    个人简介: {bio}")
                        print()
                else:
                    print("⚠️ 数据库中没有用户数据")
                    
            except Exception as e:
                print(f"❌ 用户表查询失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            # 检查员工用户
            try:
                employees = User.query.filter_by(user_type='employee').all()
                print(f"✅ 员工用户查询成功，共有 {len(employees)} 个员工")
                
                if employees:
                    print("\n👥 员工用户详情:")
                    for emp in employees:
                        print(f"  - {emp.first_name} {emp.last_name} ({emp.email})")
                        print(f"    员工编号: {getattr(emp, 'employee_id', '未设置')}")
                        print(f"    部门: {getattr(emp, 'department', '未设置')}")
                        print(f"    职位: {getattr(emp, 'position', '未设置')}")
                        print(f"    入职日期: {getattr(emp, 'hire_date', '未设置')}")
                        print()
                else:
                    print("⚠️ 数据库中没有员工用户")
                    
            except Exception as e:
                print(f"❌ 员工用户查询失败: {e}")
                import traceback
                traceback.print_exc()
                return False
            
            print("✅ 数据库检查完成")
            return True
            
    except Exception as e:
        print(f"❌ 检查失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    check_database()
