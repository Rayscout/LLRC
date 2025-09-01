#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 HR 账号 hr_auto@company.com 批量创建已通过 AI 正式面试的候选人数据，
使其显示在“审批AI面试”页面（全局审核页）。
"""

import os
import sys
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import create_app, db, applications_collection  # type: ignore
from app.models import User, Job, Application  # type: ignore
from werkzeug.security import generate_password_hash  # type: ignore


def ensure_hr_user() -> User:
    hr_email = 'hr_auto@company.com'
    hr = User.query.filter_by(email=hr_email).first()
    if hr:
        return hr
    hr = User(
        first_name='Auto',
        last_name='HR',
        company_name='自动化公司',
        position='自动化招聘经理',
        email=hr_email,
        phone_number='13800138999',
        birthday='1990-01-01',
        password=generate_password_hash('123456'),
        is_hr=True,
        user_type='recruiter',
        department='自动化部',
        employee_id='HR_AUTO'
    )
    db.session.add(hr)
    db.session.commit()
    return hr


def ensure_jobs(hr: User) -> list[Job]:
    job_titles = ['自动化测试工程师', '数据标注专员']
    jobs: list[Job] = []
    for title in job_titles:
        job = Job.query.filter_by(title=title, user_id=hr.id).first()
        if not job:
            job = Job(
                title=title,
                company_name='自动化公司',
                location='远程',
                description=f'{title} 职位（测试种子数据）',
                requirements='认真、细心、执行力强',
                salary='10k-20k',
                user_id=hr.id,
                department=hr.department or '自动化部'
            )
            db.session.add(job)
            db.session.commit()
        jobs.append(job)
    return jobs


def create_candidate(email: str, name: str, position: str) -> User:
    user = User.query.filter_by(email=email).first()
    if user:
        return user
    first_name = name[:-1] if len(name) > 1 else name
    last_name = name[-1] if len(name) > 0 else ''
    user = User(
        first_name=first_name,
        last_name=last_name,
        company_name='待业',
        position=position,
        email=email,
        phone_number='13800138{:03d}'.format(int(abs(hash(email)) % 900) + 100),
        birthday='1995-01-01',
        password=generate_password_hash('123456'),
        is_hr=False,
        user_type='candidate',
        bio=f'{position} 候选人（自动种子）',
        skills='Python, 自动化, 数据处理',
        education='本科',
        experience='3年相关经验'
    )
    db.session.add(user)
    db.session.commit()
    return user


def ensure_application(candidate: User, job: Job) -> Application:
    app_row = Application.query.filter_by(user_id=candidate.id, job_id=job.id).first()
    if app_row:
        return app_row
    app_row = Application(
        user_id=candidate.id,
        job_id=job.id,
        message='自动导入的申请',
        status='Pending'
    )
    db.session.add(app_row)
    db.session.commit()
    return app_row


def upsert_ai_interview_result(candidate: User, job: Job, score: int, status: str = 'passed') -> None:
    doc = {
        'user_id': str(candidate.id),
        'job_id': str(job.id),
        'type': 'ai_interview_result',
        'status': status,
        'score': score,
        'feedback': '自动化评估结果：表现良好',
        'created_at': datetime.utcnow(),
        'technical_score': min(100, score),
        'communication_score': min(100, int(round(score * 0.9))),
        'logic_score': min(100, int(round(score * 0.88))),
        'learning_score': min(100, int(round(score * 0.92))),
    }
    applications_collection.update_one(
        {
            'user_id': str(candidate.id),
            'job_id': str(job.id),
            'type': 'ai_interview_result'
        },
        {'$set': doc},
        upsert=True
    )


def main():
    app = create_app()
    with app.app_context():
        hr = ensure_hr_user()
        jobs = ensure_jobs(hr)

        # 创建 3 个候选人（AI 面试已通过）
        candidates_spec = [
            ('auto_candidate1@email.com', '张自动一', jobs[0], 88),
            ('auto_candidate2@email.com', '李自动二', jobs[0], 92),
            ('auto_candidate3@email.com', '王自动三', jobs[1], 85),
        ]

        for email, name, job, score in candidates_spec:
            candidate = create_candidate(email, name, job.title)
            app_row = ensure_application(candidate, job)
            # 标记申请状态以便页面更友好
            try:
                app_row.status = 'approved'
                db.session.commit()
            except Exception:
                db.session.rollback()
            upsert_ai_interview_result(candidate, job, score, status='passed')

        print('✓ hr_auto@company.com 的AI面试候选人已准备完毕。')


if __name__ == '__main__':
    main()


