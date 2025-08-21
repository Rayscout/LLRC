from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, jsonify
from datetime import datetime, timedelta
import random
import logging
from app.models import User, Job, Application, db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/hr_dashboard')
def hr_dashboard():
    """HR仪表盘"""
    try:
        if g.user is None:
            flash('请先登录。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        if not getattr(g.user, 'is_hr', False):
            flash('只有HR用户才能访问此页面。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        # 获取统计数据
        try:
            total_jobs = Job.query.filter_by(user_id=g.user.id).count()
        except Exception as e:
            logging.error(f"查询职位数量失败: {e}")
            total_jobs = 0
        
        try:
            total_applications = Application.query.join(Job).filter(Job.user_id == g.user.id).count()
        except Exception as e:
            logging.error(f"查询申请数量失败: {e}")
            total_applications = 0
        
        # 获取最近的职位
        try:
            recent_jobs = Job.query.filter_by(user_id=g.user.id).order_by(Job.date_posted.desc()).limit(5).all()
        except Exception as e:
            logging.error(f"查询最近职位失败: {e}")
            recent_jobs = []
        
        # 获取最近的申请
        try:
            recent_applications = Application.query.join(Job).filter(Job.user_id == g.user.id).order_by(Application.timestamp.desc()).limit(5).all()
        except Exception as e:
            logging.error(f"查询最近申请失败: {e}")
            recent_applications = []
        
        return render_template('smartrecruit/hr/hr_dashboard.html',
                             total_jobs=total_jobs,
                             total_applications=total_applications,
                             recent_jobs=recent_jobs,
                             recent_applications=recent_applications)
    except Exception as e:
        logging.error(f"HR仪表盘加载失败: {e}")
        flash('加载仪表盘时出现错误，请稍后重试。', 'danger')
        return render_template('smartrecruit/hr/hr_dashboard.html',
                             total_jobs=0,
                             total_applications=0,
                             recent_jobs=[],
                             recent_applications=[])

@dashboard_bp.route('/candidates')
def candidates():
    """候选人管理"""
    try:
        if g.user is None:
            flash('请先登录。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        if not getattr(g.user, 'is_hr', False):
            flash('只有HR用户才能访问此页面。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        # 获取所有候选人
        try:
            candidates = User.query.filter(User.is_hr == False).all()
        except Exception as e:
            logging.error(f"查询候选人失败: {e}")
            candidates = []
        
        return render_template('smartrecruit/hr/hr_candidates.html', candidates=candidates)
    except Exception as e:
        logging.error(f"候选人管理页面加载失败: {e}")
        flash('加载候选人管理页面时出现错误，请稍后重试。', 'danger')
        return render_template('smartrecruit/hr/hr_candidates.html', candidates=[])

@dashboard_bp.route('/interviews')
def interviews():
    """面试安排"""
    try:
        if g.user is None:
            flash('请先登录。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        if not getattr(g.user, 'is_hr', False):
            flash('只有HR用户才能访问此页面。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        # 获取面试数据（这里可以扩展为真实的面试管理）
        interviews = []
        
        return render_template('smartrecruit/hr/hr_interviews.html', interviews=interviews)
    except Exception as e:
        logging.error(f"面试安排页面加载失败: {e}")
        flash('加载面试安排页面时出现错误，请稍后重试。', 'danger')
        return render_template('smartrecruit/hr/hr_interviews.html', interviews=[])

@dashboard_bp.route('/reports')
def reports():
    """数据报告"""
    try:
        if g.user is None:
            flash('请先登录。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        if not getattr(g.user, 'is_hr', False):
            flash('只有HR用户才能访问此页面。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        # 生成报告数据
        try:
            jobs = Job.query.filter_by(user_id=g.user.id).all()
            applications = Application.query.join(Job).filter(Job.user_id == g.user.id).all()
        except Exception as e:
            logging.error(f"查询报告数据失败: {e}")
            jobs = []
            applications = []
        
        report_data = {
            'total_jobs': len(jobs),
            'total_applications': len(applications),
            'avg_applications_per_job': len(applications) / len(jobs) if jobs else 0,
            'jobs_by_status': {}
        }
        
        return render_template('smartrecruit/hr/hr_reports.html', report_data=report_data)
    except Exception as e:
        logging.error(f"数据报告页面加载失败: {e}")
        flash('加载数据报告页面时出现错误，请稍后重试。', 'danger')
        return render_template('smartrecruit/hr/hr_reports.html', report_data={
            'total_jobs': 0,
            'total_applications': 0,
            'avg_applications_per_job': 0,
            'jobs_by_status': {}
        })

@dashboard_bp.route('/insights')
def insights():
    """AI洞察"""
    try:
        if g.user is None:
            flash('请先登录。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        if not getattr(g.user, 'is_hr', False):
            flash('只有HR用户才能访问此页面。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        # AI洞察数据
        insights = {
            'top_skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL'],
            'trending_positions': ['Full Stack Developer', 'Data Scientist', 'DevOps Engineer'],
            'candidate_quality_score': 85.5
        }
        
        return render_template('smartrecruit/hr/hr_insights.html', insights=insights)
    except Exception as e:
        logging.error(f"AI洞察页面加载失败: {e}")
        flash('加载AI洞察页面时出现错误，请稍后重试。', 'danger')
        return render_template('smartrecruit/hr/hr_insights.html', insights={
            'top_skills': [],
            'trending_positions': [],
            'candidate_quality_score': 0
        })
