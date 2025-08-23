#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time

def test_candidate_ios_ui():
    """测试求职者iOS风格界面"""
    print("🎨 测试求职者iOS风格界面...")
    
    try:
        # 等待应用启动
        time.sleep(3)
        
        response = requests.get('http://localhost:5000/smartrecruit/candidate/', timeout=10)
        
        print(f"状态码: {response.status_code}")
        print(f"页面长度: {len(response.text)} 字符")
        
        if response.status_code == 200:
            content = response.text
            
            # 检查iOS风格的关键元素
            key_elements = [
                'candidate_ios_style.css',
                'candidate_ios_script.js',
                'navbar',
                'navbar-brand',
                'navbar-nav',
                'nav-link',
                'theme-toggle',
                'user-avatar',
                'main-content',
                'section',
                'card',
                'animate-fade-in-up',
                'animate-slide-in-left',
                'animate-slide-in-right',
                'job-card',
                'btn',
                'grid',
                '为您推荐',
                '快速操作',
                '智能推荐',
                '职位搜索',
                '我的申请',
                'AI面试训练',
                '个人资料'
            ]
            
            found_elements = []
            missing_elements = []
            
            for element in key_elements:
                if element in content:
                    found_elements.append(element)
                    print(f"✅ 找到: {element}")
                else:
                    missing_elements.append(element)
                    print(f"❌ 未找到: {element}")
            
            success_rate = (len(found_elements) / len(key_elements)) * 100
            print(f"\n成功率: {success_rate:.1f}% ({len(found_elements)}/{len(key_elements)})")
            
            if success_rate >= 80:
                print("🎉 iOS风格界面测试通过！")
                return True
            else:
                print("❌ iOS风格界面测试失败")
                
                # 输出页面开头和结尾的内容以供调试
                print(f"\n页面开头 (前500字符):")
                print(content[:500])
                print(f"\n页面结尾 (后500字符):")
                print(content[-500:])
                
                return False
                
        else:
            print(f"页面访问失败: {response.status_code}")
            if response.status_code == 500:
                print("内部服务器错误，请检查应用日志")
            return False
            
    except Exception as e:
        print(f"测试出错: {e}")
        return False

def test_navigation_links():
    """测试导航链接"""
    print("\n🔗 测试导航链接...")
    
    try:
        base_url = 'http://localhost:5000'
        
        # 测试各个导航链接
        nav_links = [
            '/smartrecruit/candidate/jobs/search',
            '/smartrecruit/candidate/dashboard',
            '/smartrecruit/candidate/applications/view_applications',
            '/smartrecruit/candidate/interview/'
        ]
        
        for link in nav_links:
            try:
                response = requests.get(f"{base_url}{link}", timeout=5)
                if response.status_code == 200:
                    print(f"✅ {link} - 正常")
                else:
                    print(f"❌ {link} - 状态码: {response.status_code}")
            except Exception as e:
                print(f"❌ {link} - 错误: {e}")
                
    except Exception as e:
        print(f"导航测试出错: {e}")

if __name__ == "__main__":
    print("🚀 测试求职者iOS风格界面...")
    print("=" * 60)
    
    success = test_candidate_ios_ui()
    
    if success:
        print("\n✅ iOS风格界面测试通过！")
        test_navigation_links()
    else:
        print("\n❌ iOS风格界面测试失败，需要进一步检查")
