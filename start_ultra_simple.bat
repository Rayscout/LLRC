@echo off
echo 正在启动超简化的Flask应用...
echo.

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 启动超简化的应用
python ultra_simple_run.py

pause
