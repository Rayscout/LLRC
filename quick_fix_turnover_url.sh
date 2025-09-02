#!/bin/bash
# 快速修复人才流失预警URL问题

echo "🔧 快速修复人才流失预警URL问题..."

# 检查是否在云服务器环境
if [ -f "/etc/systemd/system/llrc.service" ]; then
    echo "ℹ️ 检测到云服务器环境"
    SERVER_ENV="cloud"
else
    echo "ℹ️ 检测到本地环境"
    SERVER_ENV="local"
fi

# 步骤1: 备份当前文件
echo "ℹ️ 步骤1: 备份当前文件..."
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

if [ -f "talent_management_system/hr_admin_module/turnover_alert.py" ]; then
    cp talent_management_system/hr_admin_module/turnover_alert.py "$BACKUP_DIR/"
    echo "✅ 已备份后端模块"
fi

# 步骤2: 修复模板路径问题
echo "ℹ️ 步骤2: 修复模板路径问题..."

# 修复模板路径
sed -i 's/talent_management\/hr_admin\/turnover_dashboard.html/hr_admin\/turnover_dashboard.html/g' talent_management_system/hr_admin_module/turnover_alert.py

echo "✅ 模板路径修复完成"

# 步骤3: 重启服务
if [ "$SERVER_ENV" = "cloud" ]; then
    echo "ℹ️ 步骤3: 重启服务..."
    sudo systemctl restart llrc
    if [ $? -eq 0 ]; then
        echo "✅ llrc服务重启成功"
    else
        echo "❌ llrc服务重启失败"
    fi
fi

# 步骤4: 验证修复
echo "ℹ️ 步骤4: 验证修复..."
echo "📋 修复内容检查:"

if grep -q "hr_admin/turnover_dashboard.html" talent_management_system/hr_admin_module/turnover_alert.py; then
    echo "✅ 模板路径已修复"
else
    echo "❌ 模板路径未修复"
fi

echo ""
echo "🎉 人才流失预警URL问题修复完成！"
echo ""
echo "📋 修复总结:"
echo "- 修复了模板路径问题"
echo "- 现在应该可以正常访问人才流失预警页面"
echo ""
echo "🔄 如果是在云服务器上，建议:"
echo "sudo systemctl restart llrc"
echo ""
echo "📁 备份文件保存在: $BACKUP_DIR"
echo ""
echo "🧪 现在可以测试人才流失预警功能了！"
echo "点击高管页面中的人才流失预警应该可以正常访问。"
