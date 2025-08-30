from flask import Blueprint, request, jsonify, g, current_app
from werkzeug.utils import secure_filename
import os
import logging
from .candidate_ai import (
    analyze_candidate_emotion_from_image,
    analyze_interview_performance,
    get_ai_analysis_summary,
    recognize_speech_from_audio
)

# 配置日志
logger = logging.getLogger(__name__)

# 创建AI分析蓝图
ai_analysis_bp = Blueprint('ai_analysis', __name__, url_prefix='/ai-analysis')

# 允许的文件扩展名
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'}
ALLOWED_AUDIO_EXTENSIONS = {'wav', 'mp3', 'm4a', 'ogg', 'webm'}

def allowed_file(filename, allowed_extensions):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@ai_analysis_bp.route('/emotion-analysis', methods=['POST'])
def emotion_analysis():
    """
    表情识别分析接口
    
    接收图片文件，返回表情分析结果
    """
    if g.user is None:
        return jsonify({"error": "请先登录"}), 401
    
    try:
        # 检查是否有文件
        if 'image' not in request.files:
            return jsonify({"error": "没有上传文件"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "没有选择文件"}), 400
        
        # 检查文件类型
        if not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            return jsonify({"error": "不支持的文件类型，请上传图片文件"}), 400
        
        # 读取文件数据
        file_data = file.read()
        filename = secure_filename(file.filename)
        
        # 进行表情分析
        result = analyze_candidate_emotion_from_image(file_data, filename)
        
        if "error" in result:
            return jsonify(result), 400
        
        # 记录分析日志
        logger.info(f"用户 {g.user.id} 进行了表情分析，文件: {filename}")
        
        return jsonify({
            "success": True,
            "message": "表情分析完成",
            "data": result
        })
        
    except Exception as e:
        logger.error(f"表情分析接口错误: {e}")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500

@ai_analysis_bp.route('/interview-analysis', methods=['POST'])
def interview_analysis():
    """
    面试表现分析接口
    
    接收面试视频文件，返回表现分析结果
    """
    if g.user is None:
        return jsonify({"error": "请先登录"}), 401
    
    try:
        # 检查是否有文件
        if 'video' not in request.files:
            return jsonify({"error": "没有上传文件"}), 400
        
        file = request.files['video']
        if file.filename == '':
            return jsonify({"error": "没有选择文件"}), 400
        
        # 检查文件类型
        if not allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
            return jsonify({"error": "不支持的文件类型，请上传视频文件"}), 400
        
        # 检查文件大小（限制为100MB）
        file.seek(0, 2)  # 移动到文件末尾
        file_size = file.tell()
        file.seek(0)  # 重置到文件开头
        
        if file_size > 100 * 1024 * 1024:  # 100MB
            return jsonify({"error": "文件大小超过限制（100MB）"}), 400
        
        # 读取文件数据
        file_data = file.read()
        filename = secure_filename(file.filename)
        
        # 进行面试分析
        result = analyze_interview_performance(file_data, filename)
        
        if "error" in result:
            return jsonify(result), 400
        
        # 记录分析日志
        logger.info(f"用户 {g.user.id} 进行了面试分析，文件: {filename}")
        
        return jsonify({
            "success": True,
            "message": "面试分析完成",
            "data": result
        })
        
    except Exception as e:
        logger.error(f"面试分析接口错误: {e}")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500

@ai_analysis_bp.route('/analysis-summary', methods=['GET'])
def analysis_summary():
    """
    获取AI分析摘要接口
    
    返回用户的AI分析历史摘要
    """
    if g.user is None:
        return jsonify({"error": "请先登录"}), 401
    
    try:
        user_id = g.user.id
        summary = get_ai_analysis_summary(user_id)
        
        if "error" in summary:
            return jsonify(summary), 400
        
        return jsonify({
            "success": True,
            "data": summary
        })
        
    except Exception as e:
        logger.error(f"获取分析摘要接口错误: {e}")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500

@ai_analysis_bp.route('/health-check', methods=['GET'])
def health_check():
    """
    AI模型健康检查接口
    
    检查表情识别模型是否正常加载
    """
    try:
        from .emotion_recognition import get_emotion_recognition_ai
        
        emotion_ai = get_emotion_recognition_ai()
        
        # 检查模型状态
        models_status = {
            "face_detection_model": emotion_ai.face_model is not None,
            "emotion_recognition_model": emotion_ai.emotion_model is not None,
            "font_loaded": emotion_ai.font is not None
        }
        
        all_models_loaded = all(models_status.values())
        
        return jsonify({
            "success": True,
            "status": "healthy" if all_models_loaded else "degraded",
            "models": models_status,
            "message": "所有模型已加载" if all_models_loaded else "部分模型未加载"
        })
        
    except Exception as e:
        logger.error(f"健康检查接口错误: {e}")
        return jsonify({
            "success": False,
            "status": "unhealthy",
            "error": str(e)
        }), 500

@ai_analysis_bp.route('/supported-formats', methods=['GET'])
def supported_formats():
    """
    获取支持的文件格式接口
    """
    return jsonify({
        "success": True,
        "data": {
            "image_formats": list(ALLOWED_IMAGE_EXTENSIONS),
            "video_formats": list(ALLOWED_VIDEO_EXTENSIONS),
            "max_file_size": "100MB"
        }
    })

@ai_analysis_bp.route('/demo', methods=['GET'])
def demo_info():
    """
    获取演示信息接口
    
    返回如何使用AI分析功能的说明
    """
    demo_info = {
        "emotion_analysis": {
            "description": "上传候选人照片进行表情识别分析",
            "endpoint": "/ai-analysis/emotion-analysis",
            "method": "POST",
            "input": "image file (png, jpg, jpeg, gif, bmp)",
            "output": "表情识别结果、职业洞察、面试建议"
        },
        "interview_analysis": {
            "description": "上传面试视频进行表现分析",
            "endpoint": "/ai-analysis/interview-analysis",
            "method": "POST",
            "input": "video file (mp4, avi, mov, wmv, flv, mkv)",
            "output": "面试表现分析、情绪稳定性评估、候选人评分"
        },
        "analysis_summary": {
            "description": "获取用户的AI分析历史摘要",
            "endpoint": "/ai-analysis/analysis-summary",
            "method": "GET",
            "input": "无",
            "output": "分析历史、统计信息、建议"
        },
        "speech_recognition": {
            "description": "上传音频文件进行语音转文字",
            "endpoint": "/ai-analysis/speech-recognition",
            "method": "POST",
            "input": "audio file (wav, mp3, m4a, ogg, webm)",
            "output": "语音识别结果、转写文本"
        }
    }
    
    return jsonify({
        "success": True,
        "data": demo_info
    })

@ai_analysis_bp.route('/speech-recognition', methods=['POST'])
def speech_recognition():
    """
    语音识别接口
    
    接收音频文件，使用Gemini 1.5 Flash进行语音转文字
    """
    if g.user is None:
        return jsonify({"error": "请先登录"}), 401
    
    try:
        # 检查是否有文件
        if 'audio' not in request.files:
            return jsonify({"error": "没有上传音频文件"}), 400
        
        file = request.files['audio']
        if file.filename == '':
            return jsonify({"error": "没有选择文件"}), 400
        
        # 检查文件类型
        if not allowed_file(file.filename, ALLOWED_AUDIO_EXTENSIONS):
            return jsonify({"error": "不支持的文件类型，请上传音频文件"}), 400
        
        # 检查文件大小（限制为50MB）
        file.seek(0, 2)  # 移动到文件末尾
        file_size = file.tell()
        file.seek(0)  # 重置到文件开头
        
        if file_size > 50 * 1024 * 1024:  # 50MB
            return jsonify({"error": "文件大小超过限制（50MB）"}), 400
        
        # 读取文件数据
        file_data = file.read()
        filename = secure_filename(file.filename)
        
        # 进行语音识别
        result = recognize_speech_from_audio(file_data, filename)
        
        if "error" in result:
            return jsonify(result), 400
        
        # 记录分析日志
        logger.info(f"用户 {g.user.id} 进行了语音识别，文件: {filename}")
        
        return jsonify({
            "success": True,
            "message": "语音识别完成",
            "data": result
        })
        
    except Exception as e:
        logger.error(f"语音识别接口错误: {e}")
        return jsonify({"error": f"服务器内部错误: {str(e)}"}), 500

@ai_analysis_bp.route('/debug', methods=['GET'])
def debug_info():
    """调试信息接口"""
    try:
        from .emotion_recognition import get_emotion_recognition_ai
        
        emotion_ai = get_emotion_recognition_ai()
        
        debug_info = {
            "face_model_loaded": emotion_ai.face_model is not None,
            "emotion_model_loaded": emotion_ai.emotion_model is not None,
            "font_loaded": emotion_ai.font is not None,
            "config": {
                "face_model_path": emotion_ai.config.get_face_detection_model_path(),
                "emotion_model_path": emotion_ai.config.get_emotion_recognition_model_path(),
                "emotion_labels": emotion_ai.emotion_labels
            }
        }
        
        return jsonify({
            "success": True,
            "debug_info": debug_info
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@ai_analysis_bp.route('/test-emotion', methods=['POST'])
def test_emotion():
    """测试表情识别功能"""
    try:
        from .emotion_recognition import get_emotion_recognition_ai
        import cv2
        import numpy as np
        
        emotion_ai = get_emotion_recognition_ai()
        
        # 创建测试图像
        test_image = np.zeros((224, 224, 3), dtype=np.uint8)
        
        # 测试表情识别
        result = emotion_ai.recognize_emotion_from_image(test_image.tobytes(), "test.jpg")
        
        return jsonify({
            "success": True,
            "test_result": result
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
