from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app
from werkzeug.utils import secure_filename
import os
from app.models import User, db
from app.utils import allowed_file, get_allowed_cv_extensions, extract_text_from_resume, ai_analyze_resume_text
from .candidate_ai import update_user_skills_from_resume

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    """个人设置页面 - 更新基本信息和上传简历"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    if request.method == 'POST':
        # 删除简历
        if 'delete_cv' in request.form:
            try:
                # 删除物理文件
                if g.user.cv_file:
                    cv_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], g.user.cv_file)
                    try:
                        if os.path.isfile(cv_path):
                            os.remove(cv_path)
                    except Exception:
                        pass
                # 清空数据库字段
                g.user.cv_file = None
                g.user.cv_data = None
                db.session.commit()
                flash('已删除当前简历。', 'success')
            except Exception:
                db.session.rollback()
                flash('删除简历失败，请稍后重试。', 'danger')
            return redirect(url_for('smartrecruit.candidate.profile.settings'))

        # 处理简历上传：由提交按钮 name="upload_cv" 或存在文件来判断
        if 'upload_cv' in request.form or ('cv_file' in request.files and request.files['cv_file'].filename):
            file = request.files.get('cv_file')
            if file and file.filename:
                allowed_extensions = get_allowed_cv_extensions()
                if allowed_file(file.filename, allowed_extensions):
                    try:
                        filename = secure_filename(file.filename)
                        # 添加时间戳避免文件名冲突
                        import time
                        timestamp = int(time.time())
                        name, ext = os.path.splitext(filename)
                        filename = f"{name}_{timestamp}{ext}"
                        
                        filepath = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], filename)
                        file.save(filepath)

                        # 视频与文档分别处理：视频不入库二进制，避免数据库膨胀
                        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                        video_exts = {'mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'}

                        cv_data = None
                        if file_ext not in video_exts:
                            try:
                                file.seek(0)
                                cv_data = file.read()
                            except Exception as e:
                                flash(f'简历文本提取失败：{str(e)}', 'warning')
                                cv_data = None

                        g.user.cv_file = filename
                        g.user.cv_data = cv_data
                        db.session.commit()

                        # 基于AI自动解析技能并保存
                        try:
                            parsed_skills = update_user_skills_from_resume(g.user, cv_data or b'', filename)
                            if parsed_skills:
                                flash('已基于简历自动更新技能标签。', 'success')
                        except Exception as e:
                            current_app.logger.warning(f'AI skill extraction failed: {e}')

                        # 生成简历分析报告并展示
                        try:
                            resume_text = ''
                            if cv_data:
                                resume_text = extract_text_from_resume(cv_data, filename) or ''
                            analysis = ai_analyze_resume_text(resume_text)
                            analysis_msg = '概述：' + analysis.get('summary','')
                            if analysis.get('strengths'):
                                analysis_msg += '\n优势：' + '；'.join(analysis['strengths'])
                            if analysis.get('weaknesses'):
                                analysis_msg += '\n可改进：' + '；'.join(analysis['weaknesses'])
                            if analysis.get('suggestions'):
                                analysis_msg += '\n建议：' + '；'.join(analysis['suggestions'])
                            if analysis.get('recommended_roles'):
                                analysis_msg += '\n推荐岗位：' + '、'.join(analysis['recommended_roles'])
                            flash(analysis_msg, 'info')
                        except Exception as e:
                            current_app.logger.warning(f'AI resume analysis failed: {e}')

                        flash('简历上传成功！' if file_ext not in video_exts else '视频简历上传成功！', 'success')
                        return redirect(url_for('smartrecruit.candidate.profile.settings'))
                    except Exception as e:
                        flash(f'简历上传失败：{str(e)}', 'danger')
                        return redirect(url_for('smartrecruit.candidate.profile.settings'))
                else:
                    flash(f'不支持的文件格式。支持格式：{", ".join(allowed_extensions)}', 'danger')
                    return redirect(url_for('smartrecruit.candidate.profile.settings'))
            else:
                flash('请选择文件。', 'danger')
                return redirect(url_for('smartrecruit.candidate.profile.settings'))

        # 其余情况视为更新基本信息（包含可选头像上传）
        g.user.first_name = request.form.get('first_name', g.user.first_name)
        g.user.last_name = request.form.get('last_name', g.user.last_name)
        g.user.company_name = request.form.get('company_name', g.user.company_name)
        g.user.phone_number = request.form.get('phone_number', g.user.phone_number)
        g.user.birthday = request.form.get('birthday', g.user.birthday)
        g.user.position = request.form.get('position', g.user.position or '')

        # 处理头像上传
        photo_file = request.files.get('profile_photo')
        if photo_file and photo_file.filename:
            if allowed_file(photo_file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
                try:
                    photo_name = secure_filename(photo_file.filename)
                    # 添加时间戳避免文件名冲突
                    import time
                    timestamp = int(time.time())
                    name, ext = os.path.splitext(photo_name)
                    photo_name = f"{name}_{timestamp}{ext}"
                    
                    photo_path = os.path.join(current_app.config['UPLOAD_FOLDER_PHOTOS'], photo_name)
                    photo_file.save(photo_path)
                    g.user.profile_photo = photo_name
                    flash('头像上传成功！', 'success')
                except Exception as e:
                    flash(f'头像上传失败：{str(e)}', 'danger')
            else:
                flash('不支持的头像格式。支持格式：PNG, JPG, JPEG, GIF', 'danger')

        db.session.commit()
        flash('个人信息更新成功！', 'success')
        return redirect(url_for('smartrecruit.candidate.profile.settings'))
    
    # 计算资料完整度
    def calculate_profile_completion(user):
        fields = [
            user.first_name, user.last_name, user.email, user.phone_number,
            user.birthday, user.company_name, user.position, user.cv_file
        ]
        
        filled_fields = sum(1 for field in fields if field)
        total_fields = len(fields)
        
        return int((filled_fields / total_fields) * 100)
    
    profile_completion = calculate_profile_completion(g.user)
    
    return render_template('smartrecruit/candidate/profile_new.html', 
                         user=g.user, 
                         profile_completion=profile_completion)

# 头像上传
@profile_bp.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    file = request.files.get('avatar')
    if not file or not file.filename:
        flash('请选择图片文件。', 'warning')
        return redirect(url_for('smartrecruit.candidate.profile.settings'))
    try:
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER_PHOTO']) if hasattr(current_app.config, 'UPLOAD_FOLDER_PHOTO') else os.path.join(current_app.root_path, 'static', 'uploads', 'photos')
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, filename)
        file.save(save_path)
        g.user.profile_photo = filename
        db.session.commit()
        flash('头像上传成功。', 'success')
    except Exception as e:
        db.session.rollback()
        flash('上传失败，请稍后再试。', 'danger')
    return redirect(url_for('smartrecruit.candidate.profile.settings'))

# 视频上传
@profile_bp.route('/upload_video', methods=['POST'])
def upload_video():
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    file = request.files.get('video')
    if not file or not file.filename:
        flash('请选择视频文件。', 'warning')
        return redirect(url_for('smartrecruit.candidate.profile.settings'))
    try:
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, 'static', 'uploads', 'videos')
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, filename)
        file.save(save_path)
        # 可将视频文件名保存到用户表，如有字段可添加，这里略
        flash('视频上传成功。', 'success')
    except Exception:
        flash('上传失败，请稍后再试。', 'danger')
    return redirect(url_for('smartrecruit.candidate.profile.settings'))

# 简历上传/下载/删除/预览
@profile_bp.route('/upload_resume', methods=['POST'])
def upload_resume():
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    file = request.files.get('cv_file')
    if not file or not file.filename:
        flash('请选择简历文件。', 'warning')
        return redirect(url_for('smartrecruit.candidate.profile.settings'))
    # 允许 PDF / Word / 图片 / 视频
    allowed_extensions = set(get_allowed_cv_extensions()) | {'ppt','pptx','png','jpg','jpeg','webp','bmp','gif','mp4','webm','ogg','mov','avi','mkv'}
    if not allowed_file(file.filename, allowed_extensions):
        flash('文件格式不支持（仅支持 PDF/Word/图片/视频）。', 'danger')
        return redirect(url_for('smartrecruit.candidate.profile.settings'))
    try:
        filename = secure_filename(file.filename)
        upload_dir = current_app.config.get('UPLOAD_FOLDER_CV', os.path.join(current_app.root_path, 'static', 'uploads', 'cv'))
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, filename)
        file.save(save_path)

        # 若为可解析文本类型（非视频/图片），尝试提取文本到cv_data
        ext = filename.rsplit('.',1)[1].lower() if '.' in filename else ''
        video_exts = {'mp4','webm','ogg','mov','avi','mkv'}
        image_exts = {'png','jpg','jpeg','webp','bmp','gif'}
        ppt_exts = {'ppt','pptx'}
        cv_data = None
        if ext not in video_exts and ext not in image_exts and ext not in ppt_exts:
            try:
                file.stream.seek(0)
                cv_data = file.read()
            except Exception:
                cv_data = None
        g.user.cv_file = filename
        g.user.cv_data = cv_data
        db.session.commit()
        
        # 解析技能并提示
        try:
            if cv_data:
                parsed_skills = update_user_skills_from_resume(g.user, cv_data or b'', filename)
                if parsed_skills:
                    flash('简历上传成功，并已基于内容更新技能标签。', 'success')
                else:
                    flash('简历上传成功。', 'success')
            else:
                flash('简历上传成功（媒体文件无法解析文本，不更新技能标签）。', 'success')
        except Exception:
            flash('简历上传成功。', 'success')
    except Exception:
        db.session.rollback()
        flash('上传失败，请稍后再试。', 'danger')
    return redirect(url_for('smartrecruit.candidate.profile.settings'))

@profile_bp.route('/download_resume')
def download_resume():
    if g.user is None or not g.user.cv_file:
        flash('暂无可下载的简历。', 'warning')
        return redirect(url_for('smartrecruit.candidate.profile.settings'))
    upload_dir = current_app.config.get('UPLOAD_FOLDER_CV', os.path.join(current_app.root_path, 'static', 'uploads', 'cv'))
    path = os.path.join(upload_dir, g.user.cv_file)
    if not os.path.isfile(path):
        flash('文件不存在。', 'danger')
        return redirect(url_for('smartrecruit.candidate.profile.settings'))
    from flask import send_file
    import mimetypes
    mime, _ = mimetypes.guess_type(path)
    return send_file(path, as_attachment=True, download_name=g.user.cv_file, mimetype=mime)

@profile_bp.route('/preview_resume')
def preview_resume():
    if g.user is None or not g.user.cv_file:
        flash('暂无可预览的简历。', 'warning')
        return redirect(url_for('smartrecruit.candidate.profile.settings'))
    upload_dir = current_app.config.get('UPLOAD_FOLDER_CV', os.path.join(current_app.root_path, 'static', 'uploads', 'cv'))
    path = os.path.join(upload_dir, g.user.cv_file)
    if not os.path.isfile(path):
        flash('文件不存在。', 'danger')
        return redirect(url_for('smartrecruit.candidate.profile.settings'))
    from flask import send_file
    import mimetypes
    # 对 PPT/视频不提供在线预览，直接改为下载
    ext = g.user.cv_file.rsplit('.', 1)[-1].lower() if '.' in g.user.cv_file else ''
    if ext in {'ppt','pptx','mp4','webm','ogg','mov','avi','mkv'}:
        mime, _ = mimetypes.guess_type(path)
        return send_file(path, as_attachment=True, download_name=g.user.cv_file, mimetype=mime)
    # 其他（如 PDF/图片）允许预览
    mime, _ = mimetypes.guess_type(path)
    return send_file(path, as_attachment=False, download_name=g.user.cv_file, mimetype=mime)

@profile_bp.route('/delete_resume', methods=['POST'])
def delete_resume():
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    try:
        if g.user.cv_file:
            upload_dir = current_app.config.get('UPLOAD_FOLDER_CV', os.path.join(current_app.root_path, 'static', 'uploads', 'cv'))
            path = os.path.join(upload_dir, g.user.cv_file)
            try:
                if os.path.isfile(path):
                    os.remove(path)
            except Exception:
                pass
        g.user.cv_file = None
        g.user.cv_data = None
        db.session.commit()
        flash('已删除简历。', 'success')
    except Exception:
        db.session.rollback()
        flash('删除失败，请稍后再试。', 'danger')
    return redirect(url_for('smartrecruit.candidate.profile.settings'))

# 更新个人信息
@profile_bp.route('/update_info', methods=['POST'])
def update_info():
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    try:
        fields = ['first_name','last_name','phone_number','birthday','company_name','position','bio']
        for f in fields:
            if f in request.form:
                setattr(g.user, f, request.form.get(f))
        db.session.commit()
        flash('个人信息已更新。', 'success')
    except Exception:
        db.session.rollback()
        flash('保存失败，请稍后重试。', 'danger')
    return redirect(url_for('smartrecruit.candidate.profile.settings'))

@profile_bp.route('/career_path')
def career_path():
    """职业发展与技能差距（仅界面，前端模拟数据）"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    return render_template('smartrecruit/candidate/career_path.html', user=g.user)

@profile_bp.route('/resume_builder')
def resume_builder():
    """简历构建器"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    return render_template('smartrecruit/candidate/resume_builder.html', user=g.user)

@profile_bp.route('/skills_assessment')
def skills_assessment():
    """技能评估"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    return render_template('smartrecruit/candidate/skills_assessment.html', user=g.user)

def update_user_skills(user_id, skills):
    """更新用户技能"""
    try:
        from app.models import User
        from app import db
        import json
        
        user = User.query.get(user_id)
        if user:
            user.skills = json.dumps(skills, ensure_ascii=False)
            db.session.commit()
            return True
        return False
    except Exception:
        return False

def get_user_profile_completion(user_id):
    """获取用户资料完整度"""
    try:
        from app.models import User
        
        user = User.query.get(user_id)
        if not user:
            return 0
        
        # 定义需要填写的字段
        required_fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'birthday', 'company_name', 'position', 'cv_file'
        ]
        
        filled_count = 0
        for field in required_fields:
            if hasattr(user, field) and getattr(user, field):
                filled_count += 1
        
        return int((filled_count / len(required_fields)) * 100)
    except Exception:
        return 0

def get_user_profile_data(user_id):
    """获取用户资料数据"""
    try:
        from app.models import User
        
        user = User.query.get(user_id)
        if not user:
            return None
        
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone_number': user.phone_number,
            'birthday': user.birthday,
            'company_name': user.company_name,
            'position': user.position,
            'cv_file': user.cv_file,
            'profile_photo': user.profile_photo,
            'skills': user.skills,
            'profile_completion': get_user_profile_completion(user_id)
        }
    except Exception:
        return None

def get_skill_recommendations(user_id):
    """获取技能推荐"""
    try:
        from app.models import User
        import json
        
        user = User.query.get(user_id)
        if not user:
            return []
        
        # 基于用户当前技能推荐相关技能
        current_skills = []
        if user.skills:
            try:
                current_skills = json.loads(user.skills)
            except:
                current_skills = []
        
        # 技能推荐映射
        skill_recommendations = {
            'Python': ['Django', 'Flask', 'Pandas', 'NumPy', 'Scikit-learn'],
            'Java': ['Spring Boot', 'Hibernate', 'Maven', 'JUnit'],
            'JavaScript': ['React', 'Vue.js', 'Node.js', 'TypeScript'],
            '数据分析': ['Python', 'SQL', 'Excel', 'Tableau', 'Power BI'],
            '机器学习': ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn'],
            '前端开发': ['HTML', 'CSS', 'JavaScript', 'React', 'Vue.js'],
            '后端开发': ['Python', 'Java', 'Node.js', 'Go', 'C#'],
            '数据库': ['MySQL', 'PostgreSQL', 'MongoDB', 'Redis'],
            '云计算': ['AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes']
        }
        
        recommendations = []
        for skill in current_skills:
            if skill in skill_recommendations:
                for rec_skill in skill_recommendations[skill]:
                    if rec_skill not in current_skills and rec_skill not in recommendations:
                        recommendations.append(rec_skill)
        
        return recommendations[:10]  # 限制推荐数量
    except Exception:
        return []

def get_career_path_suggestions(user_id):
    """获取职业发展建议"""
    try:
        from app.models import User
        import json
        
        user = User.query.get(user_id)
        if not user:
            return []
        
        # 基于用户技能和职位推荐职业发展路径
        current_skills = []
        if user.skills:
            try:
                current_skills = json.loads(user.skills)
            except:
                current_skills = []
        
        # 职业发展路径建议
        career_paths = {
            'Python开发工程师': {
                'next_level': '高级Python开发工程师',
                'required_skills': ['系统设计', '微服务', 'Docker', 'Kubernetes'],
                'learning_path': [
                    '深入学习Python高级特性',
                    '掌握系统架构设计',
                    '学习容器化和微服务',
                    '了解DevOps实践'
                ]
            },
            '数据分析师': {
                'next_level': '高级数据分析师',
                'required_skills': ['机器学习', '深度学习', '大数据处理'],
                'learning_path': [
                    '学习机器学习算法',
                    '掌握深度学习框架',
                    '了解大数据技术栈',
                    '提升业务分析能力'
                ]
            },
            '前端开发工程师': {
                'next_level': '高级前端开发工程师',
                'required_skills': ['TypeScript', 'React Native', '性能优化'],
                'learning_path': [
                    '学习TypeScript',
                    '掌握移动端开发',
                    '了解前端性能优化',
                    '学习前端工程化'
                ]
            }
        }
        
        # 根据用户当前职位和技能推荐发展路径
        suggestions = []
        if user.position:
            for position, path in career_paths.items():
                if position in user.position:
                    suggestions.append({
                        'current_position': user.position,
                        'next_position': path['next_level'],
                        'required_skills': path['required_skills'],
                        'learning_path': path['learning_path']
                    })
                    break
        
        return suggestions
    except Exception:
        return []

def get_learning_resources(skill):
    """获取学习资源"""
    try:
        # 学习资源映射
        learning_resources = {
            'Python': [
                {'name': 'Python官方文档', 'url': 'https://docs.python.org/', 'type': '文档'},
                {'name': 'Python教程 - 廖雪峰', 'url': 'https://www.liaoxuefeng.com/wiki/1016959663602400', 'type': '教程'},
                {'name': 'Python进阶', 'url': 'https://eastlakeside.gitbooks.io/interpy-zh/', 'type': '进阶'},
                {'name': 'Python实战项目', 'url': 'https://github.com/topics/python-projects', 'type': '项目'}
            ],
            '机器学习': [
                {'name': '机器学习 - 吴恩达', 'url': 'https://www.coursera.org/learn/machine-learning', 'type': '课程'},
                {'name': '深度学习 - 花书', 'url': 'https://github.com/exacity/deeplearningbook-chinese', 'type': '书籍'},
                {'name': 'Scikit-learn官方文档', 'url': 'https://scikit-learn.org/stable/', 'type': '文档'},
                {'name': 'TensorFlow教程', 'url': 'https://tensorflow.org/tutorials', 'type': '教程'}
            ],
            '前端开发': [
                {'name': 'MDN Web文档', 'url': 'https://developer.mozilla.org/', 'type': '文档'},
                {'name': 'JavaScript高级程序设计', 'url': 'https://github.com/zhangxinxu/quiz', 'type': '书籍'},
                {'name': 'React官方文档', 'url': 'https://reactjs.org/docs/', 'type': '文档'},
                {'name': 'Vue.js官方文档', 'url': 'https://vuejs.org/guide/', 'type': '文档'}
            ]
        }
        
        return learning_resources.get(skill, [])
    except Exception:
        return []