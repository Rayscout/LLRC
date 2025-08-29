#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试public_jobs.html文件的修改
"""

def test_file_changes():
    """测试文件是否已正确修改"""
    try:
        with open('app/templates/common/public_jobs.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("🔍 检查public_jobs.html文件的修改...")
        
        # 检查是否还有紫色渐变背景
        if 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' in content:
            print("❌ 文件仍包含紫色渐变背景")
        else:
            print("✅ 文件已移除紫色渐变背景")
        
        # 检查是否使用了CSS变量
        if 'var(--bg)' in content and 'var(--fg)' in content:
            print("✅ 文件使用了CSS变量系统")
        else:
            print("❌ 文件未使用CSS变量系统")
        
        # 检查背景颜色设置
        if 'background: var(--bg)' in content:
            print("✅ 文件背景使用CSS变量")
        else:
            print("❌ 文件背景未使用CSS变量")
        
        # 检查CSS变量定义
        if ':root {' in content and '--ios-bg-primary: #F2F2F7' in content:
            print("✅ 文件包含正确的CSS变量定义")
        else:
            print("❌ 文件缺少CSS变量定义")
            
    except FileNotFoundError:
        print("❌ 找不到public_jobs.html文件")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

if __name__ == "__main__":
    test_file_changes()
