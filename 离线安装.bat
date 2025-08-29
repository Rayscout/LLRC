@echo off
chcp 65001 >nul
echo ========================================
echo    Python依赖包离线安装
echo ========================================
echo.

REM 检查虚拟环境是否存在
if not exist ".venv" (
    echo ❌ 虚拟环境不存在！
    echo 请先运行：setup_venv.bat
    pause
    exit /b 1
)

REM 检查离线安装包是否存在
if not exist "offline_packages" (
    echo ❌ 离线安装包目录不存在！
    echo.
    echo 解决方案：
    echo 1. 在有网络的电脑上运行：下载离线安装包.bat
    echo 2. 将 offline_packages 文件夹复制到此电脑
    echo 3. 重新运行此脚本
    echo.
    pause
    exit /b 1
)

echo ✅ 虚拟环境已存在
echo ✅ 离线安装包已准备
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

echo 正在从离线包安装依赖...
echo 这可能需要几分钟时间，请耐心等待...
echo.

REM 从离线包安装依赖
pip install --no-index --find-links offline_packages -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ 离线安装失败！
    echo.
    echo 可能的原因：
    echo 1. 离线包不完整
    echo 2. 虚拟环境有问题
    echo 3. requirements.txt文件有误
    echo.
    echo 建议：
    echo 1. 重新下载离线安装包
    echo 2. 或者尝试在线安装（如果网络允许）
    pause
    exit /b 1
)

echo.
echo ✅ 所有依赖安装完成！
echo.

echo ========================================
echo 🎉 离线安装成功！
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
