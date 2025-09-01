#!/usr/bin/env python3
"""
云服务器同步修复脚本
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, description=""):
    """运行命令并返回结果"""
    print(f"🔧 {description}")
    print(f"   执行: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ 成功")
            if result.stdout.strip():
                print(f"   输出: {result.stdout.strip()}")
        else:
            print(f"   ❌ 失败")
            if result.stderr.strip():
                print(f"   错误: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"   ❌ 异常: {e}")
        return False

def check_git_status():
    """检查Git状态"""
    print("📋 Git状态检查:")
    
    # 检查当前分支
    result = subprocess.run("git branch --show-current", shell=True, capture_output=True, text=True)
    current_branch = result.stdout.strip()
    print(f"   当前分支: {current_branch}")
    
    # 检查是否有未提交的更改
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if result.stdout.strip():
        print("   ⚠️ 有未提交的更改:")
        for line in result.stdout.strip().split('\n'):
            print(f"     {line}")
        return False
    else:
        print("   ✅ 工作目录干净")
        return True

def update_requirements():
    """更新requirements.txt"""
    print("\n📦 更新依赖文件:")
    
    # 检查是否需要添加DeepFace相关依赖
    with open('requirements.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'deepface' not in content:
        print("   ➕ 添加DeepFace依赖")
        with open('requirements.txt', 'a', encoding='utf-8') as f:
            f.write('\n# 表情识别依赖\ndeepface==0.0.79\nopencv-python==4.8.1.78\n')
        print("   ✅ DeepFace依赖已添加")
    else:
        print("   ✅ DeepFace依赖已存在")

def create_deployment_script():
    """创建部署脚本"""
    print("\n🚀 创建部署脚本:")
    
    script_content = '''#!/bin/bash
# 云服务器部署脚本

set -e

echo "🚀 开始部署LLRC应用..."

# 项目配置
PROJECT_DIR="/var/www/llrc"
SERVICE_NAME="llrc"

# 1. 拉取最新代码
echo "📥 拉取最新代码..."
cd $PROJECT_DIR
git fetch origin
git reset --hard origin/pxy

# 2. 更新依赖
echo "📦 更新Python依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 3. 检查表情识别模块
echo "🤖 检查表情识别模块..."
python3 -c "
from smartrecruit_system.candidate_module.emotion_recognition import get_emotion_recognition_ai
ai = get_emotion_recognition_ai()
print('✅ 表情识别模块正常')
"

# 4. 重启服务
echo "🔄 重启服务..."
sudo systemctl restart $SERVICE_NAME

# 5. 检查服务状态
echo "📊 检查服务状态..."
sudo systemctl status $SERVICE_NAME --no-pager

echo "✅ 部署完成！"
'''
    
    with open('cloud_deploy.sh', 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    # 设置执行权限
    os.chmod('cloud_deploy.sh', 0o755)
    print("   ✅ 部署脚本已创建: cloud_deploy.sh")

def create_environment_check():
    """创建环境检查脚本"""
    print("\n🔍 创建环境检查脚本:")
    
    check_content = '''#!/usr/bin/env python3
"""
云服务器环境检查脚本
"""

import sys
import os

def check_deepface():
    """检查DeepFace环境"""
    try:
        from deepface import DeepFace
        print("✅ DeepFace导入成功")
        return True
    except Exception as e:
        print(f"❌ DeepFace导入失败: {e}")
        return False

def check_emotion_recognition():
    """检查表情识别功能"""
    try:
        from smartrecruit_system.candidate_module.emotion_recognition import get_emotion_recognition_ai
        ai = get_emotion_recognition_ai()
        print("✅ 表情识别模块正常")
        return True
    except Exception as e:
        print(f"❌ 表情识别模块失败: {e}")
        return False

def main():
    print("🔍 云服务器环境检查")
    print("=" * 30)
    
    deepface_ok = check_deepface()
    emotion_ok = check_emotion_recognition()
    
    if deepface_ok and emotion_ok:
        print("\\n🎉 环境检查通过！")
        sys.exit(0)
    else:
        print("\\n❌ 环境检查失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open('cloud_check.py', 'w', encoding='utf-8') as f:
        f.write(check_content)
    
    print("   ✅ 环境检查脚本已创建: cloud_check.py")

def commit_and_push():
    """提交并推送更改"""
    print("\n📤 提交并推送更改:")
    
    # 添加所有文件
    run_command("git add .", "添加所有文件")
    
    # 提交更改
    run_command('git commit -m "修复云服务器同步问题 - 更新DeepFace依赖和部署脚本"', "提交更改")
    
    # 推送到远程仓库
    run_command("git push origin pxy", "推送到远程仓库")

def main():
    """主函数"""
    print("🚀 云服务器同步修复工具")
    print("=" * 50)
    
    # 1. 检查Git状态
    if not check_git_status():
        print("\n⚠️ 请先提交或暂存本地更改")
        return
    
    # 2. 更新依赖文件
    update_requirements()
    
    # 3. 创建部署脚本
    create_deployment_script()
    
    # 4. 创建环境检查脚本
    create_environment_check()
    
    # 5. 提交并推送
    commit_and_push()
    
    print("\n🎉 修复完成！")
    print("\n📋 下一步操作:")
    print("1. 在云服务器上运行: ./cloud_deploy.sh")
    print("2. 检查环境: python3 cloud_check.py")
    print("3. 查看服务状态: sudo systemctl status llrc")

if __name__ == "__main__":
    main()
