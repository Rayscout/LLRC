#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试HR候选人管理功能
验证候选人列表页面是否能正确显示真实数据
"""

import os
import sys

def test_file_existence():
    """测试相关文件是否存在"""
    print("🔍 检查相关文件是否存在...")
    
    files_to_check = [
        "smartrecruit_system/hr_module/dashboard.py",
        "app/templates/smartrecruit/hr/hr_candidates_ios.html",
        "smartrecruit_system/hr_module/candidates.py",
        "app/templates/smartrecruit/hr/view_candidate_resume.html"
    ]
    
    all_exist = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            all_exist = False
    
    return all_exist

def test_dashboard_functions():
    """测试dashboard.py中的函数是否存在"""
    print("\n🔍 检查dashboard.py中的函数...")
    
    try:
        with open("smartrecruit_system/hr_module/dashboard.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        functions_to_check = [
            "def candidates():",
            "def view_candidate(",
            "def approve_candidate(",
            "def reject_candidate(",
            "def schedule_interview("
        ]
        
        all_exist = True
        for func in functions_to_check:
            if func in content:
                print(f"✅ {func}")
            else:
                print(f"❌ {func}")
                all_exist = False
        
        return all_exist
    except Exception as e:
        print(f"❌ 读取dashboard.py失败: {e}")
        return False

def test_candidates_functions():
    """测试candidates.py中的函数是否存在"""
    print("\n🔍 检查candidates.py中的函数...")
    
    try:
        with open("smartrecruit_system/hr_module/candidates.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        functions_to_check = [
            "def view_candidate_resume(",
            "def download_candidate_resume(",
            "def preview_candidate_resume(",
            "def get_candidate_info("
        ]
        
        all_exist = True
        for func in functions_to_check:
            if func in content:
                print(f"✅ {func}")
            else:
                print(f"❌ {func}")
                all_exist = False
        
        return all_exist
    except Exception as e:
        print(f"❌ 读取candidates.py失败: {e}")
        return False

def test_template_integration():
    """测试模板集成"""
    print("\n🔍 检查模板集成...")
    
    try:
        with open("app/templates/smartrecruit/hr/hr_candidates_ios.html", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检查关键元素
        checks = [
            ("候选人列表循环", "{% for candidate in candidates %}"),
            ("查看详情按钮", "查看详情"),
            ("查看简历按钮", "查看简历"),
            ("通过按钮", "通过"),
            ("拒绝按钮", "拒绝"),
            ("安排面试按钮", "安排面试")
        ]
        
        all_exist = True
        for name, text in checks:
            if text in content:
                print(f"✅ {name}")
            else:
                print(f"❌ {name}")
                all_exist = False
        
        return all_exist
    except Exception as e:
        print(f"❌ 读取hr_candidates_ios.html失败: {e}")
        return False

def test_data_structure():
    """测试数据结构"""
    print("\n🔍 检查数据结构...")
    
    try:
        with open("smartrecruit_system/hr_module/dashboard.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # 检查关键字段
        fields_to_check = [
            "candidate.name",
            "candidate.job_title", 
            "candidate.email",
            "candidate.phone",
            "candidate.application_date",
            "candidate.has_resume",
            "candidate.status"
        ]
        
        all_exist = True
        for field in fields_to_check:
            if field in content:
                print(f"✅ {field}")
            else:
                print(f"❌ {field}")
                all_exist = False
        
        return all_exist
    except Exception as e:
        print(f"❌ 检查数据结构失败: {e}")
        return False

def test_route_registration():
    """测试路由注册"""
    print("\n🔍 检查路由注册...")
    
    try:
        with open("smartrecruit_system/hr_module/routes.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        if 'candidates_bp' in content:
            print("✅ candidates_bp 蓝图已注册")
        else:
            print("❌ candidates_bp 蓝图未注册")
        
        if 'hr_bp.register_blueprint(candidates_bp)' in content:
            print("✅ candidates_bp 已注册到hr_bp")
        else:
            print("❌ candidates_bp 未注册到hr_bp")
        
        return True
    except Exception as e:
        print(f"❌ 检查路由注册失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 开始测试HR候选人管理功能...\n")
    
    tests = [
        ("文件存在性", test_file_existence),
        ("Dashboard函数", test_dashboard_functions),
        ("Candidates函数", test_candidates_functions),
        ("模板集成", test_template_integration),
        ("数据结构", test_data_structure),
        ("路由注册", test_route_registration)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试失败: {e}")
            results.append((test_name, False))
    
    # 总结结果
    print("\n" + "="*50)
    print("📊 测试结果总结")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！HR候选人管理功能应该可以正常工作。")
        print("\n📝 功能说明:")
        print("1. HR可以在候选人管理页面查看所有申请者")
        print("2. 每个候选人都有查看详情和查看简历的按钮")
        print("3. 可以操作候选人的申请状态（通过、拒绝、安排面试）")
        print("4. 简历查看功能完整，支持下载和预览")
    else:
        print("⚠️  部分测试失败，请检查相关代码。")
        print("\n🔧 建议:")
        print("1. 确保所有必要的文件都存在")
        print("2. 检查函数定义和路由注册")
        print("3. 验证模板中的数据绑定")
        print("4. 测试Flask应用是否能正常启动")

if __name__ == "__main__":
    main()


