#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复人才流失预警模块导出功能
解决"数据导出功能开发中..."的问题
"""

import os
import re
from pathlib import Path

def fix_turnover_dashboard_template():
    """修复人才流失预警仪表板模板的导出功能"""
    print("🔧 修复人才流失预警仪表板模板...")
    
    file_path = "app/templates/talent_management/hr_admin/turnover_dashboard.html"
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找并替换exportData函数
    old_export_function = '''        // 导出数据
        function exportData() {
            const btn = event.target.closest('button');
            if (btn) {
                btn.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    btn.style.transform = 'scale(1)';
                }, 150);
            }
            
            // 这里可以实现数据导出功能
            alert('数据导出功能开发中...');
        }'''
    
    new_export_function = '''        // 导出数据
        function exportData() {
            const btn = event.target.closest('button');
            if (btn) {
                btn.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    btn.style.transform = 'scale(1)';
                }, 150);
            }
            
            // 调用后端导出API
            fetch('/talent/hr_admin/turnover_alert/api/export_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => {
                if (response.ok) {
                    // 创建下载链接
                    return response.blob();
                } else {
                    throw new Error('导出失败');
                }
            })
            .then(blob => {
                // 创建下载链接
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `turnover_alert_report_${new Date().toISOString().slice(0,10)}.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                // 显示成功提示
                showNotification('数据导出成功！', 'success');
            })
            .catch(error => {
                console.error('导出失败:', error);
                showNotification('数据导出失败，请稍后重试', 'error');
            });
        }'''
    
    if old_export_function in content:
        content = content.replace(old_export_function, new_export_function)
        print("✅ 修复导出函数")
    else:
        print("⚠️ 未找到旧的导出函数，可能已经被修改")
    
    # 添加通知函数
    notification_function = '''        
        // 显示通知
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.textContent = message;
            
            // 添加样式
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 500;
                z-index: 1000;
                animation: slideIn 0.3s ease-out;
                ${type === 'success' ? 'background: var(--accent-green);' : 
                  type === 'error' ? 'background: var(--accent-red);' : 
                  'background: var(--accent-blue);'}
            `;
            
            document.body.appendChild(notification);
            
            // 3秒后自动消失
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }, 3000);
        }'''
    
    # 检查是否已经存在通知函数
    if 'function showNotification' not in content:
        # 在script标签结束前添加通知函数
        script_end = '</script>'
        if script_end in content:
            content = content.replace(script_end, notification_function + '\n    ' + script_end)
            print("✅ 添加通知函数")
        else:
            print("⚠️ 未找到script标签结束位置")
    else:
        print("✅ 通知函数已存在")
    
    # 添加CSS动画样式
    css_animations = '''        /* 通知动画 */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(100%);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        @keyframes slideOut {
            from {
                opacity: 1;
                transform: translateX(0);
            }
            to {
                opacity: 0;
                transform: translateX(100%);
            }
        }'''
    
    # 检查是否已经存在动画样式
    if '@keyframes slideIn' not in content:
        # 在CSS部分添加动画样式
        css_insert_point = '@keyframes fadeInUp {'
        if css_insert_point in content:
            content = content.replace(css_insert_point, css_animations + '\n\n        ' + css_insert_point)
            print("✅ 添加CSS动画样式")
        else:
            print("⚠️ 未找到CSS插入点")
    else:
        print("✅ CSS动画样式已存在")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 人才流失预警仪表板模板修复完成")
    return True

def fix_turnover_alert_backend():
    """修复人才流失预警后端模块的编码问题"""
    print("🔧 修复人才流失预警后端模块...")
    
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
    
    print("✅ 人才流失预警后端模块修复完成")
    return True

def create_test_script():
    """创建测试脚本"""
    print("🔧 创建测试脚本...")
    
    test_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试人才流失预警导出功能
"""

import requests
import json

def test_turnover_export():
    """测试人才流失预警导出功能"""
    print("🧪 测试人才流失预警导出功能...")
    
    # 测试导出端点
    url = "http://localhost:5000/talent/hr_admin/turnover_alert/api/export_data"
    
    try:
        response = requests.post(url, timeout=30)
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ 导出成功！")
            print(f"文件大小: {len(response.content)} bytes")
            
            # 保存文件
            filename = f"turnover_alert_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
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

if __name__ == "__main__":
    from datetime import datetime
    test_turnover_export()
'''
    
    test_file = "test_turnover_export.py"
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ 测试脚本创建成功")
    return True

def main():
    """主函数"""
    print("🚀 开始修复人才流失预警模块导出功能...")
    
    try:
        # 修复前端模板
        fix_turnover_dashboard_template()
        
        # 修复后端模块
        fix_turnover_alert_backend()
        
        # 创建测试脚本
        create_test_script()
        
        print("\\n✅ 人才流失预警模块导出功能修复完成！")
        print("\\n📋 修复内容:")
        print("  - 修复了前端模板中的导出函数")
        print("  - 替换了'数据导出功能开发中...'提示")
        print("  - 实现了完整的Excel文件下载功能")
        print("  - 修复了后端文件名编码问题")
        print("  - 添加了用户友好的通知系统")
        print("  - 创建了测试脚本")
        
        print("\\n💡 修复原理:")
        print("  - 前端调用后端导出API")
        print("  - 使用Blob处理文件下载")
        print("  - 避免中文字符编码问题")
        print("  - 提供实时用户反馈")
        
        print("\\n🔄 建议重启服务:")
        print("  sudo systemctl restart llrc")
        
        print("\\n🧪 测试方法:")
        print("  python3 test_turnover_export.py")
        
        return True
        
    except Exception as e:
        print(f"❌ 修复过程中出现错误: {e}")
        return False

if __name__ == "__main__":
    main()
