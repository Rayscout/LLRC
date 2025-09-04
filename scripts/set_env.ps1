<#
FILE-HEADER-AUTO-ADDED
文件: scripts/set_env.ps1
功能: 通用模块
创建时间: 2025-08-29 15:09
创建人: 侯东杨
更新记录:
- 2025-08-23 17:30 by 张宇成
- 2025-08-26 11:51 by 潘显雨
#>
# 设置LLRC应用程序的环境变量
# 使用方法: .\set_env.ps1

Write-Host "设置LLRC应用程序环境变量..." -ForegroundColor Green

# 设置Google Gemini API密钥
Write-Host "请输入您的Google Gemini API密钥：" -ForegroundColor Yellow
$apiKey = Read-Host -AsSecureString

# 将安全字符串转换为普通字符串
$env:GOOGLE_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($apiKey))

# 或者直接输入（不隐藏）
# $env:GOOGLE_API_KEY = Read-Host "请输入您的Google Gemini API密钥"

$env:GEMINI_MODEL = 'gemini-1.5-flash'  # 使用更稳定的模型
$env:GEMINI_API_KEY = $env:GOOGLE_API_KEY

# 持久化设置到当前会话
[System.Environment]::SetEnvironmentVariable('GOOGLE_API_KEY', $env:GOOGLE_API_KEY, [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable('GEMINI_MODEL', $env:GEMINI_MODEL, [System.EnvironmentVariableTarget]::Process)
[System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', $env:GEMINI_API_KEY, [System.EnvironmentVariableTarget]::Process)

# 验证设置
Write-Host "环境变量设置完成：" -ForegroundColor Yellow
$keyMasked = if($env:GOOGLE_API_KEY){$env:GOOGLE_API_KEY.Substring(0, [Math]::Min(10, $env:GOOGLE_API_KEY.Length)) + "..."}else{"未设置"}
Write-Host "GOOGLE_API_KEY: $keyMasked" -ForegroundColor $(if($env:GOOGLE_API_KEY){'Green'}else{'Red'})
Write-Host "GEMINI_MODEL: $($env:GEMINI_MODEL ? $env:GEMINI_MODEL : '未设置')" -ForegroundColor $(if($env:GEMINI_MODEL){'Green'}else{'Red'})
Write-Host "GEMINI_API_KEY: $(if($env:GEMINI_API_KEY){'已设置'}else{'未设置'})" -ForegroundColor $(if($env:GEMINI_API_KEY){'Green'}else{'Red'})

Write-Host ""
Write-Host "现在可以运行应用程序了：" -ForegroundColor Cyan
Write-Host "python .\run.py"
Write-Host ""

# 提供一键运行选项
$response = Read-Host "是否要立即启动应用程序？(y/n)"
if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "启动应用程序..." -ForegroundColor Green
    python .\run.py
}
