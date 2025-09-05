"""
LLRC Header Start
文件功能: 人才管理子系统 Python 模块：talent_management_system/employee_manager_module/performance.py
创建时间: 2025-08-20 12:59
创建人: 苏杰
更新记录:
- 2025-08-20 13:29 by 侯东杨
- 2025-08-27 15:41 by 谢佳悦
- 2025-09-01 11:54 by 苏杰
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: talent_management_system/employee_manager_module/performance.py
功能: 通用模块
创建时间: 2025-08-21 17:29
创建人: 苏杰
更新记录:
- 2025-08-24 13:36 by 苏杰
- 2025-09-03 12:29 by 李雨梦
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import User, db, Job
from app.models import TaskEvaluation
from datetime import datetime, timedelta
import random

performance_bp = Blueprint('performance', __name__, url_prefix='/performance')

@performance_bp.route('/')
def performance_dashboard():
    """员工绩效仪表板"""
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
    
    # 模拟绩效数据（实际项目中应该从数据库获取）
    performance_data = generate_mock_performance_data(user)
    
    # 拉取员工的绩效评价（最新在前）
    try:
        evaluations = TaskEvaluation.query.filter_by(employee_id=user.id)\
            .order_by(TaskEvaluation.created_at.desc()).all()
    except Exception:
        evaluations = []

    return render_template('talent_management/employee_management/performance_dashboard.html',
                         user=user,
                         performance_data=performance_data,
                         evaluations=evaluations)

@performance_bp.route('/history')
def performance_history():
    """绩效历史记录"""
    try:
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
        
        # 验证用户类型
        if user.user_type != 'employee':
            flash('您没有权限访问此页面', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取真实的绩效评价数据
        real_evaluations = []
        try:
            evaluations = TaskEvaluation.query.filter_by(employee_id=user.id)\
                .order_by(TaskEvaluation.created_at.desc()).all()
            
            for eval_item in evaluations:
                real_evaluations.append({
                    'period': eval_item.created_at.strftime('%Y-%m-%d'),
                    'overall_score': eval_item.total_score,
                    'work_quality': eval_item.score_quality,
                    'work_efficiency': eval_item.score_efficiency,
                    'teamwork': eval_item.score_collaboration,
                    'initiative': (eval_item.score_quality + eval_item.score_efficiency) // 2,  # 模拟数据
                    'learning_ability': (eval_item.score_efficiency + eval_item.score_collaboration) // 2,  # 模拟数据
                    'achievements': [
                        f"{eval_item.task_title} - 质量评分: {eval_item.score_quality}",
                        f"效率评分: {eval_item.score_efficiency}",
                        f"协作评分: {eval_item.score_collaboration}"
                    ],
                    'comments': eval_item.comment or '无评语'
                })
        except Exception as eval_error:
            print(f"获取绩效评价数据失败: {eval_error}")
            # 如果获取真实数据失败，使用模拟数据
            pass
        
        # 生成模拟历史绩效数据（补充数据）
        mock_history = generate_mock_performance_history(user)
        
        # 合并真实数据和模拟数据
        history_data = real_evaluations + mock_history
        
        # 按时间排序
        history_data.sort(key=lambda x: x['period'], reverse=True)
        
        return render_template('talent_management/employee_management/performance_history.html',
                             user=user,
                             history_data=history_data)
                             
    except Exception as e:
        print(f"绩效历史记录页面错误: {e}")
        flash('加载绩效历史记录时发生错误，请稍后重试', 'danger')
        return redirect(url_for('talent_management.employee_manager.performance.performance_dashboard'))

def generate_mock_performance_data(user):
    """生成模拟绩效数据"""
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # 基础绩效指标
    base_performance = {
        'work_quality': random.randint(75, 95),
        'work_efficiency': random.randint(70, 90),
        'teamwork': random.randint(80, 95),
        'initiative': random.randint(75, 90),
        'learning_ability': random.randint(80, 95)
    }
    
    # 计算综合评分
    overall_score = sum(base_performance.values()) / len(base_performance)
    
    # 月度目标完成情况
    monthly_goals = [
        {'name': '完成项目A开发', 'status': '已完成', 'progress': 100, 'deadline': f'{current_year}-{current_month:02d}-15'},
        {'name': '学习新技术栈', 'status': '进行中', 'progress': 75, 'deadline': f'{current_year}-{current_month:02d}-30'},
        {'name': '团队协作项目', 'status': '进行中', 'progress': 60, 'deadline': f'{current_year}-{current_month:02d}-25'}
    ]
    
    # 技能评估
    skill_assessment = {
        'technical_skills': random.randint(70, 95),
        'communication': random.randint(75, 90),
        'leadership': random.randint(65, 85),
        'problem_solving': random.randint(75, 90),
        'adaptability': random.randint(80, 95)
    }
    
    return {
        'overall_score': round(overall_score, 1),
        'base_performance': base_performance,
        'monthly_goals': monthly_goals,
        'skill_assessment': skill_assessment,
        'current_month': current_month,
        'current_year': current_year
    }

def generate_mock_performance_history(user):
    """生成模拟绩效历史数据"""
    history = []
    current_date = datetime.now()
    
    for i in range(12):  # 过去12个月
        month_date = current_date - timedelta(days=30*i)
        month = month_date.month
        year = month_date.year
        
        # 生成月度绩效数据
        monthly_score = random.randint(70, 95)
        monthly_data = {
            'month': month,
            'year': year,
            'overall_score': monthly_score,
            'work_quality': random.randint(70, 95),
            'work_efficiency': random.randint(65, 90),
            'teamwork': random.randint(75, 95),
            'initiative': random.randint(70, 90),
            'learning_ability': random.randint(75, 95),
            'achievements': [
                f'{year}年{month}月完成重要项目',
                f'{year}年{month}月获得技能认证',
                f'{year}年{month}月参与团队建设活动'
            ]
        }
        history.append(monthly_data)
    
    return history
