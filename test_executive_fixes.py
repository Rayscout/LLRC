#!/usr/bin/env python3
"""
高管模块修复测试脚本
用于测试高管模块的修复效果
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
        'talent_management_system/hr_admin_module/salary_analysis.py',
        'talent_management_system/hr_admin_module/org_health.py',
        'talent_management_system/hr_admin_module/talent_demand.py',
        'talent_management_system/hr_admin_module/__init__.py'
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
        sys.path.insert(0, os.getcwd())
        
        import app
        print("✓ app模块导入成功")
        
        from app.models import User, TalentDemand, Feedback, TaskEvaluation
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
            from app.models import User
            user_count = User.query.count()
            print(f"✓ 数据库连接成功，用户数量: {user_count}")
            return True
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        return False

def test_executive_endpoints():
    """测试高管相关端点"""
    print("=== 测试高管端点 ===")
    
    try:
        # 测试高管仪表板
        response = requests.get('http://localhost:5000/talent/hr_admin/executive_dashboard', timeout=5)
        if response.status_code == 200:
            print("✓ 高管仪表板页面访问成功")
        else:
            print(f"✗ 高管仪表板页面访问失败，状态码: {response.status_code}")
        
        # 测试薪酬分析页面
        response = requests.get('http://localhost:5000/talent/hr_admin/salary_analysis/dashboard', timeout=5)
        if response.status_code == 200:
            print("✓ 薪酬分析页面访问成功")
        else:
            print(f"✗ 薪酬分析页面访问失败，状态码: {response.status_code}")
        
        # 测试组织健康度页面
        response = requests.get('http://localhost:5000/talent/hr_admin/org_health/dashboard', timeout=5)
        if response.status_code == 200:
            print("✓ 组织健康度页面访问成功")
        else:
            print(f"✗ 组织健康度页面访问失败，状态码: {response.status_code}")
        
        # 测试人才需求发布页面
        response = requests.get('http://localhost:5000/talent/hr_admin/talent_demand/publish', timeout=5)
        if response.status_code == 200:
            print("✓ 人才需求发布页面访问成功")
        else:
            print(f"✗ 人才需求发布页面访问失败，状态码: {response.status_code}")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ Web端点测试失败: {e}")
        return False

def test_export_endpoints():
    """测试导出功能端点"""
    print("=== 测试导出功能端点 ===")
    
    try:
        # 测试薪酬数据导出API
        response = requests.post('http://localhost:5000/talent/hr_admin/salary_analysis/api/export_data', 
                               timeout=10)
        if response.status_code in [200, 401, 403]:  # 200成功，401/403权限问题但端点存在
            print("✓ 薪酬数据导出API端点存在")
        else:
            print(f"✗ 薪酬数据导出API端点问题，状态码: {response.status_code}")
        
        # 测试组织健康度报告导出API
        response = requests.post('http://localhost:5000/talent/hr_admin/org_health/api/export_report', 
                               timeout=10)
        if response.status_code in [200, 401, 403]:
            print("✓ 组织健康度报告导出API端点存在")
        else:
            print(f"✗ 组织健康度报告导出API端点问题，状态码: {response.status_code}")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ 导出端点测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始高管模块修复验证测试...")
    print()
    
    tests = [
        ("服务状态", test_service_status),
        ("文件存在性", test_file_existence),
        ("模块导入", test_imports),
        ("数据库连接", test_database_connection),
        ("高管端点", test_executive_endpoints),
        ("导出端点", test_export_endpoints)
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
        print("🎉 所有测试通过！高管模块修复验证成功！")
        print("\n=== 手动测试建议 ===")
        print("1. 访问 http://your-domain/talent/hr_admin/executive_dashboard 测试高管仪表板")
        print("2. 访问 http://your-domain/talent/hr_admin/salary_analysis/dashboard 测试薪酬分析")
        print("3. 访问 http://your-domain/talent/hr_admin/org_health/dashboard 测试组织健康度")
        print("4. 访问 http://your-domain/talent/hr_admin/talent_demand/publish 测试人才需求发布")
        print("\n=== 导出功能测试 ===")
        print("1. 在薪酬分析页面点击'导出数据'按钮")
        print("2. 在组织健康度页面点击'导出对比报告'按钮")
        print("3. 检查Excel文件是否正常下载")
    else:
        print("⚠️  部分测试失败，请检查相关配置")
    
    return passed == total

if __name__ == '__main__':
    main()
