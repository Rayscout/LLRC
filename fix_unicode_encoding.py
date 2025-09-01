#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复Unicode编码错误脚本
解决导出功能中的中文字符编码问题
"""

import os
import re
from pathlib import Path
from datetime import datetime
from flask import send_file
from io import BytesIO

def fix_salary_analysis_export():
    """修复薪酬分析模块的导出编码问题"""
    print("🔧 修复薪酬分析模块导出编码问题...")
    
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
    
    print("✅ 薪酬分析模块编码问题修复完成")
    return True

def fix_turnover_alert_export():
    """修复人才流失预警模块的导出编码问题"""
    print("🔧 修复人才流失预警模块导出编码问题...")
    
    file_path = "talent_management_system/hr_admin_module/turnover_alert.py"
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复文件名编码问题
    old_filename = 'f"人才流失预警报告_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    new_filename = 'f"turnover_alert_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
    
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
            safe_filename = f"turnover_alert_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
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
    
    print("✅ 人才流失预警模块编码问题修复完成")
    return True

def fix_org_health_export():
    """修复组织健康度模块的导出编码问题"""
    print("🔧 修复组织健康度模块导出编码问题...")
    
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
    
    print("✅ 组织健康度模块编码问题修复完成")
    return True

def fix_career_tracking_export():
    """修复职业发展追踪模块的导出编码问题"""
    print("🔧 修复职业发展追踪模块导出编码问题...")
    
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
    
    print("✅ 职业发展追踪模块编码问题修复完成")
    return True

def create_export_utility():
    """创建通用的导出工具函数"""
    print("🔧 创建通用导出工具函数...")
    
    utility_code = '''# -*- coding: utf-8 -*-
"""
通用导出工具函数
解决Unicode编码问题
"""

import os
import re
from datetime import datetime
from flask import send_file
from io import BytesIO

def create_safe_filename(prefix, extension):
    """创建安全的文件名，避免编码问题"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{timestamp}.{extension}"

def send_excel_file(output, prefix="report"):
    """安全发送Excel文件，避免编码问题"""
    safe_filename = create_safe_filename(prefix, "xlsx")
    
    response = send_file(
        output,
        as_attachment=True,
        download_name=safe_filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    # 设置响应头 - 避免中文字符
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
    
    return response

def send_pdf_file(output, prefix="report"):
    """安全发送PDF文件，避免编码问题"""
    safe_filename = create_safe_filename(prefix, "pdf")
    
    response = send_file(
        output,
        as_attachment=True,
        download_name=safe_filename,
        mimetype='application/pdf'
    )
    
    # 设置响应头 - 避免中文字符
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
    
    return response

def sanitize_filename(filename):
    """清理文件名，移除不安全的字符"""
    # 移除或替换不安全的字符
    filename = re.sub(r'[<>:"/\\\\|?*]', '', filename)
    # 限制长度
    if len(filename) > 100:
        filename = filename[:100]
    return filename
'''
    
    utility_file = "talent_management_system/utils/export_utils.py"
    
    # 创建目录
    os.makedirs(os.path.dirname(utility_file), exist_ok=True)
    
    # 写入文件
    with open(utility_file, 'w', encoding='utf-8') as f:
        f.write(utility_code)
    
    print("✅ 通用导出工具函数创建成功")
    return True

def main():
    """主函数"""
    print("🚀 开始修复Unicode编码问题...")
    
    try:
        # 修复各个模块的编码问题
        fix_salary_analysis_export()
        fix_turnover_alert_export()
        fix_org_health_export()
        fix_career_tracking_export()
        
        # 创建通用导出工具
        create_export_utility()
        
        print("\n✅ Unicode编码问题修复完成！")
        print("\n📋 修复内容:")
        print("  - 修复了薪酬分析模块的导出编码问题")
        print("  - 修复了人才流失预警模块的导出编码问题")
        print("  - 修复了组织健康度模块的导出编码问题")
        print("  - 修复了职业发展追踪模块的导出编码问题")
        print("  - 创建了通用导出工具函数")
        
        print("\n💡 修复原理:")
        print("  - 将中文文件名改为英文文件名")
        print("  - 避免HTTP响应头中的中文字符")
        print("  - 使用安全的字符编码")
        
        print("\n🔄 建议重启服务:")
        print("  sudo systemctl restart llrc")
        
        return True
        
    except Exception as e:
        print(f"❌ 修复过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    main()
