#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试热招职位区域是否已被删除
"""

def test_hot_jobs_removal():
    """测试热招职位区域是否已被删除"""
    try:
        with open('app/templates/common/sign.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔍 检查热招职位区域是否已被删除...")
        
        # 检查是否还有热招职位相关的HTML
        if '热招职位' in content:
            print("❌ 文件中仍包含'热招职位'文字")
        else:
            print("✅ 文件中已移除'热招职位'文字")
        
        # 检查是否还有热招职位板块的HTML结构
        if 'id="hot-jobs"' in content:
            print("❌ 文件中仍包含热招职位板块的HTML结构")
        else:
            print("✅ 文件中已移除热招职位板块的HTML结构")
        
        # 检查是否还有职位卡片的HTML
        if 'class="job-card"' in content:
            print("❌ 文件中仍包含职位卡片的HTML")
        else:
            print("✅ 文件中已移除职位卡片的HTML")
        
        # 检查是否还有职位标签的HTML
        if 'class="job-tab"' in content:
            print("❌ 文件中仍包含职位标签的HTML")
        else:
            print("✅ 文件中已移除职位标签的HTML")
        
        # 检查是否还有工作详情弹窗
        if 'id="jobDetailModal"' in content:
            print("✅ 保留了工作详情弹窗（用于热门企业功能）")
        else:
            print("❌ 缺少工作详情弹窗")
            
    except FileNotFoundError:
        print("❌ 找不到sign.html文件")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

if __name__ == "__main__":
    test_hot_jobs_removal()
