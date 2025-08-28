from flask import current_app
from app.models import db
from app.utils import extract_text_from_resume, ai_extract_skills_from_text
from .emotion_recognition import get_emotion_recognition_ai
import logging

# 配置日志
logger = logging.getLogger(__name__)

def update_user_skills_from_resume(user, file_bytes: bytes, filename: str) -> list:
    """从上传的简历文件中解析文本，调用AI提取技能，并保存到User.skills(JSON字符串)。

    Returns: 提取到的技能列表
    """
    resume_text = ''
    try:
        resume_text = extract_text_from_resume(file_bytes, filename) or ''
    except Exception:
        resume_text = ''

    skills = ai_extract_skills_from_text(resume_text or (getattr(user, 'position', '') or '') )
    try:
        import json
        user.skills = json.dumps(skills, ensure_ascii=False)
        db.session.commit()
    except Exception as e:
        current_app.logger.warning(f'Failed to save AI skills: {e}')
    return skills


def analyze_candidate_emotion_from_image(image_data: bytes, filename: str = None) -> dict:
    """
    分析候选人照片中的表情，用于评估候选人的精神状态和职业素养
    
    Args:
        image_data: 图片的二进制数据
        filename: 文件名（可选）
        
    Returns:
        dict: 表情分析结果
    """
    try:
        emotion_ai = get_emotion_recognition_ai()
        result = emotion_ai.recognize_emotion_from_image(image_data, filename)
        
        # 添加职业评估建议
        if result.get("success") and result.get("faces"):
            result["career_insights"] = _generate_career_insights(result["faces"])
            result["interview_recommendations"] = _generate_interview_recommendations(result["emotion_summary"])
        
        return result
        
    except Exception as e:
        logger.error(f"候选人表情分析失败: {e}")
        return {"error": f"表情分析失败: {str(e)}"}


def analyze_interview_performance(video_data: bytes, filename: str = None) -> dict:
    """
    分析面试视频中的候选人表现，包括表情变化、情绪稳定性等
    
    Args:
        video_data: 面试视频的二进制数据
        filename: 文件名（可选）
        
    Returns:
        dict: 面试表现分析结果
    """
    try:
        emotion_ai = get_emotion_recognition_ai()
        result = emotion_ai.analyze_interview_video(video_data, filename)
        
        # 添加面试评估
        if result.get("success"):
            result["performance_analysis"] = _analyze_interview_performance(result)
            result["candidate_score"] = _calculate_candidate_score(result)
        
        return result
        
    except Exception as e:
        logger.error(f"面试表现分析失败: {e}")
        return {"error": f"面试分析失败: {str(e)}"}


def _generate_career_insights(faces: list) -> dict:
    """
    基于表情分析生成职业洞察
    
    Args:
        faces: 检测到的人脸列表
        
    Returns:
        dict: 职业洞察
    """
    insights = {
        "confidence_level": "未知",
        "professional_appearance": "未知",
        "emotional_stability": "未知",
        "recommendations": []
    }
    
    if not faces:
        return insights
    
    # 分析主要表情
    emotions = [face["emotion"] for face in faces]
    confidences = [face["emotion_confidence"] for face in faces]
    
    # 评估置信度水平
    if not confidences:
        avg_confidence = 0.0
    else:
        avg_confidence = sum(confidences) / len(confidences)
    if avg_confidence > 0.8:
        insights["confidence_level"] = "高"
    elif avg_confidence > 0.6:
        insights["confidence_level"] = "中"
    else:
        insights["confidence_level"] = "低"
    
    # 评估职业形象
    positive_emotions = ["高兴", "中性", "惊讶"]
    negative_emotions = ["愤怒", "厌恶", "恐惧", "悲伤"]
    
    positive_count = sum(1 for emotion in emotions if emotion in positive_emotions)
    negative_count = sum(1 for emotion in emotions if emotion in negative_emotions)
    
    if positive_count > negative_count:
        insights["professional_appearance"] = "积极"
    elif negative_count > positive_count:
        insights["professional_appearance"] = "消极"
    else:
        insights["professional_appearance"] = "中性"
    
    # 评估情绪稳定性
    unique_emotions = set(emotions)
    if len(unique_emotions) == 1:
        insights["emotional_stability"] = "稳定"
    elif len(unique_emotions) <= 2:
        insights["emotional_stability"] = "较稳定"
    else:
        insights["emotional_stability"] = "不稳定"
    
    # 生成建议
    if insights["professional_appearance"] == "消极":
        insights["recommendations"].append("建议在面试前进行情绪调节训练")
    
    if insights["emotional_stability"] == "不稳定":
        insights["recommendations"].append("建议提高情绪管理能力")
    
    if avg_confidence < 0.6:
        insights["recommendations"].append("建议提高自信心和表达能力")
    
    return insights


def _generate_interview_recommendations(emotion_summary: dict) -> list:
    """
    基于表情摘要生成面试建议
    
    Args:
        emotion_summary: 表情摘要
        
    Returns:
        list: 面试建议列表
    """
    recommendations = []
    
    if not emotion_summary:
        return recommendations
    
    dominant_emotion = emotion_summary.get("dominant_emotion", "未知")
    avg_confidence = emotion_summary.get("average_confidence", 0)
    
    # 基于主要表情的建议
    if dominant_emotion == "高兴":
        recommendations.append("候选人表现出积极乐观的态度，适合需要团队协作的岗位")
    elif dominant_emotion == "中性":
        recommendations.append("候选人情绪稳定，适合需要冷静思考的岗位")
    elif dominant_emotion == "愤怒":
        recommendations.append("候选人可能面临压力，建议了解具体情况")
    elif dominant_emotion == "恐惧":
        recommendations.append("候选人可能缺乏自信，建议提供更多鼓励和支持")
    elif dominant_emotion == "悲伤":
        recommendations.append("候选人情绪低落，建议了解个人情况")
    
    # 基于置信度的建议
    if avg_confidence > 0.8:
        recommendations.append("表情识别置信度高，分析结果可靠")
    elif avg_confidence < 0.6:
        recommendations.append("表情识别置信度较低，建议结合其他评估方法")
    
    return recommendations


def _analyze_interview_performance(video_result: dict) -> dict:
    """
    分析面试视频中的表现
    
    Args:
        video_result: 视频分析结果
        
    Returns:
        dict: 表现分析
    """
    analysis = {
        "emotional_consistency": "未知",
        "stress_management": "未知",
        "communication_style": "未知",
        "overall_impression": "未知"
    }
    
    timeline = video_result.get("emotion_timeline", [])
    if not timeline:
        return analysis
    
    # 分析情绪一致性
    all_emotions = []
    for entry in timeline:
        for face in entry.get("emotions", []):
            all_emotions.append(face.get("emotion", "未知"))
    
    unique_emotions = set(all_emotions)
    if len(unique_emotions) <= 2:
        analysis["emotional_consistency"] = "高"
    elif len(unique_emotions) <= 4:
        analysis["emotional_consistency"] = "中"
    else:
        analysis["emotional_consistency"] = "低"
    
    # 分析压力管理
    negative_emotions = ["愤怒", "恐惧", "悲伤"]
    negative_count = sum(1 for emotion in all_emotions if emotion in negative_emotions)
    total_emotions = len(all_emotions)
    
    if total_emotions > 0:
        negative_ratio = negative_count / total_emotions
        if negative_ratio < 0.2:
            analysis["stress_management"] = "优秀"
        elif negative_ratio < 0.4:
            analysis["stress_management"] = "良好"
        else:
            analysis["stress_management"] = "需要改进"
    
    # 分析沟通风格
    positive_emotions = ["高兴", "中性", "惊讶"]
    positive_count = sum(1 for emotion in all_emotions if emotion in positive_emotions)
    
    if total_emotions > 0:
        positive_ratio = positive_count / total_emotions
        if positive_ratio > 0.7:
            analysis["communication_style"] = "积极开放"
        elif positive_ratio > 0.5:
            analysis["communication_style"] = "平衡"
        else:
            analysis["communication_style"] = "保守谨慎"
    
    # 整体印象
    try:
        if analysis["emotional_consistency"] == "高" and analysis["stress_management"] in ["优秀", "良好"]:
            analysis["overall_impression"] = "优秀候选人"
        elif analysis["emotional_consistency"] in ["高", "中"] and analysis["stress_management"] != "需要改进":
            analysis["overall_impression"] = "良好候选人"
        else:
            analysis["overall_impression"] = "需要进一步评估"
    except Exception as e:
        logger.warning(f"计算整体印象时出错: {e}")
        analysis["overall_impression"] = "需要进一步评估"
    
    return analysis


def _calculate_candidate_score(video_result: dict) -> dict:
    """
    计算候选人评分
    
    Args:
        video_result: 视频分析结果
        
    Returns:
        dict: 评分结果
    """
    score = {
        "emotional_stability": 0,
        "confidence": 0,
        "professionalism": 0,
        "overall_score": 0,
        "grade": "未知"
    }
    
    timeline = video_result.get("emotion_timeline", [])
    if not timeline:
        return score
    
    # 计算情绪稳定性分数
    all_emotions = []
    for entry in timeline:
        for face in entry.get("emotions", []):
            all_emotions.append(face.get("emotion", "未知"))
    
    unique_emotions = set(all_emotions)
    try:
        if len(unique_emotions) <= 2:
            score["emotional_stability"] = 90
        elif len(unique_emotions) <= 4:
            score["emotional_stability"] = 75
        else:
            score["emotional_stability"] = 60
    except Exception as e:
        logger.warning(f"计算情绪稳定性分数时出错: {e}")
        score["emotional_stability"] = 0
    
    # 计算自信心分数
    confidences = []
    for entry in timeline:
        for face in entry.get("emotions", []):
            confidences.append(face.get("emotion_confidence", 0))
    
    if confidences:
        avg_confidence = sum(confidences) / len(confidences)
        score["confidence"] = int(avg_confidence * 100)
    
    # 计算职业素养分数
    positive_emotions = ["高兴", "中性", "惊讶"]
    positive_count = sum(1 for emotion in all_emotions if emotion in positive_emotions)
    total_emotions = len(all_emotions)
    
    if total_emotions > 0:
        positive_ratio = positive_count / total_emotions
        score["professionalism"] = int(positive_ratio * 100)
    
    # 计算总分
    score["overall_score"] = (score["emotional_stability"] + score["confidence"] + score["professionalism"]) // 3
    
    # 确定等级
    if score["overall_score"] >= 85:
        score["grade"] = "A"
    elif score["overall_score"] >= 75:
        score["grade"] = "B"
    elif score["overall_score"] >= 65:
        score["grade"] = "C"
    else:
        score["grade"] = "D"
    
    return score


def get_ai_analysis_summary(user_id: int) -> dict:
    """
    获取用户的AI分析摘要
    
    Args:
        user_id: 用户ID
        
    Returns:
        dict: AI分析摘要
    """
    try:
        # 这里可以从数据库获取用户的AI分析历史
        # 暂时返回示例数据
        summary = {
            "user_id": user_id,
            "resume_analysis_count": 0,
            "emotion_analysis_count": 0,
            "interview_analysis_count": 0,
            "last_analysis_date": None,
            "overall_ai_score": 0,
            "recommendations": []
        }
        
        return summary
        
    except Exception as e:
        logger.error(f"获取AI分析摘要失败: {e}")
        return {"error": f"获取分析摘要失败: {str(e)}"}


