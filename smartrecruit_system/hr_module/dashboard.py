from flask import Blueprint, render_template, g, redirect, url_for, flash, request, abort
from datetime import datetime
try:
    from app.models import db, User, Application, Job
except Exception:
    db = None
    User = Application = Job = None

# HR Dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/', endpoint='hr_dashboard')
def index():
    if g.get('user') is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户可以访问该页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    # Prefer iOS-styled dashboard if present
    try:
        return render_template('smartrecruit/hr/hr_dashboard_ios.html')
    except Exception:
        return render_template('smartrecruit/hr/hr_dashboard.html')


@dashboard_bp.route('/insights', endpoint='insights')
def insights():
    if g.get('user') is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户可以访问该页面。', 'danger')
        return redirect(url_for('common.auth.sign'))

    # 为AI洞察页面提供基本数据
    insights_data = {
        'total_candidates': 0,
        'ai_interviews_completed': 0,
        'success_rate': 0,
        'average_score': 0,
        'candidate_quality_score': 85.5,
        'top_skills': ['Python', 'JavaScript', 'React', 'Node.js', 'SQL'],
        'trending_positions': ['Full Stack Developer', 'Data Scientist', 'DevOps Engineer']
    }

    try:
        if db is not None:
            from app.models import Application, Job
            # 获取当前HR的职位
            jobs = Job.query.filter_by(user_id=g.user.id).all()
            job_ids = [job.id for job in jobs]

            if job_ids:
                # 统计候选人数量
                applications = Application.query.filter(Application.job_id.in_(job_ids)).all()
                insights_data['total_candidates'] = len(applications)

                # 统计AI面试完成数量（假设有ai_interview状态）
                ai_completed = sum(1 for app in applications if getattr(app, 'status', '') == 'ai_interview')
                insights_data['ai_interviews_completed'] = ai_completed

                # 计算成功率
                if insights_data['total_candidates'] > 0:
                    insights_data['success_rate'] = int((ai_completed / insights_data['total_candidates']) * 100)

    except Exception as e:
        print(f"获取AI洞察数据失败：{str(e)}")

    try:
        return render_template('smartrecruit/hr/hr_insights_ios.html', insights=insights_data)
    except Exception:
        return render_template('smartrecruit/hr/hr_dashboard.html')


@dashboard_bp.route('/interviews', endpoint='interviews')
def interviews():
    if g.get('user') is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户可以访问该页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    # 获取面试安排数据
    interviews_data = []
    candidates_data = []
    
    try:
        if db is not None:
            from app.models import InterviewSchedule
            
            # 获取当前HR的面试安排
            interview_schedules = InterviewSchedule.query.filter_by(hr_id=g.user.id).all()
            
            for schedule in interview_schedules:
                candidate = User.query.get(schedule.candidate_id)
                job = Job.query.get(schedule.job_id)
                
                if candidate and job:
                    interviews_data.append({
                        'id': schedule.id,
                        'candidate_name': f"{candidate.first_name} {candidate.last_name}",
                        'candidate_email': candidate.email,
                        'position': job.title,
                        'date': schedule.interview_date.strftime('%Y-%m-%d'),
                        'start_time': schedule.start_time.strftime('%H:%M'),
                        'end_time': schedule.end_time.strftime('%H:%M'),
                        'method': schedule.interview_type,
                        'status': schedule.status,
                        'interviewer_name': schedule.interviewer_name or '未指定',
                        'location': schedule.location or '未指定'
                    })
            
            # 获取通过AI面试的候选人数量
            from app import applications_collection
            ai_passed_count = applications_collection.count_documents({
                'type': 'ai_interview_result',
                'status': 'passed'
            })
            
            candidates_data = [{'id': i, 'name': f'候选人{i}', 'email': f'candidate{i}@example.com'} for i in range(ai_passed_count)]
            
    except Exception as e:
        print(f"获取面试数据失败：{str(e)}")
    
    try:
        return render_template('smartrecruit/hr/hr_interviews_ios.html', 
                             interviews=interviews_data,
                             candidates=candidates_data)
    except Exception:
        return render_template('smartrecruit/hr/hr_dashboard.html')


@dashboard_bp.route('/candidates', endpoint='candidates')
@dashboard_bp.route('/candidates/', endpoint='candidates_slash')
def candidates():
    if g.get('user') is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户可以访问该页面。', 'danger')
        return redirect(url_for('common.auth.sign'))

    # 准备概览统计与最近候选人（最多5条）
    recent = []
    total = pending = interview = approved = 0
    try:
        if db is None:
            raise RuntimeError('DB unavailable')

        app_rows = (
            Application.query
            .order_by(Application.timestamp.desc())
            .limit(50)
            .all()
        )
        for app_row in app_rows:
            user = User.query.get(app_row.user_id)
            if not user:
                continue
            job = Job.query.get(app_row.job_id)
            if job and job.user_id != g.user.id:
                continue
            status = (getattr(app_row, 'status', 'pending') or 'pending')
            total += 1
            if status == 'pending':
                pending += 1
            elif status == 'interview':
                interview += 1
            elif status == 'approved':
                approved += 1
            # 仅收集前5个用于首页展示
            if len(recent) < 5:
                recent.append({
                    'user': user,
                    'first_name': getattr(user, 'first_name', ''),
                    'last_name': getattr(user, 'last_name', ''),
                    'email': getattr(user, 'email', ''),
                    'position': getattr(user, 'position', ''),
                    'applied_date': app_row.timestamp.strftime('%Y-%m-%d %H:%M') if getattr(app_row, 'timestamp', None) else '',
                    'status': status,
                })
    except Exception:
        recent = []

    try:
        return render_template(
            'smartrecruit/hr/hr_candidates_ios.html',
            candidates=recent,
            total_applications=total,
            pending_applications=pending,
            interview_applications=interview,
            approved_applications=approved,
        )
    except Exception:
        return redirect(url_for('smartrecruit.hr.dashboard.candidates_list'))


@dashboard_bp.route('/reports', endpoint='reports')
def reports():
    if g.get('user') is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户可以访问该页面。', 'danger')
        return redirect(url_for('common.auth.sign'))

    # 收集报表数据
    report_data = {
        'total_jobs': 0,
        'total_applications': 0,
        'recruitment_cycle': 30,
        'offer_acceptance_rate': 85,
        'recruitment_cost': 15000,
        'funnel_data': {
            'applied': 0,
            'screened': 0,
            'interview': 0,
            'offer': 0,
            'hired': 0
        }
    }

    try:
        if db is not None:
            # 获取当前HR的职位数量
            from app.models import Job, Application
            report_data['total_jobs'] = Job.query.filter_by(user_id=g.user.id).count()

            # 获取申请数量统计
            jobs = Job.query.filter_by(user_id=g.user.id).all()
            job_ids = [job.id for job in jobs]

            if job_ids:
                applications = Application.query.filter(Application.job_id.in_(job_ids)).all()
                report_data['total_applications'] = len(applications)

                # 统计不同状态的申请
                status_counts = {}
                for app in applications:
                    status = getattr(app, 'status', 'pending') or 'pending'
                    status_counts[status] = status_counts.get(status, 0) + 1

                # 更新漏斗数据
                report_data['funnel_data']['applied'] = report_data['total_applications']
                report_data['funnel_data']['screened'] = status_counts.get('screened', 0)
                report_data['funnel_data']['interview'] = status_counts.get('interview', 0)
                report_data['funnel_data']['offer'] = status_counts.get('offer', 0)
                report_data['funnel_data']['hired'] = status_counts.get('hired', 0)

                # 计算Offer接受率
                if status_counts.get('offer', 0) > 0:
                    report_data['offer_acceptance_rate'] = int(
                        (status_counts.get('hired', 0) / status_counts.get('offer', 0)) * 100
                    )

    except Exception as e:
        print(f"获取报表数据失败：{str(e)}")

    try:
        return render_template('smartrecruit/hr/hr_reports_ios.html', report_data=report_data)
    except Exception:
        return render_template('smartrecruit/hr/hr_dashboard.html')


@dashboard_bp.route('/candidates/list', endpoint='candidates_list')
@dashboard_bp.route('/candidates/list/', endpoint='candidates_list_slash')
def candidates_list():
    if g.get('user') is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户可以访问该页面。', 'danger')
        return redirect(url_for('common.auth.sign'))

    # 汇总最近候选人申请（可选关键词/状态过滤）
    recent = []
    q_keyword = (request.args.get('q') or '').strip().lower()
    q_status = (request.args.get('status') or '').strip().lower()
    try:
        if db is None:
            raise RuntimeError('DB unavailable')
        app_query = Application.query.order_by(Application.timestamp.desc()).limit(200)
        app_rows = app_query.all()
        for app_row in app_rows:
            user = User.query.get(app_row.user_id)
            if not user:
                continue
            job = Job.query.get(app_row.job_id)
            if job and job.user_id != g.user.id:
                # 仅显示当前HR发布职位的申请
                continue
            full_name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
            item_status = (getattr(app_row, 'status', 'pending') or 'pending').lower()
            candidate_item = {
                'id': user.id,
                'name': full_name or getattr(user, 'email', '') or f"用户{user.id}",
                'job_title': getattr(user, 'position', '') or (job.title if job else ''),
                'email': getattr(user, 'email', ''),
                'phone': getattr(user, 'phone_number', ''),
                'application_date': app_row.timestamp.strftime('%Y-%m-%d %H:%M') if getattr(app_row, 'timestamp', None) else '',
                'has_resume': bool(getattr(user, 'cv_file', None)),
                'status': item_status,
            }
            # 关键词过滤（姓名/邮箱/职位）
            if q_keyword:
                blob = ' '.join([
                    candidate_item['name'].lower(),
                    candidate_item['email'].lower(),
                    (candidate_item['job_title'] or '').lower(),
                ])
                if q_keyword not in blob:
                    continue
            # 状态过滤
            if q_status and q_status != item_status:
                continue
            recent.append(candidate_item)
    except Exception:
        recent = []

    # 统计
    total = len(recent)
    pending = len([x for x in recent if x['status'] == 'pending'])
    interview = len([x for x in recent if x['status'] == 'interview'])
    approved = len([x for x in recent if x['status'] == 'approved'])
    withdrawn = len([x for x in recent if x['status'] == 'withdrawn'])

    # 复用 iOS 模板所需变量命名
    return render_template(
        'smartrecruit/hr/candidate_list.html',
        candidates=recent,
        total_applications=total,
        pending_applications=pending,
        interview_applications=interview,
        approved_applications=approved,
        withdrawn_applications=withdrawn,
        q=q_keyword,
        status=q_status,
    )


@dashboard_bp.route('/candidates/filter', endpoint='candidates_filter')
@dashboard_bp.route('/candidates/filter/', endpoint='candidates_filter_slash')
def candidates_filter():
    if g.get('user') is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户可以访问该页面。', 'danger')
        return redirect(url_for('common.auth.sign'))

    # 读取筛选参数
    search_query = (request.args.get('search') or '').strip()
    status_filter = (request.args.get('status') or '').strip().lower()
    job_filter = (request.args.get('job') or '').strip()
    sort_by = (request.args.get('sort') or 'date_desc').strip()
    auto_filter = (request.args.get('auto_filter') or 'false').lower() == 'true'
    min_skills_match = int((request.args.get('min_skills_match') or '0') or 0)
    min_experience = int((request.args.get('min_experience') or '0') or 0)
    education_required = (request.args.get('education_required') or '').strip()
    location_match = (request.args.get('location_match') or '').strip()

    # 可选职位列表（当前HR发布）
    available_jobs = []
    try:
        if db is not None:
            available_jobs = Job.query.filter_by(user_id=g.user.id).order_by(Job.id.desc()).all()
    except Exception:
        available_jobs = []

    # 构建候选人池（当前HR职位的申请）
    candidates = []
    try:
        if db is None:
            raise RuntimeError('DB unavailable')
        app_query = Application.query.join(Job, Job.id == Application.job_id).filter(Job.user_id == g.user.id)
        if job_filter:
            try:
                app_query = app_query.filter(Application.job_id == int(job_filter))
            except Exception:
                pass
        app_query = app_query.order_by(Application.timestamp.desc()).limit(300)
        app_rows = app_query.all()
        for app_row in app_rows:
            user = User.query.get(app_row.user_id)
            job = Job.query.get(app_row.job_id) if app_row.job_id else None
            if not user:
                continue
            # 计算轻量匹配指标（非AI）
            skills_text = (getattr(user, 'skills', '') or '') + ' ' + (getattr(user, 'bio', '') or '')
            job_title = (job.title if job else '')
            name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip() or getattr(user, 'email', '')
            skills_match = 0
            try:
                # 粗略：职位名中的词是否出现在技能/简介中
                import re
                tokens = [t for t in re.split(r'[\s,;，。/]+', job_title.lower()) if t]
                hit = sum(1 for t in tokens if t and t in skills_text.lower())
                skills_match = int(100 * hit / max(1, len(tokens))) if tokens else 0
            except Exception:
                skills_match = 0
            try:
                experience_years = int(getattr(user, 'experience_years', 0) or 0)
            except Exception:
                experience_years = 0
            education_level = (getattr(user, 'education', '') or '')
            location_text = (getattr(user, 'location', '') or '')
            status = (getattr(app_row, 'status', 'pending') or 'pending').lower()

            item = {
                'id': user.id,
                'name': name,
                'job_title': job_title,
                'email': getattr(user, 'email', ''),
                'phone': getattr(user, 'phone_number', ''),
                'applied_date': app_row.timestamp.strftime('%Y-%m-%d %H:%M') if getattr(app_row, 'timestamp', None) else '',
                'status': status,
                'skills_match': skills_match,
                'experience_years': experience_years,
                'education_level': education_level,
            }

            # 文本搜索
            if search_query:
                blob = ' '.join([
                    name.lower(),
                    (item['email'] or '').lower(),
                    (job_title or '').lower(),
                ])
                if search_query.lower() not in blob:
                    continue

            # 状态过滤
            if status_filter and status_filter != status:
                continue

            # 教育过滤
            if education_required and education_required not in education_level:
                continue

            # 位置过滤
            if location_match and location_match not in location_text:
                continue

            # 智能（规则）过滤：不用AI，仅按阈值剔除
            if auto_filter:
                if skills_match < min_skills_match:
                    continue
                if experience_years < min_experience:
                    continue

            candidates.append(item)

        # 排序
        def sort_key(c):
            if sort_by == 'date_asc':
                return c['applied_date']
            if sort_by == 'name_asc':
                return c['name']
            if sort_by == 'name_desc':
                return ('~' + c['name'])  # 简化逆序
            if sort_by == 'skills_match':
                return -c['skills_match']
            if sort_by == 'ai_score':
                return 0  # 未接AI，置0
            return c['applied_date']
        reverse = sort_by in ('date_desc', 'skills_match')
        candidates.sort(key=sort_key, reverse=reverse)
    except Exception:
        candidates = []

    return render_template(
        'smartrecruit/hr/candidate_filter.html',
        candidates=candidates,
        available_jobs=available_jobs,
        search_query=search_query,
        status_filter=status_filter,
        job_filter=job_filter,
        sort_by=sort_by,
        auto_filter=auto_filter,
        min_skills_match=min_skills_match,
        min_experience=min_experience,
        education_required=education_required,
        location_match=location_match,
    )


@dashboard_bp.route('/candidates/filter/apply', methods=['GET', 'POST'], endpoint='candidates_filter_apply')
def candidates_filter_apply():
    if g.get('user') is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户可以访问该页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    # 读取筛选条件，不接AI，仅服务器端过滤
    keyword = (request.values.get('q') or '').strip()
    status = (request.values.get('status') or '').strip()
    return redirect(url_for('smartrecruit.hr.dashboard.candidates_list', q=keyword, status=status))


@dashboard_bp.route('/candidates/filter/smart', methods=['POST'], endpoint='candidates_filter_smart')
def candidates_filter_smart():
    # 预留智能筛选端口：当前不接AI，返回占位响应
    return {'ok': False, 'message': '智能筛选尚未启用（接口占位）'}, 501


@dashboard_bp.route('/candidates/view/<int:candidate_id>', endpoint='view_candidate')
def view_candidate(candidate_id: int):
    # 直接复用现有的候选人简历视图
    return redirect(url_for('smartrecruit.hr.candidates.view_candidate_resume', user_id=candidate_id))


def _find_latest_app_for_user(candidate_id: int):
    if db is None:
        return None
    try:
        # 在当前HR发布的职位里找该候选人最新申请
        apps = (
            Application.query
            .join(Job, Job.id == Application.job_id)
            .filter(Application.user_id == candidate_id, Job.user_id == g.user.id)
            .order_by(Application.timestamp.desc())
            .all()
        )
        return apps[0] if apps else None
    except Exception:
        return None


@dashboard_bp.route('/candidates/approve/<int:candidate_id>', methods=['POST'], endpoint='approve_candidate')
def approve_candidate(candidate_id: int):
    if g.get('user') is None:
        abort(401)
    if not getattr(g.user, 'is_hr', False):
        abort(403)
    app_row = _find_latest_app_for_user(candidate_id)
    if not app_row:
        flash('未找到该候选人的申请记录。', 'warning')
        return redirect(url_for('smartrecruit.hr.dashboard.candidates_list'))
    try:
        app_row.status = 'approved'
        db.session.commit()
        flash('已通过该候选人的最新申请。', 'success')
    except Exception:
        if db:
            db.session.rollback()
        flash('操作失败，请稍后重试。', 'danger')
    return redirect(url_for('smartrecruit.hr.dashboard.candidates_list'))


@dashboard_bp.route('/candidates/reject/<int:candidate_id>', methods=['POST'], endpoint='reject_candidate')
def reject_candidate(candidate_id: int):
    if g.get('user') is None:
        abort(401)
    if not getattr(g.user, 'is_hr', False):
        abort(403)
    app_row = _find_latest_app_for_user(candidate_id)
    if not app_row:
        flash('未找到该候选人的申请记录。', 'warning')
        return redirect(url_for('smartrecruit.hr.dashboard.candidates_list'))
    try:
        app_row.status = 'rejected'
        db.session.commit()
        flash('已拒绝该候选人的最新申请。', 'success')
    except Exception:
        if db:
            db.session.rollback()
        flash('操作失败，请稍后重试。', 'danger')
    return redirect(url_for('smartrecruit.hr.dashboard.candidates_list'))


@dashboard_bp.route('/candidates/schedule/<int:candidate_id>', methods=['GET', 'POST'], endpoint='schedule_interview')
def schedule_interview(candidate_id: int):
    if g.get('user') is None:
        abort(401)
    if not getattr(g.user, 'is_hr', False):
        abort(403)
    # 简化：此处仅跳转到面试列表/页面，实际排期表单可后续实现
    flash('请在“面试”模块中安排面试。', 'info')
    return redirect(url_for('smartrecruit.hr.dashboard.interviews'))


@dashboard_bp.route('/candidates/notify', methods=['POST'], endpoint='send_interview_notification')
def send_interview_notification():
    # 仅返回成功，预留实际发送逻辑
    try:
        return {'success': True}, 200
    except Exception as e:
        return {'success': False, 'message': str(e)}, 500


@dashboard_bp.route('/candidates/approve_and_notify', methods=['POST'], endpoint='approve_and_notify')
def approve_and_notify():
    """将候选人设为通过并写入通知信息（用于筛选页面一键通过并通知）。"""
    if g.get('user') is None:
        abort(401)
    if not getattr(g.user, 'is_hr', False):
        abort(403)
    try:
        from app.models import Application
    except Exception:
        return {'success': False, 'message': 'DB unavailable'}, 500

    ids = (request.values.get('candidate_ids') or '').strip()
    application_id_val = (request.values.get('application_id') or '').strip()
    message = (request.values.get('message') or '请你在三天之内完成AI正式面试').strip()
    id_list = [int(x) for x in ids.split(',') if x.strip().isdigit()]
    updated = 0
    try:
        target_apps = []
        if application_id_val.isdigit():
            try:
                app_obj = Application.query.get(int(application_id_val))
                if app_obj:
                    target_apps.append(app_obj)
            except Exception:
                pass
        if not target_apps:
            for candidate_id in id_list:
                # 优先在当前HR发布的职位中查找该候选人的最近申请
                app_row = _find_latest_app_for_user(candidate_id)
                if not app_row:
                    # 回退：不限定职位归属，取候选人最近一条申请
                    try:
                        app_row = (
                            Application.query
                            .filter_by(user_id=candidate_id)
                            .order_by(Application.timestamp.desc())
                            .first()
                        )
                    except Exception:
                        app_row = None
                if app_row:
                    target_apps.append(app_row)
        if not target_apps:
            return {'success': False, 'message': '未找到可更新的申请'}, 404
        updated_candidates = set()
        for app_row in target_apps:
            # 标记通过，确保激活，并更新时间戳
            app_row.status = 'approved'
            try:
                app_row.is_active = True
            except Exception:
                pass
            try:
                # 尽量更新为当前时间，便于列表刷新排序
                app_row.timestamp = datetime.utcnow()
            except Exception:
                pass
            try:
                old_msg = getattr(app_row, 'message', '') or ''
                sep = '\n' if old_msg else ''
                app_row.message = f"{old_msg}{sep}{message}"
            except Exception:
                app_row.message = message
            updated += 1
            try:
                updated_candidates.add(int(getattr(app_row, 'user_id', 0) or 0))
            except Exception:
                pass
        if updated:
            db.session.commit()
            # 同步写入候选人消息收件箱（Mongo）
            try:
                from app import applications_collection
                from datetime import datetime as _dt
                for candidate_id in (updated_candidates or set(id_list)):
                    applications_collection.insert_one({
                        'user_id': str(candidate_id),
                        'message': message,
                        'created_at': _dt.utcnow(),
                        'type': 'ai_interview_notice'
                    })
            except Exception:
                pass
            # 同步写入SQL通知，供收件箱读取
            try:
                from app.models import FeedbackNotification
                from datetime import datetime as _dt
                for candidate_id in (updated_candidates or set(id_list)):
                    notif = FeedbackNotification(
                        user_id=candidate_id,
                        feedback_id=0,
                        notification_type='ai_interview_notice',
                        title='AI面试通知',
                        message=message,
                        is_read=False,
                        created_at=_dt.utcnow()
                    )
                    db.session.add(notif)
                db.session.commit()
            except Exception:
                if db:
                    db.session.rollback()
        return {'success': True, 'updated': updated}, 200
    except Exception as e:
        if db:
            db.session.rollback()
        return {'success': False, 'message': str(e)}, 500


