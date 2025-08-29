@echo off
chcp 65001 >nul
echo ========================================
echo    清除网络代理设置
echo ========================================
echo.

echo 正在清除系统代理设置...
echo.

REM 清除HTTP代理
set http_proxy=
set HTTP_PROXY=
set https_proxy=
set HTTPS_PROXY=

REM 清除pip代理
pip config unset global.proxy
pip config unset global.http_proxy
pip config unset global.https_proxy

echo ✅ 代理设置已清除
echo.

echo 正在测试网络连接...
echo.

REM 测试pip连接
echo 测试pip连接...
pip install --upgrade pip --index-url https://pypi.org/simple/ --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org

if errorlevel 1 (
    echo ❌ 网络连接仍有问题
    echo 请尝试方案2：使用国内镜像源
) else (
    echo ✅ 网络连接正常
    echo 现在可以重新运行：一键解决虚拟环境.bat
)

echo.
pause
