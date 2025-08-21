from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, jsonify
from app.models import Job, db
import logging

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/')
def job_list():
    """职位列表页面"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    try:
        # 获取所有职位（移除status过滤，因为Job模型没有这个字段）
        jobs = Job.query.order_by(Job.date_posted.desc()).all()
        
        # 获取推荐职位（基于用户技能）
        recommended_jobs = get_job_recommendations(g.user)
        
        # 获取用户技能
        user_skills = extract_user_skills(g.user)
        
    except Exception as e:
        flash('获取职位列表失败，请稍后重试。', 'danger')
        jobs = []
        recommended_jobs = []
        user_skills = []
    
    return render_template('smartrecruit/candidate/snippet_career_list.html', 
                         jobs=jobs, 
                         recommended_jobs=recommended_jobs,
                         user_skills=user_skills)

@jobs_bp.route('/<int:job_id>')
def job_detail(job_id):
    """职位详情页面"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    try:
        job = Job.query.get_or_404(job_id)
        return render_template('smartrecruit/candidate/job_detail.html', job=job)
    except Exception as e:
        flash('获取职位详情失败，请稍后重试。', 'danger')
        return redirect(url_for('smartrecruit.candidate.jobs.job_list'))

@jobs_bp.route('/search')
def job_search():
    """职位搜索页面"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    query = request.args.get('q', '')
    location = request.args.get('location', '')
    
    try:
        # 构建查询（移除status过滤）
        jobs_query = Job.query
        
        if query:
            jobs_query = jobs_query.filter(Job.title.contains(query) | Job.description.contains(query))
        
        if location:
            jobs_query = jobs_query.filter(Job.location.contains(location))
        
        jobs = jobs_query.order_by(Job.date_posted.desc()).all()
    except Exception as e:
        flash('搜索职位失败，请稍后重试。', 'danger')
        jobs = []
    
    return render_template('smartrecruit/candidate/job_search.html', 
                         jobs=jobs, 
                         query=query, 
                         location=location)

@jobs_bp.route('/recommendations')
def job_recommendations():
    """获取职位推荐"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    try:
        # 获取推荐职位
        recommendations = get_job_recommendations(g.user)
        
        # 转换为字典格式
        recommendations_data = []
        for rec in recommendations:
            recommendations_data.append({
                'id': rec['job'].id,
                'title': rec['job'].title,
                'company_name': getattr(rec['job'], 'company_name', ''),
                'location': rec['job'].location,
                'salary': rec['job'].salary,
                'match_score': rec['match_score']
            })
        
        return jsonify({
            'success': True,
            'recommendations': recommendations_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'推荐失败: {str(e)}'
        }), 500

@jobs_bp.route('/api/search_jobs')
def api_search_jobs():
    """智能搜索API"""
    if g.user is None:
        return jsonify({'error': '请先登录'}), 401
    
    try:
        query = request.args.get('q', '')
        location = request.args.get('location', '')
        salary_min = request.args.get('salary_min', type=float)
        salary_max = request.args.get('salary_max', type=float)
        job_type = request.args.get('job_type', '')
        experience_level = request.args.get('experience_level', '')
        
        # 构建查询
        jobs_query = Job.query
        
        if query:
            jobs_query = jobs_query.filter(Job.title.contains(query) | Job.description.contains(query))
        
        if location:
            jobs_query = jobs_query.filter(Job.location.contains(location))
        
        if salary_min is not None:
            jobs_query = jobs_query.filter(Job.salary >= salary_min)
        
        if salary_max is not None:
            jobs_query = jobs_query.filter(Job.salary <= salary_max)
        
        if job_type:
            jobs_query = jobs_query.filter(Job.job_type == job_type)
        
        if experience_level:
            jobs_query = jobs_query.filter(Job.experience_level == experience_level)
        
        jobs = jobs_query.order_by(Job.date_posted.desc()).all()
        
        # 计算技能匹配度
        jobs_with_match = []
        for job in jobs:
            match_score = calculate_job_match(g.user, job)
            jobs_with_match.append({
                'id': job.id,
                'title': job.title,
                'company_name': getattr(job, 'company_name', ''),
                'location': job.location,
                'salary': job.salary,
                'description': job.description[:200] + '...' if len(job.description) > 200 else job.description,
                'match_score': match_score
            })
        
        # 按匹配度排序
        jobs_with_match.sort(key=lambda x: x['match_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'jobs': jobs_with_match,
            'total': len(jobs_with_match)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'搜索失败: {str(e)}'
        }), 500

def get_job_recommendations(user):
    """获取职位推荐"""
    try:
        # 获取所有职位
        all_jobs = Job.query.all()
        
        # 计算每个职位的匹配度
        job_matches = []
        for job in all_jobs:
            match_score = calculate_job_match(user, job)
            job_matches.append({
                'job': job,
                'match_score': match_score
            })
        
        # 按匹配度排序，取前5个
        job_matches.sort(key=lambda x: x['match_score'], reverse=True)
        return job_matches[:5]
        
    except Exception as e:
        logging.error(f"获取职位推荐失败: {e}")
        return []

def calculate_job_match(user, job):
    """计算职位匹配度"""
    try:
        # 获取用户技能
        user_skills = extract_user_skills(user)
        if not user_skills:
            return 50  # 默认50%匹配度
        
        # 从职位描述中提取关键词
        job_keywords = extract_job_keywords(job.description)
        
        # 计算技能匹配度
        matched_skills = 0
        for skill in user_skills:
            if any(keyword.lower() in skill.lower() for keyword in job_keywords):
                matched_skills += 1
        
        # 计算匹配百分比
        match_percentage = (matched_skills / len(user_skills)) * 100
        
        # 确保在0-100范围内
        return max(0, min(100, int(match_percentage)))
        
    except Exception as e:
        logging.error(f"计算职位匹配度失败: {e}")
        return 50

def extract_user_skills(user):
    """提取用户技能"""
    try:
        skills = []
        
        # 从简历数据中提取技能
        if hasattr(user, 'cv_data') and user.cv_data:
            # 这里可以添加简历解析逻辑
            pass
        
        # 从职位字段中提取技能
        if hasattr(user, 'position') and user.position:
            skills.append(user.position)
        
        # 如果没有技能，返回默认技能
        if not skills:
            skills = ['计算机科学', '编程', '软件开发']
        
        return skills
        
    except Exception as e:
        logging.error(f"提取用户技能失败: {e}")
        return ['计算机科学', '编程', '软件开发']

def extract_job_keywords(description):
    """从职位描述中提取关键词"""
    try:
        if not description:
            return []
        
        # 简单的关键词提取（可以后续优化为NLP）
        keywords = []
        common_skills = [
            'python', 'java', 'javascript', 'react', 'vue', 'angular',
            'node.js', 'spring', 'django', 'flask', 'mysql', 'mongodb',
            'docker', 'kubernetes', 'aws', 'azure', 'git', 'agile',
            'scrum', 'ui/ux', 'design', 'marketing', 'sales', 'management'
        ]
        
        description_lower = description.lower()
        for skill in common_skills:
            if skill in description_lower:
                keywords.append(skill)
        
        return keywords
        
    except Exception as e:
        logging.error(f"提取职位关键词失败: {e}")
        return []
