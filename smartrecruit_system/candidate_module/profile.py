from flask import Blueprint, render_template, request, redirect, url_for, flash, g, current_app
from werkzeug.utils import secure_filename
import os
import time
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
        action = request.form.get('action')
        # 兼容前端未传递 action 的情况，根据按钮名称回退
        if not action:
            if 'save_changes' in request.form:
                action = 'update_info'
            elif 'upload_cv' in request.form:
                action = 'upload_cv'
        
        if action == 'update_info':
            # 更新基本信息
            g.user.first_name = request.form['first_name']
            g.user.last_name = request.form['last_name']
            g.user.company_name = request.form['company_name']
            g.user.phone_number = request.form['phone_number']
            g.user.birthday = request.form['birthday']
            g.user.position = request.form.get('position', '')
            # 同时处理头像上传（如果选择了文件）
            if 'profile_photo' in request.files:
                file = request.files['profile_photo']
                if file and file.filename and allowed_file(file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
                    # 使用用户ID与时间戳生成唯一文件名，避免覆盖
                    original_ext = os.path.splitext(secure_filename(file.filename))[1].lower()
                    unique_name = f"user_{g.user.id}_{int(time.time())}{original_ext}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER_PHOTOS'], unique_name)
                    file.save(filepath)
                    g.user.profile_photo = unique_name
                elif file and not file.filename:
                    pass  # 未选择文件时忽略
                elif file and file.filename:
                    flash('请选择有效的图片文件。', 'danger')
                    return redirect(url_for('smartrecruit.candidate.profile.settings'))
            
            db.session.commit()
            flash('个人信息更新成功！', 'success')
            return redirect(url_for('smartrecruit.candidate.profile.settings'))
            
        elif action == 'upload_photo':
            # 上传头像（备用：如果前端单独提交头像表单）
            if 'profile_photo' in request.files:
                file = request.files['profile_photo']
                if file and file.filename and allowed_file(file.filename, {'png', 'jpg', 'jpeg', 'gif'}):
                    original_ext = os.path.splitext(secure_filename(file.filename))[1].lower()
                    unique_name = f"user_{g.user.id}_{int(time.time())}{original_ext}"
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER_PHOTOS'], unique_name)
                    file.save(filepath)
                    g.user.profile_photo = unique_name
                    db.session.commit()
                    flash('头像上传成功！', 'success')
                else:
                    flash('请选择有效的图片文件。', 'danger')
            
        elif action == 'upload_cv':
            # 上传简历
            if 'cv_file' in request.files:
                file = request.files['cv_file']
                if file and file.filename:
                    allowed_extensions = get_allowed_cv_extensions()
                    if allowed_file(file.filename, allowed_extensions):
                        filename = secure_filename(file.filename)
                        filepath = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], filename)
                        file.save(filepath)
                        
                        # 读取文件内容并存储到数据库
                        file.seek(0)
                        cv_data = file.read()
                        
                        g.user.cv_file = filename
                        g.user.cv_data = cv_data
                        db.session.commit()
                        
                        flash('简历上传成功！', 'success')
                    else:
                        flash(f'不支持的文件格式。支持格式：{", ".join(allowed_extensions)}', 'danger')
                else:
                    flash('请选择文件。', 'danger')
    
    return render_template('smartrecruit/candidate/settings.html', user=g.user)
