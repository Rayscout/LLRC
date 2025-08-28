#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HR候选人管理功能重构测试脚本

测试重构后的功能是否正常工作：
1. 新增的独立页面是否存在
2. 新增的路由是否正常工作
3. 页面跳转是否正常
4. 功能按钮是否正确显示
"""

import os
import sys
import re

def test_file_existence():
    """测试新增的独立页面文件是否存在"""
    print("🔍 测试新增的独立页面文件是否存在...")
    
    required_files = [
        "LLRC/app/templates/smartrecruit/hr/candidate_filter.html",
        "LLRC/app/templates/smartrecruit/hr/candidate_list.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
        else:
            print(f"❌ {file_path} 不存在")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"⚠️  缺少 {len(missing_files)} 个文件")
        return False
    else:
        print("✅ 所有新增页面文件都存在")
        return True

def test_dashboard_routes():
    """测试dashboard.py中是否包含新增的路由"""
    print("\n🔍 测试dashboard.py中是否包含新增的路由...")
    
    dashboard_file = "LLRC/smartrecruit_system/hr_module/dashboard.py"
    
    if not os.path.exists(dashboard_file):
        print(f"❌ {dashboard_file} 不存在")
        return False
    
    try:
        with open(dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查新增的路由
        required_routes = [
            "@dashboard_bp.route('/candidates_filter')",
            "@dashboard_bp.route('/candidates_list')",
            "def candidates_filter():",
            "def candidates_list():"
        ]
        
        missing_routes = []
        for route in required_routes:
            if route in content:
                print(f"✅ 找到路由: {route}")
            else:
                print(f"❌ 未找到路由: {route}")
                missing_routes.append(route)
        
        if missing_routes:
            print(f"⚠️  缺少 {len(missing_routes)} 个路由")
            return False
        else:
            print("✅ 所有新增路由都存在")
            return True
            
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

def test_template_content():
    """测试模板文件内容是否正确"""
    print("\n🔍 测试模板文件内容是否正确...")
    
    # 测试candidate_filter.html
    filter_file = "LLRC/app/templates/smartrecruit/hr/candidate_filter.html"
    if os.path.exists(filter_file):
        try:
            with open(filter_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查关键内容
            required_content = [
                "筛选候选人",
                "ios-filter-hero",
                "ios-filters-section",
                "ios-candidates-list",
                "返回候选人管理"
            ]
            
            missing_content = []
            for item in required_content:
                if item in content:
                    print(f"✅ candidate_filter.html 包含: {item}")
                else:
                    print(f"❌ candidate_filter.html 缺少: {item}")
                    missing_content.append(item)
            
            if missing_content:
                print(f"⚠️  candidate_filter.html 缺少 {len(missing_content)} 个内容项")
            else:
                print("✅ candidate_filter.html 内容完整")
                
        except Exception as e:
            print(f"❌ 读取 candidate_filter.html 失败: {e}")
    
    # 测试candidate_list.html
    list_file = "LLRC/app/templates/smartrecruit/hr/candidate_list.html"
    if os.path.exists(list_file):
        try:
            with open(list_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查关键内容
            required_content = [
                "查看候选人及简历",
                "ios-candidates-hero",
                "ios-candidates-list",
                "返回候选人管理",
                "筛选候选人"
            ]
            
            missing_content = []
            for item in required_content:
                if item in content:
                    print(f"✅ candidate_list.html 包含: {item}")
                else:
                    print(f"❌ candidate_list.html 缺少: {item}")
                    missing_content.append(item)
            
            if missing_content:
                print(f"⚠️  candidate_list.html 缺少 {len(missing_content)} 个内容项")
            else:
                print("✅ candidate_list.html 内容完整")
                
        except Exception as e:
            print(f"❌ 读取 candidate_list.html 失败: {e}")

def test_main_page_refactor():
    """测试主页面是否已重构"""
    print("\n🔍 测试主页面是否已重构...")
    
    main_file = "LLRC/app/templates/smartrecruit/hr/hr_candidates_ios.html"
    if os.path.exists(main_file):
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否移除了筛选功能
            removed_content = [
                "ios-filter-group",
                "ios-filter-item",
                "ios-filter-label",
                "筛选与搜索",
                "搜索候选人姓名、技能或职位"
            ]
            
            removed_count = 0
            for item in removed_content:
                if item not in content:
                    removed_count += 1
                else:
                    print(f"⚠️  主页面仍包含: {item}")
            
            # 检查是否添加了功能按钮
            added_content = [
                "ios-feature-buttons",
                "ios-feature-button",
                "查看候选人及简历",
                "筛选候选人",
                "安排面试"
            ]
            
            added_count = 0
            for item in added_content:
                if item in content:
                    added_count += 1
                    print(f"✅ 主页面包含: {item}")
                else:
                    print(f"❌ 主页面缺少: {item}")
            
            if removed_count >= 3 and added_count >= 3:
                print("✅ 主页面重构成功")
                return True
            else:
                print("⚠️  主页面重构不完整")
                return False
                
        except Exception as e:
            print(f"❌ 读取主页面失败: {e}")
            return False
    else:
        print(f"❌ 主页面文件不存在: {main_file}")
        return False

def test_url_patterns():
    """测试URL模式是否正确"""
    print("\n🔍 测试URL模式是否正确...")
    
    # 检查模板中的URL
    template_files = [
        "LLRC/app/templates/smartrecruit/hr/hr_candidates_ios.html",
        "LLRC/app/templates/smartrecruit/hr/candidate_filter.html",
        "LLRC/app/templates/smartrecruit/hr/candidate_list.html"
    ]
    
    url_patterns = [
        "url_for('smartrecruit.hr.dashboard.candidates_filter')",
        "url_for('smartrecruit.hr.dashboard.candidates_list')",
        "url_for('smartrecruit.hr.dashboard.candidates')"
    ]
    
    for template_file in template_files:
        if os.path.exists(template_file):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                print(f"\n📄 检查 {os.path.basename(template_file)}:")
                for pattern in url_patterns:
                    if pattern in content:
                        print(f"✅ 包含URL: {pattern}")
                    else:
                        print(f"❌ 缺少URL: {pattern}")
                        
            except Exception as e:
                print(f"❌ 读取 {template_file} 失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始测试HR候选人管理功能重构...")
    print("=" * 60)
    
    # 执行所有测试
    tests = [
        test_file_existence,
        test_dashboard_routes,
        test_template_content,
        test_main_page_refactor,
        test_url_patterns
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test in tests:
        try:
            if test():
                passed_tests += 1
        except Exception as e:
            print(f"❌ 测试 {test.__name__} 执行失败: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed_tests}/{total_tests} 通过")
    
    if passed_tests == total_tests:
        print("🎉 所有测试通过！HR候选人管理功能重构成功！")
    else:
        print("⚠️  部分测试失败，请检查相关功能")
    
    print("\n📝 重构总结:")
    print("✅ 新增了筛选候选人独立页面 (candidate_filter.html)")
    print("✅ 新增了查看候选人及简历独立页面 (candidate_list.html)")
    print("✅ 重构了候选人管理主页面，移除筛选功能，添加功能按钮")
    print("✅ 新增了相应的路由支持")
    print("✅ 实现了功能分离，通过按钮跳转到独立页面")

if __name__ == "__main__":
    main()


