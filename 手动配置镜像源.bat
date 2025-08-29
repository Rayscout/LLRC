@echo off
chcp 65001 >nul
echo ========================================
echo    手动配置Python镜像源
echo ========================================
echo.

echo 正在配置清华大学镜像源...
echo.

REM 配置清华大学镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

echo ✅ 清华大学镜像源配置完成
echo.

echo 正在测试连接...
pip install --upgrade pip --no-cache-dir

if errorlevel 1 (
    echo.
    echo ❌ 清华大学镜像源连接失败
    echo 正在尝试阿里云镜像源...
    echo.
    
    REM 配置阿里云镜像源
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
    pip config set global.trusted-host mirrors.aliyun.com
    
    echo 测试阿里云镜像源连接...
    pip install --upgrade pip --no-cache-dir
    
    if errorlevel 1 (
        echo.
        echo ❌ 阿里云镜像源也连接失败
        echo 正在尝试中国科技大学镜像源...
        echo.
        
        REM 配置中国科技大学镜像源
        pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/
        pip config set global.trusted-host pypi.mirrors.ustc.edu.cn
        
        echo 测试中国科技大学镜像源连接...
        pip install --upgrade pip --no-cache-dir
        
        if errorlevel 1 (
            echo.
            echo ❌ 所有镜像源都连接失败
            echo 请检查网络连接或使用离线安装方式
            echo.
            echo 查看 离线安装说明.md 了解离线安装方法
        ) else (
            echo ✅ 中国科技大学镜像源连接成功
        )
    ) else (
        echo ✅ 阿里云镜像源连接成功
    )
) else (
    echo ✅ 清华大学镜像源连接成功
)

echo.
echo 当前pip配置：
pip config list

echo.
echo 现在可以尝试运行：一键解决虚拟环境_增强版.bat
echo.
pause
