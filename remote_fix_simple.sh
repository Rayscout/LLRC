#!/bin/bash
# 简化版远程修复脚本
# 不依赖expect，直接使用SSH命令

set -e

# 配置信息
SERVER_IP="60.205.251.52"
USERNAME="llrcuser"
PROJECT_DIR="/var/www/llrc"

echo "🚀 开始远程修复LLRC认证问题..."
echo "服务器: ${USERNAME}@${SERVER_IP}"
echo "项目目录: ${PROJECT_DIR}"
echo "============================================================"

# 函数：执行SSH命令
execute_ssh_command() {
    local command="$1"
    local description="$2"
    
    echo "🔧 $description"
    echo "   执行: $command"
    echo "   请在SSH会话中手动执行上述命令"
    echo ""
}

# 函数：上传文件到服务器
upload_file() {
    local local_file="$1"
    local remote_file="$2"
    
    echo "📤 上传文件: $local_file -> $remote_file"
    echo "   执行: scp $local_file ${USERNAME}@${SERVER_IP}:$remote_file"
    echo "   请在SSH会话中手动执行上述命令"
    echo ""
}

# 主函数
main() {
    echo "🎯 开始执行完整的远程修复流程..."
    echo "时间: $(date)"
    echo "============================================================"
    
    # 检查必要文件
    if [[ ! -f "diagnose_auth_issues.py" ]] || [[ ! -f "fix_auth_issues.py" ]]; then
        echo "❌ 错误：缺少必要的脚本文件"
        echo "请确保以下文件存在："
        echo "  - diagnose_auth_issues.py"
        echo "  - fix_auth_issues.py"
        exit 1
    fi
    
    echo "📋 第一步：连接到远程服务器"
    echo "执行: ssh ${USERNAME}@${SERVER_IP}"
    echo ""
    
    echo "📋 第二步：上传修复脚本到服务器"
    upload_file "diagnose_auth_issues.py" "${PROJECT_DIR}/"
    upload_file "fix_auth_issues.py" "${PROJECT_DIR}/"
    
    echo "📋 第三步：执行修复操作"
    execute_ssh_command "cd ${PROJECT_DIR} && chmod +x diagnose_auth_issues.py fix_auth_issues.py" "设置脚本执行权限"
    
    echo "📋 第四步：运行诊断脚本"
    execute_ssh_command "cd ${PROJECT_DIR} && python3 diagnose_auth_issues.py" "运行认证问题诊断"
    
    echo "📋 第五步：运行修复脚本"
    execute_ssh_command "cd ${PROJECT_DIR} && python3 fix_auth_issues.py" "运行认证问题修复"
    
    echo "📋 第六步：检查服务状态"
    execute_ssh_command "sudo systemctl status llrc --no-pager" "检查LLRC服务状态"
    execute_ssh_command "sudo systemctl status mongod --no-pager" "检查MongoDB服务状态"
    execute_ssh_command "sudo systemctl status nginx --no-pager" "检查Nginx服务状态"
    
    echo "📋 第七步：测试修复结果"
    execute_ssh_command "curl -s http://localhost/health" "测试健康检查"
    execute_ssh_command "curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign" "测试注册页面"
    
    echo "📋 第八步：分支管理"
    echo "在SSH会话中执行以下命令："
    echo ""
    echo "1. 检查Git状态："
    execute_ssh_command "cd ${PROJECT_DIR} && git status" "检查Git状态"
    execute_ssh_command "cd ${PROJECT_DIR} && git branch -a" "查看所有分支"
    
    echo "2. 切换到pxy分支并提交修复："
    execute_ssh_command "cd ${PROJECT_DIR} && git checkout pxy" "切换到pxy分支"
    execute_ssh_command "cd ${PROJECT_DIR} && git pull origin pxy" "拉取pxy分支最新代码"
    execute_ssh_command "cd ${PROJECT_DIR} && git add ." "添加所有更改"
    execute_ssh_command "cd ${PROJECT_DIR} && git commit -m '修复认证问题：添加诊断和修复脚本'" "提交修复更改"
    execute_ssh_command "cd ${PROJECT_DIR} && git push origin pxy" "推送修复到pxy分支"
    
    echo "3. 合并到RayScout分支："
    execute_ssh_command "cd ${PROJECT_DIR} && git checkout RayScout" "切换到RayScout分支"
    execute_ssh_command "cd ${PROJECT_DIR} && git pull origin RayScout" "拉取RayScout分支最新代码"
    execute_ssh_command "cd ${PROJECT_DIR} && git merge pxy" "合并pxy分支到RayScout"
    execute_ssh_command "cd ${PROJECT_DIR} && git push origin RayScout" "推送合并结果到RayScout分支"
    execute_ssh_command "cd ${PROJECT_DIR} && git checkout pxy" "切换回pxy分支"
    
    echo "📋 第九步：最终验证"
    execute_ssh_command "sudo systemctl is-active llrc" "验证LLRC服务状态"
    execute_ssh_command "sudo systemctl is-active mongod" "验证MongoDB服务状态"
    execute_ssh_command "sudo systemctl is-active nginx" "验证Nginx服务状态"
    execute_ssh_command "sudo netstat -tlnp | grep -E ':(80|5000|27017)'" "验证端口监听状态"
    execute_ssh_command "curl -s http://localhost/health" "验证健康检查"
    execute_ssh_command "curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign" "验证注册页面"
    
    echo "📋 第十步：验证数据库和表情识别"
    execute_ssh_command "cd ${PROJECT_DIR} && python3 -c \"import pymongo; client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000); client.server_info(); print('✅ MongoDB连接正常')\"" "验证MongoDB连接"
    execute_ssh_command "cd ${PROJECT_DIR} && python3 -c \"from smartrecruit_system.candidate_module.emotion_recognition import get_emotion_recognition_ai; ai = get_emotion_recognition_ai(); print('✅ 表情识别模块正常')\"" "验证表情识别模块"
    
    echo ""
    echo "🎉 所有操作步骤已列出！"
    echo "============================================================"
    echo "📋 操作总结："
    echo "  ✅ 认证问题诊断和修复"
    echo "  ✅ 服务状态检查和修复"
    echo "  ✅ 代码提交到pxy分支"
    echo "  ✅ 合并pxy分支到RayScout分支"
    echo "  ✅ 最终功能验证"
    echo ""
    echo "🌐 修复完成后，可以访问以下地址测试："
    echo "  - 主页: http://60.205.251.52"
    echo "  - 注册页面: http://60.205.251.52/auth/sign"
    echo "  - 健康检查: http://60.205.251.52/health"
    echo ""
    echo "📞 如果仍有问题，请运行："
    echo "  ssh ${USERNAME}@${SERVER_IP}"
    echo "  cd ${PROJECT_DIR}"
    echo "  python3 diagnose_auth_issues.py"
}

# 执行主函数
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main
fi
