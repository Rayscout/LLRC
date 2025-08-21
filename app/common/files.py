from flask import Blueprint, send_file, jsonify, g, current_app, abort, url_for
import os
from werkzeug.utils import secure_filename
from ..utils import allowed_file

files_bp = Blueprint('files', __name__)

@files_bp.route('/download/<filename>')
def download_file(filename):
    """下载文件"""
    if g.user is None:
        abort(401)
    
    # 安全检查：确保文件名安全
    if not allowed_file(filename, {'pdf', 'docx', 'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'webm', 'ogg', 'avi', 'mkv'}):
        abort(400)
    
    # 构建文件路径
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], filename)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        abort(404)
    
    # 发送文件
    return send_file(file_path, as_attachment=True)

@files_bp.route('/video/<filename>')
def serve_video(filename):
    """专门用于提供视频文件的路由"""
    if g.user is None:
        return jsonify({'error': 'Not authenticated'}), 401
    
    # 安全检查：确保文件名安全
    if not allowed_file(filename, {'mp4', 'mov', 'webm', 'ogg', 'avi', 'mkv'}):
        return jsonify({'error': 'Invalid filename'}), 400
    
    # 构建文件路径
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], filename)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return jsonify({'error': 'File not found'}), 404
    
    # 发送文件
    return send_file(file_path, mimetype='video/mp4')

@files_bp.route('/photo/<filename>')
def serve_photo(filename):
    """提供头像图片"""
    if g.user is None:
        abort(401)
    
    # 安全检查：确保文件名安全
    if not allowed_file(filename, {'png', 'jpg', 'jpeg', 'gif'}):
        abort(400)
    
    # 构建文件路径
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER_PHOTOS'], filename)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        abort(404)
    
    # 发送文件
    return send_file(file_path)

@files_bp.route('/debug/video/<filename>')
def debug_video(filename):
    """调试路由：测试视频文件访问"""
    if g.user is None:
        return jsonify({'error': 'Not authenticated'}), 401
    
    cv_path = os.path.join(current_app.config['UPLOAD_FOLDER_CV'], filename)
    
    if not os.path.exists(cv_path):
        return jsonify({'error': 'File not found', 'path': cv_path}), 404
    
    file_info = {
        'filename': filename,
        'path': cv_path,
        'size': os.path.getsize(cv_path),
        'exists': os.path.exists(cv_path),
        'readable': os.access(cv_path, os.R_OK),
        'url': url_for('common.files.serve_video', filename=filename),
        'mime_type': 'video/mp4' if filename.endswith('.mp4') else 'unknown'
    }
    
    return jsonify(file_info)
