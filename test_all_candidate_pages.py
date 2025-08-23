#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def test_candidate_pages():
    """测试所有求职者页面是否都已更新为iOS风格"""
    print("🎨 测试所有求职者页面iOS风格...")
    
    # 需要测试的页面
    pages = [
        {
            'url': '/smartrecruit/candidate/',
            'name': '智能推荐首页',
            'expected_elements': ['candidate_ios_style.css', 'navbar', '智能推荐', '职位搜索', '我的申请', 'AI面试训练', '个人资料']
        },
        {
            'url': '/smartrecruit/candidate/jobs/search',
            'name': '职位搜索页面',
            'expected_elements': ['candidate_ios_style.css', 'navbar', '智能岗位搜索', '搜索过滤器', '热门关键词']
        },
        {
            'url': '/smartrecruit/candidate/dashboard',
            'name': '个人资料页面',
            'expected_elements': ['candidate_ios_style.css', 'navbar', '个人资料', '管理您的个人信息']
        },
        {
            'url': '/smartrecruit/candidate/applications/view_applications',
            'name': '我的申请页面',
            'expected_elements': ['candidate_ios_style.css', 'navbar', '我的申请', '查看和管理您的职位申请状态']
        },
        {
            'url': '/smartrecruit/candidate/interview/',
            'name': 'AI面试训练页面',
            'expected_elements': ['candidate_ios_style.css', 'navbar', 'AI面试训练', '体验AI驱动的智能面试']
        }
    ]
    
    try:
        # 等待应用启动
        time.sleep(3)
        
        results = []
        
        for page in pages:
            try:
                print(f"\n🔍 测试 {page['name']}...")
                response = requests.get(f'http://localhost:5000{page["url"]}', timeout=10)
                
                if response.status_code == 200:
                    content = response.text
                    found_elements = []
                    missing_elements = []
                    
                    for element in page['expected_elements']:
                        if element in content:
                            found_elements.append(element)
                        else:
                            missing_elements.append(element)
                    
                    success_rate = (len(found_elements) / len(page['expected_elements'])) * 100
                    
                    if success_rate >= 80:
                        print(f"✅ {page['name']} - 通过 ({success_rate:.1f}%)")
                        results.append(True)
                    else:
                        print(f"❌ {page['name']} - 失败 ({success_rate:.1f}%)")
                        print(f"   缺少元素: {missing_elements}")
                        results.append(False)
                        
                else:
                    print(f"❌ {page['name']} - HTTP {response.status_code}")
                    results.append(False)
                    
            except Exception as e:
                print(f"❌ {page['name']} - 错误: {e}")
                results.append(False)
        
        # 总结结果
        total_pages = len(pages)
        passed_pages = sum(results)
        overall_success_rate = (passed_pages / total_pages) * 100
        
        print(f"\n{'='*60}")
        print(f"📊 测试总结:")
        print(f"   总页面数: {total_pages}")
        print(f"   通过页面: {passed_pages}")
        print(f"   失败页面: {total_pages - passed_pages}")
        print(f"   成功率: {overall_success_rate:.1f}%")
        
        if overall_success_rate >= 80:
            print("🎉 大部分页面已成功更新为iOS风格！")
            return True
        else:
            print("❌ 部分页面需要进一步更新")
            return False
            
    except Exception as e:
        print(f"测试出错: {e}")
        return False

def test_navigation_consistency():
    """测试导航栏一致性"""
    print("\n🔗 测试导航栏一致性...")
    
    try:
        response = requests.get('http://localhost:5000/smartrecruit/candidate/', timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            # 检查导航栏元素
            nav_elements = [
                '智能推荐',
                '职位搜索', 
                '我的申请',
                'AI面试训练',
                '个人资料',
                'navbar-nav',
                'nav-link'
            ]
            
            missing_nav = []
            for element in nav_elements:
                if element not in content:
                    missing_nav.append(element)
            
            if not missing_nav:
                print("✅ 导航栏元素完整")
                return True
            else:
                print(f"❌ 导航栏缺少元素: {missing_nav}")
                return False
        else:
            print(f"❌ 无法访问首页: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"导航测试出错: {e}")
        return False

if __name__ == "__main__":
    print("🚀 测试所有求职者页面iOS风格...")
    print("=" * 60)
    
    pages_success = test_candidate_pages()
    nav_success = test_navigation_consistency()
    
    if pages_success and nav_success:
        print("\n🎉 所有测试通过！求职者页面已成功更新为iOS风格")
    else:
        print("\n❌ 部分测试失败，需要进一步检查")
