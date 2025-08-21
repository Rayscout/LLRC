from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app
from werkzeug.utils import secure_filename
import os
from app.models import User, db
from app.utils import allowed_file, get_allowed_cv_extensions, extract_text_from_resume

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')

@profile_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    """个人设置页面 - 更新基本信息和上传简历"""
    if g.user is None:
        flash('请先登录。', 'danger')
        return redirect(url_for('common.auth.sign'))
    
    if request.method == 'POST':
        # 处理简历上传：由提交按钮 name="upload_cv" 或存在文件来判断
        if 'upload_cv' in request.form or ('cv_file' in request.files and request.files['cv_file'].filename):
            file = request.files.get('cv_file')
            if file and file.filename:
                allowed_extensions = get_allowed_cv_extensions()
                if allowed_file(file.filename, allowed_extensions):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], filename)
                    file.save(filepath)

                    # 视频与文档分别处理：视频不入库二进制，避免数据库膨胀
                    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
                    video_exts = {'mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'}

                    cv_data = None
                    if ext not in video_exts:
                        try:
                            file.seek(0)
                            cv_data = file.read()
                        except Exception:
                            cv_data = None

                    g.user.cv_file = filename
                    g.user.cv_data = cv_data
                    db.session.commit()

                    flash('简历上传成功！' if ext not in video_exts else '视频简历上传成功！', 'success')
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

        # 可选：同时处理头像上传
        photo_file = request.files.get('profile_photo')
        if photo_file and photo_file.filename and allowed_file(photo_file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
            photo_name = secure_filename(photo_file.filename)
            photo_path = os.path.join(current_app.config['UPLOAD_FOLDER_PHOTOS'], photo_name)
            photo_file.save(photo_path)
            g.user.profile_photo = photo_name

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