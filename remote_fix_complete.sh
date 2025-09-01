#!/bin/bash
# 完整的远程修复脚本
# 包含SSH连接、修复操作、分支管理和部署

set -e

# 配置信息
SERVER_IP="60.205.251.52"
USERNAME="llrcuser"
PASSWORD="pxy221850"
PROJECT_DIR="/var/www/llrc"

echo "🚀 开始远程修复LLRC认证问题..."
echo "服务器: ${USERNAME}@${SERVER_IP}"
echo "项目目录: ${PROJECT_DIR}"
echo "=" * 60

# 函数：执行SSH命令
execute_ssh_command() {
    local command="$1"
    local description="$2"
    
    echo "🔧 $description"
    echo "   执行: $command"
    
    # 使用expect自动处理密码输入
    expect << EOF
    spawn ssh -o StrictHostKeyChecking=no ${USERNAME}@${SERVER_IP} "$command"
    expect {
        "password:" {
            send "${PASSWORD}\r"
            expect eof
        }
        eof
    }
EOF
}

# 函数：上传文件到服务器
upload_file() {
    local local_file="$1"
    local remote_file="$2"
    
    echo "📤 上传文件: $local_file -> $remote_file"
    expect << EOF
    spawn scp -o StrictHostKeyChecking=no "$local_file" ${USERNAME}@${SERVER_IP}:$remote_file
    expect {
        "password:" {
            send "${PASSWORD}\r"
            expect eof
        }
        eof
    }
EOF
}

# 函数：执行完整的修复流程
perform_complete_fix() {
    echo "🔄 开始执行完整修复流程..."
    
    # 1. 上传修复脚本到服务器
    echo "📤 上传修复脚本到服务器..."
    upload_file "diagnose_auth_issues.py" "${PROJECT_DIR}/"
    upload_file "fix_auth_issues.py" "${PROJECT_DIR}/"
    
    # 2. 执行修复操作
    echo "🔧 执行修复操作..."
    execute_ssh_command "cd ${PROJECT_DIR} && chmod +x diagnose_auth_issues.py fix_auth_issues.py" "设置脚本执行权限"
    
    # 3. 运行诊断脚本
    echo "🔍 运行诊断脚本..."
    execute_ssh_command "cd ${PROJECT_DIR} && python3 diagnose_auth_issues.py" "运行认证问题诊断"
    
    # 4. 运行修复脚本
    echo "🛠️ 运行修复脚本..."
    execute_ssh_command "cd ${PROJECT_DIR} && python3 fix_auth_issues.py" "运行认证问题修复"
    
    # 5. 检查服务状态
    echo "📊 检查服务状态..."
    execute_ssh_command "sudo systemctl status llrc --no-pager" "检查LLRC服务状态"
    execute_ssh_command "sudo systemctl status mongod --no-pager" "检查MongoDB服务状态"
    execute_ssh_command "sudo systemctl status nginx --no-pager" "检查Nginx服务状态"
    
    # 6. 测试修复结果
    echo "🧪 测试修复结果..."
    execute_ssh_command "curl -s http://localhost/health" "测试健康检查"
    execute_ssh_command "curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign" "测试注册页面"
}

# 函数：分支管理和合并
manage_branches() {
    echo "🌿 开始分支管理..."
    
    # 1. 检查当前分支状态
    echo "📋 检查当前分支状态..."
    execute_ssh_command "cd ${PROJECT_DIR} && git status" "检查Git状态"
    execute_ssh_command "cd ${PROJECT_DIR} && git branch -a" "查看所有分支"
    
    # 2. 确保在pxy分支上
    echo "🔄 切换到pxy分支..."
    execute_ssh_command "cd ${PROJECT_DIR} && git checkout pxy" "切换到pxy分支"
    
    # 3. 拉取最新代码
    echo "📥 拉取最新代码..."
    execute_ssh_command "cd ${PROJECT_DIR} && git pull origin pxy" "拉取pxy分支最新代码"
    
    # 4. 提交修复更改
    echo "💾 提交修复更改..."
    execute_ssh_command "cd ${PROJECT_DIR} && git add ." "添加所有更改"
    execute_ssh_command "cd ${PROJECT_DIR} && git commit -m '修复认证问题：添加诊断和修复脚本'" "提交修复更改"
    
    # 5. 推送到pxy分支
    echo "📤 推送到pxy分支..."
    execute_ssh_command "cd ${PROJECT_DIR} && git push origin pxy" "推送修复到pxy分支"
    
    # 6. 切换到RayScout分支
    echo "🔄 切换到RayScout分支..."
    execute_ssh_command "cd ${PROJECT_DIR} && git checkout RayScout" "切换到RayScout分支"
    
    # 7. 拉取RayScout分支最新代码
    echo "📥 拉取RayScout分支最新代码..."
    execute_ssh_command "cd ${PROJECT_DIR} && git pull origin RayScout" "拉取RayScout分支最新代码"
    
    # 8. 合并pxy分支到RayScout
    echo "🔀 合并pxy分支到RayScout..."
    execute_ssh_command "cd ${PROJECT_DIR} && git merge pxy" "合并pxy分支到RayScout"
    
    # 9. 推送到RayScout分支
    echo "📤 推送到RayScout分支..."
    execute_ssh_command "cd ${PROJECT_DIR} && git push origin RayScout" "推送合并结果到RayScout分支"
    
    # 10. 切换回pxy分支继续开发
    echo "🔄 切换回pxy分支..."
    execute_ssh_command "cd ${PROJECT_DIR} && git checkout pxy" "切换回pxy分支"
}

# 函数：最终验证
final_verification() {
    echo "✅ 执行最终验证..."
    
    # 1. 验证服务状态
    echo "🔍 验证服务状态..."
    execute_ssh_command "sudo systemctl is-active llrc" "验证LLRC服务状态"
    execute_ssh_command "sudo systemctl is-active mongod" "验证MongoDB服务状态"
    execute_ssh_command "sudo systemctl is-active nginx" "验证Nginx服务状态"
    
    # 2. 验证端口监听
    echo "🔍 验证端口监听..."
    execute_ssh_command "sudo netstat -tlnp | grep -E ':(80|5000|27017)'" "验证端口监听状态"
    
    # 3. 验证Web功能
    echo "🌐 验证Web功能..."
    execute_ssh_command "curl -s http://localhost/health" "验证健康检查"
    execute_ssh_command "curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign" "验证注册页面"
    
    # 4. 验证数据库连接
    echo "🗄️ 验证数据库连接..."
    execute_ssh_command "cd ${PROJECT_DIR} && python3 -c \"import pymongo; client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000); client.server_info(); print('✅ MongoDB连接正常')\"" "验证MongoDB连接"
    
    # 5. 验证表情识别功能
    echo "🤖 验证表情识别功能..."
    execute_ssh_command "cd ${PROJECT_DIR} && python3 -c \"from smartrecruit_system.candidate_module.emotion_recognition import get_emotion_recognition_ai; ai = get_emotion_recognition_ai(); print('✅ 表情识别模块正常')\"" "验证表情识别模块"
}

# 主函数
main() {
    echo "🎯 开始执行完整的远程修复流程..."
    echo "时间: $(date)"
    echo "=" * 60
    
    # 检查必要文件
    if [[ ! -f "diagnose_auth_issues.py" ]] || [[ ! -f "fix_auth_issues.py" ]]; then
        echo "❌ 错误：缺少必要的脚本文件"
        echo "请确保以下文件存在："
        echo "  - diagnose_auth_issues.py"
        echo "  - fix_auth_issues.py"
        exit 1
    fi
    
    # 执行修复流程
    perform_complete_fix
    
    # 分支管理
    manage_branches
    
    # 最终验证
    final_verification
    
    echo ""
    echo "🎉 所有操作完成！"
    echo "=" * 60
    echo "📋 完成的操作："
    echo "  ✅ 认证问题诊断和修复"
    echo "  ✅ 服务状态检查和修复"
    echo "  ✅ 代码提交到pxy分支"
    echo "  ✅ 合并pxy分支到RayScout分支"
    echo "  ✅ 最终功能验证"
    echo ""
    echo "🌐 现在可以访问以下地址测试："
    echo "  - 主页: http://60.205.251.52"
    echo "  - 注册页面: http://60.205.251.52/auth/sign"
    echo "  - 健康检查: http://60.205.251.52/health"
    echo ""
    echo "📞 如果仍有问题，请运行："
    echo "  ssh ${USERNAME}@${SERVER_IP}"
    echo "  cd ${PROJECT_DIR}"
    echo "  python3 diagnose_auth_issues.py"
}

# 检查依赖
check_dependencies() {
    echo "🔍 检查本地依赖..."
    
    if ! command -v expect &> /dev/null; then
        echo "❌ 错误：缺少expect命令"
        echo "请安装expect："
        echo "  Ubuntu/Debian: sudo apt install expect"
        echo "  CentOS/RHEL: sudo yum install expect"
        echo "  macOS: brew install expect"
        exit 1
    fi
    
    if ! command -v ssh &> /dev/null; then
        echo "❌ 错误：缺少SSH客户端"
        exit 1
    fi
    
    echo "✅ 依赖检查通过"
}

# 执行主函数
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    check_dependencies
    main
fi
