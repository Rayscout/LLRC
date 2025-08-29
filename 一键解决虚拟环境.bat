@echo off
chcp 65001 >nul
echo ========================================
echo    智能招聘系统虚拟环境一键设置
echo ========================================
echo.

echo 正在检查系统环境...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误：未找到Python！
    echo.
    echo 解决方案：
    echo 1. 请从 https://www.python.org/downloads/ 下载并安装Python 3.8+
    echo 2. 安装时请勾选"Add Python to PATH"选项
    echo 3. 安装完成后重新运行此脚本
    echo.
    pause
    exit /b 1
)

echo ✅ Python已安装
python --version
echo.

REM 检查虚拟环境是否存在
if exist ".venv" (
    echo 发现现有虚拟环境，正在清理...
    rmdir /s /q .venv
    echo ✅ 旧虚拟环境已清理
    echo.
)

echo 正在创建新的虚拟环境...
python -m venv .venv
if errorlevel 1 (
    echo ❌ 创建虚拟环境失败！
    pause
    exit /b 1
)
echo ✅ 虚拟环境创建成功
echo.

echo 正在激活虚拟环境...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 激活虚拟环境失败！
    pause
    exit /b 1
)
echo ✅ 虚拟环境已激活
echo.

echo 正在升级pip...
python -m pip install --upgrade pip
echo ✅ pip升级完成
echo.

echo 正在安装项目依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 安装依赖失败！
    echo 请检查网络连接和requirements.txt文件
    pause
    exit /b 1
)
echo ✅ 依赖安装完成
echo.

echo ========================================
echo 🎉 虚拟环境设置完成！
echo ========================================
echo.
echo 现在您可以：
echo 1. 使用 start.bat 启动应用
echo 2. 或者手动运行：python app\run.py
echo.
echo 虚拟环境信息：
echo - 位置：%CD%\.venv
echo - 已添加到.gitignore，不会被提交到Git
echo.
pause
