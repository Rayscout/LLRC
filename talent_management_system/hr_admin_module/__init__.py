from flask import Blueprint, render_template, session, flash, redirect, url_for
from app.models import User

# 创建HR管理主蓝图
hr_admin_bp = Blueprint('hr_admin', __name__, url_prefix='/hr_admin')

# 导入子模块
from . import dashboard, employees, departments
from .turnover_alert import turnover_alert_bp
from .executive_auth import executive_auth_bp
from .pdf_report import pdf_report_bp
from .salary_analysis import salary_analysis_bp
from .org_health import org_health_bp
from .career_tracking import career_tracking_bp
from .feedback_system import feedback_system_bp
from .task_evaluation import task_evaluation_bp
from .employee_management import employee_management_bp
from .talent_demand import talent_demand_bp

# 注册子蓝图
hr_admin_bp.register_blueprint(turnover_alert_bp)
hr_admin_bp.register_blueprint(executive_auth_bp)
hr_admin_bp.register_blueprint(pdf_report_bp)
hr_admin_bp.register_blueprint(salary_analysis_bp)
hr_admin_bp.register_blueprint(org_health_bp)
hr_admin_bp.register_blueprint(career_tracking_bp)
hr_admin_bp.register_blueprint(feedback_system_bp)
hr_admin_bp.register_blueprint(task_evaluation_bp)
hr_admin_bp.register_blueprint(employee_management_bp)
hr_admin_bp.register_blueprint(talent_demand_bp)

# 高管仪表板路由
@hr_admin_bp.route('/executive_dashboard')
def executive_dashboard():
    """高管仪表板 - AI人才大盘"""
    try:
        if 'user_id' not in session or session.get('user_type') != 'executive':
            flash('请先登录高管账户。', 'danger')
            return redirect(url_for('talent_management.executive_auth.executive_auth'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'executive':
            flash('权限不足。', 'danger')
            return redirect(url_for('talent_management.executive_auth.executive_auth'))
        
        try:
            # 获取下属员工
            subordinates = User.query.filter_by(supervisor_id=user.id, user_type='employee').all()
            
            # 获取人才需求统计
            from app.models import TalentDemand
            talent_demands = TalentDemand.query.filter_by(executive_id=user.id).order_by(TalentDemand.created_at.desc()).limit(5).all()
            
            # 获取反馈统计
            from app.models import Feedback
            received_feedback = Feedback.query.filter_by(recipient_id=user.id).order_by(Feedback.created_at.desc()).limit(5).all()
            
            # 获取任务评价统计
            from app.models import TaskEvaluation
            task_evaluations = TaskEvaluation.query.filter_by(evaluator_id=user.id).order_by(TaskEvaluation.created_at.desc()).limit(5).all()
            
            # 计算统计数据
            dashboard_stats = {
                'total_subordinates': len(subordinates),
                'total_talent_demands': len(talent_demands),
                'total_feedback': len(received_feedback),
                'total_evaluations': len(task_evaluations),
                'recent_activities': []
            }
            
            # 生成最近活动列表
            activities = []
            
            # 添加人才需求活动
            for demand in talent_demands:
                activities.append({
                    'type': 'talent_demand',
                    'title': f'发布人才需求: {demand.keyword}',
                    'time': demand.created_at,
                    'description': demand.description or '无详细描述'
                })
            
            # 添加反馈活动
            for feedback in received_feedback:
                sender = User.query.get(feedback.sender_id)
                sender_name = f"{sender.first_name} {sender.last_name}" if sender else "未知用户"
                activities.append({
                    'type': 'feedback',
                    'title': f'收到反馈: {feedback.category}',
                    'time': feedback.created_at,
                    'description': f'来自 {sender_name}: {feedback.content[:50]}...'
                })
            
            # 添加任务评价活动
            for evaluation in task_evaluations:
                employee = User.query.get(evaluation.employee_id)
                employee_name = f"{employee.first_name} {employee.last_name}" if employee else "未知员工"
                activities.append({
                    'type': 'evaluation',
                    'title': f'任务评价: {evaluation.task_title}',
                    'time': evaluation.created_at,
                    'description': f'评价 {employee_name}: {evaluation.total_score}分'
                })
            
            # 按时间排序
            activities.sort(key=lambda x: x['time'], reverse=True)
            dashboard_stats['recent_activities'] = activities[:10]  # 只显示最近10个活动
            
            return render_template('talent_management/hr_admin/executive_dashboard.html', 
                                 user=user, 
                                 subordinates=subordinates,
                                 dashboard_stats=dashboard_stats,
                                 talent_demands=talent_demands,
                                 received_feedback=received_feedback,
                                 task_evaluations=task_evaluations)
                                 
        except Exception as data_error:
            print(f"获取仪表板数据失败: {data_error}")
            # 如果数据获取失败，返回基本页面
            return render_template('talent_management/hr_admin/executive_dashboard.html', 
                                 user=user, 
                                 subordinates=[],
                                 dashboard_stats={'total_subordinates': 0, 'total_talent_demands': 0, 'total_feedback': 0, 'total_evaluations': 0, 'recent_activities': []},
                                 talent_demands=[],
                                 received_feedback=[],
                                 task_evaluations=[])
                                 
    except Exception as e:
        print(f"高管仪表板页面错误: {e}")
        flash('页面加载失败，请重试', 'danger')
        return redirect(url_for('talent_management.executive_auth.executive_auth'))
