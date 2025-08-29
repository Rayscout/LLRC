#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导航栏按钮样式更改
"""

def test_nav_button_style():
    """测试导航栏按钮样式是否已更改"""
    try:
        with open('app/templates/common/sign.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔍 检查导航栏按钮样式更改...")
        
        # 检查是否还有jobs-link类
        if 'class="jobs-link"' in content:
            print("❌ 查看岗位按钮仍使用jobs-link类")
        else:
            print("✅ 查看岗位按钮已移除jobs-link类")
        
        # 检查是否还有jobs-link的CSS样式定义
        if '.jobs-link {' in content:
            print("❌ 文件中仍包含jobs-link的CSS样式定义")
        else:
            print("✅ 文件中已移除jobs-link的CSS样式定义")
        
        # 检查查看岗位按钮是否使用普通导航样式
        if '<li><a href="{{ url_for(\'public_jobs\') }}">查看岗位</a></li>' in content:
            print("✅ 查看岗位按钮现在使用普通导航按钮样式")
        else:
            print("❌ 查看岗位按钮样式更改失败")
        
        # 检查是否保留了其他必要的样式
        if '.view-more-btn {' in content:
            print("✅ 保留了查看更多按钮的链接样式")
        else:
            print("❌ 缺少查看更多按钮的链接样式")
            
    except FileNotFoundError:
        print("❌ 找不到sign.html文件")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

if __name__ == "__main__":
    test_nav_button_style()
