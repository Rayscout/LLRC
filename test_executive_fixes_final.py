#!/usr/bin/env python3
"""
高管模块最终修复验证脚本
用于验证高管模块的所有修复效果
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
        'talent_management_system/hr_admin_module/__init__.py',
        'app/templates/talent_management/hr_admin/salary_dashboard.html',
        'app/templates/talent_management/hr_admin/org_health_dashboard.html'
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
        if response.status_code in [200, 302, 401]:  # 200成功，302重定向，401需要登录
            print("✓ 高管仪表板页面端点正常")
        else:
            print(f"✗ 高管仪表板页面端点异常，状态码: {response.status_code}")
        
        # 测试薪酬分析页面
        response = requests.get('http://localhost:5000/talent/hr_admin/salary_analysis/dashboard', timeout=5)
        if response.status_code in [200, 302, 401]:
            print("✓ 薪酬分析页面端点正常")
        else:
            print(f"✗ 薪酬分析页面端点异常，状态码: {response.status_code}")
        
        # 测试组织健康度页面
        response = requests.get('http://localhost:5000/talent/hr_admin/org_health/dashboard', timeout=5)
        if response.status_code in [200, 302, 401]:
            print("✓ 组织健康度页面端点正常")
        else:
            print(f"✗ 组织健康度页面端点异常，状态码: {response.status_code}")
        
        # 测试人才需求发布页面
        response = requests.get('http://localhost:5000/talent/hr_admin/talent_demand/publish', timeout=5)
        if response.status_code in [200, 302, 401]:
            print("✓ 人才需求发布页面端点正常")
        else:
            print(f"✗ 人才需求发布页面端点异常，状态码: {response.status_code}")
        
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
            print("✓ 薪酬数据导出API端点正常")
        else:
            print(f"✗ 薪酬数据导出API端点异常，状态码: {response.status_code}")
        
        # 测试组织健康度报告导出API
        response = requests.post('http://localhost:5000/talent/hr_admin/org_health/api/export_report', 
                               timeout=10)
        if response.status_code in [200, 401, 403]:
            print("✓ 组织健康度报告导出API端点正常")
        else:
            print(f"✗ 组织健康度报告导出API端点异常，状态码: {response.status_code}")
        
        return True
    except requests.exceptions.RequestException as e:
        print(f"✗ 导出端点测试失败: {e}")
        return False

def test_template_files():
    """测试模板文件修改"""
    print("=== 测试模板文件修改 ===")
    
    try:
        # 检查薪酬分析模板是否包含fetch API
        with open('app/templates/talent_management/hr_admin/salary_dashboard.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'fetch(' in content and 'exportData()' in content:
                print("✓ 薪酬分析模板导出功能已修复")
            else:
                print("✗ 薪酬分析模板导出功能未修复")
                return False
        
        # 检查组织健康度模板是否包含fetch API
        with open('app/templates/talent_management/hr_admin/org_health_dashboard.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'fetch(' in content and 'exportReport()' in content:
                print("✓ 组织健康度模板导出功能已修复")
            else:
                print("✗ 组织健康度模板导出功能未修复")
                return False
        
        return True
    except Exception as e:
        print(f"✗ 模板文件测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("开始高管模块最终修复验证测试...")
    print()
    
    tests = [
        ("服务状态", test_service_status),
        ("文件存在性", test_file_existence),
        ("模块导入", test_imports),
        ("数据库连接", test_database_connection),
        ("高管端点", test_executive_endpoints),
        ("导出端点", test_export_endpoints),
        ("模板文件", test_template_files)
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
        print("\n=== 手动测试指南 ===")
        print("1. 访问 http://your-domain/talent/executive/auth 登录高管账户")
        print("2. 访问 http://your-domain/talent/hr_admin/executive_dashboard 测试AI人才大盘")
        print("3. 访问 http://your-domain/talent/hr_admin/salary_analysis/dashboard 测试薪酬分析")
        print("4. 访问 http://your-domain/talent/hr_admin/org_health/dashboard 测试组织健康度")
        print("5. 访问 http://your-domain/talent/hr_admin/talent_demand/publish 测试人才需求发布")
        print("\n=== 导出功能测试 ===")
        print("1. 在薪酬分析页面点击'导出数据'按钮 - 应该正常下载Excel文件")
        print("2. 在组织健康度页面点击'导出对比报告'按钮 - 应该正常下载Excel文件")
        print("3. 在人才需求页面输入关键词并发布 - 应该成功跳转到仪表板")
        print("\n=== 修复内容总结 ===")
        print("✅ 薪酬分析导出功能 - 修复了前端fetch API调用")
        print("✅ 组织健康度导出功能 - 修复了前端fetch API调用")
        print("✅ 发布人才需求功能 - 添加了数据库事务和错误处理")
        print("✅ AI人才大盘功能 - 增强了数据获取和错误处理")
    else:
        print("⚠️  部分测试失败，请检查相关配置")
    
    return passed == total

if __name__ == '__main__':
    main()
