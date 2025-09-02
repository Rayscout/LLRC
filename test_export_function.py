#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试导出功能的脚本
用于验证Excel导出功能是否正常工作
"""

import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_pandas_openpyxl():
    """测试pandas和openpyxl是否正常工作"""
    print("=== 测试pandas和openpyxl ===")
    
    try:
        import pandas as pd
        print(f"✓ pandas版本: {pd.__version__}")
        
        import openpyxl
        print(f"✓ openpyxl版本: {openpyxl.__version__}")
        
        # 测试创建Excel文件
        df = pd.DataFrame({
            '姓名': ['张三', '李四', '王五'],
            '年龄': [25, 30, 35],
            '部门': ['技术部', '市场部', '人事部']
        })
        
        # 测试保存到内存
        import io
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='测试数据', index=False)
        
        output.seek(0)
        print("✓ Excel文件创建成功")
        
        # 测试读取
        output.seek(0)
        df_read = pd.read_excel(output, sheet_name='测试数据')
        print(f"✓ Excel文件读取成功，数据行数: {len(df_read)}")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_reportlab():
    """测试reportlab是否正常工作"""
    print("\n=== 测试reportlab ===")
    
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        
        # 测试创建PDF文件
        output = io.BytesIO()
        c = canvas.Canvas(output, pagesize=A4)
        c.drawString(100, 750, "测试PDF文档")
        c.drawString(100, 700, "这是一个测试文件")
        c.save()
        
        output.seek(0)
        print("✓ PDF文件创建成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_flask_imports():
    """测试Flask相关导入"""
    print("\n=== 测试Flask导入 ===")
    
    try:
        from flask import Blueprint, jsonify, send_file
        print("✓ Flask基础模块导入成功")
        
        from flask import session
        print("✓ Flask session模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def test_salary_analysis_import():
    """测试薪酬分析模块导入"""
    print("\n=== 测试薪酬分析模块导入 ===")
    
    try:
        # 尝试导入薪酬分析模块
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'talent_management_system', 'hr_admin_module'))
        
        from salary_analysis import generate_salary_data
        print("✓ 薪酬分析模块导入成功")
        
        # 测试数据生成
        data = generate_salary_data()
        print(f"✓ 薪酬数据生成成功，岗位数: {data['summary']['total_positions']}")
        
        return True
        
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

def main():
    """主函数"""
    print("开始测试导出功能...")
    print("=" * 50)
    
    results = []
    
    # 测试各项功能
    results.append(("pandas和openpyxl", test_pandas_openpyxl()))
    results.append(("reportlab", test_reportlab()))
    results.append(("Flask导入", test_flask_imports()))
    results.append(("薪酬分析模块", test_salary_analysis_import()))
    
    # 输出结果
    print("\n=== 测试结果汇总 ===")
    success_count = 0
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n总计: {success_count}/{len(results)} 项测试通过")
    
    if success_count == len(results):
        print("🎉 所有测试通过！导出功能应该可以正常工作。")
    else:
        print("⚠️ 部分测试失败，请检查相关配置。")
    
    return success_count == len(results)

if __name__ == "__main__":
    main()
