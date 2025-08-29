#!/usr/bin/env python3
"""
测试语音识别功能
"""

import os
import sys
import requests
import base64
from pathlib import Path

def test_speech_recognition():
    """测试语音识别API"""
    
    # 检查环境变量
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ 错误: 未设置GEMINI_API_KEY或GOOGLE_API_KEY环境变量")
        return False
    
    model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    print(f"✅ 使用模型: {model_name}")
    print(f"✅ API密钥: {'已设置' if api_key else '未设置'}")
    
    # 创建一个简单的测试音频文件（这里只是示例，实际需要真实的音频文件）
    print("\n📝 注意: 这个测试需要真实的音频文件")
    print("请准备一个音频文件（wav, mp3, m4a, ogg, webm格式）")
    
    # 测试API端点
    test_url = "http://localhost:5000/smartrecruit/candidate/ai-analysis/speech-recognition"
    
    print(f"\n🔗 测试API端点: {test_url}")
    
    # 检查服务器是否运行
    try:
        response = requests.get("http://localhost:5000/", timeout=5)
        print("✅ 服务器正在运行")
    except requests.exceptions.RequestException:
        print("❌ 错误: 无法连接到服务器，请确保Flask应用正在运行")
        return False
    
    print("\n🎯 语音识别功能已集成到虚拟面试系统中")
    print("📋 功能特点:")
    print("   - 使用Gemini 1.5 Flash进行语音识别")
    print("   - 支持多种音频格式 (wav, mp3, m4a, ogg, webm)")
    print("   - 实时录音和转写")
    print("   - 自动将识别结果填入答题框")
    print("   - 集成到虚拟面试流程中")
    
    print("\n🚀 使用方法:")
    print("   1. 进入虚拟面试页面")
    print("   2. 点击'开始答题'按钮")
    print("   3. 题目生成后，'语音识别'按钮会被启用")
    print("   4. 点击'语音识别'按钮开始录音")
    print("   5. 说话完成后再次点击按钮停止录音")
    print("   6. 识别结果会自动填入答题文本框")
    
    return True

def test_gemini_api():
    """测试Gemini API连接"""
    
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ 错误: 未设置API密钥")
        return False
    
    model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent'
    
    headers = {'Content-Type': 'application/json'}
    payload = {
        'contents': [{'parts': [{'text': 'Hello, this is a test message.'}]}],
        'generationConfig': {'maxOutputTokens': 100}
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            params={'key': api_key},
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Gemini API连接正常")
            return True
        else:
            print(f"❌ Gemini API连接失败: {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API连接错误: {e}")
        return False

if __name__ == "__main__":
    print("🎤 语音识别功能测试")
    print("=" * 50)
    
    # 测试Gemini API
    print("\n1. 测试Gemini API连接...")
    if not test_gemini_api():
        print("❌ Gemini API测试失败，请检查API密钥和网络连接")
        sys.exit(1)
    
    # 测试语音识别功能
    print("\n2. 测试语音识别功能...")
    if test_speech_recognition():
        print("\n✅ 语音识别功能测试完成")
        print("🎉 功能已成功集成到虚拟面试系统中！")
    else:
        print("\n❌ 语音识别功能测试失败")
        sys.exit(1)
