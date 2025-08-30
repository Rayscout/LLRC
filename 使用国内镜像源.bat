@echo off
chcp 65001 >nul
echo ========================================
echo    使用国内镜像源安装依赖
echo ========================================
echo.

echo 正在配置国内镜像源...
echo.

REM 配置pip使用国内镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

echo ✅ 镜像源配置完成
echo.

echo 正在测试连接...
pip install --upgrade pip

if errorlevel 1 (
    echo ❌ 连接失败，尝试其他镜像源...
    echo.
    
    REM 尝试阿里云镜像
    echo 尝试阿里云镜像源...
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
    pip config set global.trusted-host mirrors.aliyun.com
    
    pip install --upgrade pip
) else (
    echo ✅ 连接成功
)

echo.
echo 现在可以重新运行：一键解决虚拟环境.bat
echo.
pause
