from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.models import User, db
from talent_management_system.models import SmartGoal, GoalProgress
from datetime import datetime, timedelta
import json
import re

smart_goals_bp = Blueprint('smart_goals', __name__, url_prefix='/smart_goals')

# SMART目标模板
SMART_GOAL_TEMPLATES = {
    'technical_skills': {
        'python_developer': [
            {
                'title': '掌握Python高级特性',
                'specific': '学习Python装饰器、生成器、上下文管理器等高级特性',
                'measurable': '完成3个实际项目，通过技能评估测试',
                'achievable': '每周投入10小时学习，分3个月完成',
                'relevant': '提升Python开发能力，为项目开发做准备',
                'time_bound': '3个月内完成',
                'category': 'technical',
                'priority': 'high',
                'estimated_hours': 120
            },
            {
                'title': '学习Django框架',
                'specific': '掌握Django ORM、视图、模板、表单处理',
                'measurable': '开发一个完整的Web应用，包含用户认证和数据库操作',
                'achievable': '每周学习15小时，2个月内完成',
                'relevant': '为公司Web项目开发做准备',
                'time_bound': '2个月内完成',
                'category': 'technical',
                'priority': 'medium',
                'estimated_hours': 90
            }
        ],
        'java_developer': [
            {
                'title': '掌握Spring Boot框架',
                'specific': '学习Spring Boot自动配置、依赖注入、数据访问',
                'measurable': '开发RESTful API服务，通过单元测试',
                'achievable': '每周投入12小时，2.5个月内完成',
                'relevant': '提升后端开发能力',
                'time_bound': '2.5个月内完成',
                'category': 'technical',
                'priority': 'high',
                'estimated_hours': 100
            }
        ],
        'frontend_developer': [
            {
                'title': '掌握React框架',
                'specific': '学习React Hooks、状态管理、组件设计',
                'measurable': '开发3个React组件库，通过代码审查',
                'achievable': '每周学习10小时，2个月内完成',
                'relevant': '提升前端开发技能',
                'time_bound': '2个月内完成',
                'category': 'technical',
                'priority': 'high',
                'estimated_hours': 80
            }
        ]
    },
    'soft_skills': {
        'communication': [
            {
                'title': '提升演讲能力',
                'specific': '参加演讲培训，练习技术分享',
                'measurable': '完成5次团队技术分享，获得正面反馈',
                'achievable': '每月准备1次分享，5个月内完成',
                'relevant': '提升团队沟通和知识分享能力',
                'time_bound': '5个月内完成',
                'category': 'soft_skills',
                'priority': 'medium',
                'estimated_hours': 50
            }
        ],
        'leadership': [
            {
                'title': '培养项目管理能力',
                'specific': '学习项目管理方法论，实践敏捷开发',
                'measurable': '成功管理1个小项目，按时交付',
                'achievable': '参加项目管理培训，实践应用',
                'relevant': '为未来晋升做准备',
                'time_bound': '6个月内完成',
                'category': 'soft_skills',
                'priority': 'medium',
                'estimated_hours': 60
            }
        ]
    },
    'business_skills': {
        'data_analysis': [
            {
                'title': '掌握数据分析技能',
                'specific': '学习SQL、Excel、Python数据分析',
                'measurable': '完成3个数据分析项目，生成分析报告',
                'achievable': '每周学习8小时，3个月内完成',
                'relevant': '支持业务决策和数据分析需求',
                'time_bound': '3个月内完成',
                'category': 'business',
                'priority': 'medium',
                'estimated_hours': 96
            }
        ]
    }
}

@smart_goals_bp.route('/')
def goals_dashboard():
    """SMART目标仪表板"""
    try:
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取用户的目标
        user_goals = get_user_goals(user.id)
        
        # 分析技能差距并推荐目标
        skill_gaps = analyze_skill_gaps(user)
        recommended_goals = generate_recommended_goals(user, skill_gaps)
        
        # 计算目标完成统计
        goal_stats = calculate_goal_stats(user_goals)
        
        return render_template('talent_management/employee_management/smart_goals_dashboard.html',
                             user=user,
                             user_goals=user_goals,
                             recommended_goals=recommended_goals,
                             goal_stats=goal_stats,
                             skill_gaps=skill_gaps)
                             
    except Exception as e:
        flash(f'加载目标页面时发生错误: {str(e)}', 'danger')
        return redirect(url_for('talent_management.employee_auth.employee_dashboard'))

@smart_goals_bp.route('/create', methods=['GET', 'POST'])
def create_goal():
    """创建SMART目标"""
    if request.method == 'POST':
        try:
            if 'user_id' not in session:
                return jsonify({'success': False, 'message': '请先登录'})
            
            user = User.query.get(session['user_id'])
            if not user:
                return jsonify({'success': False, 'message': '用户信息获取失败'})
            
            # 获取表单数据
            goal_data = {
                'user_id': user.id,
                'title': request.form.get('title'),
                'specific': request.form.get('specific'),
                'measurable': request.form.get('measurable'),
                'achievable': request.form.get('achievable'),
                'relevant': request.form.get('relevant'),
                'time_bound': request.form.get('time_bound'),
                'category': request.form.get('category', 'custom'),
                'priority': request.form.get('priority', 'medium'),
                'target_date': datetime.strptime(request.form.get('target_date'), '%Y-%m-%d').date(),
                'estimated_hours': int(request.form.get('estimated_hours', 0)),
                'status': 'active',
                'progress': 0,
                'completed_hours': 0,
                'created_at': datetime.now(),
                'last_updated': datetime.now(),
                'notes': ''
            }
            
            # 保存目标到数据库
            goal_id = save_goal_to_database(goal_data)
            
            if goal_id:
                return jsonify({
                    'success': True, 
                    'message': '目标创建成功',
                    'goal_id': goal_id
                })
            else:
                return jsonify({'success': False, 'message': '目标创建失败'})
            
        except Exception as e:
            return jsonify({'success': False, 'message': f'创建目标失败: {str(e)}'})
    
    return render_template('talent_management/employee_management/create_goal.html')

@smart_goals_bp.route('/<int:goal_id>/update_progress', methods=['POST'])
def update_progress(goal_id):
    """更新目标进度"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'})
        
        # 允许从URL参数或JSON体中获取goal_id
        json_body = request.get_json(silent=True) or {}
        goal_id = json_body.get('goal_id') or goal_id

        # 获取进度数据
        completed_hours = json_body.get('completed_hours', 0)
        notes = str(json_body.get('notes', '') or '')
        
        # 验证输入数据
        try:
            completed_hours = float(completed_hours)
            if completed_hours < 0:
                return jsonify({'success': False, 'message': '已完成时间不能为负数'})
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': '已完成时间格式不正确'})
        
        # 获取目标信息
        goal = SmartGoal.query.filter_by(id=goal_id, user_id=session['user_id']).first()
        
        if not goal:
            return jsonify({'success': False, 'message': '目标不存在或无权限访问'})
        
        # 验证已完成时间不超过预计总时间
        if completed_hours > goal.estimated_hours:
            return jsonify({'success': False, 'message': '已完成时间不能超过预计总时间'})
        
        # 计算新的进度百分比
        if goal.estimated_hours > 0:
            progress = min(100, round((completed_hours / goal.estimated_hours) * 100))
        else:
            progress = 0
        
        # 更新目标进度
        success = update_goal_progress(goal_id, progress, completed_hours, notes)
        
        if success:
            # 重新获取更新后的目标信息
            updated_goal = SmartGoal.query.get(goal_id)
            
            return jsonify({
                'success': True, 
                'message': '进度更新成功', 
                'goal_id': goal_id, 
                'progress': progress,
                'completed_hours': completed_hours,
                'notes': notes,
                'status': updated_goal.status,
                'last_updated': updated_goal.last_updated.strftime('%Y-%m-%d %H:%M:%S') if updated_goal.last_updated else None
            })
        else:
            return jsonify({'success': False, 'message': '进度更新失败'})
            
    except Exception as e:
        print(f"更新进度失败: {e}")
        return jsonify({'success': False, 'message': f'更新进度失败: {str(e)}'})

@smart_goals_bp.route('/<int:goal_id>/complete', methods=['POST'])
def complete_goal(goal_id):
    """完成目标"""
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': '请先登录'})
        
        json_body = request.get_json(silent=True) or {}
        goal_id = json_body.get('goal_id') or goal_id
        completion_notes = json_body.get('completion_notes', '')
        
        # 标记目标为完成
        success = mark_goal_complete(goal_id, completion_notes)
        
        if success:
            return jsonify({'success': True, 'message': '目标完成！恭喜！'})
        else:
            return jsonify({'success': False, 'message': '操作失败'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'操作失败: {str(e)}'})

def analyze_skill_gaps(user):
    """分析用户技能差距"""
    skill_gaps = []
    
    # 从用户资料中提取当前技能
    current_skills = extract_user_skills(user)
    
    # 根据用户职位确定目标技能
    target_skills = get_target_skills_by_position(user.position)
    
    # 计算技能差距
    for skill in target_skills:
        if skill not in current_skills:
            skill_gaps.append({
                'skill': skill,
                'category': get_skill_category(skill),
                'priority': get_skill_priority(skill, user.position),
                'estimated_learning_hours': get_learning_hours(skill)
            })
    
    return skill_gaps

def extract_user_skills(user):
    """从用户资料中提取技能"""
    skills = []
    
    # 从个人简介中提取
    if user.bio:
        skills.extend(extract_skills_from_text(user.bio))
    
    # 从工作经验中提取
    if user.experience:
        skills.extend(extract_skills_from_text(user.experience))
    
    # 从教育背景中提取
    if user.education:
        skills.extend(extract_skills_from_text(user.education))
    
    # 从技能字段中提取
    if user.skills:
        try:
            stored_skills = json.loads(user.skills)
            if isinstance(stored_skills, list):
                skills.extend(stored_skills)
        except (json.JSONDecodeError, TypeError):
            if isinstance(user.skills, str):
                skills.extend([skill.strip() for skill in user.skills.split(',') if skill.strip()])
    
    return list(set(skills))

def extract_skills_from_text(text):
    """从文本中提取技能关键词"""
    if not text:
        return []
    
    skill_keywords = [
        'Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift',
        'HTML', 'CSS', 'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'Spring',
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQL Server',
        'Docker', 'Kubernetes', 'AWS', 'Azure', 'Google Cloud', 'Linux', 'Windows',
        'Git', 'SVN', 'Jenkins', 'CI/CD', 'Agile', 'Scrum', 'DevOps',
        'Machine Learning', 'AI', 'Data Science', 'Big Data', 'Hadoop', 'Spark',
        'Excel', 'PowerBI', 'Tableau', 'Photoshop', 'Illustrator', 'Figma',
        '项目管理', '团队协作', '沟通能力', '领导力', '创新思维', '问题解决'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in skill_keywords:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills

def get_target_skills_by_position(position):
    """根据职位获取目标技能"""
    position_skills = {
        'python开发工程师': ['Python', 'Django', 'Flask', 'MySQL', 'Redis', 'Docker', 'Git'],
        'java开发工程师': ['Java', 'Spring', 'Spring Boot', 'MySQL', 'Redis', 'Maven', 'Git'],
        '前端开发工程师': ['JavaScript', 'React', 'Vue', 'HTML', 'CSS', 'TypeScript', 'Git'],
        '全栈开发工程师': ['Python', 'JavaScript', 'React', 'Django', 'MySQL', 'Docker', 'Git'],
        '数据工程师': ['Python', 'SQL', 'Hadoop', 'Spark', 'MongoDB', 'Docker', 'Git'],
        '运维工程师': ['Linux', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'Shell', 'Python']
    }
    
    return position_skills.get(position, ['Python', 'JavaScript', 'Git', '项目管理'])

def get_skill_category(skill):
    """获取技能分类"""
    technical_skills = ['Python', 'Java', 'JavaScript', 'React', 'Django', 'MySQL', 'Docker']
    soft_skills = ['沟通能力', '团队协作', '领导力', '项目管理']
    business_skills = ['数据分析', 'Excel', 'PowerBI', 'Tableau']
    
    if skill in technical_skills:
        return 'technical'
    elif skill in soft_skills:
        return 'soft_skills'
    elif skill in business_skills:
        return 'business'
    else:
        return 'technical'

def get_skill_priority(skill, position):
    """获取技能优先级"""
    high_priority_skills = {
        'python开发工程师': ['Python', 'Django', 'Git'],
        'java开发工程师': ['Java', 'Spring', 'Git'],
        '前端开发工程师': ['JavaScript', 'React', 'Git']
    }
    
    position_high_skills = high_priority_skills.get(position, [])
    return 'high' if skill in position_high_skills else 'medium'

def get_learning_hours(skill):
    """获取技能学习时间估算"""
    skill_hours = {
        'Python': 80, 'Java': 100, 'JavaScript': 60, 'React': 70,
        'Django': 50, 'Spring': 80, 'MySQL': 40, 'Docker': 30,
        'Git': 20, '项目管理': 60, '沟通能力': 40
    }
    
    return skill_hours.get(skill, 50)

def generate_recommended_goals(user, skill_gaps):
    """根据技能差距生成推荐目标"""
    recommended_goals = []
    
    # 根据用户职位选择模板
    position_templates = {
        'python开发工程师': 'python_developer',
        'java开发工程师': 'java_developer',
        '前端开发工程师': 'frontend_developer'
    }
    
    template_key = position_templates.get(user.position, 'python_developer')
    
    # 添加技术技能目标
    if template_key in SMART_GOAL_TEMPLATES['technical_skills']:
        for goal in SMART_GOAL_TEMPLATES['technical_skills'][template_key]:
            goal['type'] = 'recommended'
            goal['source'] = 'skill_gap'
            recommended_goals.append(goal)
    
    # 根据技能差距添加特定目标
    for gap in skill_gaps[:3]:  # 只推荐前3个最重要的技能差距
        goal = create_skill_goal(gap)
        goal['type'] = 'recommended'
        goal['source'] = 'skill_gap'
        recommended_goals.append(goal)
    
    # 添加软技能目标
    for category in ['communication', 'leadership']:
        if category in SMART_GOAL_TEMPLATES['soft_skills']:
            for goal in SMART_GOAL_TEMPLATES['soft_skills'][category]:
                goal['type'] = 'recommended'
                goal['source'] = 'career_development'
                recommended_goals.append(goal)
    
    return recommended_goals

def create_skill_goal(skill_gap):
    """为技能差距创建目标"""
    skill = skill_gap['skill']
    hours = skill_gap['estimated_learning_hours']
    
    return {
        'title': f'掌握{skill}技能',
        'specific': f'系统学习{skill}，掌握核心概念和实践应用',
        'measurable': f'完成{skill}相关项目，通过技能评估',
        'achievable': f'每周投入{hours//8}小时学习，{hours//40}周内完成',
        'relevant': f'提升{skill}技能，增强职业竞争力',
        'time_bound': f'{hours//40}周内完成',
        'category': skill_gap['category'],
        'priority': skill_gap['priority'],
        'estimated_hours': hours
    }

def get_user_goals(user_id):
    """获取用户的目标（从数据库）"""
    try:
        goals = SmartGoal.query.filter_by(user_id=user_id).order_by(SmartGoal.created_at.desc()).all()
        
        goals_list = []
        for goal in goals:
            goals_list.append({
                'id': goal.id,
                'title': goal.title,
                'specific': goal.specific,
                'measurable': goal.measurable,
                'achievable': goal.achievable,
                'relevant': goal.relevant,
                'time_bound': goal.time_bound,
                'category': goal.category,
                'priority': goal.priority,
                'status': goal.status,
                'progress': goal.progress,
                'target_date': goal.target_date,
                'estimated_hours': goal.estimated_hours,
                'completed_hours': goal.completed_hours,
                'created_at': goal.created_at,
                'last_updated': goal.last_updated,
                'notes': goal.notes
            })
        
        return goals_list
    except Exception as e:
        print(f"获取用户目标失败: {e}")
        return []

def calculate_goal_stats(user_goals):
    """计算目标统计信息"""
    total_goals = len(user_goals)
    active_goals = len([g for g in user_goals if g['status'] == 'active'])
    completed_goals = len([g for g in user_goals if g['status'] == 'completed'])
    
    total_progress = sum(g['progress'] for g in user_goals if g['status'] == 'active')
    avg_progress = total_progress / active_goals if active_goals > 0 else 0
    
    total_hours = sum(g['estimated_hours'] for g in user_goals)
    completed_hours = sum(g['completed_hours'] for g in user_goals)
    
    return {
        'total_goals': total_goals,
        'active_goals': active_goals,
        'completed_goals': completed_goals,
        'avg_progress': round(avg_progress, 1),
        'total_hours': total_hours,
        'completed_hours': completed_hours,
        'completion_rate': round(completed_goals / total_goals * 100, 1) if total_goals > 0 else 0
    }

def save_goal_to_database(goal_data):
    """保存目标到数据库"""
    try:
        # 创建新的SMART目标
        new_goal = SmartGoal(
            user_id=goal_data['user_id'],
            title=goal_data['title'],
            specific=goal_data['specific'],
            measurable=goal_data['measurable'],
            achievable=goal_data['achievable'],
            relevant=goal_data['relevant'],
            time_bound=goal_data['time_bound'],
            category=goal_data['category'],
            priority=goal_data['priority'],
            target_date=goal_data['target_date'],
            estimated_hours=goal_data['estimated_hours'],
            status=goal_data['status'],
            progress=goal_data['progress'],
            completed_hours=goal_data['completed_hours'],
            notes=goal_data['notes'],
            created_at=goal_data['created_at'],
            last_updated=goal_data['last_updated']
        )
        
        # 添加到数据库
        db.session.add(new_goal)
        db.session.commit()
        
        return new_goal.id
    except Exception as e:
        db.session.rollback()
        print(f"保存目标失败: {e}")
        return None

def update_goal_progress(goal_id, progress, completed_hours, notes):
    """更新目标进度"""
    try:
        # 获取目标
        goal = SmartGoal.query.get(goal_id)
        if not goal:
            return False
        
        # 更新目标进度
        goal.progress = progress
        goal.completed_hours = completed_hours
        goal.notes = notes
        goal.last_updated = datetime.now()
        
        # 如果进度达到100%，标记为完成
        if progress >= 100:
            goal.status = 'completed'
        
        # 创建进度历史记录
        progress_record = GoalProgress(
            goal_id=goal_id,
            progress=progress,
            completed_hours=completed_hours,
            notes=notes
        )
        
        db.session.add(progress_record)
        db.session.commit()
        
        return True
    except Exception as e:
        db.session.rollback()
        print(f"更新目标进度失败: {e}")
        return False

def mark_goal_complete(goal_id, completion_notes):
    """标记目标完成"""
    try:
        goal = SmartGoal.query.get(goal_id)
        if not goal:
            return False
        
        goal.status = 'completed'
        goal.progress = 100
        goal.notes = completion_notes
        goal.last_updated = datetime.now()
        
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"标记目标完成失败: {e}")
        return False
