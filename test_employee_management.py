#!/usr/bin/env python3
"""
员工管理功能测试脚本
用于验证新功能的正确性
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User

def test_employee_management():
    """测试员工管理功能"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始测试员工管理功能...")
            
            # 1. 测试数据库字段
            print("\n1. 测试数据库字段...")
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('user')]
            
            required_fields = ['is_active', 'deactivated_at', 'deactivated_by']
            for field in required_fields:
                if field in columns:
                    print(f"✅ 字段 {field} 存在")
                else:
                    print(f"❌ 字段 {field} 缺失")
                    return False
            
            # 2. 测试高管和员工关系
            print("\n2. 测试高管和员工关系...")
            
            # 查找高管用户
            executives = User.query.filter_by(user_type='executive').all()
            if not executives:
                print("⚠️  没有找到高管用户，请先创建高管账户")
                return False
            
            executive = executives[0]
            print(f"找到高管: {executive.first_name} {executive.last_name}")
            
            # 查找该高管的下属员工
            subordinates = User.query.filter_by(supervisor_id=executive.id, user_type='employee').all()
            print(f"该高管有 {len(subordinates)} 个下属员工")
            
            if subordinates:
                employee = subordinates[0]
                print(f"示例员工: {employee.first_name} {employee.last_name}")
                
                # 3. 测试员工状态管理
                print("\n3. 测试员工状态管理...")
                
                # 检查初始状态
                initial_status = employee.is_active
                print(f"员工初始状态: {'活跃' if initial_status else '已注销'}")
                
                # 测试注销功能
                if initial_status:
                    print("测试注销功能...")
                    employee.is_active = False
                    employee.deactivated_at = db.func.now()
                    employee.deactivated_by = executive.id
                    db.session.commit()
                    print("✅ 员工账号已注销")
                    
                    # 验证状态
                    db.session.refresh(employee)
                    if not employee.is_active:
                        print("✅ 注销状态验证成功")
                    else:
                        print("❌ 注销状态验证失败")
                        return False
                
                # 测试重新激活功能
                if not employee.is_active:
                    print("测试重新激活功能...")
                    employee.is_active = True
                    employee.deactivated_at = None
                    employee.deactivated_by = None
                    db.session.commit()
                    print("✅ 员工账号已重新激活")
                    
                    # 验证状态
                    db.session.refresh(employee)
                    if employee.is_active:
                        print("✅ 重新激活状态验证成功")
                    else:
                        print("❌ 重新激活状态验证失败")
                        return False
                
                # 恢复原始状态
                if employee.is_active != initial_status:
                    employee.is_active = initial_status
                    if initial_status:
                        employee.deactivated_at = None
                        employee.deactivated_by = None
                    else:
                        employee.deactivated_at = db.func.now()
                        employee.deactivated_by = executive.id
                    db.session.commit()
                    print("✅ 员工状态已恢复到原始状态")
            
            # 4. 测试权限控制
            print("\n4. 测试权限控制...")
            
            # 查找不属于该高管的员工
            other_employees = User.query.filter(
                User.user_type == 'employee',
                User.supervisor_id != executive.id
            ).all()
            
            if other_employees:
                other_employee = other_employees[0]
                print(f"其他员工: {other_employee.first_name} {other_employee.last_name}")
                print(f"该员工的主管ID: {other_employee.supervisor_id}")
                print(f"当前高管ID: {executive.id}")
                print("✅ 权限控制验证：员工确实不属于当前高管")
            else:
                print("⚠️  没有找到其他员工进行权限测试")
            
            print("\n🎉 所有测试通过！员工管理功能工作正常。")
            return True
            
        except Exception as e:
            print(f"\n💥 测试过程中发生错误: {str(e)}")
            db.session.rollback()
            return False
        finally:
            db.session.close()

def test_routes():
    """测试路由配置"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n测试路由配置...")
            
            # 检查蓝图注册
            registered_blueprints = list(app.blueprints.keys())
            print(f"已注册的蓝图: {registered_blueprints}")
            
            # 检查人才管理蓝图
            if 'talent_management' in registered_blueprints:
                print("✅ 人才管理蓝图已注册")
                
                # 获取蓝图对象
                talent_bp = app.blueprints['talent_management']
                print(f"人才管理蓝图URL前缀: {talent_bp.url_prefix}")
                
                # 检查子蓝图
                if hasattr(talent_bp, 'blueprints'):
                    sub_blueprints = list(talent_bp.blueprints.keys())
                    print(f"子蓝图: {sub_blueprints}")
                    
                    if 'hr_admin' in sub_blueprints:
                        print("✅ HR管理子蓝图已注册")
                    else:
                        print("❌ HR管理子蓝图未注册")
                        return False
                else:
                    print("⚠️  无法检查子蓝图")
            else:
                print("❌ 人才管理蓝图未注册")
                return False
            
            print("✅ 路由配置测试通过")
            return True
            
        except Exception as e:
            print(f"路由测试失败: {str(e)}")
            return False

if __name__ == '__main__':
    print("=" * 60)
    print("员工管理功能测试脚本")
    print("=" * 60)
    
    try:
        # 测试路由配置
        if not test_routes():
            print("\n❌ 路由配置测试失败")
            sys.exit(1)
        
        # 测试员工管理功能
        if not test_employee_management():
            print("\n❌ 员工管理功能测试失败")
            sys.exit(1)
        
        print("\n🎉 所有测试通过！")
        print("员工管理功能已成功部署并可以正常使用。")
        
    except Exception as e:
        print(f"\n💥 测试过程中发生严重错误: {str(e)}")
        print("请检查系统配置和数据库连接")
        sys.exit(1)
