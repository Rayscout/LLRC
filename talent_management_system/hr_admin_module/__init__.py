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

# 注册子蓝图
hr_admin_bp.register_blueprint(turnover_alert_bp)
hr_admin_bp.register_blueprint(executive_auth_bp)
hr_admin_bp.register_blueprint(pdf_report_bp)
hr_admin_bp.register_blueprint(salary_analysis_bp)
hr_admin_bp.register_blueprint(org_health_bp)
hr_admin_bp.register_blueprint(career_tracking_bp)
hr_admin_bp.register_blueprint(feedback_system_bp)
hr_admin_bp.register_blueprint(task_evaluation_bp)

# 高管仪表板路由
@hr_admin_bp.route('/executive_dashboard')
def executive_dashboard():
    if 'user_id' not in session or session.get('user_type') != 'executive':
        flash('请先登录高管账户。', 'danger')
        return redirect(url_for('talent_management.executive_auth.executive_auth'))
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'executive':
        flash('权限不足。', 'danger')
        return redirect(url_for('talent_management.executive_auth.executive_auth'))
    
    # 获取下属员工
    subordinates = User.query.filter_by(supervisor_id=user.id, user_type='employee').all()
    
    return render_template('talent_management/hr_admin/executive_dashboard.html', 
                         user=user, subordinates=subordinates)
