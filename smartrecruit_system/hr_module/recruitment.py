from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, abort
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import logging
from app.models import Job, User, Application, db
from app.sync_service import DataSyncService

recruitment_bp = Blueprint('recruitment', __name__, url_prefix='/recruitment')

@recruitment_bp.route('/publish', methods=['GET', 'POST'])
def publish_recruitment():
    """发布招聘启事"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户才能发布招聘启事。', 'danger')
        return redirect(url_for('common.auth.sign'))

    edit_job_id = request.args.get('edit')
    job_to_edit = None
    if edit_job_id:
        try:
            job_to_edit = Job.query.get_or_404(int(edit_job_id))
            if job_to_edit.user_id != g.user.id:
                flash('无权编辑该招聘启事。', 'danger')
                return redirect(url_for('smartrecruit.hr.recruitment.my_jobs'))
        except ValueError:
            flash('无效的招聘启事ID。', 'danger')
            return redirect(url_for('smartrecruit.hr.recruitment.my_jobs'))

    if request.method == 'POST':
        try:
            title = request.form['title']
            location = request.form['location']
            description = request.form['description']
            salary = request.form['salary']
            positions_needed = int(request.form.get('positions_needed') or 1)
            min_age = int(request.form['min_age']) if request.form.get('min_age') else None
            max_age = int(request.form['max_age']) if request.form.get('max_age') else None
            education_requirement = request.form.get('education_requirement')
            experience_years = int(request.form['experience_years']) if request.form.get('experience_years') else None
            skills_required = request.form.get('skills_required')
            benefits = request.form.get('benefits')
            contact_email = request.form.get('contact_email')
            contact_phone = request.form.get('contact_phone')
            application_deadline = datetime.strptime(request.form['application_deadline'], '%Y-%m-%d') if request.form.get('application_deadline') else None
            job_type = request.form.get('job_type')
            department = request.form.get('department')

            if job_to_edit:
                job_to_edit.title = title
                job_to_edit.location = location
                job_to_edit.description = description
                job_to_edit.salary = salary
                job_to_edit.positions_needed = positions_needed
                job_to_edit.min_age = min_age
                job_to_edit.max_age = max_age
                job_to_edit.education_requirement = education_requirement
                job_to_edit.experience_years = experience_years
                job_to_edit.skills_required = skills_required
                job_to_edit.benefits = benefits
                job_to_edit.contact_email = contact_email
                job_to_edit.contact_phone = contact_phone
                job_to_edit.application_deadline = application_deadline
                job_to_edit.job_type = job_type
                job_to_edit.department = department
                db.session.commit()
                # 同步职位更新到求职者端
                DataSyncService.sync_job_to_candidates(job_to_edit.id)
                flash('招聘启事更新成功！', 'success')
            else:
                new_job = Job(
                    title=title,
                    location=location,
                    description=description,
                    salary=salary,
                    user_id=g.user.id,
                    positions_needed=positions_needed,
                    min_age=min_age,
                    max_age=max_age,
                    education_requirement=education_requirement,
                    experience_years=experience_years,
                    skills_required=skills_required,
                    benefits=benefits,
                    contact_email=contact_email,
                    contact_phone=contact_phone,
                    application_deadline=application_deadline,
                    job_type=job_type,
                    department=department
                )
                db.session.add(new_job)
                db.session.commit()
                # 同步新职位到求职者端
                DataSyncService.sync_job_to_candidates(new_job.id)
                flash('招聘启事发布成功！', 'success')

            return redirect(url_for('smartrecruit.hr.recruitment.my_jobs'))
        except Exception as e:
            db.session.rollback()
            logging.error(f'发布/更新招聘启事失败: {e}')
            flash('操作失败，请稍后重试。', 'danger')

    return render_template('smartrecruit/hr/create_job_ios.html', job=job_to_edit, is_edit=bool(edit_job_id))

@recruitment_bp.route('/my_jobs')
def my_jobs():
    """我的职位列表"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    jobs = Job.query.filter_by(user_id=g.user.id).all()
    return render_template('smartrecruit/hr/my_jobs_ios.html', jobs=jobs)

@recruitment_bp.route('/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    """编辑职位"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    job = Job.query.get_or_404(job_id)
    if job.user_id != g.user.id:
        abort(403)

    if request.method == 'POST':
        job.title = request.form['title']
        job.location = request.form['location']
        job.description = request.form['description']
        job.salary = request.form['salary']
        job.positions_needed = int(request.form.get('positions_needed') or 1)
        job.min_age = int(request.form['min_age']) if request.form.get('min_age') else None
        job.max_age = int(request.form['max_age']) if request.form.get('max_age') else None
        job.education_requirement = request.form.get('education_requirement')
        job.experience_years = int(request.form['experience_years']) if request.form.get('experience_years') else None
        job.skills_required = request.form.get('skills_required')
        job.benefits = request.form.get('benefits')
        job.contact_email = request.form.get('contact_email')
        job.contact_phone = request.form.get('contact_phone')
        job.application_deadline = datetime.strptime(request.form['application_deadline'], '%Y-%m-%d') if request.form.get('application_deadline') else None
        job.job_type = request.form.get('job_type')
        job.department = request.form.get('department')
        
        db.session.commit()
        # 同步职位更新到求职者端
        DataSyncService.sync_job_to_candidates(job.id)
        flash('职位更新成功！', 'success')
        return redirect(url_for('smartrecruit.hr.recruitment.my_jobs'))

    return render_template('smartrecruit/hr/edit_job_ios.html', job=job)

@recruitment_bp.route('/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    """删除职位"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))

    job = Job.query.get_or_404(job_id)
    if job.user_id != g.user.id:
        abort(403)

    # 注意：删除职位时，相关的申请也会被级联删除
    # 这里可以添加删除前的同步逻辑
    db.session.delete(job)
    db.session.commit()
    flash('职位删除成功！', 'success')
    return redirect(url_for('smartrecruit.hr.recruitment.my_jobs'))
