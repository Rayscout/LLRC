from flask import Blueprint, render_template, request, redirect, url_for, flash, g, send_file
from app.models import User, db
from app.models import TaskEvaluation
from datetime import datetime
import json
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import tempfile

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/')
def profile_dashboard():
    """员工个人资料仪表板"""
    try:
        # 检查用户是否登录
        from flask import session
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取用户信息
        from app.models import User
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            flash('用户信息获取失败，请重新登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 验证用户类型
        if user.user_type != 'employee':
            flash('您没有权限访问此页面', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取用户的技能信息（从个人资料中提取）
        user_skills = []
        if user.bio:
            user_skills.extend(extract_skills_from_text(user.bio))
        if user.experience:
            user_skills.extend(extract_skills_from_text(user.experience))
        if user.education:
            user_skills.extend(extract_skills_from_text(user.education))
        
        # 处理skills字段（JSON格式存储）
        if user.skills:
            try:
                stored_skills = json.loads(user.skills)
                if isinstance(stored_skills, list):
                    user_skills.extend(stored_skills)
            except (json.JSONDecodeError, TypeError):
                # 如果skills不是有效的JSON，尝试按逗号分割
                if isinstance(user.skills, str):
                    user_skills.extend([skill.strip() for skill in user.skills.split(',') if skill.strip()])
        
        # 去重技能
        user_skills = list(set(user_skills))
        
        # 计算工作年限
        work_years = 0
        if user.hire_date:
            hire_date = user.hire_date
            if isinstance(hire_date, str):
                hire_date = datetime.strptime(hire_date, '%Y-%m-%d').date()
            work_years = (datetime.now().date() - hire_date).days // 365
        
        # 解析教育和工作经历
        education_history = parse_education_history(user.education)
        work_history = parse_work_history(user.experience)
        
        # 获取绩效历史（模拟数据 + 实际任务评价整合）
        performance_history = get_performance_history(user.id)
        try:
            evals = TaskEvaluation.query.filter_by(employee_id=user.id)\
                .order_by(TaskEvaluation.created_at.desc()).all()
            for ev in evals:
                performance_history.insert(0, {
                    'period': ev.created_at.strftime('%Y-%m-%d'),
                    'score': ev.total_score,
                    'level': '—',
                    'evaluator': '管理层',
                    'comments': f"{ev.task_title}｜质{ev.score_quality}/效{ev.score_efficiency}/协{ev.score_collaboration}｜{(ev.comment or '')[:60]}"
                })
        except Exception:
            pass
        
        return render_template('talent_management/employee_management/profile_dashboard.html',
                             user=user,
                             user_skills=user_skills,
                             work_years=work_years,
                             education_history=education_history,
                             work_history=work_history,
                             performance_history=performance_history)
                             
    except Exception as e:
        from app import logger
        logger.error(f"个人资料页面错误: {e}")
        flash('加载个人资料时发生错误，请稍后重试', 'danger')
        return redirect(url_for('common.auth.sign'))

@profile_bp.route('/export-pdf')
def export_pdf():
    """导出PDF简历"""
    try:
        from flask import session
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        user = User.query.get(session['user_id'])
        if not user or user.user_type != 'employee':
            flash('用户信息获取失败', 'warning')
            return redirect(url_for('common.auth.sign'))
        
        # 获取用户数据
        user_skills = []
        if user.bio:
            user_skills.extend(extract_skills_from_text(user.bio))
        if user.experience:
            user_skills.extend(extract_skills_from_text(user.experience))
        if user.education:
            user_skills.extend(extract_skills_from_text(user.education))
        
        if user.skills:
            try:
                stored_skills = json.loads(user.skills)
                if isinstance(stored_skills, list):
                    user_skills.extend(stored_skills)
            except (json.JSONDecodeError, TypeError):
                if isinstance(user.skills, str):
                    user_skills.extend([skill.strip() for skill in user.skills.split(',') if skill.strip()])
        
        user_skills = list(set(user_skills))
        
        work_years = 0
        if user.hire_date:
            hire_date = user.hire_date
            if isinstance(hire_date, str):
                hire_date = datetime.strptime(hire_date, '%Y-%m-%d').date()
            work_years = (datetime.now().date() - hire_date).days // 365
        
        education_history = parse_education_history(user.education)
        work_history = parse_work_history(user.experience)
        performance_history = get_performance_history(user.id)
        try:
            evals = TaskEvaluation.query.filter_by(employee_id=user.id)\
                .order_by(TaskEvaluation.created_at.desc()).all()
            for ev in evals:
                performance_history.insert(0, {
                    'period': ev.created_at.strftime('%Y-%m-%d'),
                    'score': ev.total_score,
                    'level': '—',
                    'evaluator': '管理层',
                    'comments': f"{ev.task_title}｜质{ev.score_quality}/效{ev.score_efficiency}/协{ev.score_collaboration}｜{(ev.comment or '')[:60]}"
                })
        except Exception:
            pass
        
        # 生成PDF
        pdf_path = generate_pdf_resume(user, user_skills, work_years, education_history, work_history, performance_history)
        
        # 返回PDF文件
        return send_file(pdf_path, as_attachment=True, download_name=f"{user.first_name}_{user.last_name}_简历.pdf")
        
    except Exception as e:
        from app import logger
        logger.error(f"PDF导出错误: {e}")
        flash('PDF导出失败，请稍后重试', 'danger')
        return redirect(url_for('talent_management.employee_manager.profile.profile_dashboard'))

def parse_education_history(education_text):
    """解析教育经历"""
    if not education_text:
        return []
    
    # 简单的解析逻辑，可以根据实际格式调整
    education_items = []
    lines = education_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if line:
            # 假设格式：学校名称 - 专业 - 学位 - 时间
            parts = line.split(' - ')
            if len(parts) >= 3:
                education_items.append({
                    'school': parts[0],
                    'major': parts[1] if len(parts) > 1 else '',
                    'degree': parts[2] if len(parts) > 2 else '',
                    'period': parts[3] if len(parts) > 3 else ''
                })
            else:
                education_items.append({
                    'school': line,
                    'major': '',
                    'degree': '',
                    'period': ''
                })
    
    return education_items

def parse_work_history(experience_text):
    """解析工作经历"""
    if not experience_text:
        return []
    
    work_items = []
    lines = experience_text.split('\n')
    
    for line in lines:
        line = line.strip()
        if line:
            # 假设格式：公司名称 - 职位 - 时间 - 描述
            parts = line.split(' - ')
            if len(parts) >= 2:
                work_items.append({
                    'company': parts[0],
                    'position': parts[1] if len(parts) > 1 else '',
                    'period': parts[2] if len(parts) > 2 else '',
                    'description': parts[3] if len(parts) > 3 else ''
                })
            else:
                work_items.append({
                    'company': line,
                    'position': '',
                    'period': '',
                    'description': ''
                })
    
    return work_items

def get_performance_history(user_id):
    """获取绩效历史（模拟数据）"""
    # 这里可以连接实际的绩效数据库
    return [
        {
            'period': '2024年Q1',
            'score': 92,
            'level': '优秀',
            'evaluator': '张主管',
            'comments': '工作积极主动，技术能力突出，团队协作良好。'
        },
        {
            'period': '2023年Q4',
            'score': 88,
            'level': '良好',
            'evaluator': '李经理',
            'comments': '按时完成任务，质量达标，需要加强创新思维。'
        },
        {
            'period': '2023年Q3',
            'score': 85,
            'level': '良好',
            'evaluator': '王总监',
            'comments': '基础工作扎实，学习能力强，建议多参与项目。'
        }
    ]

def generate_pdf_resume(user, skills, work_years, education_history, work_history, performance_history):
    """生成PDF简历"""
    # 创建临时文件
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    doc = SimpleDocTemplate(temp_file.name, pagesize=A4)
    
    # 获取样式
    styles = getSampleStyleSheet()
    
    # 创建自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        spaceBefore=20,
        textColor=colors.darkblue
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )
    
    # 构建PDF内容
    story = []
    
    # 标题
    story.append(Paragraph(f"{user.first_name} {user.last_name} - 个人简历", title_style))
    story.append(Spacer(1, 20))
    
    # 基本信息
    story.append(Paragraph("基本信息", heading_style))
    basic_info = [
        ['姓名', f"{user.first_name} {user.last_name}"],
        ['员工编号', user.employee_id or '未设置'],
        ['部门', user.department or '未设置'],
        ['职位', user.position or '未设置'],
        ['邮箱', user.email],
        ['电话', user.phone_number or '未设置'],
        ['入职日期', str(user.hire_date) if user.hire_date else '未设置'],
        ['工作年限', f"{work_years} 年"]
    ]
    
    basic_table = Table(basic_info, colWidths=[1.5*inch, 4*inch])
    basic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(basic_table)
    story.append(Spacer(1, 20))
    
    # 个人简介
    if user.bio:
        story.append(Paragraph("个人简介", heading_style))
        story.append(Paragraph(user.bio, normal_style))
        story.append(Spacer(1, 20))
    
    # 技能标签
    if skills:
        story.append(Paragraph("技能标签", heading_style))
        skills_text = ', '.join(skills)
        story.append(Paragraph(skills_text, normal_style))
        story.append(Spacer(1, 20))
    
    # 教育经历
    if education_history:
        story.append(Paragraph("教育经历", heading_style))
        for edu in education_history:
            edu_text = f"<b>{edu['school']}</b> - {edu['major']} - {edu['degree']}"
            if edu['period']:
                edu_text += f" ({edu['period']})"
            story.append(Paragraph(edu_text, normal_style))
        story.append(Spacer(1, 20))
    
    # 工作经历
    if work_history:
        story.append(Paragraph("工作经历", heading_style))
        for work in work_history:
            work_text = f"<b>{work['company']}</b> - {work['position']}"
            if work['period']:
                work_text += f" ({work['period']})"
            story.append(Paragraph(work_text, normal_style))
            if work['description']:
                story.append(Paragraph(work['description'], normal_style))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 20))
    
    # 绩效历史
    if performance_history:
        story.append(Paragraph("绩效历史", heading_style))
        perf_data = [['期间', '评分', '等级', '评价人', '评语']]
        for perf in performance_history:
            perf_data.append([
                perf['period'],
                str(perf['score']),
                perf['level'],
                perf['evaluator'],
                perf['comments']
            ])
        
        perf_table = Table(perf_data, colWidths=[1*inch, 0.8*inch, 0.8*inch, 1*inch, 2.4*inch])
        perf_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(perf_table)
    
    # 生成PDF
    doc.build(story)
    return temp_file.name

@profile_bp.route('/edit', methods=['GET', 'POST'])
def edit_profile():
    """编辑个人资料"""
    # 检查用户是否登录
    from flask import session
    if 'user_id' not in session:
        flash('请先登录', 'warning')
        return redirect(url_for('common.auth.sign'))
    
    # 获取用户信息
    from app.models import User
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('用户信息获取失败，请重新登录', 'warning')
        return redirect(url_for('common.auth.sign'))
    
    if request.method == 'POST':
        # 更新基本信息
        user.first_name = request.form.get('first_name', user.first_name)
        user.last_name = request.form.get('last_name', user.last_name)
        user.phone_number = request.form.get('phone_number', user.phone_number)
        user.birthday = datetime.strptime(request.form.get('birthday'), '%Y-%m-%d').date() if request.form.get('birthday') else user.birthday
        
        # 更新专业信息
        user.bio = request.form.get('bio', user.bio)
        user.experience = request.form.get('experience', user.experience)
        user.education = request.form.get('education', user.education)
        
        # 更新技能标签
        skills = request.form.get('skills', '')
        if skills:
            # 将技能列表转换为JSON字符串存储
            skills_list = [skill.strip() for skill in skills.split(',') if skill.strip()]
            user.skills = json.dumps(skills_list, ensure_ascii=False)
        else:
            user.skills = None
        
        try:
            db.session.commit()
            flash('个人资料更新成功！', 'success')
            return redirect(url_for('talent_management.employee_manager.profile.profile_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'更新失败：{str(e)}', 'danger')
    
    return render_template('talent_management/employee_management/edit_profile.html', user=user)

def extract_skills_from_text(text):
    """从文本中提取技能关键词"""
    if not text:
        return []
    
    # 技能关键词列表
    skill_keywords = [
        'Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift',
        'HTML', 'CSS', 'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'Spring',
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle', 'SQL Server',
        'Docker', 'Kubernetes', 'AWS', 'Azure', 'Google Cloud', 'Linux', 'Windows',
        'Git', 'SVN', 'Jenkins', 'CI/CD', 'Agile', 'Scrum', 'DevOps',
        'Machine Learning', 'AI', 'Data Science', 'Big Data', 'Hadoop', 'Spark',
        'Excel', 'PowerBI', 'Tableau', 'Photoshop', 'Illustrator', 'Figma',
        '项目管理', '团队协作', '沟通能力', '领导力', '创新思维', '问题解决'
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in skill_keywords:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills
