@echo off
chcp 65001 >nul
echo ========================================
echo    强力清除网络代理设置
echo ========================================
echo.

echo 正在强力清除系统代理设置...
echo.

REM 清除环境变量代理
set http_proxy=
set HTTP_PROXY=
set https_proxy=
set HTTPS_PROXY=
set ftp_proxy=
set FTP_PROXY=
set no_proxy=
set NO_PROXY=

REM 清除pip配置
echo 正在清除pip代理配置...
pip config unset global.proxy 2>nul
pip config unset global.http_proxy 2>nul
pip config unset global.https_proxy 2>nul
pip config unset global.ftp_proxy 2>nul

REM 删除pip配置文件
echo 正在删除pip配置文件...
if exist "%USERPROFILE%\pip\pip.ini" (
    del "%USERPROFILE%\pip\pip.ini"
    echo ✅ 已删除用户pip.ini
)
if exist "%APPDATA%\pip\pip.ini" (
    del "%APPDATA%\pip\pip.ini"
    echo ✅ 已删除系统pip.ini
)

REM 清除系统代理设置
echo 正在清除系统代理设置...
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /f >nul 2>&1

echo ✅ 代理设置已强力清除
echo.

echo 正在测试网络连接...
echo.

REM 测试pip连接（使用国内镜像源）
echo 测试pip连接（使用清华大学镜像源）...
pip install --upgrade pip --index-url https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.tuna.tsinghua.edu.cn --no-cache-dir

if errorlevel 1 (
    echo.
    echo ❌ 网络连接仍有问题
    echo 请尝试手动配置镜像源
    echo.
    echo 手动执行以下命令：
    echo pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
    echo pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn
) else (
    echo.
    echo ✅ 网络连接正常
    echo 现在可以重新运行：一键解决虚拟环境_增强版.bat
)

echo.
pause
