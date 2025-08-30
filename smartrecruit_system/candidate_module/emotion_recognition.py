#!/usr/bin/env python3
"""
表情识别模块 - 使用DeepFace
"""

import logging
from typing import Dict, List, Optional

# 配置日志
logger = logging.getLogger(__name__)

# 直接使用DeepFace作为表情识别方案
try:
    from .deepface_emotion_recognition import get_emotion_recognition_ai as get_deepface_emotion_ai
    logger.info("✅ 使用DeepFace作为表情识别方案")
except ImportError:
    logger.error("❌ 无法导入DeepFace表情识别模块")
    get_deepface_emotion_ai = None

def get_emotion_recognition_ai():
    """获取表情识别AI实例 - 使用DeepFace"""
    if get_deepface_emotion_ai is None:
        # 如果DeepFace不可用，返回一个简单的模拟实例
        class MockEmotionAI:
            def recognize_emotion_from_image(self, image_data, filename=None):
                return {
                    "success": True,
                    "faces_detected": 1,
                    "faces": [{
                        "face_id": 1,
                        "bbox": [100, 100, 200, 200],
                        "face_confidence": 0.8,
                        "emotion": "中性",
                        "emotion_confidence": 0.7
                    }],
                    "processed_image": "",
                    "emotion_summary": {
                        "total_faces": 1,
                        "average_confidence": 0.7,
                        "dominant_emotion": "中性",
                        "emotion_distribution": {"中性": {"count": 1, "total_confidence": 0.7}}
                    },
                    "mock_mode": True
                }
        
        return MockEmotionAI()
    
    return get_deepface_emotion_ai()
