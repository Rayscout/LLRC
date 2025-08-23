from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.models import User, db
from datetime import datetime, timedelta
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
    
    # 模拟项目数据（实际项目中应该从数据库获取）
    projects_data = generate_mock_projects_data(user)
    
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
        # 这里可以添加项目到数据库的逻辑
        flash('项目添加功能开发中...', 'info')
        return redirect(url_for('talent_management.employee_manager.projects.projects_dashboard'))
    
    return render_template('talent_management/employee_management/add_project.html', user=user)

def generate_mock_projects_data(user):
    """生成模拟项目数据"""
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
