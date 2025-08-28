# 环境变量设置说明

本项目需要设置Google Gemini API密钥才能使用AI功能。

## 方法1：使用PowerShell脚本（推荐）

1. 打开PowerShell终端
2. 导航到项目目录：
   ```powershell
   cd C:\Users\86199\Desktop\LLRC
   ```

3. 运行设置脚本：
   ```powershell
   .\set_env.ps1
   ```

4. 根据提示输入您的Google Gemini API密钥

5. 启动应用程序：
   ```powershell
   python .\run.py
   ```

## 方法2：手动设置环境变量

如果您不想使用脚本，也可以手动设置环境变量：

1. 打开PowerShell终端
2. 导航到项目目录：
   ```powershell
   cd C:\Users\86199\Desktop\LLRC
   ```

3. 设置环境变量（将 `YOUR_API_KEY_HERE` 替换为您的实际API密钥）：
   ```powershell
   $env:GOOGLE_API_KEY = 'YOUR_API_KEY_HERE'
   $env:GEMINI_MODEL = 'gemini-1.5-flash'
   $env:GEMINI_API_KEY = $env:GOOGLE_API_KEY
   ```

4. 启动应用程序：
   ```powershell
   python .\run.py
   ```

## 注意事项

- API密钥不会保存在文件中，仅在当前PowerShell会话中有效
- 每次重新打开PowerShell都需要重新设置环境变量
- 建议使用方法1的脚本，它会提供更好的用户体验和验证

## 获取Google Gemini API密钥

1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登录Google账户
3. 创建新的API密钥
4. 复制生成的API密钥

## 故障排除

如果遇到以下错误：
- `Invalid value at 'safety_settings[3].category'` - 这是已修复的问题
- `Failed to establish a new connection` - 这是因为没有设置API密钥

请确保：
1. API密钥正确设置
2. 网络连接正常
3. API密钥有效且有足够的额度
