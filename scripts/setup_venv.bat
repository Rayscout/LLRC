REM FILE-HEADER-AUTO-ADDED
REM 文件: scripts/setup_venv.bat
REM 功能: 通用模块
REM 创建时间: 2025-08-27 18:38
REM 创建人: 李雨梦
REM 更新记录:
REM - 2025-08-20 17:37 by 侯东杨
REM - 2025-08-27 12:19 by 张宇成
REM - 2025-09-01 12:26 by 苏杰
@echo off
echo 正在设置智能招聘系统虚拟环境...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python！
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 显示Python版本
echo Python版本：
python --version
echo.

REM 删除旧的虚拟环境（如果存在）
if exist ".venv" (
    echo 删除旧的虚拟环境...
    rmdir /s /q .venv
)

REM 创建新的虚拟环境
echo 创建新的虚拟环境...
python -m venv .venv

REM 激活虚拟环境
echo 激活虚拟环境...
call .venv\Scripts\activate.bat

REM 升级pip
echo 升级pip...
python -m pip install --upgrade pip

REM 安装依赖
echo 安装项目依赖...
pip install -r requirements.txt

echo.
echo 虚拟环境设置完成！
echo 现在可以使用 start.bat 启动应用
echo.
pause
