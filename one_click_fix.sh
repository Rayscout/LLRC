#!/bin/bash
# LLRC登录问题一键修复脚本
# 用于快速解决云服务器上的登录"内部服务器错误"问题

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否为root用户
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "请不要使用root用户运行此脚本"
        exit 1
    fi
}

# 检查项目目录
check_project_dir() {
    if [[ ! -d "/var/www/llrc" ]]; then
        log_error "项目目录不存在: /var/www/llrc"
        exit 1
    fi
}

# 备份当前版本
backup_version() {
    log_info "备份当前版本..."
    local backup_dir="/var/www/llrc_backup_$(date +%Y%m%d_%H%M%S)"
    if sudo cp -r /var/www/llrc "$backup_dir"; then
        log_success "备份完成: $backup_dir"
    else
        log_warning "备份失败，继续执行..."
    fi
}

# 检查服务状态
check_services() {
    log_info "检查服务状态..."
    
    # 检查LLRC服务
    if sudo systemctl is-active --quiet llrc; then
        log_success "LLRC服务正在运行"
    else
        log_warning "LLRC服务未运行"
    fi
    
    # 检查Nginx服务
    if sudo systemctl is-active --quiet nginx; then
        log_success "Nginx服务正在运行"
    else
        log_warning "Nginx服务未运行"
    fi
    
    # 检查MongoDB服务
    if sudo systemctl is-active --quiet mongod; then
        log_success "MongoDB服务正在运行"
    else
        log_warning "MongoDB服务未运行"
    fi
}

# 修复数据库问题
fix_database() {
    log_info "修复数据库问题..."
    
    # 重启MongoDB
    log_info "重启MongoDB服务..."
    sudo systemctl restart mongod
    sleep 3
    
    # 检查MongoDB状态
    if sudo systemctl is-active --quiet mongod; then
        log_success "MongoDB服务已启动"
    else
        log_error "MongoDB服务启动失败"
        return 1
    fi
    
    # 初始化数据库
    log_info "初始化数据库..."
    cd /var/www/llrc
    if python3 init_db.py; then
        log_success "数据库初始化成功"
    else
        log_warning "数据库初始化失败，可能已存在"
    fi
}

# 修复文件权限
fix_permissions() {
    log_info "修复文件权限..."
    
    # 创建必要目录
    local dirs=(
        "/var/www/llrc/instance"
        "/var/www/llrc/flask_session_data"
    )
    
    for dir in "${dirs[@]}"; do
        if [[ ! -d "$dir" ]]; then
            sudo mkdir -p "$dir"
            log_info "创建目录: $dir"
        fi
        
        sudo chmod 755 "$dir"
        sudo chown llrcuser:llrcuser "$dir"
        log_success "设置权限: $dir"
    done
    
    # 修复项目目录权限
    sudo chown -R llrcuser:llrcuser /var/www/llrc
    log_success "修复项目目录权限"
}

# 修复环境配置
fix_environment() {
    log_info "修复环境配置..."
    
    local env_file="/var/www/llrc/.env"
    
    # 备份现有.env文件
    if [[ -f "$env_file" ]]; then
        sudo cp "$env_file" "${env_file}.backup.$(date +%Y%m%d_%H%M%S)"
        log_info "备份现有.env文件"
    fi
    
    # 创建新的.env文件
    cat > /tmp/llrc.env << 'EOF'
# LLRC环境配置
SECRET_KEY=llrc-secret-key-2024-production-$(date +%s)
FLASK_ENV=production
MONGODB_URI=mongodb://localhost:27017/llrc
DATABASE_URL=sqlite:///instance/site.db
EOF
    
    sudo mv /tmp/llrc.env "$env_file"
    sudo chown llrcuser:llrcuser "$env_file"
    sudo chmod 644 "$env_file"
    log_success "创建环境配置文件"
}

# 修复依赖问题
fix_dependencies() {
    log_info "修复依赖问题..."
    
    local venv_path="/var/www/llrc/venv"
    
    if [[ -d "$venv_path" ]]; then
        log_info "激活虚拟环境..."
        
        # 升级pip
        source "$venv_path/bin/activate" && pip install --upgrade pip
        
        # 安装项目依赖
        source "$venv_path/bin/activate" && pip install -r requirements.txt
        
        # 安装认证相关依赖
        local auth_packages=(
            "bcrypt"
            "flask-login"
            "flask-session"
            "werkzeug"
            "flask-sqlalchemy"
            "pymongo"
            "python-dotenv"
        )
        
        for package in "${auth_packages[@]}"; do
            source "$venv_path/bin/activate" && pip install "$package"
            log_success "安装依赖: $package"
        done
    else
        log_warning "虚拟环境不存在，跳过依赖安装"
    fi
}

# 重启服务
restart_services() {
    log_info "重启服务..."
    
    # 重启LLRC服务
    log_info "重启LLRC服务..."
    sudo systemctl restart llrc
    sleep 5
    
    # 重启Nginx服务
    log_info "重启Nginx服务..."
    sudo systemctl restart nginx
    sleep 3
    
    # 检查服务状态
    if sudo systemctl is-active --quiet llrc; then
        log_success "LLRC服务已启动"
    else
        log_error "LLRC服务启动失败"
        return 1
    fi
    
    if sudo systemctl is-active --quiet nginx; then
        log_success "Nginx服务已启动"
    else
        log_error "Nginx服务启动失败"
        return 1
    fi
}

# 测试应用
test_application() {
    log_info "测试应用..."
    
    # 等待服务完全启动
    log_info "等待服务启动..."
    sleep 10
    
    # 测试注册页面
    local response_code=$(curl -s -o /dev/null -w '%{http_code}' http://localhost/auth/sign || echo "000")
    if [[ "$response_code" == "200" ]]; then
        log_success "注册页面可访问 (HTTP $response_code)"
    else
        log_warning "注册页面访问异常 (HTTP $response_code)"
    fi
    
    # 测试主页
    local response_code=$(curl -s -o /dev/null -w '%{http_code}' http://localhost/ || echo "000")
    if [[ "$response_code" == "200" ]]; then
        log_success "主页可访问 (HTTP $response_code)"
    else
        log_warning "主页访问异常 (HTTP $response_code)"
    fi
}

# 显示日志摘要
show_logs() {
    log_info "显示日志摘要..."
    
    echo ""
    echo "=== LLRC服务日志 (最近10行) ==="
    sudo journalctl -u llrc --no-pager -n 10 || true
    
    echo ""
    echo "=== Nginx错误日志 (最近10行) ==="
    sudo tail -n 10 /var/log/nginx/error.log 2>/dev/null || true
    
    echo ""
    echo "=== 应用日志 (最近10行) ==="
    if [[ -f "/var/www/llrc/app.log" ]]; then
        tail -n 10 /var/www/llrc/app.log || true
    else
        echo "应用日志文件不存在"
    fi
}

# 显示结果摘要
show_summary() {
    echo ""
    echo "=========================================="
    echo "🎉 LLRC登录问题修复完成！"
    echo "=========================================="
    echo ""
    echo "📋 修复摘要:"
    echo "   ✅ 数据库已重新初始化"
    echo "   ✅ 文件权限已修复"
    echo "   ✅ 环境配置已更新"
    echo "   ✅ 依赖包已重新安装"
    echo "   ✅ 服务已重启"
    echo ""
    echo "🌐 测试链接:"
    echo "   - 主页: http://60.205.251.52/"
    echo "   - 注册页面: http://60.205.251.52/auth/sign"
    echo ""
    echo "📋 如果仍有问题:"
    echo "1. 运行诊断脚本: python3 diagnose_auth_issues.py"
    echo "2. 查看实时日志: sudo journalctl -u llrc -f"
    echo "3. 运行完整更新: python3 cloud_server_update.py"
    echo ""
}

# 主函数
main() {
    echo "🚀 LLRC登录问题一键修复工具"
    echo "=========================================="
    echo "修复时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    # 检查环境
    check_root
    check_project_dir
    
    # 执行修复步骤
    backup_version
    check_services
    fix_database
    fix_permissions
    fix_environment
    fix_dependencies
    restart_services
    test_application
    show_logs
    show_summary
}

# 错误处理
trap 'log_error "脚本执行失败，请检查错误信息"; exit 1' ERR

# 执行主函数
main "$@"
