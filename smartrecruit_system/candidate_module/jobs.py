from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, jsonify
from app.models import Job, db
import logging
from .recommendation_config import (
    RECOMMENDATION_WEIGHTS, SKILL_CATEGORIES, CHINESE_SKILLS, 
    EXPERIENCE_LEVELS, RECOMMENDATION_PARAMS, COMPANY_SKILL_MAPPING,
    OPTIMIZATION_CONFIG
)

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/home')
def home_recommended():
    """候选人首页：仅展示为您推荐的岗位"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    try:
        recommended_jobs = get_job_recommendations(g.user)
        user_skills = extract_user_skills(g.user)
    except Exception:
        recommended_jobs = []
        user_skills = []

    return render_template(
        'smartrecruit/candidate/home_recommended.html',
        recommended_jobs=recommended_jobs,
        user_skills=user_skills,
    )

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

    # 提供 user_skills 给模板（某些脚本会读取）
    try:
        user_skills = extract_user_skills(g.user)
    except Exception:
        user_skills = []

    return render_template('smartrecruit/candidate/job_search.html', 
                         jobs=jobs, 
                         query=query, 
                         location=location,
                         user_skills=user_skills)

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
                'job_type': getattr(rec['job'], 'job_type', '全职'),
                'experience_level': getattr(rec['job'], 'experience_level', '不限'),
                'description': rec['job'].description[:200] + '...' if len(rec['job'].description) > 200 else rec['job'].description,
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
            
            # 应用优化因子
            optimized_score = apply_optimization_factors(user, job, match_score)
            
            # 只推荐匹配度达到最小要求的职位
            if optimized_score >= RECOMMENDATION_PARAMS['min_match_score']:
                job_matches.append({
                    'job': job,
                    'match_score': optimized_score
                })
        
        # 按匹配度排序，取前N个
        job_matches.sort(key=lambda x: x['match_score'], reverse=True)
        return job_matches[:RECOMMENDATION_PARAMS['max_recommendations']]
        
    except Exception as e:
        logging.error(f"获取职位推荐失败: {e}")
        return []

def apply_optimization_factors(user, job, base_score):
    """应用优化因子"""
    try:
        optimized_score = base_score
        
        # 新职位提升（7天内发布的职位）
        if OPTIMIZATION_CONFIG['enable_fresh_job_boost']:
            from datetime import datetime, timedelta
            if job.date_posted and (datetime.utcnow() - job.date_posted).days <= 7:
                optimized_score *= RECOMMENDATION_PARAMS['fresh_job_boost']
        
        # 公司类型匹配提升
        if OPTIMIZATION_CONFIG['enable_company_type_boost']:
            company_boost = calculate_company_type_boost(user, job)
            optimized_score *= company_boost
        
        # 技能匹配提升
        if OPTIMIZATION_CONFIG['enable_skill_boost']:
            skill_boost = calculate_skill_boost(user, job)
            optimized_score *= skill_boost
        
        return min(100, optimized_score)  # 确保不超过100分
        
    except Exception as e:
        logging.error(f"应用优化因子失败: {e}")
        return base_score

def calculate_company_type_boost(user, job):
    """计算公司类型匹配提升"""
    try:
        user_company = getattr(user, 'company_name', '').lower()
        job_company = getattr(job, 'company_name', '').lower()
        
        for company_type, config in COMPANY_SKILL_MAPPING.items():
            # 检查用户公司类型
            user_company_match = any(keyword in user_company for keyword in config['keywords'])
            # 检查职位公司类型
            job_company_match = any(keyword in job_company for keyword in config['keywords'])
            
            if user_company_match and job_company_match:
                return 1.1  # 相同公司类型提升10%
        
        return 1.0
        
    except Exception as e:
        logging.error(f"计算公司类型提升失败: {e}")
        return 1.0

def calculate_skill_boost(user, job):
    """计算技能匹配提升"""
    try:
        user_skills = extract_user_skills(user)
        job_keywords = extract_job_keywords(job.description)
        
        if not user_skills or not job_keywords:
            return 1.0
        
        # 计算技能匹配数量
        matched_skills = 0
        for skill in user_skills:
            if any(keyword.lower() in skill.lower() for keyword in job_keywords):
                matched_skills += 1
        
        # 如果匹配的技能超过50%，给予提升
        match_ratio = matched_skills / len(user_skills)
        if match_ratio > 0.5:
            return RECOMMENDATION_PARAMS['skill_boost_factor']
        
        return 1.0
        
    except Exception as e:
        logging.error(f"计算技能提升失败: {e}")
        return 1.0

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
        
        # 基础匹配分数
        skill_match_score = (matched_skills / len(user_skills)) * 100 * RECOMMENDATION_WEIGHTS['skill_match']
        
        # 经验匹配分数
        experience_score = calculate_experience_match(user, job) * RECOMMENDATION_WEIGHTS['experience_match']
        
        # 薪资匹配分数
        salary_score = calculate_salary_match(user, job) * RECOMMENDATION_WEIGHTS['salary_match']
        
        # 地理位置匹配分数
        location_score = calculate_location_match(user, job) * RECOMMENDATION_WEIGHTS['location_match']
        
        # 综合匹配分数
        total_score = skill_match_score + experience_score + salary_score + location_score
        
        # 确保在0-100范围内
        return max(0, min(100, int(total_score)))
        
    except Exception as e:
        logging.error(f"计算职位匹配度失败: {e}")
        return 50

def calculate_experience_match(user, job):
    """计算经验匹配度"""
    try:
        # 从用户职位推断经验水平
        user_position = getattr(user, 'position', '').lower()
        job_experience = getattr(job, 'experience_level', '').lower()
        
        # 推断用户经验水平
        user_level = 2  # 默认中级
        for level_name, config in EXPERIENCE_LEVELS.items():
            if any(keyword in user_position for keyword in config['keywords']):
                user_level = config['level']
                break
        
        # 获取职位要求经验水平
        job_level = 2  # 默认中级
        for level_name, config in EXPERIENCE_LEVELS.items():
            if any(keyword in job_experience for keyword in config['keywords']):
                job_level = config['level']
                break
        
        # 计算匹配度（返回0-100的分数）
        level_diff = abs(user_level - job_level)
        if level_diff == 0:
            return 100  # 完全匹配
        elif level_diff == 1:
            return 75   # 接近匹配
        elif level_diff == 2:
            return 50   # 部分匹配
        else:
            return 25   # 低匹配
        
    except Exception as e:
        logging.error(f"计算经验匹配度失败: {e}")
        return 50

def calculate_salary_match(user, job):
    """计算薪资匹配度"""
    try:
        # 这里可以根据用户的薪资期望和职位薪资计算匹配度
        # 目前返回默认分数（返回0-100的分数）
        return 80  # 默认80%匹配度
        
    except Exception as e:
        logging.error(f"计算薪资匹配度失败: {e}")
        return 80

def calculate_location_match(user, job):
    """计算地理位置匹配度"""
    try:
        # 这里可以根据用户位置和职位位置计算匹配度
        # 目前返回默认分数（返回0-100的分数）
        return 80  # 默认80%匹配度
        
    except Exception as e:
        logging.error(f"计算地理位置匹配度失败: {e}")
        return 80

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
        
        # 从公司名称推断技能
        if hasattr(user, 'company_name') and user.company_name:
            company_skills = infer_skills_from_company(user.company_name)
            skills.extend(company_skills)
        
        # 如果没有技能，返回默认技能
        if not skills:
            skills = ['计算机科学', '编程', '软件开发', '项目管理', '团队协作']
        
        # 去重并返回
        return list(set(skills))
        
    except Exception as e:
        logging.error(f"提取用户技能失败: {e}")
        return ['计算机科学', '编程', '软件开发', '项目管理', '团队协作']

def infer_skills_from_company(company_name):
    """从公司名称推断技能"""
    company_lower = company_name.lower()
    skills = []
    
    # 使用配置文件中的公司类型技能映射
    for company_type, config in COMPANY_SKILL_MAPPING.items():
        if any(keyword in company_lower for keyword in config['keywords']):
            skills.extend(config['skills'])
    
    return skills

def extract_job_keywords(description):
    """从职位描述中提取关键词"""
    try:
        if not description:
            return []
        
        # 使用配置文件中的技能分类
        keywords = []
        description_lower = description.lower()
        
        # 从英文技能分类中提取
        for category, skills in SKILL_CATEGORIES.items():
            for skill in skills:
                if skill in description_lower:
                    keywords.append(skill)
        
        # 从中文技能分类中提取
        for category, skills in CHINESE_SKILLS.items():
            for skill in skills:
                if skill in description_lower:
                    keywords.append(skill)
        
        return list(set(keywords))  # 去重
        
    except Exception as e:
        logging.error(f"提取职位关键词失败: {e}")
        return []

def get_user_saved_jobs_count(user_id):
    """获取用户收藏职位数量"""
    try:
        # 这里可以添加实际的数据库查询逻辑
        # 目前返回模拟数据
        return 3  # 模拟数据
    except Exception:
        return 0
