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
    
    return render_template('smartrecruit/candidate/settings.html', user=g.user)

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