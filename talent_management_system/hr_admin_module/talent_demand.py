"""
LLRC Header Start
文件功能: 人才管理子系统 Python 模块：talent_management_system/hr_admin_module/talent_demand.py
创建时间: 2025-08-19 11:08
创建人: 谢佳悦
更新记录:
- 2025-08-19 11:38 by 谢佳悦
- 2025-08-27 16:33 by 苏杰
LLRC Header End
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FILE-HEADER-AUTO-ADDED
文件: talent_management_system/hr_admin_module/talent_demand.py
功能: 通用模块
创建时间: 2025-08-27 18:36
创建人: 侯东杨
更新记录:
- 2025-08-23 16:34 by 张宇成
- 2025-08-31 09:05 by 张宇成
- 2025-09-02 12:01 by 谢佳悦
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, User, TalentDemand, TalentDemandNotification, TalentDemandDraft

talent_demand_bp = Blueprint('talent_demand', __name__, url_prefix='/talent_demand')


def notify_all_hr_for_demand(demand: TalentDemand, executive: User) -> int:
    """为所有 HR 用户创建通知，返回创建的通知数量"""
    hr_users = User.query.filter_by(is_hr=True).all()
    created = 0
    for hr in hr_users:
        exec_name = f"{executive.first_name} {executive.last_name}".strip()
        notification = TalentDemandNotification(
            hr_user_id=hr.id,
            demand_id=demand.id,
            title=f"来自{exec_name}高管的招聘需求",
            message=f"关键词：{demand.keyword}" + (f"\n描述：{demand.description}" if demand.description else "")
        )
        db.session.add(notification)
        created += 1
    db.session.commit()
    return created


@talent_demand_bp.route('/publish', methods=['GET', 'POST'])
def publish():
    """高管发布人才需求（输入关键词，可选描述）"""
    try:
        if 'user_id' not in session or session.get('user_type') != 'executive':
            flash('请先使用高管账户登录', 'danger')
            return redirect(url_for('talent_management.executive_auth.executive_auth'))

        executive = User.query.get(session['user_id'])
        if not executive or executive.user_type != 'executive':
            flash('权限不足', 'danger')
            return redirect(url_for('talent_management.executive_auth.executive_auth'))

        if request.method == 'POST':
            keyword = request.form.get('keyword', '').strip()
            description = request.form.get('description', '').strip()
            
            if not keyword:
                flash('请输入人才需求关键词', 'warning')
                return redirect(url_for('talent_management.hr_admin.talent_demand.publish'))

            try:
                # 创建人才需求
                demand = TalentDemand(
                    executive_id=executive.id,
                    keyword=keyword,
                    description=description or None
                )
                db.session.add(demand)
                db.session.commit()

                # 验证数据是否成功保存
                saved_demand = TalentDemand.query.filter_by(
                    executive_id=executive.id,
                    keyword=keyword
                ).first()

                if not saved_demand:
                    db.session.rollback()
                    flash('人才需求保存失败，请重试', 'danger')
                    return redirect(url_for('talent_management.hr_admin.talent_demand.publish'))

                # 通知所有 HR
                try:
                    count = notify_all_hr_for_demand(demand, executive)
                    flash(f'人才需求已发布，并通知 {count} 位HR', 'success')
                except Exception as notify_error:
                    print(f"通知HR失败: {notify_error}")
                    flash('人才需求已发布，但通知HR时出现问题', 'warning')

                return redirect(url_for('talent_management.hr_admin.executive_dashboard'))

            except Exception as db_error:
                db.session.rollback()
                print(f"发布人才需求失败: {db_error}")
                flash('发布失败，请重试', 'danger')
                return redirect(url_for('talent_management.hr_admin.talent_demand.publish'))

        return render_template('talent_management/hr_admin/talent_demand_publish.html', user=executive)
        
    except Exception as e:
        print(f"发布人才需求页面错误: {e}")
        flash('页面加载失败，请重试', 'danger')
        return redirect(url_for('talent_management.executive_auth.executive_auth'))


@talent_demand_bp.route('/hr_inbox')
def hr_inbox():
    """HR 查看来自高管的人才需求通知"""
    if 'user_id' not in session:
        flash('请先登录', 'danger')
        return redirect(url_for('common.auth.sign'))

    user = User.query.get(session['user_id'])
    if not user or not user.is_hr:
        flash('仅HR可访问消息通知', 'danger')
        return redirect(url_for('talent_management.hr_admin.employee_management.employee_list'))

    notifications = TalentDemandNotification.query.filter_by(hr_user_id=user.id).order_by(TalentDemandNotification.created_at.desc()).all()
    # 展开所需字段供模板使用
    rows = []
    for n in notifications:
        demand = n.demand
        exec_user = demand.executive if demand else None
        rows.append({
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'is_read': n.is_read,
            'created_at': n.created_at,
            'executive_email': exec_user.email if exec_user else '未知',
            'executive_name': (f"{exec_user.first_name} {exec_user.last_name}".strip() if exec_user else '未知'),
            'keyword': demand.keyword if demand else '—'
        })

    return render_template('talent_management/hr_admin/hr_inbox.html', user=user, notifications=rows)


@talent_demand_bp.route('/hr_inbox/<int:notification_id>')
def hr_inbox_detail(notification_id: int):
    """通知详情页，进入即标记为已读"""
    if 'user_id' not in session:
        flash('请先登录', 'danger')
        return redirect(url_for('common.auth.sign'))

    user = User.query.get(session['user_id'])
    if not user or not user.is_hr:
        flash('仅HR可访问消息通知', 'danger')
        return redirect(url_for('talent_management.hr_admin.employee_management.employee_list'))

    n = TalentDemandNotification.query.get_or_404(notification_id)
    if n.hr_user_id != user.id:
        flash('无权查看该消息', 'danger')
        return redirect(url_for('talent_management.hr_admin.talent_demand.hr_inbox'))

    # 标记已读
    if not n.is_read:
        n.is_read = True
        db.session.commit()

    demand = n.demand
    exec_user = demand.executive if demand else None
    data = {
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'is_read': n.is_read,
        'created_at': n.created_at,
        'executive_email': exec_user.email if exec_user else '未知',
        'executive_name': (f"{exec_user.first_name} {exec_user.last_name}".strip() if exec_user else '未知'),
        'keyword': demand.keyword if demand else '—',
        'description': demand.description if demand else ''
    }

    return render_template('talent_management/hr_admin/hr_inbox_detail.html', user=user, n=data)


@talent_demand_bp.route('/hr_inbox/mark_read/<int:notification_id>', methods=['POST'])
def mark_read(notification_id: int):
    """函数 mark_read：处理 notification_id 相关逻辑。"""
    if 'user_id' not in session:
        return redirect(url_for('common.auth.sign'))
    user = User.query.get(session['user_id'])
    n = TalentDemandNotification.query.get_or_404(notification_id)
    if n.hr_user_id == user.id:
        if not n.is_read:
            n.is_read = True
            db.session.commit()
        flash('已标记为已读', 'success')
    return redirect(url_for('talent_management.hr_admin.talent_demand.hr_inbox'))


@talent_demand_bp.route('/hr_inbox/mark_all_read', methods=['POST'])
def mark_all_read():
    """函数 mark_all_read：核心业务逻辑。"""
    if 'user_id' not in session:
        return redirect(url_for('common.auth.sign'))
    user = User.query.get(session['user_id'])
    TalentDemandNotification.query.filter_by(hr_user_id=user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    flash('全部标记为已读', 'success')
    return redirect(url_for('talent_management.hr_admin.talent_demand.hr_inbox'))


@talent_demand_bp.route('/hr_inbox/clear_read', methods=['POST'])
def clear_read():
    """函数 clear_read：核心业务逻辑。"""
    if 'user_id' not in session:
        return redirect(url_for('common.auth.sign'))
    user = User.query.get(session['user_id'])
    # 删除本HR用户所有已读通知
    TalentDemandNotification.query.filter_by(hr_user_id=user.id, is_read=True).delete(synchronize_session=False)
    db.session.commit()
    flash('已清除所有已读消息', 'success')
    return redirect(url_for('talent_management.hr_admin.talent_demand.hr_inbox'))


@talent_demand_bp.route('/hr_inbox/go_publish/<int:notification_id>', methods=['POST'])
def go_publish(notification_id: int):
    """从通知详情一键去发布职位：将通知内容存入暂存箱并跳转到发布职位页"""
    if 'user_id' not in session:
        return redirect(url_for('common.auth.sign'))
    user = User.query.get(session['user_id'])
    if not user or not user.is_hr:
        return redirect(url_for('common.auth.sign'))

    n = TalentDemandNotification.query.get_or_404(notification_id)
    demand = n.demand
    exec_user = demand.executive if demand else None

    draft = TalentDemandDraft(
        hr_user_id=user.id,
        notification_id=n.id,
        executive_name=(f"{exec_user.first_name} {exec_user.last_name}".strip() if exec_user else ''),
        executive_email=(exec_user.email if exec_user else ''),
        keyword=(demand.keyword if demand else ''),
        description=(demand.description if demand else '')
    )
    db.session.add(draft)
    db.session.commit()

    # 跳转到HR发布职位页面并携带暂存ID，供页面侧边展示
    return redirect(url_for('smartrecruit.hr.recruitment.publish_recruitment', draft_id=draft.id))



