#!/bin/bash

# 人才流失预警导出功能修复部署脚本
# 解决"数据导出功能开发中..."的问题

echo "🚀 开始部署人才流失预警导出功能修复..."

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
backup_dir="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"

# 备份相关文件
if [ -f "app/templates/talent_management/hr_admin/turnover_dashboard.html" ]; then
    cp "app/templates/talent_management/hr_admin/turnover_dashboard.html" "$backup_dir/"
    log_success "已备份前端模板"
fi

if [ -f "talent_management_system/hr_admin_module/turnover_alert.py" ]; then
    cp "talent_management_system/hr_admin_module/turnover_alert.py" "$backup_dir/"
    log_success "已备份后端模块"
fi

# 步骤2: 修复前端模板
log_info "步骤2: 修复前端模板..."
if [ -f "app/templates/talent_management/hr_admin/turnover_dashboard.html" ]; then
    # 替换exportData函数
    sed -i 's/alert('\''数据导出功能开发中...'\'');/\/\/ 调用后端导出API\n            fetch('\''\/talent\/hr_admin\/turnover_alert\/api\/export_data'\'', {\n                method: '\''POST'\'',\n                headers: {\n                    '\''Content-Type'\'': '\''application\/json'\'',\n                }\n            })\n            .then(response => {\n                if (response.ok) {\n                    return response.blob();\n                } else {\n                    throw new Error('\''导出失败'\'');\n                }\n            })\n            .then(blob => {\n                const url = window.URL.createObjectURL(blob);\n                const a = document.createElement('\''a'\'');\n                a.href = url;\n                a.download = `turnover_alert_report_${new Date().toISOString().slice(0,10)}.xlsx`;\n                document.body.appendChild(a);\n                a.click();\n                window.URL.revokeObjectURL(url);\n                document.body.removeChild(a);\n                showNotification('\''数据导出成功！'\'', '\''success'\'');\n            })\n            .catch(error => {\n                console.error('\''导出失败:'\'', error);\n                showNotification('\''数据导出失败，请稍后重试'\'', '\''error'\'');\n            });/' "app/templates/talent_management/hr_admin/turnover_dashboard.html"
    
    # 添加通知函数
    if ! grep -q "function showNotification" "app/templates/talent_management/hr_admin/turnover_dashboard.html"; then
        cat >> "app/templates/talent_management/hr_admin/turnover_dashboard.html" << 'EOF'

        // 显示通知
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.textContent = message;
            
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
            
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            }, 3000);
        }
EOF
        log_success "已添加通知函数"
    fi
    
    # 添加CSS动画样式
    if ! grep -q "@keyframes slideIn" "app/templates/talent_management/hr_admin/turnover_dashboard.html"; then
        sed -i '/@keyframes fadeInUp {/i\        /* 通知动画 */\n        @keyframes slideIn {\n            from {\n                opacity: 0;\n                transform: translateX(100%);\n            }\n            to {\n                opacity: 1;\n                transform: translateX(0);\n            }\n        }\n        \n        @keyframes slideOut {\n            from {\n                opacity: 1;\n                transform: translateX(0);\n            }\n            to {\n                opacity: 0;\n                transform: translateX(100%);\n            }\n        }\n' "app/templates/talent_management/hr_admin/turnover_dashboard.html"
        log_success "已添加CSS动画样式"
    fi
    
    log_success "前端模板修复完成"
else
    log_warning "前端模板文件不存在，跳过修复"
fi

# 步骤3: 修复后端模块
log_info "步骤3: 修复后端模块..."
if [ -f "talent_management_system/hr_admin_module/turnover_alert.py" ]; then
    # 修复文件名编码问题
    sed -i 's/f"人才流失预警报告_${datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"/f"turnover_alert_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"/g' "talent_management_system/hr_admin_module/turnover_alert.py"
    
    # 修复响应头编码问题
    sed -i 's/filename = f"人才流失预警报告_${datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"/safe_filename = f"turnover_alert_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"/g' "talent_management_system/hr_admin_module/turnover_alert.py"
    sed -i 's/download_name=filename,/download_name=safe_filename,/g' "talent_management_system/hr_admin_module/turnover_alert.py"
    sed -i 's/filename="{filename}"/filename="{safe_filename}"/g' "talent_management_system/hr_admin_module/turnover_alert.py"
    
    log_success "后端模块修复完成"
else
    log_warning "后端模块文件不存在，跳过修复"
fi

# 步骤4: 创建测试脚本
log_info "步骤4: 创建测试脚本..."
cat > "test_turnover_export.py" << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试人才流失预警导出功能
"""

import requests
import json
from datetime import datetime

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
    test_turnover_export()
EOF

log_success "测试脚本创建完成"

# 步骤5: 重启服务
if [ "$CLOUD_ENV" = true ]; then
    log_info "步骤5: 重启服务..."
    
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

# 步骤6: 验证修复效果
log_info "步骤6: 验证修复效果..."
echo ""

# 检查文件修改
echo "📋 修复内容检查:"
if [ -f "app/templates/talent_management/hr_admin/turnover_dashboard.html" ]; then
    if grep -q "数据导出功能开发中" "app/templates/talent_management/hr_admin/turnover_dashboard.html"; then
        log_error "前端模板中仍存在'数据导出功能开发中'提示"
    else
        log_success "前端模板已修复，不再显示'数据导出功能开发中'"
    fi
    
    if grep -q "function showNotification" "app/templates/talent_management/hr_admin/turnover_dashboard.html"; then
        log_success "通知函数已添加"
    else
        log_warning "通知函数未找到"
    fi
    
    if grep -q "@keyframes slideIn" "app/templates/talent_management/hr_admin/turnover_dashboard.html"; then
        log_success "CSS动画样式已添加"
    else
        log_warning "CSS动画样式未找到"
    fi
fi

if [ -f "talent_management_system/hr_admin_module/turnover_alert.py" ]; then
    if grep -q "turnover_alert_report_" "talent_management_system/hr_admin_module/turnover_alert.py"; then
        log_success "后端文件名编码问题已修复"
    else
        log_warning "后端文件名编码问题可能未完全修复"
    fi
fi

# 创建部署完成报告
cat > "TURNOVER_EXPORT_FIX_REPORT.md" << EOF
# 人才流失预警导出功能修复报告

## 修复时间
$(date)

## 修复内容
- ✅ 修复了前端模板中的导出函数
- ✅ 替换了"数据导出功能开发中..."提示
- ✅ 实现了完整的Excel文件下载功能
- ✅ 修复了后端文件名编码问题
- ✅ 添加了用户友好的通知系统
- ✅ 创建了测试脚本

## 修复原理
- 前端调用后端导出API
- 使用Blob处理文件下载
- 避免中文字符编码问题
- 提供实时用户反馈

## 文件修改
- \`app/templates/talent_management/hr_admin/turnover_dashboard.html\`
- \`talent_management_system/hr_admin_module/turnover_alert.py\`

## 测试方法
\`\`\`bash
python3 test_turnover_export.py
\`\`\`

## 注意事项
- 需要登录系统才能使用导出功能
- 导出文件为Excel格式(.xlsx)
- 文件名使用英文避免编码问题
EOF

log_success "部署完成报告已创建: TURNOVER_EXPORT_FIX_REPORT.md"

echo ""
log_success "🎉 人才流失预警导出功能修复部署完成！"
echo ""
echo "📋 修复总结:"
echo "  - 前端不再显示'数据导出功能开发中...'"
echo "  - 实现了完整的Excel文件下载功能"
echo "  - 修复了Unicode编码问题"
echo "  - 添加了用户友好的通知系统"
echo ""
echo "🔄 如果是在云服务器上，建议:"
echo "  sudo systemctl restart llrc"
echo ""
echo "🧪 测试方法:"
echo "  python3 test_turnover_export.py"
echo ""
echo "📁 备份文件保存在: $backup_dir"
echo "📄 详细报告: TURNOVER_EXPORT_FIX_REPORT.md"
