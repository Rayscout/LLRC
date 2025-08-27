from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models import User, Feedback, FeedbackNotification, db
from app.utils import _gemini_generate
from datetime import datetime, timedelta
import json
import uuid
import os
import re
from urllib.parse import quote_plus
from typing import List, Dict, Any

# 可选依赖：DuckDuckGo 搜索
try:
    from duckduckgo_search import DDGS  # type: ignore
except Exception:  # pragma: no cover
    DDGS = None  # type: ignore

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')

@feedback_bp.route('/')
def feedback_dashboard():
    """反馈管理仪表板"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取收到的反馈（来自高管和主管）
        received_feedback = Feedback.query.filter_by(recipient_id=user.id)\
            .order_by(Feedback.created_at.desc()).all()
        
        # 获取发送的反馈（员工发送给高管）
        sent_feedback = Feedback.query.filter_by(sender_id=user.id)\
            .order_by(Feedback.created_at.desc()).all()
        
        # 获取未读反馈
        unread_feedback = [f for f in received_feedback if f.status == 'sent']
        
        # 获取反馈统计
        feedback_stats = get_feedback_statistics(user.id)
        
        # 获取最近的反馈通知
        recent_notifications = FeedbackNotification.query.filter_by(
            user_id=user.id, is_read=False
        ).order_by(FeedbackNotification.created_at.desc()).limit(5).all()
        
        # 使用AI生成反馈总结与学习建议（Gemini）
        ai_summary = generate_feedback_summary(received_feedback)
        ai_recommendations = generate_learning_suggestions(ai_summary, user)

        return render_template(
            'talent_management/employee_management/feedback_dashboard.html',
            user=user,
            received_feedback=received_feedback,
            sent_feedback=sent_feedback,
            unread_feedback=unread_feedback,
            feedback_stats=feedback_stats,
            recent_notifications=recent_notifications,
            ai_summary=ai_summary,
            ai_recommendations=ai_recommendations,
        )
                             
    except Exception as e:
        flash(f'加载反馈页面时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_auth.employee_dashboard'))

@feedback_bp.route('/send', methods=['GET', 'POST'])
def send_feedback():
    """发送反馈给高管"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        if request.method == 'POST':
            # 处理反馈发送
            recipient_id = request.form.get('recipient_id')
            category = request.form.get('category')
            feedback_type = request.form.get('feedback_type')
            content = request.form.get('content')
            priority = request.form.get('priority', 'medium')
            
            if not all([recipient_id, category, feedback_type, content]):
                flash('请填写所有必填字段', 'warning')
                return redirect(url_for('talent_management.employee_manager.feedback.send_feedback'))
            
            # 验证接收者是否存在且是高管
            recipient = User.query.get(recipient_id)
            if not recipient or recipient.user_type not in ['supervisor', 'executive']:
                flash('接收者不存在或无权限接收反馈', 'warning')
                return redirect(url_for('talent_management.employee_manager.feedback.send_feedback'))
            
            # 创建新反馈
            new_feedback = Feedback(
                sender_id=user.id,
                recipient_id=recipient_id,
                category=category,
                feedback_type=feedback_type,
                content=content,
                priority=priority,
                status='sent'
            )
            
            db.session.add(new_feedback)
            db.session.commit()
            
            # 创建通知给接收者
            create_feedback_notification(new_feedback.id, recipient_id, user.id)
            
            flash('反馈已成功发送', 'success')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 获取可接收反馈的高管和主管
        executives = User.query.filter(User.user_type.in_(['supervisor', 'executive'])).all()
        
        return render_template('talent_management/employee_management/send_feedback.html',
                             user=user, executives=executives)
                             
    except Exception as e:
        flash(f'发送反馈时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))

@feedback_bp.route('/sent')
def sent_feedback():
    """查看已发送的反馈"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取发送的反馈
        sent_feedback = Feedback.query.filter_by(sender_id=user.id)\
            .order_by(Feedback.created_at.desc()).all()
        
        return render_template('talent_management/employee_management/sent_feedback.html',
                             user=user, sent_feedback=sent_feedback)
                             
    except Exception as e:
        flash(f'查看已发送反馈时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))

@feedback_bp.route('/view/<feedback_id>')
def view_feedback(feedback_id):
    """查看反馈详情"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取反馈详情
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            flash('反馈不存在', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 检查是否有权限查看
        if feedback.recipient_id != user.id:
            flash('您没有权限查看此反馈', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 标记为已读
        if feedback.status == 'sent':
            feedback.status = 'read'
            feedback.read_at = datetime.now()
            db.session.commit()
        
        # 获取发送者信息
        sender = User.query.get(feedback.sender_id)
        
        return render_template('talent_management/employee_management/view_feedback.html',
                             user=user, feedback=feedback, sender=sender)
                             
    except Exception as e:
        flash(f'查看反馈时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))

@feedback_bp.route('/respond/<feedback_id>', methods=['GET', 'POST'])
def respond_feedback(feedback_id):
    """回复反馈"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取反馈详情
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            flash('反馈不存在', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 检查是否有权限回复
        if feedback.recipient_id != user.id:
            flash('您没有权限回复此反馈', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        if request.method == 'POST':
            # 处理反馈回复
            response_text = request.form.get('response_text')
            rating = request.form.get('rating')
            suggestions = request.form.get('suggestions', '')
            
            if not response_text:
                flash('请填写反馈回复', 'warning')
                return redirect(url_for('talent_management.employee_manager.feedback.respond_feedback', feedback_id=feedback_id))
            
            # 更新反馈状态
            feedback.status = 'responded'
            feedback.responded_at = datetime.now()
            
            # 这里可以添加回复内容到反馈记录中（如果需要的话）
            # 或者创建单独的回复表
            
            db.session.commit()
            
            # 创建通知给发送者
            create_response_notification(feedback.id, feedback.sender_id, user.id)
            
            flash('反馈回复已提交', 'success')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 获取发送者信息
        sender = User.query.get(feedback.sender_id)
        
        return render_template('talent_management/employee_management/respond_feedback.html',
                             user=user, feedback=feedback, sender=sender)
                             
    except Exception as e:
        flash(f'回复反馈时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))

@feedback_bp.route('/archive/<feedback_id>')
def archive_feedback(feedback_id):
    """归档反馈"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取反馈详情
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            flash('反馈不存在', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 检查是否有权限归档
        if feedback.recipient_id != user.id:
            flash('您没有权限归档此反馈', 'warning')
            return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
        
        # 归档反馈
        feedback.status = 'archived'
        db.session.commit()
        
        flash('反馈已归档', 'success')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))
                             
    except Exception as e:
        flash(f'归档反馈时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_manager.feedback.feedback_dashboard'))

@feedback_bp.route('/api/notifications')
def api_notifications():
    """获取通知API"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'})
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': '用户信息获取失败'})
        
        notifications = FeedbackNotification.query.filter_by(
            user_id=user.id, is_read=False
        ).order_by(FeedbackNotification.created_at.desc()).all()
        
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                'id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'type': notification.notification_type,
                'created_at': notification.created_at.isoformat(),
                'feedback_id': notification.feedback_id
            })
        
        return jsonify({'success': True, 'data': notifications_data})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'获取通知失败: {str(e)}'})

@feedback_bp.route('/api/mark_read/<notification_id>')
def api_mark_read(notification_id):
    """标记通知为已读API"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'})
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': '用户信息获取失败'})
        
        notification = FeedbackNotification.query.get(notification_id)
        if not notification or notification.user_id != user.id:
            return jsonify({'success': False, 'message': '通知不存在或无权限'})
        
        notification.is_read = True
        db.session.commit()
        
        return jsonify({'success': True, 'message': '通知已标记为已读'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'标记失败: {str(e)}'})

@feedback_bp.route('/api/mark_all_read', methods=['GET', 'POST'])
def api_mark_all_read():
    """标记所有通知为已读API"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'})
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'message': '用户信息获取失败'})
        
        # 标记所有未读的通知为已读
        FeedbackNotification.query.filter_by(
            user_id=user.id, is_read=False
        ).update({'is_read': True})
        
        # 同时标记所有未读的反馈为已读
        Feedback.query.filter_by(
            recipient_id=user.id, status='sent'
        ).update({'status': 'read'})
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': '所有反馈已标记为已读'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'标记失败: {str(e)}'})

# 辅助函数
def get_feedback_statistics(user_id):
    """获取反馈统计"""
    try:
        # 获取用户收到的所有反馈
        received_feedback = Feedback.query.filter_by(recipient_id=user_id).all()
        
        # 获取用户发送的所有反馈
        sent_feedback = Feedback.query.filter_by(sender_id=user_id).all()
        
        stats = {
            'total_received': len(received_feedback),
            'total_sent': len(sent_feedback),
            'unread': len([f for f in received_feedback if f.status == 'sent']),
            'read': len([f for f in received_feedback if f.status == 'read']),
            'responded': len([f for f in received_feedback if f.status == 'responded']),
            'archived': len([f for f in received_feedback if f.status == 'archived']),
            'pending_responses': len([f for f in sent_feedback if f.status == 'sent']),
            'completed': len([f for f in sent_feedback if f.status == 'responded']),
            'high_priority': len([f for f in received_feedback if f.priority == 'high']),
            'medium_priority': len([f for f in received_feedback if f.priority == 'medium']),
            'low_priority': len([f for f in received_feedback if f.priority == 'low'])
        }
        
        return stats
    except Exception as e:
        print(f"获取反馈统计失败: {e}")
        return {}


# === AI 与搜索相关的辅助函数（Gemini 优先，环境变量注入密钥） ===
def _format_feedback_items(feedback_list: List[Feedback]) -> List[Dict[str, Any]]:
    formatted: List[Dict[str, Any]] = []
    for f in feedback_list:
        try:
            formatted.append({
                'category': f.category,
                'type': getattr(f, 'feedback_type', ''),
                'priority': f.priority,
                'content': f.content,
                'created_at': f.created_at.isoformat() if getattr(f, 'created_at', None) else ''
            })
        except Exception:
            continue
    return formatted

def generate_feedback_summary(received_feedback: List[Feedback]) -> Dict[str, Any]:
    """基于收到的反馈生成总结：优点/缺点。优先调用OpenAI；失败则基于规则回退。"""
    items = _format_feedback_items(received_feedback)
    if not items:
        return {"strengths": [], "weaknesses": []}

    prompt = (
        "你是一名资深学习与反馈分析顾问。请阅读以下员工收到的反馈列表（JSON数组），"
        "总结其主要优点(strengths)与主要缺点(weaknesses)。"
        "用简体中文输出严格的JSON对象：{\"strengths\":[...],\"weaknesses\":[...] }，"
        "每项尽量不超过20字，数量各3-6条。\n\n"
        f"反馈数据: {json.dumps(items, ensure_ascii=False)}\n"
        "只输出JSON，不要解释、不要Markdown。"
    )
    data: Dict[str, Any] = {}
    try:
        text = _gemini_generate(prompt, max_tokens=600) or ''
        cleaned = text.replace('```json', '').replace('```', '').strip()
        m = re.search(r"\{[\s\S]*\}", cleaned)
        candidate = m.group(0) if m else cleaned
        maybe = json.loads(candidate)
        if isinstance(maybe, dict):
            data = maybe
    except Exception:
        data = {}
    if data.get('strengths') or data.get('weaknesses'):
        return {
            'strengths': [s for s in (data.get('strengths') or []) if isinstance(s, str)][:6],
            'weaknesses': [w for w in (data.get('weaknesses') or []) if isinstance(w, str)][:6],
        }

    # 规则回退：基于关键词的粗略统计
    positive_keywords = ["优秀", "出色", "清晰", "主动", "高效", "准确", "合作", "沟通良好", "有条理"]
    negative_keywords = ["延迟", "不足", "缺陷", "需要改进", "不清晰", "沟通问题", "错误", "低效", "不及时"]

    pos_counts: Dict[str, int] = {}
    neg_counts: Dict[str, int] = {}
    for it in items:
        text = (it.get('content') or '')
        for kw in positive_keywords:
            if kw in text:
                pos_counts[kw] = pos_counts.get(kw, 0) + 1
        for kw in negative_keywords:
            if kw in text:
                neg_counts[kw] = neg_counts.get(kw, 0) + 1

    strengths = sorted(pos_counts, key=pos_counts.get, reverse=True)[:5]
    weaknesses = sorted(neg_counts, key=neg_counts.get, reverse=True)[:5]

    # 若没有匹配，基于类别兜底
    if not strengths:
        strengths = ["积极配合", "执行到位"]
    if not weaknesses:
        weaknesses = ["沟通需要更主动", "时间管理待提升"]

    return {
        'strengths': strengths,
        'weaknesses': weaknesses,
    }


def _search_courses(query: str, max_results: int = 3) -> List[Dict[str, str]]:
    results: List[Dict[str, str]] = []
    try:
        if DDGS is None:
            return results
        # 多区域、多策略重试，避免地区/网络限制导致空结果
        regions = ['wt-wt', 'us-en', 'cn-zh']
        safes = ['moderate', 'off']
        with DDGS() as ddg:
            for rg in regions:
                for sf in safes:
                    try:
                        for r in ddg.text(query, max_results=max_results, region=rg, safesearch=sf, timelimit='y'):
                            url = r.get('href') or r.get('url') or ''
                            title = r.get('title') or r.get('body') or '相关课程'
                            body = r.get('body') or ''
                            if url:
                                results.append({'title': title, 'url': url, 'snippet': body})
                        if results:
                            return results
                    except Exception:
                        continue
    except Exception:
        results = []
    # 回退：直接生成主流平台站内搜索链接，确保页面可点击
    if not results:
        try:
            q = quote_plus(query)
            candidates = [
                {'title': 'Coursera 搜索', 'url': f'https://www.coursera.org/search?query={q}', 'snippet': 'Coursera 课程搜索'},
                {'title': '网易公开课/中国大学MOOC', 'url': f'https://www.icourse163.org/search.htm?search={q}', 'snippet': '中国大学MOOC 搜索'},
                {'title': 'Udemy 搜索', 'url': f'https://www.udemy.com/courses/search/?q={q}', 'snippet': 'Udemy 课程搜索'},
                {'title': 'Class Central 搜索', 'url': f'https://www.classcentral.com/search?q={q}', 'snippet': 'Class Central 课程聚合'},
            ]
            return candidates[:max_results]
        except Exception:
            return []
    return results


def generate_learning_suggestions(summary: Dict[str, Any], user: User) -> List[Dict[str, Any]]:
    """根据总结提出学习建议，并检索课程链接（优先内置课程库 + Gemini 主题 + 搜索补齐）。

    逻辑调整：即使没有 AI 总结（summary 为空），也提供内置精选课程链接，保证页面上始终有可点击的外部课程超链接。
    """
    # 即使 summary 为空也不提前返回，保证能展示内置课程链接
    weaknesses: List[str] = (summary or {}).get('weaknesses') or []

    # 让 Gemini 先基于总结推荐主题（带搜索关键词），失败则走规则兜底
    dedup_topics: List[str] = []
    search_keywords: Dict[str, str] = {}
    try:
        prompt = (
            "基于以下反馈总结，提出3个针对性的学习主题，并给出每个主题的中文搜索关键词。"
            "输出严格JSON：{\"topics\":[{\"topic\":...,\"keyword\":...}, ...]}。\n\n"
            f"总结：{json.dumps(summary, ensure_ascii=False)}\n只输出JSON。"
        )
        text = _gemini_generate(prompt, max_tokens=400) or ''
        cleaned = text.replace('```json', '').replace('```', '').strip()
        m = re.search(r"\{[\s\S]*\}", cleaned)
        candidate = m.group(0) if m else cleaned
        obj = json.loads(candidate)
        arr = obj.get('topics') if isinstance(obj, dict) else []
        for it in arr or []:
            t = str(it.get('topic', '')).strip()
            k = str(it.get('keyword', '')).strip() or t
            if t and t not in dedup_topics:
                dedup_topics.append(t)
                search_keywords[t] = k
    except Exception:
        dedup_topics = []

    if not dedup_topics:
        dedup_topics = _match_topics_from_weaknesses(weaknesses)
        if not dedup_topics:
            dedup_topics = ["持续学习方法论", "目标管理(OKR)", "有效反馈的接收与落实"]

    # 结合主题：先取内置课程库，若不足再用搜索补齐
    recommendations: List[Dict[str, Any]] = []
    for t in dedup_topics:
        keyword = search_keywords.get(t, t)
        # 先优先返回精挑细选的课程库（可点击超链接）
        curated = _get_curated_links_for_topic(t, limit=3)
        links = list(curated)
        if len(links) < 3:
            query = f"{keyword} 在线课程 site:coursera.org OR site:icourse163.org OR site:udemy.com OR site:classcentral.com"
            more = _search_courses(query, max_results=(3 - len(links)))
            if not more:
                more = _search_courses(f"{keyword} 在线课程", max_results=(3 - len(links)))
            links.extend(more)
        recommendations.append({
            'topic': t,
            'links': links,
            'reason': f"围绕弱项'{t}'进行针对性提升",
        })

    return recommendations


# === 主题匹配与内置课程库（≥50条，全部超链接可点击） ===
def _match_topics_from_weaknesses(weaknesses: List[str]) -> List[str]:
    topics: List[str] = []
    for w in weaknesses or []:
        w = str(w or '').strip()
        if not w:
            continue
        if any(k in w for k in ["沟通", "表达", "跨部门", "协作", "会议", "演讲", "倾听"]):
            topics.append("职场沟通与跨部门协作")
        elif any(k in w for k in ["时间", "进度", "延期", "拖延", "优先级", "节奏"]):
            topics.append("时间管理与任务优先级")
        elif any(k in w for k in ["需求", "不清晰", "文档", "规范", "验收", "范围", "变更", "UAT"]):
            topics.append("需求澄清与文档规范")
        elif any(k in w for k in ["效率", "流程", "低效", "优化", "复盘", "交付", "质量", "缺陷"]):
            topics.append("工作流程优化与复盘")
        elif any(k in w for k in ["目标", "OKR", "KPI", "对齐"]):
            topics.append("目标管理(OKR)")
        elif any(k in w for k in ["反馈", "回顾", "改进建议"]):
            topics.append("有效反馈的接收与落实")
        elif any(k in w for k in ["学习", "成长", "方法", "自驱", "习惯"]):
            topics.append("持续学习方法论")
    # 去重并截断
    dedup: List[str] = []
    for t in topics:
        if t not in dedup:
            dedup.append(t)
    return dedup[:3]


CURATED_COURSES: Dict[str, List[Dict[str, str]]] = {
    # 职场沟通与跨部门协作（10）
    "职场沟通与跨部门协作": [
        {"title": "Improving Communication Skills (宾大)", "url": "https://www.coursera.org/learn/wharton-communication-skills", "snippet": "沟通技巧与影响力"},
        {"title": "Teamwork Skills: Communicating Effectively (UCI)", "url": "https://www.coursera.org/learn/teamwork-skills-effective-communication", "snippet": "团队沟通与协作"},
        {"title": "Successful Negotiation (密歇根)", "url": "https://www.coursera.org/learn/negotiation", "snippet": "谈判与双赢"},
        {"title": "High-Impact Business Writing (UCI)", "url": "https://www.coursera.org/learn/high-impact-writing", "snippet": "商务写作"},
        {"title": "Presentation Skills (华盛顿大学)", "url": "https://www.coursera.org/learn/public-speaking", "snippet": "演讲与表达"},
        {"title": "跨部门沟通技巧 搜索-中国大学MOOC", "url": "https://www.icourse163.org/search.htm?search=%E8%B7%A8%E9%83%A8%E9%97%A8%E6%B2%9F%E9%80%9A", "snippet": "中文课程聚合"},
        {"title": "Effective Communication: Writing, Design, and Presentation", "url": "https://www.coursera.org/specializations/effective-business-communication", "snippet": "沟通专项"},
        {"title": "Business Communication (IIMB)", "url": "https://www.edx.org/course/business-communication", "snippet": "edX 商务沟通"},
        {"title": "Communication Fundamentals (Udemy)", "url": "https://www.udemy.com/course/communication-fundamentals-how-to-communicate-better", "snippet": "Udemy 沟通基础"},
        {"title": "Active Listening (Udemy)", "url": "https://www.udemy.com/course/active-listening-masterclass", "snippet": "积极倾听"},
    ],
    # 时间管理与任务优先级（8）
    "时间管理与任务优先级": [
        {"title": "Work Smarter, Not Harder (UCI)", "url": "https://www.coursera.org/learn/work-smarter-not-harder", "snippet": "时间管理"},
        {"title": "Get Beyond Work-Life Balance (UC Irvine)", "url": "https://www.coursera.org/learn/work-life-balance", "snippet": "效率与平衡"},
        {"title": "Time Management Mastery (Udemy)", "url": "https://www.udemy.com/course/time-management-mastery-do-more-stress-less", "snippet": "Udemy 时间管理"},
        {"title": "Productivity and Time Management (Udemy)", "url": "https://www.udemy.com/course/productivity-time-management", "snippet": "效率提升"},
        {"title": "项目时间管理 搜索-中国大学MOOC", "url": "https://www.icourse163.org/search.htm?search=%E6%97%B6%E9%97%B4%E7%AE%A1%E7%90%86", "snippet": "中文课程聚合"},
        {"title": "Google Project Management", "url": "https://www.coursera.org/professional-certificates/google-project-management", "snippet": "项目管理职业证书"},
        {"title": "Agile Project Management (UVA)", "url": "https://www.coursera.org/learn/agile-project-management", "snippet": "敏捷项目管理"},
        {"title": "Project Planning: Putting It All Together (Google)", "url": "https://www.coursera.org/learn/project-planning-google", "snippet": "计划与优先级"},
    ],
    # 需求澄清与文档规范（8）
    "需求澄清与文档规范": [
        {"title": "Business Analysis Fundamentals (Udemy)", "url": "https://www.udemy.com/course/business-analysis-fundamentals", "snippet": "业务分析基础"},
        {"title": "Requirements Engineering: Secure Software (edX)", "url": "https://www.edx.org/course/requirements-engineering-secure-software-specification", "snippet": "需求工程"},
        {"title": "Software Processes and Agile Practices (Alberta)", "url": "https://www.coursera.org/learn/software-processes-and-agile-practices", "snippet": "软件过程与文档"},
        {"title": "UAT & Acceptance Testing (Udemy)", "url": "https://www.udemy.com/course/user-acceptance-testing-uat", "snippet": "用户验收测试"},
        {"title": "需求工程 搜索-中国大学MOOC", "url": "https://www.icourse163.org/search.htm?search=%E9%9C%80%E6%B1%82%E5%B7%A5%E7%A8%8B", "snippet": "中文课程聚合"},
        {"title": "Business Writing (Coursera)", "url": "https://www.coursera.org/specializations/improve-business-writing", "snippet": "需求文档写作"},
        {"title": "Confluence for Documentation (Udemy)", "url": "https://www.udemy.com/course/confluence-complete-guide", "snippet": "知识库文档"},
        {"title": "API Documentation (Udemy)", "url": "https://www.udemy.com/course/technical-writing-how-to-write-software-documentation", "snippet": "技术文档"},
    ],
    # 工作流程优化与复盘（8）
    "工作流程优化与复盘": [
        {"title": "Six Sigma Yellow Belt (Coursera)", "url": "https://www.coursera.org/learn/six-sigma-define-measure-analyze", "snippet": "六西格玛入门"},
        {"title": "Lean Six Sigma (Udemy)", "url": "https://www.udemy.com/course/lean-six-sigma-white-belt", "snippet": "精益六西格玛"},
        {"title": "Kaizen Continuous Improvement (Udemy)", "url": "https://www.udemy.com/course/kaizen-continuous-improvement", "snippet": "持续改进"},
        {"title": "DevOps Foundations (Coursera)", "url": "https://www.coursera.org/learn/devops-culture-and-mindset", "snippet": "DevOps 文化"},
        {"title": "Agile with Atlassian Jira (Coursera)", "url": "https://www.coursera.org/learn/agile-development", "snippet": "敏捷与Jira"},
        {"title": "流程优化 搜索-中国大学MOOC", "url": "https://www.icourse163.org/search.htm?search=%E6%B5%81%E7%A8%8B%E4%BC%98%E5%8C%96", "snippet": "中文课程聚合"},
        {"title": "Root Cause Analysis (Udemy)", "url": "https://www.udemy.com/course/root-cause-analysis-problem-solving", "snippet": "根因分析"},
        {"title": "Quality Management (edX)", "url": "https://www.edx.org/course/quality-management", "snippet": "质量管理"},
    ],
    # 持续学习方法论（6）
    "持续学习方法论": [
        {"title": "Learning How to Learn (Coursera)", "url": "https://www.coursera.org/learn/learning-how-to-learn", "snippet": "学习如何学习"},
        {"title": "Mindshift: Break Through Obstacles (Coursera)", "url": "https://www.coursera.org/learn/mindshift", "snippet": "学习心智"},
        {"title": "Ultralearning (Udemy)", "url": "https://www.udemy.com/course/ultralearning", "snippet": "深度学习术（自我提升）"},
        {"title": "元学习与认知提升 搜索-中国大学MOOC", "url": "https://www.icourse163.org/search.htm?search=%E5%AD%A6%E4%B9%A0%E6%96%B9%E6%B3%95", "snippet": "中文课程聚合"},
        {"title": "Becoming a Super Learner (Udemy)", "url": "https://www.udemy.com/course/superlearner", "snippet": "快速学习"},
        {"title": "Learning Strategies (edX)", "url": "https://www.edx.org/learn/learning-skills", "snippet": "学习策略"},
    ],
    # 目标管理(OKR)（5）
    "目标管理(OKR)": [
        {"title": "Introduction to OKRs (Coursera)", "url": "https://www.coursera.org/learn/okrs", "snippet": "OKR 入门"},
        {"title": "Goal Setting: Objectives and Key Results (Udemy)", "url": "https://www.udemy.com/course/okr-objectives-and-key-results", "snippet": "OKR 实战"},
        {"title": "OKR 实践 搜索-中国大学MOOC", "url": "https://www.icourse163.org/search.htm?search=OKR", "snippet": "中文课程聚合"},
        {"title": "Performance Management (Coursera)", "url": "https://www.coursera.org/learn/performance-management", "snippet": "绩效与目标"},
        {"title": "Agile OKRs (Udemy)", "url": "https://www.udemy.com/course/agile-okrs", "snippet": "敏捷与OKR"},
    ],
    # 有效反馈的接收与落实（5）
    "有效反馈的接收与落实": [
        {"title": "Giving and Receiving Feedback (Coursera)", "url": "https://www.coursera.org/learn/giving-and-receiving-feedback", "snippet": "反馈技巧"},
        {"title": "Difficult Conversations (Udemy)", "url": "https://www.udemy.com/course/difficult-conversations-masterclass", "snippet": "困难对话"},
        {"title": "Constructive Feedback (Udemy)", "url": "https://www.udemy.com/course/constructive-feedback", "snippet": "建设性反馈"},
        {"title": "反馈与复盘 搜索-中国大学MOOC", "url": "https://www.icourse163.org/search.htm?search=%E5%8F%8D%E9%A6%88", "snippet": "中文课程聚合"},
        {"title": "Leadership Communication (edX)", "url": "https://www.edx.org/learn/leadership-communication", "snippet": "领导者反馈沟通"},
    ],
}


def _get_curated_links_for_topic(topic_display: str, limit: int = 3) -> List[Dict[str, str]]:
    arr = CURATED_COURSES.get(topic_display) or []
    return arr[:max(0, min(limit, len(arr)))]

def create_feedback_notification(feedback_id, recipient_id, sender_id):
    """创建反馈通知"""
    try:
        recipient = User.query.get(recipient_id)
        recipient_name = f"{recipient.first_name} {recipient.last_name}"
        
        notification = FeedbackNotification(
            user_id=recipient_id,
            feedback_id=feedback_id,
            notification_type='new_feedback',
            title=f'新反馈',
            message=f'{recipient_name}已发送新反馈给您',
            is_read=False
        )
        db.session.add(notification)
        db.session.commit()
        return True
    except Exception as e:
        print(f"创建反馈通知失败: {e}")
        db.session.rollback()
        return False

def create_response_notification(feedback_id, sender_id, responder_id):
    """创建回复通知"""
    try:
        responder = User.query.get(responder_id)
        responder_name = f"{responder.first_name} {responder.last_name}"
        
        notification = FeedbackNotification(
            user_id=sender_id,
            feedback_id=feedback_id,
            notification_type='feedback_responded',
            title=f'反馈已回复',
            message=f'{responder_name}已回复了您的反馈',
            is_read=False
        )
        db.session.add(notification)
        db.session.commit()
        return True
    except Exception as e:
        print(f"创建回复通知失败: {e}")
        db.session.rollback()
        return False
