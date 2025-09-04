"""
LLRC Header Start
文件功能: SmartRecruit 子系统 Python 模块：smartrecruit_system/hr_module/recruitment.py
创建时间: 2025-08-19 13:54
创建人: 苏杰
更新记录:
- 2025-08-19 14:24 by 潘显雨
- 2025-08-26 09:29 by 侯东杨
LLRC Header End
"""
"""
FILE-HEADER-AUTO-ADDED
文件: smartrecruit_system/hr_module/recruitment.py
功能: 通用模块
创建时间: 2025-08-27 13:18
创建人: 张宇成
更新记录:
- 2025-08-20 13:55 by 张宇成
- 2025-08-31 10:08 by 谢佳悦
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app, abort
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import logging
from app.models import Job, User, Application, db, TalentDemandDraft

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
                flash('招聘启事发布成功！', 'success')

            return redirect(url_for('smartrecruit.hr.recruitment.my_jobs'))
        except Exception as e:
            db.session.rollback()
            logging.error(f'发布/更新招聘启事失败: {e}')
            flash('操作失败，请稍后重试。', 'danger')

    # 读取HR需求暂存箱
    drafts = []
    draft_text = ''
    try:
        drafts_query = TalentDemandDraft.query.filter_by(hr_user_id=g.user.id).order_by(TalentDemandDraft.created_at.desc())
        # 如果有特定的 draft_id，放到列表最前并高亮
        highlighted_id = request.args.get('draft_id')
        if highlighted_id:
            try:
                highlighted = drafts_query.filter(TalentDemandDraft.id == int(highlighted_id)).first()
                others = TalentDemandDraft.query.filter_by(hr_user_id=g.user.id).filter(TalentDemandDraft.id != int(highlighted_id)).order_by(TalentDemandDraft.created_at.desc()).all()
                drafts = [d for d in [highlighted] if d] + others
                # 预填暂存文本
                if highlighted:
                    parts = []
                    if highlighted.keyword:
                        parts.append(f"关键词：{highlighted.keyword}")
                    if highlighted.description:
                        parts.append(f"描述：{highlighted.description}")
                    draft_text = "\n".join(parts)
            except ValueError:
                drafts = drafts_query.all()
        else:
            drafts = drafts_query.all()
            # 若没有指定，取最新一条作为默认文本
            if drafts:
                latest = drafts[0]
                parts = []
                if latest.keyword:
                    parts.append(f"关键词：{latest.keyword}")
                if latest.description:
                    parts.append(f"描述：{latest.description}")
                draft_text = "\n".join(parts)
    except Exception:
        drafts = []

    return render_template('smartrecruit/hr/create_job_ios.html', job=job_to_edit, is_edit=bool(edit_job_id), drafts=drafts, highlight_id=request.args.get('draft_id'), draft_text=draft_text)


@recruitment_bp.route('/generate_from_draft', methods=['POST'])
def generate_from_draft():
    """根据暂存文本调用 Gemini 生成职位信息（严格JSON返回）"""
    from flask import jsonify, request
    import os, json, re

    try:
        current_app.logger.info('generate_from_draft: request received')
    except Exception:
        pass

    data = request.get_json(silent=True) or {}
    draft = (data.get('draft') or '').strip()
    try:
        current_app.logger.info(f'generate_from_draft: payload received, draft_len={len(draft)}')
    except Exception:
        pass

    empty = {'title':'','location':'','salary':'','job_type':'fulltime','description':'','skills':''}

    def _estimate_salary(title: str, skills: str, description: str, location: str) -> str:
        """函数 _estimate_salary：处理 title, skills, description, location 相关逻辑。"""
        t = (title or '' + ' ' + skills or '' + ' ' + description or '').lower()
        # 角色分类
        role = 'other'
        mapping = [
            ('nlp', 'algo'), ('算法', 'algo'), ('机器学习', 'algo'), ('ai', 'algo'), ('深度学习', 'algo'),
            ('后端', 'backend'), ('java', 'backend'), ('go', 'backend'), ('python', 'backend'),
            ('前端', 'frontend'), ('react', 'frontend'), ('vue', 'frontend'),
            ('数据工程', 'dataeng'), ('大数据', 'dataeng'), ('hadoop', 'dataeng'),
            ('数据分析', 'da'), ('分析师', 'da'),
            ('产品经理', 'pm'), ('产品', 'pm'),
            ('测试', 'qa'), ('qa', 'qa'),
            ('运维', 'devops'), ('devops', 'devops')
        ]
        for key, val in mapping:
            if key in t:
                role = val
                break
        # 级别
        level = 'mid'
        txt_all = (title or '') + (description or '')
        if any(k in txt_all for k in ['资深','高级','专家','负责人','主管','架构师','lead','senior']):
            level = 'senior'
        elif any(k in txt_all for k in ['初级','助理','junior','实习']):
            level = 'junior'
        # 地域系数
        loc = location or ''
        coeff = 1.0
        tier1 = ['北京','上海','深圳','广州','杭州']
        tier15 = ['南京','苏州','成都','重庆','武汉','西安','合肥','天津','厦门','青岛']
        if any(city in loc for city in tier1):
            coeff = 1.2
        elif any(city in loc for city in tier15):
            coeff = 1.1
        # 基础范围（单位k/月）
        base = {
            'algo':   {'junior':(12,20), 'mid':(20,40), 'senior':(35,60)},
            'backend':{'junior':(12,18), 'mid':(15,30), 'senior':(28,50)},
            'frontend':{'junior':(12,18), 'mid':(15,28), 'senior':(26,45)},
            'dataeng':{'junior':(14,22), 'mid':(18,35), 'senior':(32,55)},
            'da':     {'junior':(10,16), 'mid':(12,25), 'senior':(22,35)},
            'pm':     {'junior':(12,18), 'mid':(15,30), 'senior':(28,45)},
            'qa':     {'junior':(8,14),  'mid':(10,20), 'senior':(18,30)},
            'devops': {'junior':(12,18), 'mid':(15,30), 'senior':(26,45)},
            'other':  {'junior':(8,12),  'mid':(10,18), 'senior':(18,28)}
        }
        lo, hi = base.get(role, base['other'])[level]
        lo = int(round(lo*coeff))
        hi = int(round(hi*coeff))
        # 保证不重叠
        if hi <= lo:
            hi = lo + 2
        return f"{lo}k-{hi}k/月"

    def _fallback_from_draft(text: str):
        """当未配置API或调用异常时，基于暂存文本粗生成字段。"""
        try:
            import re as _re
            kw_match = _re.search(r'关键词：([^\n]+)', text or '')
            desc_match = _re.search(r'描述：([\s\S]+)$', text or '')
            keywords_line = (kw_match.group(1).strip() if kw_match else '')
            first_kw = ''
            if keywords_line:
                parts = [s.strip() for s in _re.split(r'[，,]\s*', keywords_line) if s.strip()]
                first_kw = parts[0] if parts else ''
            result = {
                'title': (first_kw + ' 工程师') if first_kw else '',
                'location': '',
                'salary': '',
                'job_type': 'fulltime',
                'description': (desc_match.group(1).strip() if desc_match else ''),
                'skills': keywords_line,
            }
            return result
        except Exception:
            return empty
    api_key = os.getenv('GEMINI_API_KEY')
    model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    if not api_key:
        current_app.logger.error('GEMINI_API_KEY 未配置，无法接入AI，返回兜底')
        fb = _fallback_from_draft(draft)
        return jsonify(fb), 200

    try:
        try:
            import google.generativeai as genai  # 延后导入，避免环境未安装导致直接500
        except Exception as ie:
            current_app.logger.error(f'google.generativeai 导入失败: {ie}')
            raise

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)

        prompt = f"""
你是资深招聘专家。基于以下“暂存内容”（包含 关键词 与 描述），生成职位信息并只输出JSON：

字段要求（全部字符串）：
- title: 职位标题（精炼，如“算法工程师”）
- location: 工作地点（可留空）
- salary: 薪资范围（可留空，如“15k-25k”）
- job_type: 枚举 fulltime/parttime/internship/contract（默认 fulltime）
- description: 职位详细描述（中文，分段）
- skills: 逗号分隔技能清单（中文，比如“Python, 算法, 数据结构”）

暂存内容：
{draft}

严格要求：
- 只输出JSON本体，不要任何前后缀、解释或代码围栏。
- 各字段的内容必须为纯文本，禁止任何富文本/格式，如加粗、列表、markdown、HTML标签、表情符号等。
 - salary 请根据岗位（结合标题/技能/描述）与城市（若提供）给出符合中国一线/新一线市场的合理区间，格式如“15k-20k/月”，不得随机编造。
"""

        resp = model.generate_content(prompt)
        text = resp.text.strip() if hasattr(resp, 'text') else ''
        current_app.logger.info(f'Gemini raw response text length: {len(text)}')
        m = re.search(r'\{[\s\S]*\}$', text)
        text = m.group(0) if m else text
        try:
            obj = json.loads(text)
        except Exception as e:
            current_app.logger.warning(f'JSON解析失败，使用兜底规则。error={e}')
            # 兜底：从 draft 里粗提取
            kw_match = re.search(r'关键词：([^\n]+)', draft)
            desc_match = re.search(r'描述：([\s\S]+)$', draft)
            obj = {
                'title': '',
                'location': '',
                'salary': '',
                'job_type': 'fulltime',
                'description': (desc_match.group(1).strip() if desc_match else ''),
                'skills': ', '.join([s.strip() for s in re.split(r'[，,]\s*', (kw_match.group(1) if kw_match else '')) if s.strip()])
            }
            if kw_match:
                hint = kw_match.group(1).split(',')[0].split('，')[0].strip()
                if hint:
                    obj['title'] = f'{hint} 工程师'
        result = {
            'title': (obj.get('title') or ''),
            'location': (obj.get('location') or ''),
            'salary': (obj.get('salary') or ''),
            'job_type': ((obj.get('job_type') or 'fulltime').lower()),
            'description': (obj.get('description') or ''),
            'skills': (obj.get('skills') or ''),
        }
        # 若AI未给出薪资，则基于规则估算
        if not result['salary']:
            result['salary'] = _estimate_salary(result['title'], result['skills'], result['description'], result['location'])
        if result['job_type'] not in ['fulltime','parttime','internship','contract']:
            result['job_type'] = 'fulltime'
        current_app.logger.info(f'Gemini parsed result keys: {list(result.keys())}')
        try:
            current_app.logger.info('generate_from_draft: success 200')
        except Exception:
            pass
        return jsonify(result), 200
    except Exception as e:
        current_app.logger.error(f'Gemini 调用异常: {e}')
        try:
            current_app.logger.warning('generate_from_draft: exception path, using fallback 200')
        except Exception:
            pass
        fb = _fallback_from_draft(draft)
        return jsonify(fb), 200


@recruitment_bp.route('/materialize_draft', methods=['POST'])
def materialize_draft():
    """接收暂存文本，调用 Gemini 具象化，将新文本打印到终端并返回给前端（限制300字）。"""
    from flask import jsonify, request
    import os, json, re, textwrap

    data = request.get_json(silent=True) or {}
    draft = (data.get('draft') or '').strip()
    current_app.logger.info('materialize_draft: request received')
    current_app.logger.info(f'materialize_draft: draft_len={len(draft)}')

    def _fallback_from_draft(text: str):
        """函数 _fallback_from_draft：处理 text 相关逻辑。"""
        try:
            import re as _re
            kw_match = _re.search(r'关键词：([^\n]+)', text or '')
            desc_match = _re.search(r'描述：([\s\S]+)$', text or '')
            keywords_line = (kw_match.group(1).strip() if kw_match else '')
            first_kw = ''
            if keywords_line:
                parts = [s.strip() for s in _re.split(r'[，,]\s*', keywords_line) if s.strip()]
                first_kw = parts[0] if parts else ''
            result = {
                'title': (first_kw + ' 工程师') if first_kw else '',
                'location': '',
                'salary': '',
                'job_type': 'fulltime',
                'description': (desc_match.group(1).strip() if desc_match else ''),
                'skills': keywords_line,
            }
            return result
        except Exception:
            return {'title':'','location':'','salary':'','job_type':'fulltime','description':'','skills':''}

    api_key = os.getenv('GEMINI_API_KEY')
    model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    try:
        current_app.logger.info(f"materialize_draft: model={model_name}, has_key={'yes' if bool(api_key) else 'no'}")
    except Exception:
        pass

    def _estimate_salary(title: str, skills: str, description: str, location: str) -> str:
        """函数 _estimate_salary：处理 title, skills, description, location 相关逻辑。"""
        t_all = ((title or '') + ' ' + (skills or '') + ' ' + (description or '')).lower()
        role = 'other'
        mapping = [
            ('nlp', 'algo'), ('算法', 'algo'), ('机器学习', 'algo'), ('ai', 'algo'), ('深度学习', 'algo'),
            ('后端', 'backend'), ('java', 'backend'), ('go', 'backend'), ('python', 'backend'),
            ('前端', 'frontend'), ('react', 'frontend'), ('vue', 'frontend'),
            ('数据工程', 'dataeng'), ('大数据', 'dataeng'),
            ('数据分析', 'da'), ('分析师', 'da'),
            ('产品经理', 'pm'), ('产品', 'pm'),
            ('测试', 'qa'), ('qa', 'qa'),
            ('运维', 'devops'), ('devops', 'devops')
        ]
        for key, val in mapping:
            if key in t_all:
                role = val
                break
        level = 'mid'
        txt = (title or '') + (description or '')
        if any(k in txt for k in ['资深','高级','专家','负责人','主管','架构师','lead','senior']):
            level = 'senior'
        elif any(k in txt for k in ['初级','助理','junior','实习']):
            level = 'junior'
        coeff = 1.0
        loc = location or ''
        tier1 = ['北京','上海','深圳','广州','杭州']
        tier15 = ['南京','苏州','成都','重庆','武汉','西安','合肥','天津','厦门','青岛']
        if any(c in loc for c in tier1):
            coeff = 1.2
        elif any(c in loc for c in tier15):
            coeff = 1.1
        base = {
            'algo':   {'junior':(12,20), 'mid':(20,40), 'senior':(35,60)},
            'backend':{'junior':(12,18), 'mid':(15,30), 'senior':(28,50)},
            'frontend':{'junior':(12,18), 'mid':(15,28), 'senior':(26,45)},
            'dataeng':{'junior':(14,22), 'mid':(18,35), 'senior':(32,55)},
            'da':     {'junior':(10,16), 'mid':(12,25), 'senior':(22,35)},
            'pm':     {'junior':(12,18), 'mid':(15,30), 'senior':(28,45)},
            'qa':     {'junior':(8,14),  'mid':(10,20), 'senior':(18,30)},
            'devops': {'junior':(12,18), 'mid':(15,30), 'senior':(26,45)},
            'other':  {'junior':(8,12),  'mid':(10,18), 'senior':(18,28)}
        }
        lo, hi = base.get(role, base['other'])[level]
        lo = int(round(lo*coeff)); hi = int(round(hi*coeff))
        if hi <= lo:
            hi = lo + 2
        return f"{lo}k-{hi}k/月"

    def _compose_text(title: str, skills: str, description: str, location: str, salary: str) -> str:
        """函数 _compose_text：处理 title, skills, description, location, salary 相关逻辑。"""
        parts = []
        if title:
            parts.append(f"标题：{title}")
        if skills:
            parts.append(f"技能：{skills}")
        # 补全或采用AI返回的薪资
        sal = (salary or '').strip()
        if not sal:
            sal = _estimate_salary(title, skills, description, location)
        if sal:
            parts.append(f"薪资：{sal}")
        if description:
            parts.append(f"描述：{description}")
        text = "\n".join(parts).strip()
        LIMIT = 300
        if len(text) <= LIMIT:
            return text
        # 寻找限制内的最后一个句子终止符，避免截断半句话
        snippet = text[:LIMIT]
        enders = ['。', '！', '？', '.', '!', '?', '；', ';', '\n']
        last_idx = -1
        for ch in enders:
            idx = snippet.rfind(ch)
            if idx > last_idx:
                last_idx = idx
        if last_idx != -1:
            return snippet[:last_idx+1]
        # 若找不到终止符，认为首句即超过限制，则不返回任何不完整句子
        return ''

    # 同步请求并返回内容
    try:
        import requests
    except Exception:
        fb = _fallback_from_draft(draft)
        content = _compose_text(fb.get('title',''), fb.get('skills',''), fb.get('description',''), fb.get('location',''), fb.get('salary',''))
        print(content)
        try: current_app.logger.info(content)
        except Exception: pass
        return jsonify({'ok': True, 'content': content, 'mode': 'fallback'}), 200

    if not api_key:
        fb = _fallback_from_draft(draft)
        content = _compose_text(fb.get('title',''), fb.get('skills',''), fb.get('description',''), fb.get('location',''), fb.get('salary',''))
        print(content)
        try: current_app.logger.info(content)
        except Exception: pass
        return jsonify({'ok': True, 'content': content, 'mode': 'fallback'}), 200

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        prompt = (
            "你是资深招聘专家。把以下‘暂存内容’具象化为更具体、可执行的招聘表述。"
            "使用中文，且‘只输出严格JSON’，没有任何多余文字/markdown/注释/代码围栏。\n"
            "字段与含义（全为字符串）：\n"
            "- title: 职位标题（简洁，如‘算法工程师’）\n"
            "- description: 具体职责与要求（分段中文）\n"
            "- skills: 逗号分隔技能（如‘Python, 算法, NLP’）\n\n"
            "输出示例：{\"title\":\"算法工程师\",\"description\":\"……\",\"skills\":\"Python, 算法\"}\n\n"
            f"暂存内容：\n{draft}"
        )
        # 追加纯文本要求，禁止富文本格式
        prompt += "\n严格要求：仅输出JSON，各字段内容必须为纯文本，禁止任何富文本/格式（如加粗、列表、markdown、HTML标签、表情符号）。若能推断，请给出 salary 字段，要求结合岗位与城市（如有）给出合理区间，格式如‘15k-20k/月’，不得随机编造。"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        resp = requests.post(url, json=payload, timeout=12)
        raw = ''
        try:
            data = resp.json()
            raw = (
                data.get('candidates',[{}])[0]
                    .get('content',{})
                    .get('parts',[{}])[0]
                    .get('text','')
            )
        except Exception:
            raw = resp.text or ''
        # 解析JSON
        try:
            fenced = re.search(r"```(?:json)?([\s\S]*?)```", raw)
            if fenced:
                raw = fenced.group(1)
            m = re.search(r'\{[\s\S]*\}$', raw.strip())
            raw = m.group(0) if m else raw
            obj = json.loads(raw)
        except Exception:
            title = ''
            skills = ''
            desc = ''
            loc = ''
            sal = ''
            try:
                title = re.search(r'(?:标题|title)[:：]\s*([^\n]+)', raw, re.I).group(1).strip()
            except Exception:
                pass
            try:
                skills = re.search(r'(?:技能|skills)[:：]\s*([^\n]+)', raw, re.I).group(1).strip()
            except Exception:
                pass
            try:
                m2 = re.search(r'(?:描述|description)[:：]([\s\S]+)$', raw, re.I)
                if m2:
                    desc = m2.group(1).strip()
            except Exception:
                pass
            try:
                loc = re.search(r'(?:地点|城市|location)[:：]\s*([^\n]+)', raw, re.I).group(1).strip()
            except Exception:
                pass
            try:
                sal = re.search(r'(?:薪资|salary)[:：]\s*([^\n]+)', raw, re.I).group(1).strip()
            except Exception:
                pass
            obj = {"title": title, "skills": skills, "description": desc, "location": loc, "salary": sal}
        content = _compose_text(obj.get('title',''), obj.get('skills',''), obj.get('description',''), obj.get('location',''), obj.get('salary',''))
        print(content)
        try: current_app.logger.info(content)
        except Exception: pass
        return jsonify({'ok': True, 'content': content, 'mode': 'sync'}), 200
    except Exception as e:
        current_app.logger.error(f"materialize_draft: error {e}")
        fb = _fallback_from_draft(draft)
        content = _compose_text(fb.get('title',''), fb.get('skills',''), fb.get('description',''), fb.get('location',''), fb.get('salary',''))
        print(content)
        try: current_app.logger.info(content)
        except Exception: pass
        return jsonify({'ok': True, 'content': content, 'mode': 'error_fallback'}), 200

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

    db.session.delete(job)
    db.session.commit()
    flash('职位删除成功！', 'success')
    return redirect(url_for('smartrecruit.hr.recruitment.my_jobs'))
