from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, jsonify
from datetime import datetime, timedelta
import random
import logging
from app.models import User, Job, Application, db

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/test')
def test():
    """测试路由"""
    return "测试路由工作正常！"

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
        
        # 获取所有候选人及其申请信息
        try:
            # 获取HR发布的职位
            hr_jobs = Job.query.filter_by(user_id=g.user.id).all()
            job_ids = [job.id for job in hr_jobs]
            
            # 获取申请了这些职位的候选人
            applications = Application.query.filter(Application.job_id.in_(job_ids)).all()
            
            # 构建候选人数据
            candidates_data = []
            for app in applications:
                user = User.query.get(app.user_id)
                if user:
                    # 计算技能匹配度（基于职位要求）
                    job = Job.query.get(app.job_id)
                    skills_match = calculate_skills_match(user, job) if job else 0
                    
                    # 获取申请时间
                    applied_date = app.timestamp.strftime('%Y-%m-%d') if app.timestamp else '未知'
                    
                    # 获取最后更新时间
                    last_updated = app.timestamp.strftime('%Y-%m-%d %H:%M') if app.timestamp else '未知'
                    
                    candidates_data.append({
                        'id': user.id,
                        'user': user,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'profile_photo': user.profile_photo,
                        'position': job.title if job else '未知职位',
                        'skills_match': skills_match,
                        'status': app.status,
                        'applied_date': applied_date,
                        'last_updated': last_updated
                    })
        except Exception as e:
            logging.error(f"查询候选人数据失败: {e}")
            candidates_data = []
        
        return render_template('smartrecruit/hr/hr_candidates.html', candidates=candidates_data)
    except Exception as e:
        logging.error(f"候选人管理页面加载失败: {e}")
        flash('加载候选人管理页面时出现错误，请稍后重试。', 'danger')
        return render_template('smartrecruit/hr/hr_candidates.html', candidates=[])

@dashboard_bp.route('/interviews')
def interviews():
    """面试安排管理"""
    try:
        print("开始加载面试安排页面")  # 调试信息
        
        if g.user is None:
            print("用户未登录")  # 调试信息
            flash('请先登录。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        if not getattr(g.user, 'is_hr', False):
            print("用户不是HR")  # 调试信息
            flash('只有HR用户才能访问此页面。', 'danger')
            return redirect(url_for('common.auth.sign'))
        
        print(f"用户ID: {g.user.id}")  # 调试信息
        
        # 获取所有候选人（用于面试安排表单）
        try:
            print("开始查询候选人数据")  # 调试信息
            hr_jobs = Job.query.filter_by(user_id=g.user.id).all()
            print(f"找到职位数量: {len(hr_jobs)}")  # 调试信息
            
            job_ids = [job.id for job in hr_jobs]
            applications = Application.query.filter(Application.job_id.in_(job_ids)).all()
            print(f"找到申请数量: {len(applications)}")  # 调试信息
            
            candidates_data = []
            for app in applications:
                user = User.query.get(app.user_id)
                if user:
                    candidates_data.append({
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'position': Job.query.get(app.job_id).title if Job.query.get(app.job_id) else '未知职位'
                    })
            
            print(f"构建候选人数据: {len(candidates_data)}")  # 调试信息
            
        except Exception as e:
            print(f"查询候选人数据失败: {e}")  # 调试信息
            logging.error(f"查询候选人数据失败: {e}")
            candidates_data = []
        
        # 模拟面试数据（实际应用中应该从数据库获取）
        interviews_data = [
            {
                'id': 1,
                'candidate_name': '张三',
                'candidate_email': 'zhangsan@example.com',
                'position': '前端工程师',
                'interviewer_name': '王经理',
                'date': '2024-01-15',
                'start_time': '10:00',
                'end_time': '11:00',
                'method': 'online',
                'status': 'scheduled'
            },
            {
                'id': 2,
                'candidate_name': '李四',
                'candidate_email': 'lisi@example.com',
                'position': '后端工程师',
                'interviewer_name': '李总监',
                'date': '2024-01-16',
                'start_time': '14:00',
                'end_time': '15:00',
                'method': 'offline',
                'status': 'completed'
            }
        ]
        
        print("准备渲染模板")  # 调试信息
        return render_template('smartrecruit/hr/hr_interviews_new.html', 
                             candidates=candidates_data,
                             interviews=interviews_data)
    except Exception as e:
        print(f"面试安排页面加载失败: {e}")  # 调试信息
        logging.error(f"面试安排页面加载失败: {e}")
        flash('加载面试安排页面时出现错误，请稍后重试。', 'danger')
        return render_template('smartrecruit/hr/hr_interviews_new.html', 
                             candidates=[],
                             interviews=[])

def calculate_skills_match(user, job):
    """计算技能匹配度"""
    if not job or not job.skills_required:
        return 75  # 默认匹配度
    
    # 这里可以实现更复杂的技能匹配算法
    # 目前返回一个基于职位要求的模拟匹配度
    required_skills = job.skills_required.lower().split(',') if job.skills_required else []
    if not required_skills:
        return 75
    
    # 模拟匹配度计算
    base_match = 60
    skill_bonus = min(len(required_skills) * 5, 30)
    return min(base_match + skill_bonus, 95)

def calculate_experience_years(birthday_str):
    """根据生日计算工作经验年数"""
    try:
        if not birthday_str:
            return 0
        
        # 假设18岁开始工作
        birth_year = int(birthday_str.split('-')[0])
        current_year = datetime.now().year
        age = current_year - birth_year
        experience = max(0, age - 18)
        return min(experience, 30)  # 最大30年经验
    except:
        return 0

def get_education_level(user):
    """获取教育水平"""
    # 这里可以根据实际需求扩展
    return "本科"  # 默认值

def get_sample_candidates_data():
    """获取示例候选人数据"""
    return [
        {
            'id': 1,
            'user': None,
            'application': None,
            'job': None,
            'position': '高级软件工程师',
            'skills_match': 85,
            'status': 'interview',
            'applied_date': '2024-01-15',
            'last_updated': '2024-01-20 14:30',
            'experience_years': 5,
            'education': '本科',
            'phone': '138****8888',
            'cv_file': 'resume_1.pdf',
            'profile_photo': None,
            'first_name': '张三',
            'last_name': '',
            'email': 'zhangsan@email.com'
        },
        {
            'id': 2,
            'user': None,
            'application': None,
            'job': None,
            'position': '产品经理',
            'skills_match': 92,
            'status': 'offer',
            'applied_date': '2024-01-10',
            'last_updated': '2024-01-18 16:45',
            'experience_years': 7,
            'education': '硕士',
            'phone': '139****9999',
            'cv_file': 'resume_2.pdf',
            'profile_photo': None,
            'first_name': '李四',
            'last_name': '',
            'email': 'lisi@email.com'
        },
        {
            'id': 3,
            'user': None,
            'application': None,
            'job': None,
            'position': 'UI设计师',
            'skills_match': 78,
            'status': 'screened',
            'applied_date': '2024-01-12',
            'last_updated': '2024-01-19 10:20',
            'experience_years': 3,
            'education': '本科',
            'phone': '137****7777',
            'cv_file': 'resume_3.pdf',
            'profile_photo': None,
            'first_name': '王五',
            'last_name': '',
            'email': 'wangwu@email.com'
        },
        {
            'id': 4,
            'user': None,
            'application': None,
            'job': None,
            'position': '前端开发工程师',
            'skills_match': 88,
            'status': 'applied',
            'applied_date': '2024-01-22',
            'last_updated': '2024-01-22 09:15',
            'experience_years': 4,
            'education': '本科',
            'phone': '136****6666',
            'cv_file': 'resume_4.pdf',
            'profile_photo': None,
            'first_name': '赵六',
            'last_name': '',
            'email': 'zhaoliu@email.com'
        }
    ]

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
