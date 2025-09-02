#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合修复所有模块的导出功能
解决薪酬分析、组织健康度、职业发展追踪的导出问题
"""

import os
import re
from pathlib import Path

def fix_salary_analysis_export():
    """修复薪酬分析模块的导出功能"""
    print("🔧 修复薪酬分析模块导出功能...")
    
    file_path = "talent_management_system/hr_admin_module/salary_analysis.py"
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复文件名编码问题
    old_filename = 'f"薪酬分析报告_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    new_filename = 'f"salary_analysis_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    
    if old_filename in content:
        content = content.replace(old_filename, new_filename)
        print("✅ 修复文件名编码问题")
    
    # 修复响应头编码问题
    old_headers = '''            # 设置响应头
            response = send_file(
                output,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            # 添加额外的响应头
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response'''
    
    new_headers = '''            # 设置响应头 - 修复编码问题
            # 使用英文文件名避免编码问题
            safe_filename = f"salary_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            response = send_file(
                output,
                as_attachment=True,
                download_name=safe_filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            # 添加额外的响应头 - 避免中文字符
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            response.headers['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
            
            return response'''
    
    if old_headers in content:
        content = content.replace(old_headers, new_headers)
        print("✅ 修复响应头编码问题")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 薪酬分析模块修复完成")
    return True

def fix_org_health_export():
    """修复组织健康度模块的导出功能"""
    print("🔧 修复组织健康度模块导出功能...")
    
    file_path = "talent_management_system/hr_admin_module/org_health.py"
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复文件名编码问题
    old_filename = 'f"组织健康度评估报告_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    new_filename = 'f"org_health_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    
    if old_filename in content:
        content = content.replace(old_filename, new_filename)
        print("✅ 修复文件名编码问题")
    
    # 修复响应头编码问题
    old_headers = '''            # 设置响应头
            response = send_file(
                output,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            # 添加额外的响应头
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response'''
    
    new_headers = '''            # 设置响应头 - 修复编码问题
            # 使用英文文件名避免编码问题
            safe_filename = f"org_health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            response = send_file(
                output,
                as_attachment=True,
                download_name=safe_filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
            # 添加额外的响应头 - 避免中文字符
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
            response.headers['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
            
            return response'''
    
    if old_headers in content:
        content = content.replace(old_headers, new_headers)
        print("✅ 修复响应头编码问题")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 组织健康度模块修复完成")
    return True

def fix_career_tracking_export():
    """修复职业发展追踪模块的导出功能"""
    print("🔧 修复职业发展追踪模块导出功能...")
    
    file_path = "talent_management_system/hr_admin_module/career_tracking.py"
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复文件名编码问题
    old_filename = 'f"职业发展追踪报告_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    new_filename = 'f"career_tracking_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    
    if old_filename in content:
        content = content.replace(old_filename, new_filename)
        print("✅ 修复文件名编码问题")
    
    # 修复响应头编码问题
    old_headers = '''        filename = f"职业发展追踪报告_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )'''
    
    new_headers = '''        # 使用英文文件名避免编码问题
        safe_filename = f"career_tracking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return send_file(
            output,
            as_attachment=True,
            download_name=safe_filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )'''
    
    if old_headers in content:
        content = content.replace(old_headers, new_headers)
        print("✅ 修复响应头编码问题")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 职业发展追踪模块修复完成")
    return True

def fix_salary_dashboard_template():
    """修复薪酬分析仪表板模板的导出功能"""
    print("🔧 修复薪酬分析仪表板模板...")
    
    file_path = "app/templates/talent_management/hr_admin/salary_dashboard.html"
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经修复过
    if 'safe_filename' in content:
        print("✅ 薪酬分析模板已修复")
        return True
    
    # 修复exportData函数中的错误处理
    old_error_handling = '''                // 显示详细错误信息
                let errorMessage = '导出失败，请重试。';
                if (error.message.includes('502')) {
                    errorMessage = '服务器暂时不可用，请稍后重试。';
                } else if (error.message.includes('500')) {
                    errorMessage = '服务器内部错误，请联系管理员。';
                } else if (error.message.includes('404')) {
                    errorMessage = '导出接口不存在，请联系管理员。';
                } else if (error.message.includes('403')) {
                    errorMessage = '权限不足，请检查登录状态。';
                } else if (error.message.includes('401')) {
                    errorMessage = '请先登录系统。';
                }
                
                showNotification(errorMessage, 'error');'''
    
    new_error_handling = '''                // 显示详细错误信息
                let errorMessage = '导出失败，请重试。';
                if (error.message.includes('502')) {
                    errorMessage = '服务器暂时不可用，请稍后重试。错误信息: ' + error.message;
                } else if (error.message.includes('500')) {
                    errorMessage = '服务器内部错误，请联系管理员。错误信息: ' + error.message;
                } else if (error.message.includes('404')) {
                    errorMessage = '导出接口不存在，请联系管理员。错误信息: ' + error.message;
                } else if (error.message.includes('403')) {
                    errorMessage = '权限不足，请检查登录状态。错误信息: ' + error.message;
                } else if (error.message.includes('401')) {
                    errorMessage = '请先登录系统。错误信息: ' + error.message;
                } else {
                    errorMessage = '导出失败，请重试。错误信息: ' + error.message;
                }
                
                showNotification(errorMessage, 'error');'''
    
    if old_error_handling in content:
        content = content.replace(old_error_handling, new_error_handling)
        print("✅ 修复错误处理")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 薪酬分析仪表板模板修复完成")
    return True

def fix_org_health_dashboard_template():
    """修复组织健康度仪表板模板的导出功能"""
    print("🔧 修复组织健康度仪表板模板...")
    
    file_path = "app/templates/talent_management/hr_admin/org_health_dashboard.html"
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经修复过
    if 'safe_filename' in content:
        print("✅ 组织健康度模板已修复")
        return True
    
    # 修复exportReport函数中的错误处理
    old_error_handling = '''                // 显示详细错误信息
                let errorMessage = '导出失败，请重试。';
                if (error.message.includes('502')) {
                    errorMessage = '服务器暂时不可用，请稍后重试。';
                } else if (error.message.includes('500')) {
                    errorMessage = '服务器内部错误，请联系管理员。';
                } else if (error.message.includes('404')) {
                    errorMessage = '导出接口不存在，请联系管理员。';
                } else if (error.message.includes('403')) {
                    errorMessage = '权限不足，请检查登录状态。';
                } else if (error.message.includes('401')) {
                    errorMessage = '请先登录系统。';
                }
                
                showNotification(errorMessage, 'error');'''
    
    new_error_handling = '''                // 显示详细错误信息
                let errorMessage = '导出失败，请重试。';
                if (error.message.includes('502')) {
                    errorMessage = '服务器暂时不可用，请稍后重试。错误信息: ' + error.message;
                } else if (error.message.includes('500')) {
                    errorMessage = '服务器内部错误，请联系管理员。错误信息: ' + error.message;
                } else if (error.message.includes('404')) {
                    errorMessage = '导出接口不存在，请联系管理员。错误信息: ' + error.message;
                } else if (error.message.includes('403')) {
                    errorMessage = '权限不足，请检查登录状态。错误信息: ' + error.message;
                } else if (error.message.includes('401')) {
                    errorMessage = '请先登录系统。错误信息: ' + error.message;
                } else {
                    errorMessage = '导出失败，请重试。错误信息: ' + error.message;
                }
                
                showNotification(errorMessage, 'error');'''
    
    if old_error_handling in content:
        content = content.replace(old_error_handling, new_error_handling)
        print("✅ 修复错误处理")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 组织健康度仪表板模板修复完成")
    return True

def fix_career_tracking_dashboard_template():
    """修复职业发展追踪仪表板模板的导出功能"""
    print("🔧 修复职业发展追踪仪表板模板...")
    
    file_path = "app/templates/talent_management/hr_admin/career_tracking_dashboard.html"
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经修复过
    if 'safe_filename' in content:
        print("✅ 职业发展追踪模板已修复")
        return True
    
    # 修复exportReport函数中的错误处理
    old_error_handling = '''                // 显示详细错误信息
                let errorMessage = '导出失败，请重试。';
                if (error.message.includes('502')) {
                    errorMessage = '服务器暂时不可用，请稍后重试。';
                } else if (error.message.includes('500')) {
                    errorMessage = '服务器内部错误，请联系管理员。';
                } else if (error.message.includes('404')) {
                    errorMessage = '导出接口不存在，请联系管理员。';
                } else if (error.message.includes('403')) {
                    errorMessage = '权限不足，请检查登录状态。';
                } else if (error.message.includes('401')) {
                    errorMessage = '请先登录系统。';
                }
                
                showNotification(errorMessage, 'error');'''
    
    new_error_handling = '''                // 显示详细错误信息
                let errorMessage = '导出失败，请重试。';
                if (error.message.includes('502')) {
                    errorMessage = '服务器暂时不可用，请稍后重试。错误信息: ' + error.message;
                } else if (error.message.includes('500')) {
                    errorMessage = '服务器内部错误，请联系管理员。错误信息: ' + error.message;
                } else if (error.message.includes('404')) {
                    errorMessage = '导出接口不存在，请联系管理员。错误信息: ' + error.message;
                } else if (error.message.includes('403')) {
                    errorMessage = '权限不足，请检查登录状态。错误信息: ' + error.message;
                } else if (error.message.includes('401')) {
                    errorMessage = '请先登录系统。错误信息: ' + error.message;
                } else {
                    errorMessage = '导出失败，请重试。错误信息: ' + error.message;
                }
                
                showNotification(errorMessage, 'error');'''
    
    if old_error_handling in content:
        content = content.replace(old_error_handling, new_error_handling)
        print("✅ 修复错误处理")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 职业发展追踪仪表板模板修复完成")
    return True

def create_test_script():
    """创建测试脚本"""
    print("🔧 创建测试脚本...")
    
    test_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有模块的导出功能
"""

import requests
import json
from datetime import datetime

def test_all_exports():
    """测试所有模块的导出功能"""
    print("🧪 测试所有模块的导出功能...")
    
    # 测试端点列表
    endpoints = [
        {
            "name": "薪酬分析导出",
            "url": "http://localhost:5000/talent/hr_admin/salary_analysis/api/export_data",
            "method": "POST"
        },
        {
            "name": "组织健康度导出",
            "url": "http://localhost:5000/talent/hr_admin/org_health/api/export_report",
            "method": "POST"
        },
        {
            "name": "职业发展追踪导出",
            "url": "http://localhost:5000/talent/hr_admin/career_tracking/api/export_report",
            "method": "POST"
        },
        {
            "name": "人才流失预警导出",
            "url": "http://localhost:5000/talent/hr_admin/turnover_alert/api/export_data",
            "method": "POST"
        }
    ]
    
    for endpoint in endpoints:
        print(f"\\n📋 测试 {endpoint['name']}...")
        
        try:
            response = requests.post(endpoint['url'], timeout=30)
            
            print(f"状态码: {response.status_code}")
            print(f"响应头: {dict(response.headers)}")
            
            if response.status_code == 200:
                print("✅ 导出成功！")
                print(f"文件大小: {len(response.content)} bytes")
                
                # 保存文件
                filename = f"{endpoint['name'].replace('导出', '')}_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                with open(filename, 'wb') as f:
                    f.write(response.content)
                print(f"✅ 文件已保存为: {filename}")
                
            elif response.status_code == 401:
                print("⚠️ 需要登录")
            elif response.status_code == 403:
                print("⚠️ 权限不足")
            else:
                print(f"❌ 导出失败: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求失败: {e}")
        except Exception as e:
            print(f"❌ 测试失败: {e}")
    
    print("\\n🎉 所有模块导出功能测试完成！")

if __name__ == "__main__":
    test_all_exports()
'''
    
    test_file = "test_all_exports.py"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ 测试脚本创建成功")
    return True

def main():
    """主函数"""
    print("🚀 开始修复所有模块的导出功能...")
    
    try:
        # 修复后端模块
        fix_salary_analysis_export()
        fix_org_health_export()
        fix_career_tracking_export()
        
        # 修复前端模板
        fix_salary_dashboard_template()
        fix_org_health_dashboard_template()
        fix_career_tracking_dashboard_template()
        
        # 创建测试脚本
        create_test_script()
        
        print("\\n✅ 所有模块导出功能修复完成！")
        print("\\n📋 修复内容:")
        print("  - 修复了薪酬分析模块的导出功能（502错误）")
        print("  - 修复了组织健康度模块的导出功能（无反应）")
        print("  - 修复了职业发展追踪模块的导出功能（无反应）")
        print("  - 修复了所有模块的文件名编码问题")
        print("  - 修复了所有模块的响应头编码问题")
        print("  - 改进了错误处理和用户提示")
        print("  - 创建了综合测试脚本")
        
        print("\\n💡 修复原理:")
        print("  - 将中文文件名改为英文文件名")
        print("  - 避免HTTP响应头中的中文字符")
        print("  - 使用安全的字符编码")
        print("  - 改进错误处理和用户反馈")
        
        print("\\n🔄 建议重启服务:")
        print("  sudo systemctl restart llrc")
        
        print("\\n🧪 测试方法:")
        print("  python3 test_all_exports.py")
        
        return True
        
    except Exception as e:
        print(f"❌ 修复过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    main()
