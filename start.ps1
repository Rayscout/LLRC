Write-Host "正在启动智能招聘系统..." -ForegroundColor Green
Write-Host ""

# 激活虚拟环境
Write-Host "激活虚拟环境..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# 安装依赖（如果需要）
Write-Host "检查并安装依赖..." -ForegroundColor Yellow
pip install -r requirements_simple.txt

# 启动应用
Write-Host "启动应用..." -ForegroundColor Yellow
python run_app.py

Read-Host "按回车键退出"

