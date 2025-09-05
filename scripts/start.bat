REM FILE-HEADER-AUTO-ADDED
REM 文件: scripts/start.bat
REM 功能: 通用模块
REM 创建时间: 2025-08-21 16:54
REM 创建人: 侯东杨
REM 更新记录:
REM - 2025-09-01 12:03 by 谢佳悦
@echo off
echo 正在启动智能招聘系统...
echo.

REM 检查虚拟环境是否存在
if not exist ".venv\Scripts\activate.bat" (
    echo 错误：虚拟环境不存在！
    echo 请先创建虚拟环境：
    echo python -m venv .venv
    echo.
    pause
    exit /b 1
)

REM 激活虚拟环境
echo 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 检查Python是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：无法找到Python！
    echo 请检查虚拟环境是否正确激活
    pause
    exit /b 1
)

REM 安装依赖（如果需要）
echo 检查并安装依赖...
pip install -r requirements.txt

REM 启动应用
echo 启动应用...
python app\run.py

pause

