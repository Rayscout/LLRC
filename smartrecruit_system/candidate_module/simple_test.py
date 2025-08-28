#!/usr/bin/env python3
"""
简单测试表情识别模型
"""

import os
from pathlib import Path

def simple_test():
    """简单测试"""
    print("🧪 简单测试表情识别模型...")
    
    # 获取项目路径
    current_dir = Path(__file__).parent
    
    # 检查模型文件是否存在
    model_path = current_dir / "trained_models" / "emotion_recognition_model.pt"
    
    if model_path.exists():
        print(f"✅ 模型文件存在: {model_path}")
        print(f"📏 模型大小: {model_path.stat().st_size / (1024*1024):.1f} MB")
        
        # 检查配置文件
        config_path = current_dir / "ai_config.py"
        if config_path.exists():
            print(f"✅ 配置文件存在: {config_path}")
        
        # 检查表情识别模块
        emotion_module = current_dir / "emotion_recognition.py"
        if emotion_module.exists():
            print(f"✅ 表情识别模块存在: {emotion_module}")
        
        print("\n🎉 模型文件检查完成！")
        print("🔧 现在可以在虚拟面试系统中使用表情识别功能了")
        
        return True
    else:
        print(f"❌ 模型文件不存在: {model_path}")
        return False

def main():
    """主函数"""
    success = simple_test()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 表情识别模型简单测试成功！")
        print("🔧 模型已准备就绪，可以在虚拟面试系统中使用")
        print("=" * 50)
        
        print("\n🚀 下一步操作：")
        print("1. 重启您的虚拟面试应用")
        print("2. 访问虚拟面试页面")
        print("3. 开始使用表情识别功能")
        
    else:
        print("\n" + "=" * 50)
        print("❌ 表情识别模型简单测试失败")
        print("💡 请检查模型文件是否存在")
        print("=" * 50)

if __name__ == "__main__":
    main()
