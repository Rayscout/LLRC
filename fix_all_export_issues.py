#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合修复所有模块的导出功能
解决薪酬分析、组织健康度、职业发展追踪等模块的导出问题
"""

import os
import re
from pathlib import Path

def fix_salary_dashboard_export():
    """修复薪酬分析模块的导出功能"""
    print("🔧 修复薪酬分析模块导出功能...")
    
    file_path = "app/templates/talent_management/hr_admin/salary_dashboard.html"
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复exportData函数 - 改进错误处理和用户体验
    old_export_function = '''        // 导出数据功能
        function exportData() {
            console.log('开始导出数据...');
            alert('正在导出薪酬数据报表...');
            
            // 使用fetch API发送POST请求
            fetch('{{ url_for("talent_management.hr_admin.salary_analysis.export_salary_data") }}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                console.log('响应状态:', response.status);
                console.log('响应头:', response.headers);
                
                if (response.ok) {
                    return response.blob();
                } else {
                    // 尝试获取错误信息
                    return response.text().then(text => {
                        console.error('错误响应:', text);
                        throw new Error(`导出失败: ${response.status} ${response.statusText}`);
                    });
                }
            })
            .then(blob => {
                console.log('获取到blob数据:', blob);
                // 创建下载链接
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `薪酬分析报告_${new Date().toISOString().slice(0,10)}.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                alert('导出成功！');
            })
            .catch(error => {
                console.error('导出错误:', error);
                alert('导出失败，请重试。错误信息: ' + error.message);
            });
        }'''
    
    new_export_function = '''        // 导出数据功能
        function exportData() {
            console.log('开始导出数据...');
            
            // 显示加载状态
            const exportBtn = event.target.closest('button');
            if (exportBtn) {
                const originalText = exportBtn.innerHTML;
                exportBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 导出中...';
                exportBtn.disabled = true;
                
                // 恢复按钮状态
                setTimeout(() => {
                    exportBtn.innerHTML = originalText;
                    exportBtn.disabled = false;
                }, 5000);
            }
            
            // 使用fetch API发送POST请求
            fetch('{{ url_for("talent_management.hr_admin.salary_analysis.export_salary_data") }}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                console.log('响应状态:', response.status);
                console.log('响应头:', response.headers);
                
                if (response.ok) {
                    return response.blob();
                } else {
                    // 尝试获取错误信息
                    return response.text().then(text => {
                        console.error('错误响应:', text);
                        throw new Error(`导出失败: ${response.status} ${response.statusText}`);
                    });
                }
            })
            .then(blob => {
                console.log('获取到blob数据:', blob);
                // 创建下载链接
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `salary_analysis_report_${new Date().toISOString().slice(0,10)}.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                // 显示成功通知
                showNotification('薪酬数据导出成功！', 'success');
            })
            .catch(error => {
                console.error('导出错误:', error);
                
                // 显示详细错误信息
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
                
                showNotification(errorMessage, 'error');
            });
        }'''
    
    if old_export_function in content:
        content = content.replace(old_export_function, new_export_function)
        print("✅ 修复导出函数")
    else:
        print("⚠️ 未找到旧的导出函数，可能已经被修改")
    
    # 添加通知函数
    if 'function showNotification' not in content:
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
                ${type === 'success' ? 'background: #34C759;' : 
                  type === 'error' ? 'background: #FF3B30;' : 
                  'background: #007AFF;'}
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
        
        # 在script标签结束前添加通知函数
        script_end = '</script>'
        if script_end in content:
            content = content.replace(script_end, notification_function + '\n    ' + script_end)
            print("✅ 添加通知函数")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 薪酬分析模块导出功能修复完成")
    return True

def fix_org_health_dashboard_export():
    """修复组织健康度模块的导出功能"""
    print("🔧 修复组织健康度模块导出功能...")
    
    file_path = "app/templates/talent_management/hr_admin/org_health_dashboard.html"
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复exportReport函数
    old_export_function = '''        function exportReport() {
            alert('正在导出组织健康度对比报告...');
            
            // 使用fetch API发送POST请求
            fetch('{{ url_for("talent_management.hr_admin.org_health.export_org_health_report") }}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (response.ok) {
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
                a.download = `组织健康度评估报告_${new Date().toISOString().slice(0,10)}.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                alert('导出成功！');
            })
            .catch(error => {
                console.error('导出错误:', error);
                alert('导出失败，请重试');
            });
        }'''
    
    new_export_function = '''        function exportReport() {
            console.log('开始导出组织健康度报告...');
            
            // 显示加载状态
            const exportBtn = event.target.closest('button');
            if (exportBtn) {
                const originalText = exportBtn.innerHTML;
                exportBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 导出中...';
                exportBtn.disabled = true;
                
                // 恢复按钮状态
                setTimeout(() => {
                    exportBtn.innerHTML = originalText;
                    exportBtn.disabled = false;
                }, 5000);
            }
            
            // 使用fetch API发送POST请求
            fetch('{{ url_for("talent_management.hr_admin.org_health.export_org_health_report") }}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                console.log('响应状态:', response.status);
                
                if (response.ok) {
                    return response.blob();
                } else {
                    return response.text().then(text => {
                        console.error('错误响应:', text);
                        throw new Error(`导出失败: ${response.status} ${response.statusText}`);
                    });
                }
            })
            .then(blob => {
                // 创建下载链接
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `org_health_report_${new Date().toISOString().slice(0,10)}.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                // 显示成功通知
                showNotification('组织健康度报告导出成功！', 'success');
            })
            .catch(error => {
                console.error('导出错误:', error);
                
                // 显示详细错误信息
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
                
                showNotification(errorMessage, 'error');
            });
        }'''
    
    if old_export_function in content:
        content = content.replace(old_export_function, new_export_function)
        print("✅ 修复导出函数")
    else:
        print("⚠️ 未找到旧的导出函数，可能已经被修改")
    
    # 添加通知函数
    if 'function showNotification' not in content:
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
                ${type === 'success' ? 'background: #34C759;' : 
                  type === 'error' ? 'background: #FF3B30;' : 
                  'background: #007AFF;'}
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
        
        # 在script标签结束前添加通知函数
        script_end = '</script>'
        if script_end in content:
            content = content.replace(script_end, notification_function + '\n    ' + script_end)
            print("✅ 添加通知函数")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 组织健康度模块导出功能修复完成")
    return True

def fix_career_tracking_dashboard_export():
    """修复职业发展追踪模块的导出功能"""
    print("🔧 修复职业发展追踪模块导出功能...")
    
    file_path = "app/templates/talent_management/hr_admin/career_tracking_dashboard.html"
    
    if not Path(file_path).exists():
        print(f"❌ 文件不存在: {file_path}")
        return False
    
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 修复exportReport函数
    old_export_function = '''        // 导出报告功能
        function exportReport() {
            alert('正在导出职业发展追踪报告...');
            
            // 创建表单并提交
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '{{ url_for("talent_management.hr_admin.career_tracking.export_career_report") }}';
            form.target = '_blank';
            
            document.body.appendChild(form);
            form.submit();
            document.body.removeChild(form);
        }'''
    
    new_export_function = '''        // 导出报告功能
        function exportReport() {
            console.log('开始导出职业发展追踪报告...');
            
            // 显示加载状态
            const exportBtn = event.target.closest('button');
            if (exportBtn) {
                const originalText = exportBtn.innerHTML;
                exportBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 导出中...';
                exportBtn.disabled = true;
                
                // 恢复按钮状态
                setTimeout(() => {
                    exportBtn.innerHTML = originalText;
                    exportBtn.disabled = false;
                }, 5000);
            }
            
            // 使用fetch API发送POST请求
            fetch('{{ url_for("talent_management.hr_admin.career_tracking.export_career_report") }}', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                console.log('响应状态:', response.status);
                
                if (response.ok) {
                    return response.blob();
                } else {
                    return response.text().then(text => {
                        console.error('错误响应:', text);
                        throw new Error(`导出失败: ${response.status} ${response.statusText}`);
                    });
                }
            })
            .then(blob => {
                // 创建下载链接
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `career_tracking_report_${new Date().toISOString().slice(0,10)}.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                // 显示成功通知
                showNotification('职业发展追踪报告导出成功！', 'success');
            })
            .catch(error => {
                console.error('导出错误:', error);
                
                // 显示详细错误信息
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
                
                showNotification(errorMessage, 'error');
            });
        }'''
    
    if old_export_function in content:
        content = content.replace(old_export_function, new_export_function)
        print("✅ 修复导出函数")
    else:
        print("⚠️ 未找到旧的导出函数，可能已经被修改")
    
    # 添加通知函数
    if 'function showNotification' not in content:
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
                ${type === 'success' ? 'background: #34C759;' : 
                  type === 'error' ? 'background: #FF3B30;' : 
                  'background: #007AFF;'}
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
        
        # 在script标签结束前添加通知函数
        script_end = '</script>'
        if script_end in content:
            content = content.replace(script_end, notification_function + '\n    ' + script_end)
            print("✅ 添加通知函数")
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 职业发展追踪模块导出功能修复完成")
    return True

def add_css_animations_to_all_templates():
    """为所有模板添加CSS动画样式"""
    print("🔧 为所有模板添加CSS动画样式...")
    
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
    
    templates = [
        "app/templates/talent_management/hr_admin/salary_dashboard.html",
        "app/templates/talent_management/hr_admin/org_health_dashboard.html",
        "app/templates/talent_management/hr_admin/career_tracking_dashboard.html"
    ]
    
    for template_path in templates:
        if Path(template_path).exists():
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否已经存在动画样式
            if '@keyframes slideIn' not in content:
                # 在CSS部分添加动画样式
                css_insert_point = '@keyframes fadeInUp {'
                if css_insert_point in content:
                    content = content.replace(css_insert_point, css_animations + '\n\n        ' + css_insert_point)
                    print(f"✅ 为 {template_path} 添加CSS动画样式")
                else:
                    print(f"⚠️ 未找到CSS插入点: {template_path}")
                
                # 写回文件
                with open(template_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            else:
                print(f"✅ {template_path} 已有CSS动画样式")
    
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
            "url": "http://localhost:5000/talent/hr_admin/salary_analysis/export_salary_data",
            "method": "POST"
        },
        {
            "name": "组织健康度导出",
            "url": "http://localhost:5000/talent/hr_admin/org_health/export_org_health_report",
            "method": "POST"
        },
        {
            "name": "职业发展追踪导出",
            "url": "http://localhost:5000/talent/hr_admin/career_tracking/export_career_report",
            "method": "POST"
        },
        {
            "name": "人才流失预警导出",
            "url": "http://localhost:5000/talent/hr_admin/turnover_alert/api/export_data",
            "method": "POST"
        }
    ]
    
    for endpoint in endpoints:
        print(f"\\n🔍 测试 {endpoint['name']}...")
        test_endpoint(endpoint)

def test_endpoint(endpoint):
    """测试单个端点"""
    try:
        response = requests.request(
            endpoint['method'], 
            endpoint['url'], 
            timeout=30,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"  状态码: {response.status_code}")
        print(f"  响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"  ✅ {endpoint['name']}成功！")
            print(f"  文件大小: {len(response.content)} bytes")
            
            # 保存文件
            filename = f"{endpoint['name'].replace('导出', '')}_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"  ✅ 文件已保存为: {filename}")
            
        elif response.status_code == 401:
            print(f"  ⚠️ {endpoint['name']}需要登录")
        elif response.status_code == 403:
            print(f"  ⚠️ {endpoint['name']}权限不足")
        elif response.status_code == 404:
            print(f"  ❌ {endpoint['name']}接口不存在")
        elif response.status_code == 500:
            print(f"  ❌ {endpoint['name']}服务器内部错误")
        elif response.status_code == 502:
            print(f"  ❌ {endpoint['name']}网关错误")
        else:
            print(f"  ❌ {endpoint['name']}失败: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"  ❌ {endpoint['name']}请求失败: {e}")
    except Exception as e:
        print(f"  ❌ {endpoint['name']}测试失败: {e}")

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
        # 修复各个模块的导出功能
        fix_salary_dashboard_export()
        fix_org_health_dashboard_export()
        fix_career_tracking_dashboard_export()
        
        # 添加CSS动画样式
        add_css_animations_to_all_templates()
        
        # 创建测试脚本
        create_test_script()
        
        print("\\n✅ 所有模块导出功能修复完成！")
        print("\\n📋 修复内容:")
        print("  - 修复了薪酬分析模块的导出功能")
        print("  - 修复了组织健康度模块的导出功能")
        print("  - 修复了职业发展追踪模块的导出功能")
        print("  - 改进了错误处理和用户反馈")
        print("  - 添加了加载状态指示")
        print("  - 统一了通知系统")
        print("  - 创建了综合测试脚本")
        
        print("\\n💡 修复原理:")
        print("  - 改进fetch API的错误处理")
        print("  - 添加详细的错误信息提示")
        print("  - 实现用户友好的通知系统")
        print("  - 添加加载状态指示")
        print("  - 统一文件名格式避免编码问题")
        
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
