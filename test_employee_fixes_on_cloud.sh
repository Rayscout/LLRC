#!/bin/bash

# 员工模块修复云服务器测试脚本
# 用于在云服务器上快速测试修复效果

echo "=== 员工模块修复云服务器测试脚本 ==="
echo "开始时间: $(date)"
echo

# 1. 备份当前代码
echo "1. 备份当前代码..."
BACKUP_DIR="/tmp/llrc_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r . "$BACKUP_DIR/"
echo "✓ 代码已备份到: $BACKUP_DIR"

# 2. 切换到pxy分支并拉取最新代码
echo "2. 切换到pxy分支并拉取最新代码..."
git stash
git checkout pxy
git pull origin pxy
echo "✓ 已切换到pxy分支并拉取最新代码"

# 3. 检查修复的文件
echo "3. 检查修复的文件..."
FIXED_FILES=(
    "talent_management_system/employee_manager_module/feedback.py"
    "talent_management_system/employee_manager_module/profile.py"
    "talent_management_system/employee_manager_module/performance.py"
    "talent_management_system/tools/test_employee_module_fixes.py"
)

for file in "${FIXED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file 存在"
    else
        echo "✗ $file 不存在"
    fi
done

# 4. 重启应用服务
echo "4. 重启应用服务..."
if systemctl is-active --quiet llrc; then
    echo "停止llrc服务..."
    sudo systemctl stop llrc
fi

echo "启动llrc服务..."
sudo systemctl start llrc

# 等待服务启动
sleep 5

# 检查服务状态
if systemctl is-active --quiet llrc; then
    echo "✓ llrc服务已启动"
else
    echo "✗ llrc服务启动失败"
    echo "查看服务日志:"
    sudo journalctl -u llrc -n 20
    exit 1
fi

# 5. 运行测试脚本
echo "5. 运行测试脚本..."
cd talent_management_system/tools
python3 test_employee_module_fixes.py
TEST_RESULT=$?

if [ $TEST_RESULT -eq 0 ]; then
    echo "✓ 测试脚本运行成功"
else
    echo "✗ 测试脚本运行失败"
fi

# 6. 检查应用日志
echo "6. 检查应用日志..."
echo "最近的错误日志:"
tail -n 20 ../app.log 2>/dev/null || echo "未找到app.log文件"

# 7. 提供测试指导
echo
echo "=== 测试指导 ==="
echo "请在浏览器中访问以下页面进行手动测试:"
echo "1. 反馈管理测试: http://your-domain/feedback/"
echo "   - 尝试发送反馈给高管"
echo "   - 检查是否在'已发送反馈'中显示"
echo
echo "2. PDF导出测试: http://your-domain/profile/"
echo "   - 点击'导出PDF简历'"
echo "   - 检查PDF是否正常生成和下载"
echo
echo "3. 绩效历史测试: http://your-domain/performance/history"
echo "   - 检查页面是否正常加载"
echo "   - 检查历史记录是否显示"
echo
echo "如果发现问题，请检查以下日志文件:"
echo "- 应用日志: tail -f app.log"
echo "- 系统日志: sudo journalctl -u llrc -f"
echo "- Nginx日志: sudo tail -f /var/log/nginx/error.log"
echo
echo "测试完成后，如需回滚:"
echo "git checkout RayScout"
echo "sudo systemctl restart llrc"
echo
echo "脚本执行完成时间: $(date)"
