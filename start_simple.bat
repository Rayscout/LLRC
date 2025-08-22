@echo off
echo 正在启动简化的Flask应用...
echo.

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 启动简化的应用
python simple_run.py

pause
