# 智能招聘系统虚拟环境设置脚本
Write-Host "正在设置智能招聘系统虚拟环境..." -ForegroundColor Green
Write-Host ""

# 检查Python是否安装
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "错误：未找到Python！" -ForegroundColor Red
    Write-Host "请先安装Python 3.8或更高版本" -ForegroundColor Yellow
    Read-Host "按回车键退出"
    exit 1
}

Write-Host ""

# 删除旧的虚拟环境（如果存在）
if (Test-Path ".venv") {
    Write-Host "删除旧的虚拟环境..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force ".venv"
}

# 创建新的虚拟环境
Write-Host "创建新的虚拟环境..." -ForegroundColor Yellow
python -m venv .venv

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

# 升级pip
Write-Host "升级pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# 安装依赖
Write-Host "安装项目依赖..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "虚拟环境设置完成！" -ForegroundColor Green
Write-Host "现在可以使用 start.ps1 启动应用" -ForegroundColor Cyan
Write-Host ""
Read-Host "按回车键退出"
