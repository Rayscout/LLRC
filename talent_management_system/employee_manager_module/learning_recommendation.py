from flask import Blueprint, render_template, request, jsonify, g, flash, redirect, url_for
from app.models import User, Job, Application, db
import json
from datetime import datetime
import re

# 简单的登录检查装饰器
def login_required(f):
    def decorated_function(*args, **kwargs):
        # 暂时跳过登录检查，用于测试
        # if not hasattr(g, 'user') or g.user is None:
        #     flash('请先登录', 'warning')
        #     return redirect(url_for('common.auth.sign'))
        
        # 创建一个模拟用户用于测试
        if not hasattr(g, 'user'):
            from app.models import User
            # 使用第一个员工用户作为测试用户
            test_user = User.query.filter_by(user_type='employee').first()
            if not test_user:
                # 如果没有员工用户，创建一个模拟用户对象
                class MockUser:
                    def __init__(self):
                        self.id = 1
                        self.username = "测试员工"
                        self.bio = "我是一名Python开发工程师"
                        self.experience = "有3年Python开发经验"
                        self.education = "计算机科学学士"
                test_user = MockUser()
            g.user = test_user
        
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

learning_recommendation_bp = Blueprint('learning_recommendation', __name__, url_prefix='/learning_recommendation')

# 技能分类和权重配置
SKILL_CATEGORIES = {
    'technical': {
        'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift'],
        'database': ['mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'sqlite'],
        'framework': ['django', 'flask', 'spring', 'express', 'react', 'vue', 'angular', 'laravel'],
        'cloud': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'gitlab'],
        'ai_ml': ['tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib']
    },
    'soft_skills': {
        'communication': ['沟通', '演讲', '写作', '谈判', 'presentation'],
        'leadership': ['领导力', '团队管理', '项目管理', '决策', 'motivation'],
        'problem_solving': ['问题解决', '分析思维', '创新', 'critical thinking'],
        'collaboration': ['团队合作', '跨部门协作', 'conflict resolution']
    },
    'business': {
        'domain_knowledge': ['行业知识', '业务流程', '产品管理', '市场分析'],
        'analytics': ['数据分析', '商业智能', 'excel', 'tableau', 'powerbi'],
        'strategy': ['战略规划', '业务发展', '竞争分析', 'risk management']
    }
}

# 学习课程推荐配置
LEARNING_COURSES = {
    'technical': {
        'programming': {
            'beginner': [
                {'name': 'Python基础入门', 'duration': '4周', 'level': '初级', 'skills': ['python', '编程基础']},
                {'name': 'Java编程基础', 'duration': '6周', 'level': '初级', 'skills': ['java', '面向对象']},
                {'name': 'Web开发入门', 'duration': '8周', 'level': '初级', 'skills': ['html', 'css', 'javascript']}
            ],
            'intermediate': [
                {'name': 'Python进阶开发', 'duration': '6周', 'level': '中级', 'skills': ['python', 'django', 'flask']},
                {'name': 'Java企业级开发', 'duration': '8周', 'level': '中级', 'skills': ['java', 'spring', '微服务']},
                {'name': '前端框架实战', 'duration': '6周', 'level': '中级', 'skills': ['react', 'vue', 'typescript']}
            ],
            'advanced': [
                {'name': '系统架构设计', 'duration': '10周', 'level': '高级', 'skills': ['架构设计', '分布式系统']},
                {'name': '性能优化实战', 'duration': '8周', 'level': '高级', 'skills': ['性能优化', '系统调优']},
                {'name': 'DevOps实践', 'duration': '12周', 'level': '高级', 'skills': ['docker', 'kubernetes', 'ci/cd']}
            ]
        },
        'database': {
            'beginner': [
                {'name': 'SQL基础入门', 'duration': '4周', 'level': '初级', 'skills': ['sql', '数据库基础']},
                {'name': 'MySQL数据库管理', 'duration': '6周', 'level': '初级', 'skills': ['mysql', '数据库设计']},
                {'name': 'PostgreSQL数据库管理', 'duration': '6周', 'level': '初级', 'skills': ['postgresql', '数据库设计']}
            ],
            'intermediate': [
                {'name': '数据库性能优化', 'duration': '6周', 'level': '中级', 'skills': ['数据库优化', '索引设计']},
                {'name': 'NoSQL数据库应用', 'duration': '8周', 'level': '中级', 'skills': ['mongodb', 'redis']}
            ]
        },
        'cloud': {
            'beginner': [
                {'name': 'Docker容器化入门', 'duration': '4周', 'level': '初级', 'skills': ['docker', '容器化']},
                {'name': '云计算基础', 'duration': '6周', 'level': '初级', 'skills': ['云计算', '云服务']}
            ],
            'intermediate': [
                {'name': 'Docker高级应用', 'duration': '6周', 'level': '中级', 'skills': ['docker', '容器编排']},
                {'name': 'Kubernetes集群管理', 'duration': '8周', 'level': '中级', 'skills': ['kubernetes', '容器编排']}
            ]
        }
    },
    'soft_skills': {
        'communication': {
            'beginner': [
                {'name': '职场沟通技巧', 'duration': '4周', 'level': '初级', 'skills': ['沟通技巧', '职场礼仪']},
                {'name': '商务写作基础', 'duration': '6周', 'level': '初级', 'skills': ['商务写作', '邮件沟通']}
            ],
            'intermediate': [
                {'name': '演讲与表达', 'duration': '6周', 'level': '中级', 'skills': ['演讲技巧', 'presentation']},
                {'name': '跨文化沟通', 'duration': '8周', 'level': '中级', 'skills': ['跨文化', '国际商务']}
            ]
        },
        'leadership': {
            'beginner': [
                {'name': '团队管理基础', 'duration': '6周', 'level': '初级', 'skills': ['团队管理', '领导力基础']},
                {'name': '项目管理入门', 'duration': '8周', 'level': '初级', 'skills': ['项目管理', '敏捷开发']}
            ],
            'intermediate': [
                {'name': '高级领导力', 'duration': '10周', 'level': '中级', 'skills': ['战略领导', '变革管理']},
                {'name': '敏捷项目管理', 'duration': '8周', 'level': '中级', 'skills': ['scrum', 'kanban', '敏捷']}
            ]
        }
    },
    'business': {
        'analytics': {
            'beginner': [
                {'name': '数据分析基础', 'duration': '6周', 'level': '初级', 'skills': ['数据分析', 'excel']},
                {'name': '商业智能入门', 'duration': '8周', 'level': '初级', 'skills': ['bi', '数据可视化']}
            ],
            'intermediate': [
                {'name': '高级数据分析', 'duration': '10周', 'level': '中级', 'skills': ['python', 'pandas', '统计分析']},
                {'name': '数据挖掘实战', 'duration': '12周', 'level': '中级', 'skills': ['机器学习', '数据挖掘']}
            ]
        }
    }
}

def extract_user_skills(user_profile):
    """从用户资料中提取技能"""
    skills = set()
    
    # 从个人简介中提取
    if user_profile.get('bio'):
        bio = user_profile['bio'].lower()
        for category, subcategories in SKILL_CATEGORIES.items():
            for subcategory, skill_list in subcategories.items():
                for skill in skill_list:
                    if skill.lower() in bio:
                        skills.add(skill.lower())
    
    # 从工作经验中提取
    if user_profile.get('experience'):
        experience = user_profile['experience'].lower()
        for category, subcategories in SKILL_CATEGORIES.items():
            for subcategory, skill_list in subcategories.items():
                for skill in skill_list:
                    if skill.lower() in experience:
                        skills.add(skill.lower())
    
    # 从教育背景中提取
    if user_profile.get('education'):
        education = user_profile['education'].lower()
        for category, subcategories in SKILL_CATEGORIES.items():
            for subcategory, skill_list in subcategories.items():
                for skill in skill_list:
                    if skill.lower() in education:
                        skills.add(skill.lower())
    
    return list(skills)

def analyze_job_requirements(job_description):
    """分析职位要求"""
    requirements = set()
    description = job_description.lower()
    
    for category, subcategories in SKILL_CATEGORIES.items():
        for subcategory, skill_list in subcategories.items():
            for skill in skill_list:
                if skill.lower() in description:
                    requirements.add(skill.lower())
    
    return list(requirements)

def calculate_skill_gap(user_skills, job_requirements):
    """计算技能差距"""
    user_skill_set = set(user_skills)
    job_requirement_set = set(job_requirements)
    
    # 缺失的技能
    missing_skills = job_requirement_set - user_skill_set
    
    # 匹配的技能
    matched_skills = user_skill_set & job_requirement_set
    
    # 计算匹配度
    match_rate = len(matched_skills) / len(job_requirement_set) if job_requirement_set else 0
    
    return {
        'missing_skills': list(missing_skills),
        'matched_skills': list(matched_skills),
        'match_rate': match_rate,
        'total_requirements': len(job_requirement_set),
        'user_skills_count': len(user_skill_set)
    }

def recommend_courses(skill_gap, user_level='intermediate'):
    """推荐学习课程"""
    recommended_courses = []
    
    for missing_skill in skill_gap['missing_skills']:
        for category, subcategories in LEARNING_COURSES.items():
            for subcategory, levels in subcategories.items():
                if subcategory in SKILL_CATEGORIES.get(category, {}):
                    skill_list = SKILL_CATEGORIES[category][subcategory]
                    # 检查技能是否在技能列表中（包括部分匹配）
                    skill_found = False
                    for skill in skill_list:
                        if missing_skill.lower() in skill.lower() or skill.lower() in missing_skill.lower():
                            skill_found = True
                            break
                    
                    if skill_found:
                        # 根据用户水平选择课程
                        level_courses = levels.get(user_level, levels.get('beginner', []))
                        for course in level_courses:
                            # 检查课程技能是否匹配缺失技能
                            course_skill_match = False
                            for course_skill in course['skills']:
                                if (missing_skill.lower() in course_skill.lower() or 
                                    course_skill.lower() in missing_skill.lower()):
                                    course_skill_match = True
                                    break
                            
                            if course_skill_match:
                                recommended_courses.append({
                                    'course': course,
                                    'target_skill': missing_skill,
                                    'category': category,
                                    'subcategory': subcategory
                                })
    
    # 去重并按优先级排序
    unique_courses = {}
    for rec in recommended_courses:
        course_key = rec['course']['name']
        if course_key not in unique_courses:
            unique_courses[course_key] = rec
    
    return list(unique_courses.values())

def generate_learning_plan(user_skills, job_requirements, user_level='intermediate'):
    """生成完整的学习计划"""
    # 分析技能差距
    skill_gap = calculate_skill_gap(user_skills, job_requirements)
    
    # 推荐课程
    recommended_courses = recommend_courses(skill_gap, user_level)
    
    # 生成学习路径
    learning_path = {
        'current_status': {
            'match_rate': skill_gap['match_rate'],
            'matched_skills': skill_gap['matched_skills'],
            'missing_skills': skill_gap['missing_skills']
        },
        'recommended_courses': recommended_courses,
        'learning_objectives': [
            f"提升{skill}技能" for skill in skill_gap['missing_skills'][:5]  # 前5个最重要的技能
        ],
        'estimated_duration': sum(int(course['course']['duration'].split('周')[0]) for course in recommended_courses[:3]),
        'priority_skills': skill_gap['missing_skills'][:3]  # 优先级最高的3个技能
    }
    
    return learning_path

@learning_recommendation_bp.route('/dashboard')
@login_required
def dashboard():
    """学习推荐仪表板"""
    try:
        # 获取用户信息
        from flask import session
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        from app.models import User
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            flash('用户信息获取失败，请重新登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取用户当前职位（如果有的话）
        current_job = None
        if hasattr(user, 'current_position'):
            current_job = user.current_position
        
        # 获取用户技能
        user_profile = {
            'bio': getattr(user, 'bio', ''),
            'experience': getattr(user, 'experience', ''),
            'education': getattr(user, 'education', '')
        }
        user_skills = extract_user_skills(user_profile)
        
        # 获取推荐职位
        recommended_jobs = Job.query.limit(5).all()
        
        # 为每个推荐职位生成学习计划
        job_recommendations = []
        for job in recommended_jobs:
            job_requirements = analyze_job_requirements(job.description)
            learning_plan = generate_learning_plan(user_skills, job_requirements)
            
            job_recommendations.append({
                'job': job,
                'learning_plan': learning_plan
            })
        
        return render_template(
            'talent_management/employee_management/learning_dashboard.html',
            user=user,
            user_skills=user_skills,
            job_recommendations=job_recommendations,
            current_job=current_job
        )
        
    except Exception as e:
        flash(f'加载学习推荐时出错: {str(e)}', 'error')
        return redirect(url_for('talent_management.employee_auth.employee_dashboard'))

@learning_recommendation_bp.route('/analyze/<int:job_id>')
@login_required
def analyze_job(job_id):
    """分析特定职位的技能匹配"""
    try:
        job = Job.query.get_or_404(job_id)
        
        # 获取用户信息
        from flask import session
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        from app.models import User
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            flash('用户信息获取失败，请重新登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取用户技能
        user_profile = {
            'bio': getattr(user, 'bio', ''),
            'experience': getattr(user, 'experience', ''),
            'education': getattr(user, 'education', '')
        }
        user_skills = extract_user_skills(user_profile)
        
        # 分析职位要求
        job_requirements = analyze_job_requirements(job.description)
        
        # 生成学习计划
        learning_plan = generate_learning_plan(user_skills, job_requirements)
        
        return render_template(
            'talent_management/employee_management/job_analysis.html',
            job=job,
            user_skills=user_skills,
            job_requirements=job_requirements,
            learning_plan=learning_plan
        )
        
    except Exception as e:
        flash(f'分析职位时出错: {str(e)}', 'error')
        return redirect(url_for('talent_management.employee_manager.learning_recommendation.dashboard'))

@learning_recommendation_bp.route('/courses')
@login_required
def courses():
    """查看所有可用课程"""
    try:
        # 获取用户技能
        from flask import session
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        from app.models import User
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            flash('用户信息获取失败，请重新登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        user_profile = {
            'bio': getattr(user, 'bio', ''),
            'experience': getattr(user, 'experience', ''),
            'education': getattr(user, 'education', '')
        }
        user_skills = extract_user_skills(user_profile)
        
        # 获取所有课程并按类别组织
        all_courses = {}
        for category, subcategories in LEARNING_COURSES.items():
            all_courses[category] = {}
            for subcategory, levels in subcategories.items():
                all_courses[category][subcategory] = []
                for level, courses in levels.items():
                    for course in courses:
                        # 标记用户是否已掌握相关技能
                        course_skills = set(course['skills'])
                        user_skill_set = set(user_skills)
                        mastered_skills = course_skills & user_skill_set
                        missing_skills = course_skills - user_skill_set
                        
                        course_info = course.copy()
                        course_info['level'] = level
                        course_info['mastered_skills'] = list(mastered_skills)
                        course_info['missing_skills'] = list(missing_skills)
                        course_info['progress'] = len(mastered_skills) / len(course_skills) if course_skills else 0
                        
                        all_courses[category][subcategory].append(course_info)
        
        return render_template(
            'talent_management/employee_management/courses.html',
            all_courses=all_courses,
            user_skills=user_skills
        )
        
    except Exception as e:
        flash(f'加载课程时出错: {str(e)}', 'error')
        return redirect(url_for('talent_management.employee_manager.learning_recommendation.dashboard'))

@learning_recommendation_bp.route('/api/skill_analysis', methods=['POST'])
@login_required
def api_skill_analysis():
    """API: 技能分析"""
    try:
        data = request.get_json()
        job_description = data.get('job_description', '')
        
        # 获取用户技能
        from flask import session
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': '请先登录'}), 401
        
        from app.models import User
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'success': False, 'error': '用户信息获取失败'}), 401
        user_profile = {
            'bio': getattr(user, 'bio', ''),
            'experience': getattr(user, 'experience', ''),
            'education': getattr(user, 'education', '')
        }
        user_skills = extract_user_skills(user_profile)
        
        # 分析职位要求
        job_requirements = analyze_job_requirements(job_description)
        
        # 生成学习计划
        learning_plan = generate_learning_plan(user_skills, job_requirements)
        
        return jsonify({
            'success': True,
            'user_skills': user_skills,
            'job_requirements': job_requirements,
            'learning_plan': learning_plan
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
