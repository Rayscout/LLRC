"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/hr_module/profile.py
创建时间: 2025-08-21 09:01
创建人: 张宇成
更新记录:
- 2025-08-21 09:31 by 潘显雨
- 2025-09-01 17:33 by 李雨梦
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/hr_module/profile.py
功能: 通用模块
创建时间: 2025-09-02 14:55
创建人: 张宇成
更新记录:
- 2025-08-24 12:51 by 李雨梦
- 2025-08-27 17:17 by 李雨梦
- 2025-09-03 15:10 by 张宇成
"""
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
