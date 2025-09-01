#!/usr/bin/env python3
"""
简化的云服务器测试脚本
用于快速验证员工模块修复
"""

import os
import sys
import subprocess
import requests
import time

def test_service_status():
    """测试服务状态"""
    print("=== 测试服务状态 ===")
    
    try:
        # 检查服务是否运行
        result = subprocess.run(['systemctl', 'is-active', 'llrc'], 
                              capture_output=True, text=True)
        if result.stdout.strip() == 'active':
            print("✓ llrc服务正在运行")
            return True
        else:
            print("✗ llrc服务未运行")
            return False
    except Exception as e:
        print(f"✗ 检查服务状态失败: {e}")
        return False

def test_file_existence():
    """测试修复文件是否存在"""
    print("=== 测试修复文件 ===")
    
    files_to_check = [
        'talent_management_system/employee_manager_module/feedback.py',
        'talent_management_system/employee_manager_module/profile.py',
        'talent_management_system/employee_manager_module/performance.py',
        'talent_management_system/employee_manager_module/employee_auth.py',
        'talent_management_system/employee_manager_module/projects.py',
        'talent_management_system/employee_manager_module/smart_goals.py',
        'talent_management_system/employee_manager_module/learning_recommendation.py'
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✓ {file_path} 存在")
        else:
            print(f"✗ {file_path} 不存在")
            all_exist = False
    
    return all_exist

def test_imports():
    """测试模块导入"""
    print("=== 测试模块导入 ===")
    
    try:
        # 添加当前目录到Python路径
        sys.path.insert(0, os.getcwd())
        
        # 测试导入
        import app
        print("✓ app模块导入成功")
        
        from app.models import User, Feedback, TaskEvaluation
        print("✓ 数据库模型导入成功")
        
        return True
    except ImportError as e:
        print(f"✗ 模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"✗ 导入测试失败: {e}")
        return False

def test_database_connection():
    """测试数据库连接"""
    print("=== 测试数据库连接 ===")
    
    try:
        from app import create_app
        from app.models import db
        
        app = create_app()
        with app.app_context():
            # 尝试执行简单查询
            from app.models import User
            user_count = User.query.count()
            print(f"✓ 数据库连接成功，用户数量: {user_count}")
            return True
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        return False

def test_web_endpoints():
    """测试Web端点"""
    print("=== 测试Web端点 ===")
    
    try:
        # 测试主页
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✓ 主页访问成功")
        else:
            print(f"✗ 主页访问失败，状态码: {response.status_code}")
            return False
        
        # 测试员工认证页面
        response = requests.get('http://localhost:5000/employee/auth', timeout=5)
        if response.status_code == 200:
            print("✓ 员工认证页面访问成功")
        else:
            print(f"✗ 员工认证页面访问失败，状态码: {response.status_code}")
            return False
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Web端点测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始云服务器修复验证测试...")
    print()
    
    tests = [
        ("服务状态", test_service_status),
        ("文件存在性", test_file_existence),
        ("模块导入", test_imports),
        ("数据库连接", test_database_connection),
        ("Web端点", test_web_endpoints)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name}测试 ---")
        try:
            if test_func():
                passed += 1
                print(f"✓ {test_name}测试通过")
            else:
                print(f"✗ {test_name}测试失败")
        except Exception as e:
            print(f"✗ {test_name}测试异常: {e}")
    
    print(f"\n=== 测试结果 ===")
    print(f"通过: {passed}/{total}")
    print(f"成功率: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 所有测试通过！修复验证成功！")
        print("\n=== 手动测试建议 ===")
        print("1. 访问 http://your-domain/employee/auth 测试员工登录")
        print("2. 访问 http://your-domain/feedback/ 测试反馈功能")
        print("3. 访问 http://your-domain/profile/ 测试PDF导出")
        print("4. 访问 http://your-domain/performance/history 测试绩效历史")
    else:
        print("⚠️  部分测试失败，请检查相关配置")
    
    return passed == total

if __name__ == '__main__':
    main()
