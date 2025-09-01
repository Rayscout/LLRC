#!/bin/bash

# 综合修复所有模块导出功能部署脚本
# 解决薪酬分析、组织健康度、职业发展追踪等模块的导出问题

echo "🚀 开始部署所有模块导出功能修复..."

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查是否在云服务器上
if [[ "$(hostname)" == *"iZ"* ]] || [[ "$(hostname)" == *"cloud"* ]]; then
    log_info "检测到云服务器环境"
    CLOUD_ENV=true
else
    log_info "检测到本地环境"
    CLOUD_ENV=false
fi

# 步骤1: 备份当前文件
log_info "步骤1: 备份当前文件..."
backup_dir="backup_all_exports_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"

# 备份相关文件
templates_to_backup=(
    "app/templates/talent_management/hr_admin/salary_dashboard.html"
    "app/templates/talent_management/hr_admin/org_health_dashboard.html"
    "app/templates/talent_management/hr_admin/career_tracking_dashboard.html"
)

for template in "${templates_to_backup[@]}"; do
    if [ -f "$template" ]; then
        cp "$template" "$backup_dir/"
        log_success "已备份: $template"
    else
        log_warning "文件不存在: $template"
    fi
done

# 步骤2: 修复薪酬分析模块
log_info "步骤2: 修复薪酬分析模块..."
if [ -f "app/templates/talent_management/hr_admin/salary_dashboard.html" ]; then
    # 修复exportData函数 - 改进错误处理
    sed -i 's/alert('\''导出失败，请重试。错误信息: '\'' + error.message);/\/\/ 显示详细错误信息\n                let errorMessage = '\''导出失败，请重试。'\'';\n                if (error.message.includes('\''502'\'')) {\n                    errorMessage = '\''服务器暂时不可用，请稍后重试。'\'';\n                } else if (error.message.includes('\''500'\'')) {\n                    errorMessage = '\''服务器内部错误，请联系管理员。'\'';\n                } else if (error.message.includes('\''404'\'')) {\n                    errorMessage = '\''导出接口不存在，请联系管理员。'\'';\n                } else if (error.message.includes('\''403'\'')) {\n                    errorMessage = '\''权限不足，请检查登录状态。'\'';\n                } else if (error.message.includes('\''401'\'')) {\n                    errorMessage = '\''请先登录系统。'\'';\n                }\n                \n                showNotification(errorMessage, '\''error'\'');/' "app/templates/talent_management/hr_admin/salary_dashboard.html"
    
    # 修复文件名编码问题
    sed -i 's/薪酬分析报告_/salary_analysis_report_/g' "app/templates/talent_management/hr_admin/salary_dashboard.html"
    
    # 添加加载状态指示
    sed -i '/console.log('\''开始导出数据...'\'');/a\            \n            // 显示加载状态\n            const exportBtn = event.target.closest('\''button'\'');\n            if (exportBtn) {\n                const originalText = exportBtn.innerHTML;\n                exportBtn.innerHTML = '\''<i class="fas fa-spinner fa-spin"></i> 导出中...'\'';\n                exportBtn.disabled = true;\n                \n                // 恢复按钮状态\n                setTimeout(() => {\n                    exportBtn.innerHTML = originalText;\n                    exportBtn.disabled = false;\n                }, 5000);\n            }' "app/templates/talent_management/hr_admin/salary_dashboard.html"
    
    # 替换成功提示
    sed -i 's/alert('\''导出成功！'\'');/\/\/ 显示成功通知\n                showNotification('\''薪酬数据导出成功！'\'', '\''success'\'');/' "app/templates/talent_management/hr_admin/salary_dashboard.html"
    
    log_success "薪酬分析模块修复完成"
else
    log_warning "薪酬分析模板文件不存在，跳过修复"
fi

# 步骤3: 修复组织健康度模块
log_info "步骤3: 修复组织健康度模块..."
if [ -f "app/templates/talent_management/hr_admin/org_health_dashboard.html" ]; then
    # 修复exportReport函数 - 改进错误处理
    sed -i 's/throw new Error('\''导出失败'\'');/return response.text().then(text => {\n                        console.error('\''错误响应'\'', text);\n                        throw new Error(`导出失败: ${response.status} ${response.statusText}`);\n                    });/' "app/templates/talent_management/hr_admin/org_health_dashboard.html"
    
    # 修复文件名编码问题
    sed -i 's/组织健康度评估报告_/org_health_report_/g' "app/templates/talent_management/hr_admin/org_health_dashboard.html"
    
    # 添加加载状态指示
    sed -i '/console.log('\''开始导出组织健康度报告...'\'');/a\            \n            // 显示加载状态\n            const exportBtn = event.target.closest('\''button'\'');\n            if (exportBtn) {\n                const originalText = exportBtn.innerHTML;\n                exportBtn.innerHTML = '\''<i class="fas fa-spinner fa-spin"></i> 导出中...'\'';\n                exportBtn.disabled = true;\n                \n                // 恢复按钮状态\n                setTimeout(() => {\n                    exportBtn.innerHTML = originalText;\n                    exportBtn.disabled = false;\n                }, 5000);\n            }' "app/templates/talent_management/hr_admin/org_health_dashboard.html"
    
    # 替换成功提示
    sed -i 's/alert('\''导出成功！'\'');/\/\/ 显示成功通知\n                showNotification('\''组织健康度报告导出成功！'\'', '\''success'\'');/' "app/templates/talent_management/hr_admin/org_health_dashboard.html"
    
    # 替换错误提示
    sed -i 's/alert('\''导出失败，请重试'\'');/\/\/ 显示详细错误信息\n                let errorMessage = '\''导出失败，请重试。'\'';\n                if (error.message.includes('\''502'\'')) {\n                    errorMessage = '\''服务器暂时不可用，请稍后重试。'\'';\n                } else if (error.message.includes('\''500'\'')) {\n                    errorMessage = '\''服务器内部错误，请联系管理员。'\'';\n                } else if (error.message.includes('\''404'\'')) {\n                    errorMessage = '\''导出接口不存在，请联系管理员。'\'';\n                } else if (error.message.includes('\''403'\'')) {\n                    errorMessage = '\''权限不足，请检查登录状态。'\'';\n                } else if (error.message.includes('\''401'\'')) {\n                    errorMessage = '\''请先登录系统。'\'';\n                }\n                \n                showNotification(errorMessage, '\''error'\'');/' "app/templates/talent_management/hr_admin/org_health_dashboard.html"
    
    log_success "组织健康度模块修复完成"
else
    log_warning "组织健康度模板文件不存在，跳过修复"
fi

# 步骤4: 修复职业发展追踪模块
log_info "步骤4: 修复职业发展追踪模块..."
if [ -f "app/templates/talent_management/hr_admin/career_tracking_dashboard.html" ]; then
    # 完全替换exportReport函数
    old_export_function='        // 导出报告功能
        function exportReport() {
            alert('\''正在导出职业发展追踪报告...'\'');
            
            // 创建表单并提交
            const form = document.createElement('\''form'\'');
            form.method = '\''POST'\'';
            form.action = '\''{{ url_for("talent_management.hr_admin.career_tracking.export_career_report") }}'\'';
            form.target = '\''_blank'\'';
            
            document.body.appendChild(form);
            form.submit();
            document.body.removeChild(form);
        }'
    
    new_export_function='        // 导出报告功能
        function exportReport() {
            console.log('\''开始导出职业发展追踪报告...'\'');
            
            // 显示加载状态
            const exportBtn = event.target.closest('\''button'\'');
            if (exportBtn) {
                const originalText = exportBtn.innerHTML;
                exportBtn.innerHTML = '\''<i class="fas fa-spinner fa-spin"></i> 导出中...'\'';
                exportBtn.disabled = true;
                
                // 恢复按钮状态
                setTimeout(() => {
                    exportBtn.innerHTML = originalText;
                    exportBtn.disabled = false;
                }, 5000);
            }
            
            // 使用fetch API发送POST请求
            fetch('\''{{ url_for("talent_management.hr_admin.career_tracking.export_career_report") }}'\'', {
                method: '\''POST'\'',
                headers: {
                    '\''Content-Type'\'': '\''application/json'\'',
                    '\''X-Requested-With'\'': '\''XMLHttpRequest'\''
                }
            })
            .then(response => {
                console.log('\''响应状态:'\'', response.status);
                
                if (response.ok) {
                    return response.blob();
                } else {
                    return response.text().then(text => {
                        console.error('\''错误响应:'\'', text);
                        throw new Error(`导出失败: ${response.status} ${response.statusText}`);
                    });
                }
            })
            .then(blob => {
                // 创建下载链接
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('\''a'\'');
                a.href = url;
                a.download = `career_tracking_report_${new Date().toISOString().slice(0,10)}.xlsx`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);
                
                // 显示成功通知
                showNotification('\''职业发展追踪报告导出成功！'\'', '\''success'\'');
            })
            .catch(error => {
                console.error('\''导出错误:'\'', error);
                
                // 显示详细错误信息
                let errorMessage = '\''导出失败，请重试。'\'';
                if (error.message.includes('\''502'\'')) {
                    errorMessage = '\''服务器暂时不可用，请稍后重试。'\'';
                } else if (error.message.includes('\''500'\'')) {
                    errorMessage = '\''服务器内部错误，请联系管理员。'\'';
                } else if (error.message.includes('\''404'\'')) {
                    errorMessage = '\''导出接口不存在，请联系管理员。'\'';
                } else if (error.message.includes('\''403'\'')) {
                    errorMessage = '\''权限不足，请检查登录状态。'\'';
                } else if (error.message.includes('\''401'\'')) {
                    errorMessage = '\''请先登录系统。'\'';
                }
                
                showNotification(errorMessage, '\''error'\'');
            });
        }'
    
    if grep -q "正在导出职业发展追踪报告" "app/templates/talent_management/hr_admin/career_tracking_dashboard.html"; then
        # 使用sed替换整个函数
        sed -i '/\/\/ 导出报告功能/,/^        }$/c\'"$new_export_function" "app/templates/talent_management/hr_admin/career_tracking_dashboard.html"
        log_success "职业发展追踪模块导出函数修复完成"
    else
        log_warning "未找到职业发展追踪导出函数，可能已经被修改"
    fi
    
    log_success "职业发展追踪模块修复完成"
else
    log_warning "职业发展追踪模板文件不存在，跳过修复"
fi

# 步骤5: 为所有模板添加通知函数和CSS动画
log_info "步骤5: 为所有模板添加通知函数和CSS动画..."

# 通知函数
notification_function='        
        // 显示通知
        function showNotification(message, type = '\''info'\'') {
            const notification = document.createElement('\''div'\'');
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
                ${type === '\''success'\'' ? '\''background: #34C759;'\'' : 
                  type === '\''error'\'' ? '\''background: #FF3B30;'\'' : 
                  '\''background: #007AFF;'\''}
            `;
            
            document.body.appendChild(notification);
            
            // 3秒后自动消失
            setTimeout(() => {
                notification.style.animation = '\''slideOut 0.3s ease-out'\'';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }, 3000);
        }'

# CSS动画样式
css_animations='        /* 通知动画 */
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
        }'

# 为每个模板添加通知函数和CSS动画
for template in "${templates_to_backup[@]}"; do
    if [ -f "$template" ]; then
        # 添加通知函数
        if ! grep -q "function showNotification" "$template"; then
            sed -i 's/<\/script>/'"$notification_function"'\n    <\/script>/' "$template"
            log_success "为 $template 添加通知函数"
        fi
        
        # 添加CSS动画样式
        if ! grep -q "@keyframes slideIn" "$template"; then
            sed -i '/@keyframes fadeInUp {/i\'"$css_animations"'\n\n        ' "$template"
            log_success "为 $template 添加CSS动画样式"
        fi
    fi
done

# 步骤6: 创建测试脚本
log_info "步骤6: 创建测试脚本..."
cat > "test_all_exports.py" << 'EOF'
#!/usr/bin/env python3
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
        print(f"\n🔍 测试 {endpoint['name']}...")
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
EOF

log_success "测试脚本创建完成"

# 步骤7: 重启服务
if [ "$CLOUD_ENV" = true ]; then
    log_info "步骤7: 重启服务..."
    
    # 重启llrc服务
    log_info "重启llrc服务..."
    sudo systemctl restart llrc
    
    # 等待服务启动
    sleep 5
    
    # 检查服务状态
    if systemctl is-active --quiet llrc; then
        log_success "llrc服务重启成功"
    else
        log_error "llrc服务重启失败"
        systemctl status llrc
    fi
else
    log_info "本地环境，跳过服务重启"
fi

# 步骤8: 验证修复效果
log_info "步骤8: 验证修复效果..."
echo ""

# 检查文件修改
echo "📋 修复内容检查:"
for template in "${templates_to_backup[@]}"; do
    if [ -f "$template" ]; then
        template_name=$(basename "$template")
        echo "  📄 $template_name:"
        
        # 检查通知函数
        if grep -q "function showNotification" "$template"; then
            log_success "    ✅ 通知函数已添加"
        else
            log_warning "    ⚠️ 通知函数未找到"
        fi
        
        # 检查CSS动画
        if grep -q "@keyframes slideIn" "$template"; then
            log_success "    ✅ CSS动画样式已添加"
        else
            log_warning "    ⚠️ CSS动画样式未找到"
        fi
        
        # 检查文件名编码
        if grep -q "salary_analysis_report_" "$template" || grep -q "org_health_report_" "$template" || grep -q "career_tracking_report_" "$template"; then
            log_success "    ✅ 文件名编码问题已修复"
        else
            log_warning "    ⚠️ 文件名编码问题可能未完全修复"
        fi
    fi
done

# 创建部署完成报告
cat > "ALL_EXPORTS_FIX_REPORT.md" << EOF
# 所有模块导出功能修复报告

## 修复时间
$(date)

## 修复内容
- ✅ 修复了薪酬分析模块的导出功能
- ✅ 修复了组织健康度模块的导出功能
- ✅ 修复了职业发展追踪模块的导出功能
- ✅ 改进了错误处理和用户反馈
- ✅ 添加了加载状态指示
- ✅ 统一了通知系统
- ✅ 创建了综合测试脚本

## 修复原理
- 改进fetch API的错误处理
- 添加详细的错误信息提示
- 实现用户友好的通知系统
- 添加加载状态指示
- 统一文件名格式避免编码问题

## 文件修改
- \`app/templates/talent_management/hr_admin/salary_dashboard.html\`
- \`app/templates/talent_management/hr_admin/org_health_dashboard.html\`
- \`app/templates/talent_management/hr_admin/career_tracking_dashboard.html\`

## 测试方法
\`\`\`bash
python3 test_all_exports.py
\`\`\`

## 注意事项
- 需要登录系统才能使用导出功能
- 导出文件为Excel格式(.xlsx)
- 文件名使用英文避免编码问题
- 提供详细的错误信息提示
EOF

log_success "部署完成报告已创建: ALL_EXPORTS_FIX_REPORT.md"

echo ""
log_success "🎉 所有模块导出功能修复部署完成！"
echo ""
echo "📋 修复总结:"
echo "  - 薪酬分析模块：改进错误处理，添加加载状态"
echo "  - 组织健康度模块：修复导出功能，改进用户体验"
echo "  - 职业发展追踪模块：完全重写导出函数"
echo "  - 统一通知系统：用户友好的成功/失败提示"
echo "  - 文件名编码：避免Unicode问题"
echo ""
echo "🔄 如果是在云服务器上，建议:"
echo "  sudo systemctl restart llrc"
echo ""
echo "🧪 测试方法:"
echo "  python3 test_all_exports.py"
echo ""
echo "📁 备份文件保存在: $backup_dir"
echo "📄 详细报告: ALL_EXPORTS_FIX_REPORT.md"
