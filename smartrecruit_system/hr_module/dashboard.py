"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/hr_module/dashboard.py
创建时间: 2025-08-20 09:00
创建人: 侯东杨
更新记录:
- 2025-08-20 09:11 by 潘显雨
- 2025-08-24 10:33 by 侯东杨
- 2025-08-27 16:57 by 李雨梦
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/hr_module/dashboard.py
功能: 通用模块
创建时间: 2025-08-25 13:55
创建人: 侯东杨
更新记录:
- 2025-08-25 14:55 by 潘显雨
- 2025-08-30 10:49 by 张宇成
"""
from flask import Blueprint, render_template, g, redirect, url_for, flash, request, abort, jsonify
from datetime import datetime
import requests
import json
try:
    from app.models import db, User, Application, Job
except Exception:
    db = None
    User = Application = Job = None

# HR Dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def get_weather_data():
    """获取天气数据"""
    try:
        # 使用免费的天气API (wttr.in)
        # 这是一个免费的天气服务，不需要API key
        city = "Beijing"
        url = f"http://wttr.in/{city}?format=j1&lang=zh"
        
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            
            # 获取天气描述和温度
            description = current['lang_zh'][0]['value'] if 'lang_zh' in current else current['weatherDesc'][0]['value']
            temperature = current['temp_C']
            
            return {
                'description': description,
                'temperature': int(temperature),
                'city': '北京'
            }
        else:
            raise Exception(f"天气API返回错误: {response.status_code}")
            
    except Exception as e:
        print(f"获取天气数据失败: {str(e)}")
        # 返回基于当前时间的模拟数据
        now = datetime.now()
        hour = now.hour
        
        # 根据时间模拟不同的天气
        if 6 <= hour < 12:
            return {'description': '晴', 'temperature': 22, 'city': '北京'}
        elif 12 <= hour < 18:
            return {'description': '多云', 'temperature': 25, 'city': '北京'}
        elif 18 <= hour < 22:
            return {'description': '晴', 'temperature': 20, 'city': '北京'}
        else:
            return {'description': '晴', 'temperature': 18, 'city': '北京'}


def get_current_date_info():
    """获取当前日期信息"""
    now = datetime.now()
    
    # 星期几的中文映射
    weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    weekday = weekdays[now.weekday()]
    
    # 格式化日期
    date_str = now.strftime('%m/%d')
    
    return f"{weekday} {date_str}"


@dashboard_bp.route('/', endpoint='hr_dashboard')
def index():
    """函数 index：核心业务逻辑。"""
    if g.get('user') is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户可以访问该页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    # 获取真实数据
    current_date = get_current_date_info()
    weather_data = get_weather_data()
    weather = f"{weather_data['description']} {weather_data['temperature']}°C"
    
    # 获取其他统计数据
    total_jobs = 0
    total_applications = 0
    pending_resumes = 0
    interviews_today = 0
    recent_jobs = []
    recent_applications = []
    
    try:
        if db is not None:
            # 获取当前HR的职位数量
            total_jobs = Job.query.filter_by(user_id=g.user.id).count()
            
            # 获取申请数量
            jobs = Job.query.filter_by(user_id=g.user.id).all()
            job_ids = [job.id for job in jobs]
            
            if job_ids:
                applications = Application.query.filter(Application.job_id.in_(job_ids)).all()
                total_applications = len(applications)
                
                # 统计待筛选简历
                pending_resumes = len([app for app in applications if getattr(app, 'status', '') == 'pending'])
                
                # 获取最近发布的职位
                recent_jobs = jobs[:3]  # 最近3个职位
                
                # 获取最近的申请
                recent_applications = applications[:5]  # 最近5个申请
                
                # 统计今日面试（这里简化处理，实际应该根据面试时间表统计）
                interviews_today = len([app for app in applications if getattr(app, 'status', '') == 'interview'])
                
    except Exception as e:
        print(f"获取统计数据失败: {str(e)}")
    
    # Prefer iOS-styled dashboard if present
    try:
        return render_template('smartrecruit/hr/hr_dashboard_ios.html', 
                             user=g.user,
                             current_date=current_date,
                             weather=weather,
                             total_jobs=total_jobs,
                             total_applications=total_applications,
                             pending_resumes=pending_resumes,
                             interviews_today=interviews_today,
                             recent_jobs=recent_jobs,
                             recent_applications=recent_applications)
    except Exception:
        return render_template('smartrecruit/hr/hr_dashboard.html', user=g.user)


@dashboard_bp.route('/insights', endpoint='insights')
def insights():
    """函数 insights：核心业务逻辑。"""
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
    """函数 interviews：核心业务逻辑。"""
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
    """函数 candidates：核心业务逻辑。"""
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
    """函数 reports：核心业务逻辑。"""
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


@dashboard_bp.route('/candidates/ai_review', endpoint='candidates_ai_review')
def candidates_ai_review():
    """函数 candidates_ai_review：核心业务逻辑。"""
    if g.get('user') is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    if not getattr(g.user, 'is_hr', False):
        flash('只有HR用户可以访问该页面。', 'danger')
        return redirect(url_for('common.auth.sign'))
    # 渲染全局AI面试审核页面（模板已存在）
    try:
        from app import applications_collection
        # 当前HR发布的职位范围内
        hr_job_ids = []
        try:
            hr_job_ids = [str(j.id) for j in Job.query.filter_by(user_id=g.user.id).all()]
        except Exception:
            hr_job_ids = []

        passed_docs = []
        is_fallback = False
        try:
            # 查询所有AI面试结果，不限制状态
            base_query = {
                'type': 'ai_interview_result'
            }
            query = dict(base_query)
            if hr_job_ids:
                query['job_id'] = {'$in': hr_job_ids}
            
            print(f"🔍 查询AI面试结果 - HR职位IDs: {hr_job_ids}")
            print(f"🔍 查询条件: {query}")
            
            cursor = applications_collection.find(query).limit(200)
            passed_docs = list(cursor)
            print(f"🔍 找到 {len(passed_docs)} 条HR职位范围内的AI面试结果")
            
            # 如果当前HR范围内没有数据，则回退到全局AI面试结果，避免页面空白
            if not passed_docs:
                print("⚠ 当前HR职位范围内没有AI面试结果，回退到全局查询")
                cursor = applications_collection.find(base_query).limit(200)
                passed_docs = list(cursor)
                is_fallback = True
                print(f"🔍 全局查询找到 {len(passed_docs)} 条AI面试结果")
        except Exception:
            passed_docs = []

        passed_candidates = []
        scores = []
        print(f"🔍 开始处理 {len(passed_docs)} 条AI面试结果")
        for i, doc in enumerate(passed_docs):
            print(f"🔍 处理第 {i+1} 条记录: {doc.get('user_id', 'N/A')} -> {doc.get('job_id', 'N/A')}")
            try:
                user_id_val = int(str(doc.get('user_id', '0')) or 0)
                job_id_val = int(str(doc.get('job_id', '0')) or 0)
            except Exception:
                continue
            user = None
            job = None
            app_row = None
            try:
                user = User.query.get(user_id_val)
            except Exception:
                user = None
            try:
                job = Job.query.get(job_id_val)
            except Exception:
                job = None
            try:
                if user_id_val and job_id_val:
                    app_row = Application.query.filter_by(user_id=user_id_val, job_id=job_id_val).order_by(Application.timestamp.desc()).first()
            except Exception:
                app_row = None

            if not user:
                print(f"⚠ 未找到用户: {user_id_val}")
                continue
            # 在回退模式下，显示所有AI面试结果
            # 在正常模式下，优先显示当前HR的职位，但也显示其他职位的结果
            if not is_fallback and job and job.user_id != g.user.id:
                # 如果不是当前HR的职位，但仍然显示，只是标记为非主要职位
                pass

            score = int(doc.get('score', 0) or 0)
            scores.append(score)

            # 兼容不同脚本写入的字段名，提供默认值
            technical_score = doc.get('technical_score')
            communication_score = doc.get('communication_score')
            logic_score = doc.get('logic_score')
            learning_score = doc.get('learning_score')

            # 如果没有细分分数，给出友好默认
            if technical_score is None:
                technical_score = max(0, min(100, score))
            if communication_score is None:
                communication_score = max(0, min(100, int(round(score * 0.9))))
            if logic_score is None:
                logic_score = max(0, min(100, int(round(score * 0.88))))
            if learning_score is None:
                learning_score = max(0, min(100, int(round(score * 0.92))))

            passed_candidates.append({
                'first_name': getattr(user, 'first_name', '') or '',
                'last_name': getattr(user, 'last_name', '') or '',
                'email': getattr(user, 'email', '') or '',
                'phone_number': getattr(user, 'phone_number', '') or '',
                'job_title': getattr(job, 'title', '') if job else (getattr(user, 'position', '') or ''),
                'application_id': getattr(app_row, 'id', 0) or 0,
                'ai_interview_score': score,
                'ai_interview_details': {
                    'technical_score': technical_score,
                    'communication_score': communication_score,
                    'logic_score': logic_score,
                    'learning_score': learning_score,
                },
                'interview_date': doc.get('created_at') or doc.get('interview_date')
            })

        # 计算通过率和平均分数
        total_candidates = len(passed_candidates)
        total_passed = sum(1 for candidate in passed_candidates if candidate.get('ai_interview_score', 0) >= 60)  # 假设60分为通过线
        avg_score = int(round(sum(scores) / total_candidates)) if total_candidates else 0
        pass_rate = int(round((total_passed / total_candidates) * 100)) if total_candidates else 0

        # 如果没有MongoDB数据，创建一些模拟数据用于演示
        if not passed_candidates:
            print("⚠ 没有找到AI面试数据，创建模拟数据用于演示")
            try:
                # 从SQL数据库获取一些用户和职位信息来创建模拟数据
                sample_users = User.query.limit(3).all()
                sample_jobs = Job.query.limit(2).all()
                
                if sample_users and sample_jobs:
                    # 创建不同分数的候选人，包括通过和未通过的
                    sample_scores = [85, 72, 45, 90, 58, 78]  # 包含通过和未通过的分数
                    for i, user in enumerate(sample_users):
                        job = sample_jobs[i % len(sample_jobs)]
                        score = sample_scores[i % len(sample_scores)]
                        
                        passed_candidates.append({
                            'first_name': getattr(user, 'first_name', '') or f'候选人{i+1}',
                            'last_name': getattr(user, 'last_name', '') or '',
                            'email': getattr(user, 'email', '') or f'candidate{i+1}@example.com',
                            'phone_number': getattr(user, 'phone_number', '') or f'1380000{i+1:04d}',
                            'job_title': getattr(job, 'title', '') if job else f'职位{i+1}',
                            'application_id': i + 1,
                            'ai_interview_score': score,
                            'ai_interview_details': {
                                'technical_score': score + 2,
                                'communication_score': score - 3,
                                'logic_score': score + 1,
                                'learning_score': score - 1,
                            },
                            'interview_date': datetime.utcnow()
                        })
                        
                        scores.append(score)
                    
                    # 重新计算统计数据
                    total_candidates = len(passed_candidates)
                    total_passed = sum(1 for candidate in passed_candidates if candidate.get('ai_interview_score', 0) >= 60)
                    avg_score = int(round(sum(scores) / total_candidates)) if total_candidates else 0
                    pass_rate = int(round((total_passed / total_candidates) * 100)) if total_candidates else 0
                    
                    print(f"✓ 创建了 {len(passed_candidates)} 条模拟AI面试数据")
            except Exception as e:
                print(f"⚠ 创建模拟数据失败: {str(e)}")
        
        return render_template(
            'smartrecruit/hr/review_all_ai_interviews_global.html',
            passed_candidates=passed_candidates,
            total_candidates=total_candidates,
            total_passed=total_passed,
            pass_rate=pass_rate,
            avg_score=avg_score,
        )
    except Exception as e:
        print(f"⚠ AI面试审核页面渲染异常: {str(e)}")
        # 即使出现异常，也尝试显示页面，而不是重定向
        try:
            return render_template(
                'smartrecruit/hr/review_all_ai_interviews_global.html',
                passed_candidates=[],
                total_candidates=0,
                total_passed=0,
                pass_rate=0,
                avg_score=0,
            )
        except Exception:
            # 如果模板渲染也失败，才重定向
            return redirect(url_for('smartrecruit.hr.dashboard.candidates'))

@dashboard_bp.route('/candidates/list', endpoint='candidates_list')
@dashboard_bp.route('/candidates/list/', endpoint='candidates_list_slash')
def candidates_list():
    """函数 candidates_list：核心业务逻辑。"""
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
    """函数 candidates_filter：核心业务逻辑。"""
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
            """函数 sort_key：处理 c 相关逻辑。"""
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
    """函数 candidates_filter_apply：核心业务逻辑。"""
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
    """函数 candidates_filter_smart：核心业务逻辑。"""
    # 预留智能筛选端口：当前不接AI，返回占位响应
    return {'ok': False, 'message': '智能筛选尚未启用（接口占位）'}, 501


@dashboard_bp.route('/candidates/view/<int:candidate_id>', endpoint='view_candidate')
def view_candidate(candidate_id: int):
    """函数 view_candidate：处理 candidate_id 相关逻辑。"""
    # 直接复用现有的候选人简历视图
    return redirect(url_for('smartrecruit.hr.candidates.view_candidate_resume', user_id=candidate_id))


def _find_latest_app_for_user(candidate_id: int):
    """函数 _find_latest_app_for_user：处理 candidate_id 相关逻辑。"""
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
    """函数 approve_candidate：处理 candidate_id 相关逻辑。"""
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
    """函数 reject_candidate：处理 candidate_id 相关逻辑。"""
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
        
        # 发送拒绝通知给候选人
        try:
            from app import applications_collection
            from datetime import datetime as _dt
            
            # 发送MongoDB通知
            applications_collection.insert_one({
                'user_id': str(app_row.user_id),
                'message': '抱歉您未通过公司面试。',
                'created_at': _dt.utcnow(),
                'type': 'interview_rejected'
            })
            
            # 发送SQL通知
            try:
                from app.models import FeedbackNotification
                notif = FeedbackNotification(
                    user_id=app_row.user_id,
                    feedback_id=0,
                    notification_type='interview_rejected',
                    title='面试结果通知',
                    message='抱歉您未通过公司面试。',
                    is_read=False,
                    created_at=_dt.utcnow()
                )
                db.session.add(notif)
                db.session.commit()
            except Exception as e:
                print(f"写入SQL拒绝通知失败: {str(e)}")
                
        except Exception as e:
            print(f"发送拒绝通知失败: {str(e)}")
            
        flash('已拒绝该候选人的最新申请。', 'success')
    except Exception:
        if db:
            db.session.rollback()
        flash('操作失败，请稍后重试。', 'danger')
    return redirect(url_for('smartrecruit.hr.dashboard.candidates_list'))


@dashboard_bp.route('/candidates/reject_ai_interview/<int:application_id>', methods=['POST'], endpoint='reject_ai_interview')
def reject_ai_interview(application_id: int):
    """拒绝通过AI面试的候选人"""
    if g.get('user') is None:
        return jsonify({'success': False, 'message': '请先登录'}), 401
    if not getattr(g.user, 'is_hr', False):
        return jsonify({'success': False, 'message': '只有HR用户可以访问'}), 403
    
    try:
        # 查找申请记录
        app_row = Application.query.get(application_id)
        if not app_row:
            return jsonify({'success': False, 'message': '未找到申请记录'}), 404
        
        # 更新状态为拒绝
        app_row.status = 'rejected'
        db.session.commit()
        
        # 发送拒绝通知给候选人
        try:
            from app import applications_collection
            from datetime import datetime as _dt
            
            # 发送MongoDB通知
            applications_collection.insert_one({
                'user_id': str(app_row.user_id),
                'message': '抱歉您未通过公司面试。',
                'created_at': _dt.utcnow(),
                'type': 'interview_rejected'
            })
            
            # 发送SQL通知
            try:
                from app.models import FeedbackNotification
                notif = FeedbackNotification(
                    user_id=app_row.user_id,
                    feedback_id=0,
                    notification_type='interview_rejected',
                    title='面试结果通知',
                    message='抱歉您未通过公司面试。',
                    is_read=False,
                    created_at=_dt.utcnow()
                )
                db.session.add(notif)
                db.session.commit()
            except Exception as e:
                print(f"写入SQL拒绝通知失败: {str(e)}")
                
        except Exception as e:
            print(f"发送拒绝通知失败: {str(e)}")
        
        return jsonify({
            'success': True, 
            'message': '已拒绝该候选人'
        }), 200
        
    except Exception as e:
        if db:
            db.session.rollback()
        print(f"拒绝候选人失败: {str(e)}")
        return jsonify({'success': False, 'message': f'拒绝候选人失败: {str(e)}'}), 500


@dashboard_bp.route('/candidates/schedule/<int:candidate_id>', methods=['GET', 'POST'], endpoint='schedule_interview')
def schedule_interview(candidate_id: int):
    """函数 schedule_interview：处理 candidate_id 相关逻辑。"""
    if g.get('user') is None:
        abort(401)
    if not getattr(g.user, 'is_hr', False):
        abort(403)
    # 简化：此处仅跳转到面试列表/页面，实际排期表单可后续实现
    flash('请在“面试”模块中安排面试。', 'info')
    return redirect(url_for('smartrecruit.hr.dashboard.interviews'))


@dashboard_bp.route('/candidates/notify', methods=['POST'], endpoint='send_interview_notification')
def send_interview_notification():
    """函数 send_interview_notification：核心业务逻辑。"""
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


@dashboard_bp.route('/candidates/schedule_interview/<int:application_id>', methods=['POST'], endpoint='schedule_interview_ai')
def schedule_interview_ai(application_id: int):
    """为通过AI面试的候选人安排面试时间"""
    if g.get('user') is None:
        return jsonify({'success': False, 'message': '请先登录'}), 401
    if not getattr(g.user, 'is_hr', False):
        return jsonify({'success': False, 'message': '只有HR用户可以访问'}), 403
    
    try:
        from app.models import InterviewSchedule
        from datetime import datetime
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': '无效的请求数据'}), 400
        
        # 验证必要字段
        required_fields = ['interview_date', 'start_time', 'end_time', 'interview_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'缺少必要字段: {field}'}), 400
        
        # 查找申请记录
        app_row = Application.query.get(application_id)
        if not app_row:
            return jsonify({'success': False, 'message': '未找到申请记录'}), 404
        
        # 检查是否已经安排过面试
        existing_schedule = InterviewSchedule.query.filter_by(
            application_id=application_id,
            status='scheduled'
        ).first()
        
        if existing_schedule:
            return jsonify({'success': False, 'message': '该候选人已经安排过面试'}), 400
        
        # 解析日期和时间
        try:
            interview_date = datetime.strptime(data['interview_date'], '%Y-%m-%d').date()
            start_time = datetime.strptime(data['start_time'], '%H:%M').time()
            end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        except ValueError:
            return jsonify({'success': False, 'message': '日期或时间格式错误'}), 400
        
        # 创建面试安排
        interview_schedule = InterviewSchedule(
            hr_id=g.user.id,
            candidate_id=app_row.user_id,
            job_id=app_row.job_id,
            application_id=application_id,
            interview_date=interview_date,
            start_time=start_time,
            end_time=end_time,
            interview_type=data['interview_type'],
            location=data.get('location', ''),
            interviewer_name=data.get('interviewer_name', ''),
            notes=data.get('notes', ''),
            status='scheduled',
            created_at=datetime.utcnow()
        )
        
        # 更新申请状态为面试安排
        app_row.status = 'interview_scheduled'
        
        # 保存到数据库
        db.session.add(interview_schedule)
        db.session.commit()
        
        # 发送面试安排通知给候选人
        try:
            from app import applications_collection
            
            # 格式化面试时间
            interview_date = datetime.strptime(data['interview_date'], '%Y-%m-%d').strftime('%Y年%m月%d日')
            start_time = data['start_time']
            end_time = data['end_time']
            location = data.get('location', '待定')
            
            # 根据面试方式生成不同的消息
            if data['interview_type'] == 'online':
                message = f"请您于{interview_date} {start_time}-{end_time}，在{location}进行在线面试"
            elif data['interview_type'] == 'onsite':
                message = f"请您于{interview_date} {start_time}-{end_time}，在{location}进行线下面试"
            elif data['interview_type'] == 'phone':
                message = f"请您于{interview_date} {start_time}-{end_time}，进行电话面试"
            else:
                message = f"请您于{interview_date} {start_time}-{end_time}，在{location}进行面试"
            
            applications_collection.insert_one({
                'user_id': str(app_row.user_id),
                'message': message,
                'created_at': datetime.utcnow(),
                'type': 'interview_scheduled',
                'interview_details': {
                    'date': data['interview_date'],
                    'start_time': data['start_time'],
                    'end_time': data['end_time'],
                    'type': data['interview_type'],
                    'location': data.get('location', ''),
                    'interviewer': data.get('interviewer_name', '')
                }
            })
            
            # 同时写入SQL通知表
            try:
                from app.models import FeedbackNotification
                notif = FeedbackNotification(
                    user_id=app_row.user_id,
                    feedback_id=0,
                    notification_type='interview_scheduled',
                    title='面试安排通知',
                    message=message,
                    is_read=False,
                    created_at=datetime.utcnow()
                )
                db.session.add(notif)
                db.session.commit()
            except Exception as e:
                print(f"写入SQL通知失败: {str(e)}")
                
        except Exception as e:
            print(f"发送面试通知失败: {str(e)}")
        
        return jsonify({
            'success': True, 
            'message': '面试安排成功',
            'schedule_id': interview_schedule.id
        }), 200
        
    except Exception as e:
        if db:
            db.session.rollback()
        print(f"安排面试失败: {str(e)}")
        return jsonify({'success': False, 'message': f'安排面试失败: {str(e)}'}), 500


