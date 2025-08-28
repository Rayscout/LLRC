#!/usr/bin/env python3
"""
测试表情识别模型
"""

import os
import sys
from pathlib import Path

def test_emotion_model():
    """测试表情识别模型"""
    print("🧪 测试表情识别模型...")
    
    # 获取项目路径
    current_dir = Path(__file__).parent
    
    try:
        # 导入表情识别模块
        import importlib.util
        spec = importlib.util.spec_from_file_location("emotion_recognition", current_dir / "emotion_recognition.py")
        emotion_recognition = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(emotion_recognition)
        
        # 获取AI实例
        emotion_ai = emotion_recognition.get_emotion_recognition_ai()
        
        # 检查模型状态
        status = emotion_ai.get_system_status()
        
        print("📊 模型状态:")
        print(f"   - 人脸检测模型: {'✅ 已加载' if status['models_loaded']['face_detection'] else '❌ 未加载'}")
        print(f"   - 表情识别模型: {'✅ 已加载' if status['models_loaded']['emotion_recognition'] else '❌ 未加载'}")
        print(f"   - 字体文件: {'✅ 已加载' if status['models_loaded']['font'] else '❌ 未加载'}")
        
        if status['models_loaded']['emotion_recognition']:
            print("\n✅ 表情识别模型测试成功！")
            print("🎉 模型已准备就绪，可以在虚拟面试系统中使用")
            
            # 显示模型信息
            print("\n📋 模型信息:")
            print(f"   - 模型路径: {emotion_ai.emotion_model_path}")
            print(f"   - 模型大小: {Path(emotion_ai.emotion_model_path).stat().st_size / (1024*1024):.1f} MB")
            print(f"   - 表情类别: {emotion_ai.emotion_labels}")
            
            return True
        else:
            print("\n❌ 表情识别模型测试失败")
            print("💡 请检查模型文件是否正确加载")
            return False
            
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False

def main():
    """主函数"""
    success = test_emotion_model()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 表情识别模型测试成功！")
        print("🔧 现在可以在虚拟面试系统中使用表情识别功能了")
        print("=" * 50)
    else:
        print("\n" + "=" * 50)
        print("❌ 表情识别模型测试失败")
        print("💡 请检查模型文件和配置")
        print("=" * 50)

if __name__ == "__main__":
    main()
