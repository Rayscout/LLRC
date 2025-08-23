#!/usr/bin/env python3
"""
人才管理系统测试脚本
测试主管和员工的登录注册功能
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_models():
    """测试数据库模型"""
    try:
        from app import create_app, db
        from app.models import User
        
        app = create_app()
        with app.app_context():
            # 测试创建主管用户
            supervisor = User(
                first_name='张',
                last_name='主管',
                company_name='测试公司',
                department='技术部',
                position='技术主管',
                email='supervisor@test.com',
                phone_number='13800000001',
                birthday='1990-01-01',
                password='password123',
                user_type='supervisor',
                is_hr=False
            )
            
            # 测试创建员工用户
            employee = User(
                first_name='李',
                last_name='员工',
                company_name='测试公司',
                department='技术部',
                position='软件工程师',
                employee_id='EMP001',
                supervisor_id=1,  # 假设主管ID为1
                hire_date=datetime.now().date(),
                email='employee@test.com',
                phone_number='13800000002',
                birthday='1995-01-01',
                password='password123',
                user_type='employee',
                is_hr=False
            )
            
            print("✅ 数据库模型测试通过")
            print(f"主管用户: {supervisor.first_name} {supervisor.last_name}")
            print(f"员工用户: {employee.first_name} {employee.last_name}")
            
    except Exception as e:
        print(f"❌ 数据库模型测试失败: {e}")
        return False
    
    return True

def test_blueprint_registration():
    """测试蓝图注册"""
    try:
        from app import create_app
        from talent_management_system.routes import talent_management_bp
        
        app = create_app()
        
        # 检查蓝图是否已注册
        registered_blueprints = [bp.name for bp in app.blueprints.values()]
        print(f"已注册的蓝图: {registered_blueprints}")
        
        if 'talent_management' in registered_blueprints:
            print("✅ 人才管理系统蓝图注册成功")
            return True
        else:
            print("❌ 人才管理系统蓝图注册失败")
            return False
            
    except Exception as e:
        print(f"❌ 蓝图注册测试失败: {e}")
        return False

def test_routes():
    """测试路由配置"""
    try:
        from talent_management_system.hr_admin_module.supervisor_auth import supervisor_auth_bp
        from talent_management_system.employee_manager_module.employee_auth import employee_auth_bp
        
        print("✅ 主管认证蓝图导入成功")
        print(f"主管认证URL前缀: {supervisor_auth_bp.url_prefix}")
        
        print("✅ 员工认证蓝图导入成功")
        print(f"员工认证URL前缀: {employee_auth_bp.url_prefix}")
        
        return True
        
    except Exception as e:
        print(f"❌ 路由测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试人才管理系统...")
    print("=" * 50)
    
    tests = [
        ("数据库模型", test_database_models),
        ("蓝图注册", test_blueprint_registration),
        ("路由配置", test_routes),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！人才管理系统配置成功。")
        return True
    else:
        print("⚠️  部分测试失败，请检查配置。")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
