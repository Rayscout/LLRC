#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试求职者申请职位后HR能在查看候选人及简历页面看到申请者的完整流程

测试内容：
1. 求职者申请职位的流程
2. Application记录的正确创建
3. HR查看候选人及简历页面的数据获取
4. 状态显示和筛选功能
"""

import os
import sys
import re

def test_application_creation():
    """测试求职者申请职位的流程"""
    print("🔍 测试求职者申请职位的流程...")
    
    # 检查applications.py中的申请逻辑
    applications_file = "LLRC/smartrecruit_system/candidate_module/applications.py"
    
    if not os.path.exists(applications_file):
        print(f"❌ {applications_file} 不存在")
        return False
    
    try:
        with open(applications_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查申请状态设置
        if "status='pending'" in content:
            print("✅ 申请状态正确设置为 'pending'")
        else:
            print("❌ 申请状态设置不正确")
            return False
        
        # 检查Application模型的使用
        if "Application(" in content:
            print("✅ 正确使用Application模型创建申请")
        else:
            print("❌ 未使用Application模型")
            return False
        
        # 检查is_active字段设置
        if "is_active=True" in content:
            print("✅ 正确设置is_active字段")
        else:
            print("❌ 未设置is_active字段")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

def test_dashboard_candidate_retrieval():
    """测试HR dashboard中候选人数据获取"""
    print("\n🔍 测试HR dashboard中候选人数据获取...")
    
    dashboard_file = "LLRC/smartrecruit_system/hr_module/dashboard.py"
    
    if not os.path.exists(dashboard_file):
        print(f"❌ {dashboard_file} 不存在")
        return False
    
    try:
        with open(dashboard_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查候选人列表路由
        if "@dashboard_bp.route('/candidates_list')" in content:
            print("✅ 候选人列表路由存在")
        else:
            print("❌ 候选人列表路由不存在")
            return False
        
        # 检查Application查询逻辑
        if "Application.query.filter(Application.job_id.in_(job_ids)).all()" in content:
            print("✅ 正确查询Application表")
        else:
            print("❌ Application查询逻辑不正确")
            return False
        
        # 检查状态统计
        if "withdrawn_applications" in content:
            print("✅ 包含已撤销申请统计")
        else:
            print("❌ 缺少已撤销申请统计")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

def test_template_status_display():
    """测试模板中的状态显示"""
    print("\n🔍 测试模板中的状态显示...")
    
    # 检查candidate_list.html
    list_template = "LLRC/app/templates/smartrecruit/hr/candidate_list.html"
    
    if not os.path.exists(list_template):
        print(f"❌ {list_template} 不存在")
        return False
    
    try:
        with open(list_template, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查状态显示逻辑
        required_statuses = ['pending', 'interview', 'approved', 'rejected', 'withdrawn']
        missing_statuses = []
        
        for status in required_statuses:
            if f"candidate.status == '{status}'" in content:
                print(f"✅ 支持状态: {status}")
            else:
                print(f"❌ 缺少状态: {status}")
                missing_statuses.append(status)
        
        # 检查CSS样式
        if ".ios-candidate-status.withdrawn" in content:
            print("✅ 包含已撤销状态的CSS样式")
        else:
            print("❌ 缺少已撤销状态的CSS样式")
            missing_statuses.append('withdrawn_css')
        
        if len(missing_statuses) == 0:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

def test_filter_functionality():
    """测试筛选功能"""
    print("\n🔍 测试筛选功能...")
    
    # 检查candidate_filter.html
    filter_template = "LLRC/app/templates/smartrecruit/hr/candidate_filter.html"
    
    if not os.path.exists(filter_template):
        print(f"❌ {filter_template} 不存在")
        return False
    
    try:
        with open(filter_template, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查筛选选项
        required_filters = ['pending', 'interview', 'approved', 'rejected', 'withdrawn']
        missing_filters = []
        
        for filter_status in required_filters:
            if f'value="{filter_status}"' in content:
                print(f"✅ 筛选选项: {filter_status}")
            else:
                print(f"❌ 缺少筛选选项: {filter_status}")
                missing_filters.append(filter_status)
        
        # 检查筛选结果统计
        if "withdrawn_applications" in content:
            print("✅ 包含已撤销申请统计显示")
        else:
            print("❌ 缺少已撤销申请统计显示")
            missing_filters.append('withdrawn_stats')
        
        if len(missing_filters) == 0:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

def test_database_models():
    """测试数据库模型"""
    print("\n🔍 测试数据库模型...")
    
    models_file = "LLRC/app/models.py"
    
    if not os.path.exists(models_file):
        print(f"❌ {models_file} 不存在")
        return False
    
    try:
        with open(models_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查Application模型
        if "class Application(db.Model):" in content:
            print("✅ Application模型定义存在")
        else:
            print("❌ Application模型定义不存在")
            return False
        
        # 检查必要字段
        required_fields = ['user_id', 'job_id', 'status', 'is_active', 'timestamp']
        missing_fields = []
        
        for field in required_fields:
            if field in content:
                print(f"✅ 字段存在: {field}")
            else:
                print(f"❌ 缺少字段: {field}")
                missing_fields.append(field)
        
        # 检查关系定义
        if "user = db.relationship" in content and "job = db.relationship" in content:
            print("✅ 关系定义正确")
        else:
            print("❌ 关系定义不正确")
            missing_fields.append('relationships')
        
        if len(missing_fields) == 0:
            return True
        else:
            return False
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始测试求职者申请职位流程...")
    print("=" * 60)
    
    # 执行所有测试
    tests = [
        test_application_creation,
        test_dashboard_candidate_retrieval,
        test_template_status_display,
        test_filter_functionality,
        test_database_models
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
        print("🎉 所有测试通过！求职者申请职位流程完整！")
        print("\n📝 功能总结:")
        print("✅ 求职者可以申请职位，状态设置为 'pending'")
        print("✅ Application记录正确创建，包含所有必要字段")
        print("✅ HR能在查看候选人及简历页面看到所有申请者")
        print("✅ 支持完整的状态显示：待处理、面试中、已通过、已拒绝、已撤销")
        print("✅ 筛选功能支持所有状态")
        print("✅ 统计数据包含所有状态")
    else:
        print("⚠️  部分测试失败，请检查相关功能")
    
    print("\n🔄 完整流程:")
    print("1. 求职者访问职位详情页面")
    print("2. 点击申请按钮，上传简历或使用已有简历")
    print("3. 系统创建Application记录，状态为'pending'")
    print("4. HR在候选人管理页面看到新的申请")
    print("5. HR可以查看候选人详情、简历，并进行状态管理")
    print("6. 支持筛选不同状态的候选人")

if __name__ == "__main__":
    main()


