#!/bin/bash
# 调试人才流失预警报告函数注释

echo "🔍 调试人才流失预警报告函数注释..."

echo "📋 查找包含'api_generate_report'的行:"
grep -n "api_generate_report" talent_management_system/hr_admin_module/turnover_alert.py

echo ""
echo "📋 查找包含'生成'的行:"
grep -n "生成" talent_management_system/hr_admin_module/turnover_alert.py

echo ""
echo "📋 查看函数定义周围的上下文:"
grep -n "def api_generate_report" -B 2 -A 3 talent_management_system/hr_admin_module/turnover_alert.py

echo ""
echo "📋 查看整个函数:"
grep -n "def api_generate_report" -A 20 talent_management_system/hr_admin_module/turnover_alert.py | head -25

echo ""
echo "🎯 调试完成，请查看上面的输出来了解实际的函数注释格式"
