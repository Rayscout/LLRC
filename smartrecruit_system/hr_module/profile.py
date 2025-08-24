from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.models import User, db

# 创建HR个人资料蓝图
profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/hr_profile')
def hr_profile():
    """HR个人资料页面"""
    if g.user is None or not g.user.is_hr:
        flash('请先登录或没有权限访问此页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    return render_template('smartrecruit/hr/hr_profile.html', user=g.user)

@profile_bp.route('/hr_settings')
def hr_settings():
    """HR设置页面"""
    if g.user is None or not g.user.is_hr:
        flash('请先登录或没有权限访问此页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    return render_template('smartrecruit/hr/hr_settings.html', user=g.user)
