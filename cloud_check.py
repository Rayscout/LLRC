#!/usr/bin/env python3
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
        print("\n🎉 环境检查通过！")
        sys.exit(0)
    else:
        print("\n❌ 环境检查失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()
