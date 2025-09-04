<#
FILE-HEADER-AUTO-ADDED
文件: scripts/start.ps1
功能: 通用模块
创建时间: 2025-09-03 18:02
创建人: 侯东杨
更新记录:
- 2025-08-23 18:46 by 李雨梦
#>
# 智能招聘系统启动脚本
Write-Host "正在启动智能招聘系统..." -ForegroundColor Green
Write-Host ""

# 检查虚拟环境是否存在
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "错误：虚拟环境不存在！" -ForegroundColor Red
    Write-Host "请先创建虚拟环境：" -ForegroundColor Yellow
    Write-Host "python -m venv .venv" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "按回车键退出"
    exit 1
}

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

# 检查Python是否可用
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "错误：无法找到Python！" -ForegroundColor Red
    Write-Host "请检查虚拟环境是否正确激活" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

# 安装依赖（如果需要）
Write-Host "检查并安装依赖..." -ForegroundColor Yellow
pip install -r requirements.txt

# 启动应用
Write-Host "启动应用..." -ForegroundColor Green
python app\run.py

Read-Host "按回车键退出"
