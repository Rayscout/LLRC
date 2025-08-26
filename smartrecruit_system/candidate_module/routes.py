from flask import Blueprint, render_template, g, session, redirect, url_for, flash, jsonify, request
from .profile import profile_bp
from .jobs import jobs_bp
from .applications import applications_bp
from .interview import interview_bp
from app.utils import extract_text_from_resume, ai_analyze_resume_text

# 创建求职者主蓝图
candidate_bp = Blueprint('candidate', __name__, url_prefix='/candidate')

# 注意：之前为了清空界面加入过统一占位的 before_request 钩子，此处已移除，恢复正常页面渲染。

@candidate_bp.route('/')
def home():
    """候选人首页 - 智能推荐（全新界面）"""
    if g.user is None:
        from flask import redirect, url_for, flash
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    # 用户技能
    try:
        from .jobs import extract_user_skills
        user_skills = extract_user_skills(g.user)
    except Exception:
        user_skills = []

    # 生成简历AI分析（轻量运行，失败忽略）
    resume_analysis = None
    try:
        cv_text = ''
        if getattr(g.user, 'cv_data', None) and getattr(g.user, 'cv_file', None):
            cv_text = extract_text_from_resume(g.user.cv_data, g.user.cv_file) or ''
        if cv_text:
            resume_analysis = ai_analyze_resume_text(cv_text)
    except Exception:
        resume_analysis = None

    # 智能推荐：基于匹配度排序
    try:
        from .jobs import get_job_recommendations
        recommended = get_job_recommendations(g.user)
    except Exception:
        recommended = []

    return render_template(
        'smartrecruit/candidate/home_recommend.html',
        user=g.user,
        user_skills=user_skills,
        recommended_jobs=recommended
    )

@candidate_bp.route('/dashboard')
def dashboard():
    """候选人仪表盘 - 综合功能"""
    if g.user is None:
        from flask import redirect, url_for, flash
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    try:
        from .jobs import extract_user_skills
        user_skills = extract_user_skills(g.user)
    except Exception:
        user_skills = []

    # 获取统计数据
    try:
        from .applications import get_user_applications_count
        applications_count = get_user_applications_count(g.user.id)
    except Exception:
        applications_count = 0

    try:
        from .jobs import get_user_saved_jobs_count
        saved_jobs_count = get_user_saved_jobs_count(g.user.id)
    except Exception:
        saved_jobs_count = 0

    # 计算资料完整度
    profile_completion = calculate_profile_completion(g.user)

    return render_template('smartrecruit/candidate/dashboard_new.html', 
                         user=g.user,
                         user_skills=user_skills,
                         applications_count=applications_count,
                         saved_jobs_count=saved_jobs_count,
                         profile_completion=profile_completion)

def calculate_profile_completion(user):
    """计算用户资料完整度"""
    fields = [
        user.first_name, user.last_name, user.email, user.phone_number,
        user.birthday, user.company_name, user.position, user.cv_file
    ]
    
    filled_fields = sum(1 for field in fields if field)
    total_fields = len(fields)
    
    return int((filled_fields / total_fields) * 100)

@candidate_bp.route('/logout')
def logout():
    """求职者登出"""
    session.pop('user_id', None)
    session.pop('user_type', None)
    session.clear()
    flash('您已退出登录。', 'success')
    return redirect(url_for('common.auth.logout'))

@candidate_bp.route('/settings')
def settings():
    """求职者设置页面"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    return redirect(url_for('smartrecruit.candidate.profile.settings'))

# API路由
@candidate_bp.route('/api/dashboard-stats')
def dashboard_stats():
    """获取仪表板统计数据"""
    if g.user is None:
        return jsonify({'success': False, 'message': '请先登录'})
    
    try:
        # 获取今日新增职位数
        from .jobs import get_new_jobs_count
        new_jobs_count = get_new_jobs_count()
        
        # 获取待处理申请数
        from .applications import get_pending_applications_count
        pending_applications = get_pending_applications_count(g.user.id)
        
        # 获取面试练习次数
        from .interview import get_interview_count
        interview_count = get_interview_count(g.user.id)
        
        # 获取申请成功率
        from .applications import get_success_rate
        success_rate = get_success_rate(g.user.id)
        
        return jsonify({
            'success': True,
            'data': {
                'new_jobs_count': new_jobs_count,
                'pending_applications': pending_applications,
                'interview_count': interview_count,
                'success_rate': success_rate
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@candidate_bp.route('/api/save-job', methods=['POST'])
def save_job():
    """收藏职位"""
    if g.user is None:
        return jsonify({'success': False, 'message': '请先登录'})
    
    try:
        data = request.get_json()
        job_id = data.get('job_id')
        
        if not job_id:
            return jsonify({'success': False, 'message': '职位ID不能为空'})
        
        from .jobs import save_job_for_user
        result = save_job_for_user(g.user.id, job_id)
        
        if result:
            return jsonify({'success': True, 'message': '职位收藏成功'})
        else:
            return jsonify({'success': False, 'message': '职位收藏失败'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@candidate_bp.route('/api/recommended-jobs')
def recommended_jobs():
    """获取推荐职位"""
    if g.user is None:
        return jsonify({'success': False, 'message': '请先登录'})
    
    try:
        from .jobs import get_recommended_jobs
        jobs = get_recommended_jobs(g.user.id)
        
        return jsonify({
            'success': True,
            'data': jobs
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@candidate_bp.route('/api/user-skills')
def user_skills():
    """获取用户技能"""
    if g.user is None:
        return jsonify({'success': False, 'message': '请先登录'})
    
    try:
        from .jobs import extract_user_skills
        skills = extract_user_skills(g.user)
        
        return jsonify({
            'success': True,
            'data': skills
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@candidate_bp.route('/api/update-skills', methods=['POST'])
def update_skills():
    """更新用户技能"""
    if g.user is None:
        return jsonify({'success': False, 'message': '请先登录'})
    
    try:
        data = request.get_json()
        skills = data.get('skills', [])
        
        from .profile import update_user_skills
        result = update_user_skills(g.user.id, skills)
        
        if result:
            return jsonify({'success': True, 'message': '技能更新成功'})
        else:
            return jsonify({'success': False, 'message': '技能更新失败'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@candidate_bp.route('/api/analyze-resume')
def analyze_resume():
    """分析简历"""
    if g.user is None:
        return jsonify({'success': False, 'message': '请先登录'})
    
    try:
        if not g.user.cv_file:
            return jsonify({'success': False, 'message': '请先上传简历'})
        
        cv_text = extract_text_from_resume(g.user.cv_data, g.user.cv_file)
        if cv_text:
            analysis = ai_analyze_resume_text(cv_text)
            return jsonify({
                'success': True,
                'data': analysis
            })
        else:
            return jsonify({'success': False, 'message': '简历内容解析失败'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@candidate_bp.route('/test')
def test_dashboard():
    """测试页面"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    return render_template('smartrecruit/candidate/test_dashboard.html', user=g.user)

@candidate_bp.route('/ios-preview')
def ios_preview():
    """iOS风格预览页面"""
    return render_template('smartrecruit/candidate/ios_preview.html')

# 注册子蓝图
candidate_bp.register_blueprint(profile_bp, url_prefix='/profile')
candidate_bp.register_blueprint(jobs_bp, url_prefix='/jobs')
candidate_bp.register_blueprint(applications_bp, url_prefix='/applications')
candidate_bp.register_blueprint(interview_bp, url_prefix='/interview')
