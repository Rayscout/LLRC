#!/usr/bin/env python3
"""
测试Gemini API连接和语音识别功能
"""

import os
import requests
import base64
import json

def test_gemini_connection():
    """测试Gemini API基本连接"""
    print("=== 测试Gemini API连接 ===")
    
    # 获取API密钥
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ 未找到API密钥")
        print("请设置环境变量: GEMINI_API_KEY 或 GOOGLE_API_KEY")
        return False
    
    print(f"✅ 找到API密钥: {api_key[:10]}...")
    
    # 测试基本文本生成
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    payload = {
        "contents": [{
            "parts": [{"text": "Hello, how are you?"}]
        }],
        "generationConfig": {
            "maxOutputTokens": 100
        }
    }
    
    try:
        print("🔄 测试文本生成API...")
        response = requests.post(
            url,
            params={'key': api_key},
            json=payload,
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 文本生成API测试成功")
            print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"❌ 文本生成API测试失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 连接测试失败: {e}")
        return False

def test_audio_recognition():
    """测试音频识别API"""
    print("\n=== 测试音频识别API ===")
    
    api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        print("❌ 未找到API密钥")
        return False
    
    # 创建一个简单的测试音频数据（1秒的静音）
    # 这里使用一个最小的WAV文件头
    test_audio = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00'
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    
    payload = {
        "contents": [{
            "parts": [
                {
                    "text": "请将这段音频转换为文字。请只返回转写的文字内容，不要添加任何解释或标点符号。"
                },
                {
                    "inline_data": {
                        "mime_type": "audio/wav",
                        "data": base64.b64encode(test_audio).decode('utf-8')
                    }
                }
            ]
        }],
        "generationConfig": {
            "maxOutputTokens": 1000,
            "temperature": 0.1
        }
    }
    
    try:
        print("🔄 测试音频识别API...")
        print(f"音频数据大小: {len(test_audio)} 字节")
        print(f"音频MIME类型: audio/wav")
        
        response = requests.post(
            url,
            params={'key': api_key},
            json=payload,
            timeout=60
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ 音频识别API测试成功")
            print(f"响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return True
        else:
            print(f"❌ 音频识别API测试失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 音频识别测试失败: {e}")
        import traceback
        print(f"详细错误: {traceback.format_exc()}")
        return False

def check_environment():
    """检查环境变量"""
    print("=== 环境变量检查 ===")
    
    env_vars = {
        'GEMINI_API_KEY': os.getenv('GEMINI_API_KEY'),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY'),
        'GEMINI_MODEL': os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    }
    
    for key, value in env_vars.items():
        if value:
            if 'KEY' in key:
                print(f"✅ {key}: {value[:10]}...")
            else:
                print(f"✅ {key}: {value}")
        else:
            print(f"❌ {key}: 未设置")
    
    return bool(env_vars['GEMINI_API_KEY'] or env_vars['GOOGLE_API_KEY'])

def main():
    """主函数"""
    print("🚀 Gemini API 连接测试工具")
    print("=" * 50)
    
    # 检查环境变量
    if not check_environment():
        print("\n❌ 环境变量配置不完整，无法继续测试")
        return
    
    print("\n" + "=" * 50)
    
    # 测试基本连接
    if test_gemini_connection():
        print("\n✅ 基本API连接测试通过")
        
        # 测试音频识别
        if test_audio_recognition():
            print("\n✅ 音频识别API测试通过")
            print("\n🎉 所有测试通过！Gemini API配置正确。")
        else:
            print("\n❌ 音频识别API测试失败，请检查错误信息")
    else:
        print("\n❌ 基本API连接测试失败")

if __name__ == "__main__":
    main()
