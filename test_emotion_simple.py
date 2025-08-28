
#!/usr/bin/env python3
"""
简单的表情识别测试脚本
"""

import requests
import json
from PIL import Image, ImageDraw

def test_emotion_api():
    """测试表情识别API"""
    print("🧪 测试表情识别API...")
    
    try:
        # 创建测试图片
        img = Image.new('RGB', (224, 224), color='red')
        draw = ImageDraw.Draw(img)
        draw.ellipse([50, 50, 174, 174], fill='white')
        
        # 保存测试图片
        test_image_path = 'test_face.jpg'
        img.save(test_image_path)
        
        # 发送请求
        with open(test_image_path, 'rb') as f:
            files = {'image': ('test_face.jpg', f, 'image/jpeg')}
            response = requests.post(
                'http://127.0.0.1:5000/smartrecruit/candidate/ai-analysis/emotion-analysis',
                files=files,
                timeout=30
            )
        
        # 清理测试文件
        import os
        os.remove(test_image_path)
        
        print(f"响应状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API测试成功")
            print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        else:
            print(f"❌ API测试失败: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试异常: {e}")

if __name__ == "__main__":
    test_emotion_api()
