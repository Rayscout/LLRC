@echo off
REM LLRC 环境变量快速设置脚本
REM 使用方法: 双击此文件或在命令行中运行

echo 设置LLRC应用程序环境变量...
echo.

REM 设置控制台编码为UTF-8
chcp 65001 >nul

echo 请输入您的Google Gemini API密钥：
set /p GOOGLE_API_KEY="API密钥: "

if "%GOOGLE_API_KEY%"=="" (
    echo 错误：API密钥不能为空！
    pause
    exit /b 1
)

REM 设置环境变量
set GEMINI_MODEL=gemini-1.5-flash
set GEMINI_API_KEY=%GOOGLE_API_KEY%

echo.
echo 环境变量设置完成：
echo GOOGLE_API_KEY: %GOOGLE_API_KEY:~0,10%...
echo GEMINI_MODEL: %GEMINI_MODEL%
echo GEMINI_API_KEY: 已设置
echo.

echo 启动应用程序...
python run.py

pause
