# LLRC 应用程序使用指南

## 环境设置

在运行应用程序之前，您需要设置Google Gemini API密钥。有三种方法：

### 方法1：PowerShell脚本（推荐）

```powershell
cd C:\Users\86199\Desktop\LLRC
.\set_env.ps1
```

脚本会提示您输入API密钥，并自动设置所有必需的环境变量。

### 方法2：批处理文件

```cmd
cd C:\Users\86199\Desktop\LLRC
quick_setup.bat
```

批处理文件会提示您输入API密钥，然后自动启动应用程序。

### 方法3：手动设置

```powershell
cd C:\Users\86199\Desktop\LLRC
$env:GOOGLE_API_KEY = '您的API密钥'
$env:GEMINI_MODEL = 'gemini-1.5-flash'
$env:GEMINI_API_KEY = $env:GOOGLE_API_KEY
python .\run.py
```

## 应用程序功能

### 员工反馈管理

访问地址：`http://127.0.0.1:5000/talent/employee_management/feedback/`

#### 新增功能

1. **反馈总结模块**
   - 点击"生成总结"按钮
   - AI会分析员工收到的所有反馈
   - 显示关键主题、优势、改进领域和建议

2. **课程学习建议模块**
   - 点击"获取推荐"按钮
   - 基于反馈分析结果推荐相关课程
   - 显示课程详细信息和推荐理由
   - 点击课程标题可跳转到学习平台

#### 现有功能

- 查看收到的反馈
- 发送反馈给高管
- 查看发送的历史反馈
- 反馈统计信息

## 故障排除

### 常见问题

1. **API密钥错误**
   ```
   Gemini HTTP 400: Invalid value at 'safety_settings[3].category'
   ```
   **解决方案**: 重新运行环境设置脚本，API密钥已自动修复。

2. **连接失败**
   ```
   Failed to establish a new connection
   ```
   **解决方案**: 确保API密钥正确设置且网络连接正常。

3. **本地分析模式**
   如果AI服务不可用，系统会自动回退到本地分析模式。

### 验证设置

运行以下PowerShell命令验证环境变量：

```powershell
Write-Host "GOOGLE_API_KEY: $($env:GOOGLE_API_KEY ? '已设置' : '未设置')"
Write-Host "GEMINI_MODEL: $env:GEMINI_MODEL"
Write-Host "GEMINI_API_KEY: $($env:GEMINI_API_KEY ? '已设置' : '未设置')"
```

## 技术支持

如果遇到问题，请检查：
1. API密钥是否正确设置
2. 网络连接是否正常
3. Google Gemini API服务是否可用

## 更新日志

### v1.0
- 新增反馈总结AI分析功能
- 新增课程推荐功能
- 新增32门优质课程数据库
- 修复Gemini API安全设置问题
- 优化环境变量设置流程
