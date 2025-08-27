from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from app.models import User, db
from talent_management_system.models import EmployeeProjectExperience
from datetime import datetime, timedelta
import json
import random

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/')
def projects_dashboard():
    """员工项目经验仪表板"""
    # 检查用户是否登录
    from flask import session
    if 'user_id' not in session:
        flash('请先登录', 'warning')
        return redirect(url_for('common.auth.sign'))
    
    # 获取用户信息
    from app.models import User
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('用户信息获取失败，请重新登录', 'warning')
        return redirect(url_for('common.auth.sign'))
    
    # 从数据库获取项目经验数据
    projects_data = get_user_projects_data(user)
    
    return render_template('talent_management/employee_management/projects_dashboard.html',
                         user=user,
                         projects_data=projects_data)

@projects_bp.route('/add', methods=['GET', 'POST'])
def add_project():
    """添加新项目经验"""
    # 检查用户是否登录
    from flask import session
    if 'user_id' not in session:
        flash('请先登录', 'warning')
        return redirect(url_for('common.auth.sign'))
    
    # 获取用户信息
    from app.models import User
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('用户信息获取失败，请重新登录', 'warning')
        return redirect(url_for('common.auth.sign'))
    
    if request.method == 'POST':
        try:
            # 获取表单数据
            project_data = {
                'user_id': user.id,
                'name': request.form.get('name'),
                'role': request.form.get('role'),
                'description': request.form.get('description'),
                'start_date': datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date(),
                'status': request.form.get('status'),
                'team_size': int(request.form.get('team_size')) if request.form.get('team_size') else None,
                'technologies': request.form.get('technologies', ''),
                'contribution': request.form.get('contribution', ''),
                'project_url': request.form.get('project_url', ''),
                'notes': request.form.get('notes', '')
            }
            
            # 处理结束日期
            if request.form.get('end_date'):
                project_data['end_date'] = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
            
            # 处理预计结束日期
            if request.form.get('estimated_end_date'):
                project_data['estimated_end_date'] = datetime.strptime(request.form.get('estimated_end_date'), '%Y-%m-%d').date()
            
            # 处理成就数据
            achievements = request.form.getlist('achievements[]')
            if achievements:
                # 过滤空值并转换为JSON字符串
                achievements = [achievement.strip() for achievement in achievements if achievement.strip()]
                project_data['achievements'] = json.dumps(achievements, ensure_ascii=False)
            
            # 保存项目经验到数据库
            project_id = save_project_experience_to_database(project_data)
            
            if project_id:
                flash('项目经验添加成功！', 'success')
                return redirect(url_for('talent_management.employee_manager.projects.projects_dashboard'))
            else:
                flash('项目经验添加失败，请稍后重试', 'error')
                
        except Exception as e:
            flash(f'添加项目经验失败: {str(e)}', 'error')
            print(f"添加项目经验失败: {e}")
    
    return render_template('talent_management/employee_management/add_project.html', user=user)

def get_user_projects_data(user):
    """从数据库获取用户项目经验数据"""
    try:
        # 查询用户的项目经验
        projects = EmployeeProjectExperience.query.filter_by(user_id=user.id).order_by(EmployeeProjectExperience.start_date.desc()).all()
        
        if not projects:
            # 如果没有项目经验，返回空数据
            return {
                'projects': [],
                'stats': {
                    'total': 0,
                    'completed': 0,
                    'ongoing': 0,
                    'technologies': 0
                },
                'technologies': []
            }
        
        # 转换数据库对象为字典格式
        projects_data = []
        all_technologies = []
        
        for project in projects:
            # 解析成就数据
            achievements = []
            if project.achievements:
                try:
                    achievements = json.loads(project.achievements)
                except:
                    achievements = []
            
            # 解析技术栈
            technologies = []
            if project.technologies:
                technologies = [tech.strip() for tech in project.technologies.split(',') if tech.strip()]
                all_technologies.extend(technologies)
            
            project_dict = {
                'id': project.id,
                'name': project.name,
                'role': project.role,
                'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else '',
                'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
                'status': project.status,
                'description': project.description,
                'technologies': technologies,
                'achievements': achievements,
                'team_size': project.team_size,
                'contribution': project.contribution
            }
            projects_data.append(project_dict)
        
        # 计算统计信息
        total_projects = len(projects_data)
        completed_projects = len([p for p in projects_data if p['status'] == 'completed'])
        ongoing_projects = len([p for p in projects_data if p['status'] == 'active'])
        unique_technologies = list(set(all_technologies))
        
        return {
            'projects': projects_data,
            'stats': {
                'total': total_projects,
                'completed': completed_projects,
                'ongoing': ongoing_projects,
                'technologies': len(unique_technologies)
            },
            'technologies': unique_technologies
        }
        
    except Exception as e:
        print(f"获取项目经验数据失败: {e}")
        # 返回空数据
        return {
            'projects': [],
            'stats': {
                'total': 0,
                'completed': 0,
                'ongoing': 0,
                'technologies': 0
            },
            'technologies': []
        }

def save_project_experience_to_database(project_data):
    """保存项目经验到数据库"""
    try:
        # 创建新的项目经验记录
        new_project = EmployeeProjectExperience(**project_data)
        
        # 添加到数据库
        db.session.add(new_project)
        db.session.commit()
        
        return new_project.id
    except Exception as e:
        db.session.rollback()
        print(f"保存项目经验失败: {e}")
        return None

def generate_mock_projects_data(user):
    """生成模拟项目数据（保留作为备用）"""
    current_date = datetime.now()
    
    projects = [
        {
            'id': 1,
            'name': '企业管理系统重构',
            'role': '后端开发工程师',
            'start_date': (current_date - timedelta(days=180)).strftime('%Y-%m-%d'),
            'end_date': (current_date - timedelta(days=30)).strftime('%Y-%m-%d'),
            'status': '已完成',
            'description': '负责重构公司核心业务系统，提升系统性能和稳定性',
            'technologies': ['Python', 'Django', 'PostgreSQL', 'Redis', 'Docker'],
            'achievements': [
                '系统响应时间提升40%',
                '成功处理并发用户1000+',
                '获得团队优秀员工奖'
            ],
            'team_size': 8,
            'contribution': '负责核心模块开发，参与系统架构设计'
        },
        {
            'id': 2,
            'name': '移动端APP开发',
            'role': '全栈开发工程师',
            'start_date': (current_date - timedelta(days=90)).strftime('%Y-%m-%d'),
            'end_date': None,
            'status': '进行中',
            'description': '开发公司移动端应用，提供便捷的业务办理服务',
            'technologies': ['React Native', 'Node.js', 'MongoDB', 'AWS'],
            'achievements': [
                '完成核心功能模块开发',
                '实现跨平台兼容性',
                '用户满意度达到95%'
            ],
            'team_size': 5,
            'contribution': '负责前端开发，参与后端API设计'
        },
        {
            'id': 3,
            'name': '数据分析平台',
            'role': '数据工程师',
            'start_date': (current_date - timedelta(days=120)).strftime('%Y-%m-%d'),
            'end_date': (current_date - timedelta(days=60)).strftime('%Y-%m-%d'),
            'status': '已完成',
            'description': '构建公司数据分析平台，为业务决策提供数据支持',
            'technologies': ['Python', 'Pandas', 'NumPy', 'Matplotlib', 'SQL'],
            'achievements': [
                '建立完整的数据分析流程',
                '生成关键业务指标报告',
                '提升数据分析效率60%'
            ],
            'team_size': 4,
            'contribution': '负责数据模型设计，开发分析工具'
        }
    ]
    
    # 计算项目统计
    total_projects = len(projects)
    completed_projects = len([p for p in projects if p['status'] == '已完成'])
    ongoing_projects = len([p for p in projects if p['status'] == '进行中'])
    
    # 技术栈统计
    all_technologies = []
    for project in projects:
        all_technologies.extend(project['technologies'])
    unique_technologies = list(set(all_technologies))
    
    return {
        'projects': projects,
        'stats': {
            'total': total_projects,
            'completed': completed_projects,
            'ongoing': ongoing_projects,
            'technologies': len(unique_technologies)
        },
        'technologies': unique_technologies
    }
