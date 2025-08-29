@echo off
chcp 65001 >nul
echo ========================================
echo    下载Python离线安装包
echo ========================================
echo.

echo 此脚本需要在有网络的电脑上运行
echo 用于下载所有依赖包，然后传输到目标电脑
echo.

REM 检查是否有网络连接
echo 正在检查网络连接...
ping -n 1 pypi.org >nul 2>&1
if errorlevel 1 (
    echo ❌ 无法连接到pypi.org
    echo 请检查网络连接
    pause
    exit /b 1
)

echo ✅ 网络连接正常
echo.

REM 创建下载目录
if not exist "offline_packages" (
    mkdir offline_packages
    echo ✅ 创建下载目录：offline_packages
) else (
    echo ✅ 下载目录已存在：offline_packages
)
echo.

echo 正在下载所有依赖包...
echo 这可能需要几分钟时间，请耐心等待...
echo.

REM 下载所有依赖包
pip download -r requirements.txt -d offline_packages --index-url https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn

if errorlevel 1 (
    echo.
    echo ❌ 下载失败，尝试使用默认源...
    pip download -r requirements.txt -d offline_packages
)

if errorlevel 1 (
    echo.
    echo ❌ 下载仍然失败
    echo 请检查网络连接和requirements.txt文件
    pause
    exit /b 1
)

echo.
echo ✅ 所有依赖包下载完成！
echo.

REM 显示下载的文件
echo 下载的文件列表：
dir offline_packages /b

echo.
echo ========================================
echo 🎉 离线安装包准备完成！
echo ========================================
echo.
echo 下一步操作：
echo 1. 将整个 offline_packages 文件夹复制到目标电脑
echo 2. 在目标电脑上运行：离线安装.bat
echo.
pause
