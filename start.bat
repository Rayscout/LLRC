@echo off
echo 正在启动智能招聘系统...
echo.

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat

REM 安装依赖（如果需要）
echo 检查并安装依赖...
pip install -r requirements_simple.txt

REM 启动应用
echo 启动应用...
python run.py

pause

