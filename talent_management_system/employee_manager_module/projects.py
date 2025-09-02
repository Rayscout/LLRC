from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from app.models import User, Project, db
from datetime import datetime, timedelta
import random
import json

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
    
    # 从数据库获取项目数据
    projects = Project.query.filter_by(user_id=user.id).order_by(Project.created_at.desc()).all()

    # 转换项目数据为前端需要的格式
    formatted_projects = []
    for project in projects:
        formatted_projects.append({
            'id': project.id,
            'name': project.name,
            'role': project.role,
            'start_date': project.start_date.strftime('%Y-%m-%d'),
            'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else None,
            'status': project.status,
            'description': project.description,
            'technologies': project.technologies_list,
            'achievements': project.achievements_list,
            'team_size': project.team_size,
            'contribution': project.contribution
        })

    # 计算项目统计
    total_projects = len(formatted_projects)
    completed_projects = len([p for p in formatted_projects if p['status'] == '已完成'])
    ongoing_projects = len([p for p in formatted_projects if p['status'] == '进行中'])

    # 技术栈统计
    all_technologies = []
    for project in formatted_projects:
        all_technologies.extend(project['technologies'])
    unique_technologies = list(set(all_technologies))

    projects_data = {
        'projects': formatted_projects,
        'stats': {
            'total': total_projects,
            'completed': completed_projects,
            'ongoing': ongoing_projects,
            'technologies': len(unique_technologies)
        },
        'technologies': unique_technologies
    }

    return render_template('talent_management/employee_management/projects_dashboard.html',
                         user=user,
                         projects_data=projects_data)

@projects_bp.route('/add', methods=['GET', 'POST'])
def add_project():
    """添加项目经验"""
    # 检查用户是否登录
    from flask import session
    if 'user_id' not in session:
        flash('请先登录', 'warning')
        return redirect(url_for('common.auth.sign'))

    # 获取用户信息
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('用户信息获取失败，请重新登录', 'warning')
        return redirect(url_for('common.auth.sign'))

    if request.method == 'POST':
        try:
            # 获取表单数据
            name = request.form.get('name')
            role = request.form.get('role')
            description = request.form.get('description')
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            status = request.form.get('status')
            team_size = int(request.form.get('team_size', 1))
            contribution = request.form.get('contribution')

            # 验证必填字段
            if not all([name, role, description, start_date_str, status]):
                flash('请填写所有必填字段', 'danger')
                return redirect(request.url)

            # 处理技术栈（支持多选）
            technologies = request.form.getlist('technologies[]')

            # 处理成就（支持多行输入）
            achievements_text = request.form.get('achievements', '')
            achievements = [achievement.strip() for achievement in achievements_text.split('\n') if achievement.strip()]

            # 转换日期
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
                
                # 验证日期逻辑
                if end_date and start_date > end_date:
                    flash('开始日期不能晚于结束日期', 'danger')
                    return redirect(request.url)
                    
            except ValueError as ve:
                flash(f'日期格式错误: {str(ve)}', 'danger')
                return redirect(request.url)

            # 创建新项目
            new_project = Project(
                user_id=user.id,
                name=name,
                role=role,
                description=description,
                start_date=start_date,
                end_date=end_date,
                status=status,
                team_size=team_size,
                contribution=contribution
            )

            # 设置技术栈和成就
            new_project.set_technologies(technologies)
            new_project.set_achievements(achievements)

            # 保存到数据库
            db.session.add(new_project)
            db.session.commit()

            # 验证数据是否成功保存
            saved_project = Project.query.filter_by(
                user_id=user.id,
                name=name,
                role=role
            ).first()

            if not saved_project:
                db.session.rollback()
                flash('项目保存失败，请重试', 'danger')
                return redirect(request.url)

            flash('项目添加成功！', 'success')
            return redirect(url_for('talent_management.employee_manager.projects.projects_dashboard'))

        except ValueError as ve:
            db.session.rollback()
            flash(f'数据格式错误: {str(ve)}', 'danger')
            return redirect(request.url)
        except Exception as e:
            db.session.rollback()
            print(f"项目添加失败: {e}")
            flash(f'项目添加失败: {str(e)}', 'danger')
            return redirect(request.url)

    return render_template('talent_management/employee_management/add_project.html', user=user)

@projects_bp.route('/edit/<int:project_id>', methods=['GET', 'POST'])
def edit_project(project_id):
    """编辑项目经验"""
    # 检查用户是否登录
    from flask import session
    if 'user_id' not in session:
        flash('请先登录', 'warning')
        return redirect(url_for('common.auth.sign'))

    # 获取用户信息
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('用户信息获取失败，请重新登录', 'warning')
        return redirect(url_for('common.auth.sign'))

    # 查找项目
    project = Project.query.filter_by(id=project_id, user_id=user.id).first()
    if not project:
        flash('项目不存在', 'danger')
        return redirect(url_for('talent_management.employee_manager.projects.projects_dashboard'))

    if request.method == 'POST':
        try:
            # 获取表单数据
            name = request.form.get('name')
            role = request.form.get('role')
            description = request.form.get('description')
            start_date_str = request.form.get('start_date')
            end_date_str = request.form.get('end_date')
            status = request.form.get('status')
            team_size = int(request.form.get('team_size', 1))
            contribution = request.form.get('contribution')

            # 处理技术栈（支持多选）
            technologies = request.form.getlist('technologies[]')

            # 处理成就（支持多行输入）
            achievements_text = request.form.get('achievements', '')
            achievements = [achievement.strip() for achievement in achievements_text.split('\n') if achievement.strip()]

            # 验证必填字段
            if not all([name, role, description, start_date_str, status]):
                flash('请填写所有必填字段', 'danger')
                return redirect(request.url)

            # 转换日期
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
            except ValueError:
                flash('日期格式错误', 'danger')
                return redirect(request.url)

            # 更新项目数据
            project.name = name
            project.role = role
            project.description = description
            project.start_date = start_date
            project.end_date = end_date
            project.status = status
            project.team_size = team_size
            project.contribution = contribution

            # 更新技术栈和成就
            project.set_technologies(technologies)
            project.set_achievements(achievements)

            # 保存到数据库
            db.session.commit()

            flash('项目修改成功！', 'success')
            return redirect(url_for('talent_management.employee_manager.projects.projects_dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f'项目修改失败: {str(e)}', 'danger')
            return redirect(request.url)

    return render_template('talent_management/employee_management/edit_project.html',
                         user=user, project=project)

@projects_bp.route('/delete/<int:project_id>', methods=['POST'])
def delete_project(project_id):
    """删除项目经验"""
    # 检查用户是否登录
    from flask import session
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': '请先登录'})

    # 获取用户信息
    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'success': False, 'message': '用户信息获取失败'})

    try:
        # 查找项目
        project = Project.query.filter_by(id=project_id, user_id=user.id).first()
        if not project:
            return jsonify({'success': False, 'message': '项目不存在'})

        # 删除项目
        db.session.delete(project)
        db.session.commit()

        return jsonify({'success': True, 'message': '项目删除成功'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'删除失败: {str(e)}'})

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
