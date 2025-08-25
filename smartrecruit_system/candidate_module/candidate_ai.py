from flask import current_app
from app.models import db
from app.utils import extract_text_from_resume, ai_extract_skills_from_text

def update_user_skills_from_resume(user, file_bytes: bytes, filename: str) -> list:
    """从上传的简历文件中解析文本，调用AI提取技能，并保存到User.skills(JSON字符串)。

    Returns: 提取到的技能列表
    """
    resume_text = ''
    try:
        resume_text = extract_text_from_resume(file_bytes, filename) or ''
    except Exception:
        resume_text = ''

    skills = ai_extract_skills_from_text(resume_text or (getattr(user, 'position', '') or '') )
    try:
        import json
        user.skills = json.dumps(skills, ensure_ascii=False)
        db.session.commit()
    except Exception as e:
        current_app.logger.warning(f'Failed to save AI skills: {e}')
    return skills


