"""
LLRC Header Start
文件功能: 人才管理子系统 Python 模块：talent_management_system/hr_admin_module/employee_management.py
创建时间: 2025-08-21 09:00
创建人: 张宇成
更新记录:
- 2025-08-25 15:04 by 张宇成
- 2025-08-31 14:22 by 苏杰
- 2025-09-03 17:16 by 潘显雨
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: talent_management_system/hr_admin_module/employee_management.py
功能: 通用模块
创建时间: 2025-09-03 10:37
创建人: 侯东杨
更新记录:
- 2025-08-21 09:04 by 侯东杨
- 2025-08-30 11:05 by 苏杰
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.models import User, db
from datetime import datetime

employee_management_bp = Blueprint('employee_management', __name__, url_prefix='/employee-management')

@employee_management_bp.route('/list')
def employee_list():
    """高管查看下属员工列表"""
    if 'user_id' not in session or session.get('user_type') != 'executive':
        flash('请先登录高管账户。', 'danger')
        return redirect(url_for('talent_management.executive_auth.executive_auth'))
    
    user = User.query.get(session['user_id'])
    if not user or user.user_type != 'executive':
        flash('权限不足。', 'danger')
        return redirect(url_for('talent_management.executive_auth.executive_auth'))
    
    # 获取下属员工
    subordinates = User.query.filter_by(supervisor_id=user.id, user_type='employee').all()
    
    return render_template('talent_management/hr_admin/employee_management.html', 
                         user=user, subordinates=subordinates)

@employee_management_bp.route('/deactivate/<int:employee_id>', methods=['POST'])
def deactivate_employee(employee_id):
    """高管注销下属员工账号"""
    if 'user_id' not in session or session.get('user_type') != 'executive':
        return jsonify({'success': False, 'message': '请先登录高管账户。'}), 401
    
    executive = User.query.get(session['user_id'])
    if not executive or executive.user_type != 'executive':
        return jsonify({'success': False, 'message': '权限不足。'}), 403
    
    # 查找要注销的员工
    employee = User.query.get(employee_id)
    if not employee:
        return jsonify({'success': False, 'message': '员工不存在。'}), 404
    
    # 验证该员工是否属于该高管
    if employee.supervisor_id != executive.id:
        return jsonify({'success': False, 'message': '您没有权限注销该员工账号。'}), 403
    
    # 检查员工类型
    if employee.user_type != 'employee':
        return jsonify({'success': False, 'message': '只能注销员工账号。'}), 400
    
    try:
        # 注销员工账号（软删除：标记为非活跃状态）
        employee.is_active = False
        employee.deactivated_at = datetime.utcnow()
        employee.deactivated_by = executive.id
        
        # 或者完全删除账号（硬删除）
        # db.session.delete(employee)
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'员工 {employee.first_name} {employee.last_name} 的账号已成功注销。'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'注销失败：{str(e)}'}), 500

@employee_management_bp.route('/reactivate/<int:employee_id>', methods=['POST'])
def reactivate_employee(employee_id):
    """高管重新激活下属员工账号"""
    if 'user_id' not in session or session.get('user_type') != 'executive':
        return jsonify({'success': False, 'message': '请先登录高管账户。'}), 401
    
    executive = User.query.get(session['user_id'])
    if not executive or executive.user_type != 'executive':
        return jsonify({'success': False, 'message': '权限不足。'}), 403
    
    # 查找要重新激活的员工
    employee = User.query.get(employee_id)
    if not employee:
        return jsonify({'success': False, 'message': '员工不存在。'}), 404
    
    # 验证该员工是否属于该高管
    if employee.supervisor_id != executive.id:
        return jsonify({'success': False, 'message': '您没有权限重新激活该员工账号。'}), 403
    
    try:
        # 重新激活员工账号
        employee.is_active = True
        employee.deactivated_at = None
        employee.deactivated_by = None
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': f'员工 {employee.first_name} {employee.last_name} 的账号已重新激活。'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'重新激活失败：{str(e)}'}), 500

@employee_management_bp.route('/employee/<int:employee_id>')
def employee_detail(employee_id):
    """高管查看下属员工详细信息"""
    if 'user_id' not in session or session.get('user_type') != 'executive':
        flash('请先登录高管账户。', 'danger')
        return redirect(url_for('talent_management.executive_auth.executive_auth'))
    
    executive = User.query.get(session['user_id'])
    if not executive or executive.user_type != 'executive':
        flash('权限不足。', 'danger')
        return redirect(url_for('talent_management.executive_auth.executive_auth'))
    
    # 查找员工
    employee = User.query.get(employee_id)
    if not employee:
        flash('员工不存在。', 'danger')
        return redirect(url_for('talent_management.hr_admin.employee_management.employee_list'))
    
    # 验证该员工是否属于该高管
    if employee.supervisor_id != executive.id:
        flash('您没有权限查看该员工信息。', 'danger')
        return redirect(url_for('talent_management.hr_admin.employee_management.employee_list'))
    
    return render_template('talent_management/hr_admin/employee_detail.html', 
                         user=executive, employee=employee)
