import os
from werkzeug.utils import secure_filename
from flask import current_app
import re
try:
    import requests
except Exception:
    requests = None  # type: ignore
import json
import time
import logging
try:
    import pdfplumber  # type: ignore
except Exception:
    pdfplumber = None  # type: ignore
try:
    from sentence_transformers import SentenceTransformer, util  # type: ignore
except Exception:
    SentenceTransformer = None  # type: ignore
    util = None  # type: ignore

# Lazily initialize the sentence transformer model to avoid network/download at import time
model = None

def get_sentence_transformer():
    global model
    if model is not None:
        return model
    if SentenceTransformer is None:
        return None
    try:
        model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
        return model
    except Exception as e:
        logging.warning(f"SentenceTransformer load failed: {e}")
        model = None
        return None
logging.basicConfig(level=logging.DEBUG)

# --- Minimal DeepSeek text generation integration (env-based, optional) ---
def _deepseek_generate(prompt: str, max_tokens: int = 800):
    """
    Generate text via DeepSeek chat API if DEEPSEEK_API_KEY is set.

    Env vars:
      - DEEPSEEK_API_KEY: required to enable this path
      - DEEPSEEK_API_URL: optional, defaults to https://api.deepseek.com/v1/chat/completions
      - DEEPSEEK_MODEL: optional, defaults to deepseek-chat
    """
    if requests is None:
        return None
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        return None
    api_url = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com/v1/chat/completions')
    model = os.getenv('DEEPSEEK_MODEL', 'deepseek-chat')
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'stream': False,
            'max_tokens': max_tokens
        }
        resp = requests.post(api_url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        choices = data.get('choices') or []
        if not choices:
            return None
        message = choices[0].get('message') or {}
        content = message.get('content')
        return content.strip() if isinstance(content, str) else None
    except Exception as e:
        logging.warning(f"DeepSeek generation failed: {e}")
        return None

# --- Minimal Google Gemini text generation integration (env-based, optional) ---
def _gemini_generate(prompt: str, max_tokens: int = 800):
    """
    Generate text via Google Gemini if GOOGLE_API_KEY is set.

    Env:
      - GOOGLE_API_KEY: required
      - GEMINI_MODEL: optional, defaults to gemini-1.5-pro
    """
    if requests is None:
        return None
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return None
    model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-pro')
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent'
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {
            'contents': [{'parts': [{'text': prompt}]}],
            'generationConfig': {'maxOutputTokens': max_tokens}
        }
        resp = requests.post(url, headers=headers, params={'key': api_key}, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        candidates = data.get('candidates') or []
        if not candidates:
            return None
        content = candidates[0].get('content') or {}
        parts = content.get('parts') or []
        text = ''.join(p.get('text', '') for p in parts if isinstance(p, dict))
        return text.strip() if text else None
    except Exception as e:
        logging.warning(f"Gemini generation failed: {e}")
        return None

def create_upload_folders(app):
    """
    Creates the necessary upload folders for CVs and profile photos.
    If the folders already exist, it does nothing.

    Args:
        app (Flask): The Flask application instance.
    """
    os.makedirs(app.config['UPLOAD_FOLDER_CV'], exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER_PHOTOS'], exist_ok=True)

def allowed_file(filename, allowed_extensions):
    """
    Checks if a given filename has an allowed extension.

    Args:
        filename (str): The name of the file to check.
        allowed_extensions (set): A set of allowed file extensions.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def preprocess_text(text):
    """
    Preprocesses the input text by removing unwanted characters and normalizing spaces.

    Args:
        text (str): The text to preprocess.

    Returns:
        str: The cleaned and normalized text.
    """
    text = re.sub(r'\s+', ' ', text)  
    text = re.sub(r'[^\w\s]', '', text)  
    return text

def compute_similarity(cv_text, job_description):
    """
    Computes the cosine similarity between the CV text and job description.

    Args:
        cv_text (str): The text from the candidate's CV.
        job_description (str): The text from the job description.

    Returns:
        float: The cosine similarity score between the CV and job description.
    """
    cv_text = preprocess_text(cv_text)
    job_description = preprocess_text(job_description)

    st_model = get_sentence_transformer()
    if st_model and util:
        embeddings_cv = st_model.encode(cv_text, convert_to_tensor=True)
        embeddings_job_desc = st_model.encode(job_description, convert_to_tensor=True)
        similarity_score = util.cos_sim(embeddings_cv, embeddings_job_desc)
        return similarity_score.item()
    # Fallback: naive token overlap ratio when transformer model not available
    set_cv = set(cv_text.lower().split())
    set_job = set(job_description.lower().split())
    if not set_cv or not set_job:
        return 0.0
    overlap = len(set_cv & set_job)
    union = len(set_cv | set_job)
    return overlap / union

def evaluate_cv(cv_text, job_description, threshold = 0.5):
    """
    Evaluates the CV against the job description using the similarity score.

    Args:
        cv_text (str): The text from the candidate's CV.
        job_description (str): The text from the job description.
        threshold (float): The similarity threshold to determine a match.

    Returns:
        bool: True if the similarity score is above the threshold, False otherwise.
    """
    similarity = compute_similarity(cv_text, job_description)
    logging.info(f"Similarity score: {similarity:.2f}")

    return similarity > threshold, similarity

def _hf_generate(prompt: str, max_new_tokens: int = 600):
    if requests is None:
        return None
    try:
        headers = {
            'Authorization': f"Bearer {current_app.config.get('API_TOKEN', '')}",
            'Content-Type': 'application/json'
        }
        data = {
            'inputs': prompt,
            'parameters': {
                'max_new_tokens': max_new_tokens,
                'temperature': 0.6,
                'top_p': 0.9,
                'do_sample': True
            }
        }
        resp = requests.post(current_app.config.get('API_URL'), headers=headers, data=json.dumps(data), timeout=30)
        resp.raise_for_status()
        js = resp.json()
        return js[0].get('generated_text') if isinstance(js, list) and js else None
    except Exception as e:
        logging.warning(f"HF generation failed: {e}")
        return None

def generate_interview_questions(cv_text, job_description, max_retries=3):
    """
    Generates personalized interview questions based on the candidate's CV and the job description.

    Args:
        cv_text (str): The text from the candidate's CV.
        job_description (str): The text from the job description.
        max_retries (int): The maximum number of retries if the API call fails.

    Returns:
        list: A list of generated interview questions or an error message.
    """
    # 先尝试通过 Gemini 生成
    prompt = (
        "Generate 10 concise, non-repetitive interview questions in Chinese based on the candidate resume and the job description.\n"
        "Resume:\n" + cv_text + "\nJob Description:\n" + job_description + "\nQuestions:" 
    )
    generated = _gemini_generate(prompt, max_tokens=800)
    if generated:
        lines = [ln.strip() for ln in generated.splitlines() if ln.strip()]
        questions = [ln for ln in lines if ln.endswith('？') or ln.endswith('?')]
        if len(questions) >= 5:
            return questions[:10]
    # 再尝试通过 DeepSeek 生成
    generated = _deepseek_generate(prompt, max_tokens=800)
    if generated:
        lines = [ln.strip() for ln in generated.splitlines() if ln.strip()]
        questions = [ln for ln in lines if ln.endswith('？') or ln.endswith('?')]
        if len(questions) >= 5:
            return questions[:10]
    # 再尝试通过 HF API 生成（后备）
    generated = _hf_generate(prompt, max_new_tokens=800)
    if generated:
        lines = [ln.strip() for ln in generated.splitlines() if ln.strip()]
        questions = [ln for ln in lines if ln.endswith('？') or ln.endswith('?')]
        if len(questions) >= 5:
            return questions[:10]
    # 返回通用问题作为降级
    return [
        "请介绍一下你的技术背景和主要技能栈？",
        "你最近完成的一个项目是什么？遇到了什么挑战？",
        "你是如何保持技术学习的？",
        "在团队协作中，你通常承担什么角色？",
        "你如何看待技术债务？",
        "请描述一个你解决过的技术难题？",
        "你如何评估一个技术方案的可行性？",
        "在项目开发中，你如何确保代码质量？",
        "你如何与产品经理和设计师协作？",
        "你对这个职位有什么期望？"
    ]

def generate_feedback(question_text, response_text, job_description, max_retries=3):
    """
    Generates feedback based on the candidate's response to an interview question, the question itself, and the job description, and generates a score out of 10 at the end.

    Args:
        question_text (str): The interview question asked to the candidate.
        response_text (str): The candidate's response to the interview question.
        job_description (str): The text from the job description.
        max_retries (int): The maximum number of retries if the API call fails.

    Returns:
        str: The generated feedback or an error message.
    """
    # 先尝试通过 Gemini 生成
    prompt = (
        "使用中文，对候选人答复给出简短建设性的反馈，并在结尾给出形如‘评分：X/10’的分数。\n"
        f"问题：{question_text}\n回答：{response_text}\n职位描述：{job_description}\n反馈："
    )
    generated = _gemini_generate(prompt, max_tokens=400)
    if generated:
        return generated.strip()
    # 再尝试通过 DeepSeek 生成
    generated = _deepseek_generate(prompt, max_tokens=400)
    if generated:
        return generated.strip()
    # 再尝试通过 HF API 生成（后备）
    generated = _hf_generate(prompt, max_new_tokens=400)
    if generated:
        return generated.strip()
    # 简单的评分算法作为降级
    score_base = 5
    overlap = len(set(response_text.lower().split()) & set(job_description.lower().split()))
    length_bonus = min(len(response_text) // 120, 3)
    score = max(3, min(9, score_base + (1 if overlap > 10 else 0) + length_bonus))
    return f"感谢您的回答。建议可以增加更多具体的例子和量化成果。评分：{score}/10"

def ai_extract_skills_from_text(resume_text: str) -> list:
    """从简历文本中提取技能列表。优先调用 Gemini，再调用 DeepSeek，最后本地关键词提取降级。

    Returns: list[str]
    """
    prompt = (
        "请从以下中文简历文本中提取候选人的关键技能，输出JSON数组，数组内仅包含技能字符串，不要多余说明。\n"
        f"简历：\n{resume_text}\n输出："
    )
    # Gemini
    generated = _gemini_generate(prompt, max_tokens=300)
    if generated:
        try:
            parsed = json.loads(generated)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed if str(x).strip()]
        except Exception:
            pass
    # DeepSeek
    generated = _deepseek_generate(prompt, max_tokens=300)
    if generated:
        try:
            parsed = json.loads(generated)
            if isinstance(parsed, list):
                return [str(x).strip() for x in parsed if str(x).strip()]
        except Exception:
            pass
    # Fallback: 关键词匹配
    try:
        from .smartrecruit_system.candidate_module.recommendation_config import SKILL_CATEGORIES, CHINESE_SKILLS
    except Exception:
        SKILL_CATEGORIES, CHINESE_SKILLS = {}, {}
    text_lower = resume_text.lower()
    skills = set()
    for _, arr in SKILL_CATEGORIES.items():
        for s in arr:
            if s in text_lower:
                skills.add(s)
    zh_lower = resume_text
    for _, arr in CHINESE_SKILLS.items():
        for s in arr:
            if s in zh_lower:
                skills.add(s)
    if not skills:
        # 基础兜底
        return ["编程", "软件开发", "团队协作"]
    return list(skills)

def ai_analyze_resume_text(resume_text: str) -> dict:
    """对简历文本做详尽分析，返回结构化结果。

    返回字段：summary, strengths, weaknesses, suggestions, recommended_roles
    """
    prompt = (
        "你是一名资深HR。请深入分析下面的中文简历，输出JSON，字段为：\n"
        "summary: 对候选人的背景做150-250字概述；\n"
        "strengths: 用条目列出3-6条优势；\n"
        "weaknesses: 用条目列出2-4条可改进点；\n"
        "suggestions: 给出具体可执行的改进建议（3-6条）；\n"
        "recommended_roles: 推荐3-6个适合的岗位名称。\n"
        "只输出JSON，不要额外说明。\n\n"
        f"简历：\n{resume_text}\n\n输出："
    )
    import json, re
    # Gemini 优先
    text = _gemini_generate(prompt, max_tokens=900) or _deepseek_generate(prompt, max_tokens=900)
    result: dict = {}
    if text:
        cleaned = text.replace('```json', '').replace('```', '').strip()
        m = re.search(r"\{[\s\S]*\}", cleaned)
        candidate = m.group(0) if m else cleaned
        try:
            js = json.loads(candidate)
            if isinstance(js, dict):
                result = js
        except Exception:
            pass
    # Fallback 简易分析
    if not result:
        tokens = resume_text.lower()
        strengths = []
        if 'flask' in tokens or 'django' in tokens:
            strengths.append('熟悉主流Python后端框架，具备Web开发经验')
        if 'sql' in tokens or 'mysql' in tokens or 'postgres' in tokens:
            strengths.append('掌握关系型数据库与SQL调优基础')
        if 'docker' in tokens or 'kubernetes' in tokens:
            strengths.append('具备容器化与部署能力')
        if not strengths:
            strengths = ['具备扎实的计算机基础与项目实践']
        weaknesses = ['简历中的量化成果偏少', '项目角色与个人贡献需更清晰']
        suggestions = ['补充关键项目的指标与影响（如性能提升、成本下降）', '在技能小节中突出核心技术与掌握程度', '增加与目标岗位匹配的关键词']
        recommended_roles = ['Python后端工程师', '数据开发工程师', '平台工程师']
        result = {
            'summary': '候选人具备一定的软件开发背景与实践能力，技术栈集中在后端/数据方向，具备学习与落地能力，适合进一步在目标岗位进行深耕与提升。',
            'strengths': strengths,
            'weaknesses': weaknesses,
            'suggestions': suggestions,
            'recommended_roles': recommended_roles,
        }
    # 规整类型
    def _to_list(x):
        if isinstance(x, list):
            return [str(i).strip() for i in x if str(i).strip()]
        if isinstance(x, str):
            # 可能是用换行/分号分隔
            parts = [i.strip('- •\t ').strip() for i in re.split(r"[\n;]\s*", x) if i.strip()]
            return parts or [x.strip()]
        return []
    result = {
        'summary': str(result.get('summary', '')).strip(),
        'strengths': _to_list(result.get('strengths', [])),
        'weaknesses': _to_list(result.get('weaknesses', [])),
        'suggestions': _to_list(result.get('suggestions', [])),
        'recommended_roles': _to_list(result.get('recommended_roles', [])),
    }
    return result

def extract_text_from_resume(file_bytes: bytes, filename: str) -> str:
    """从简历二进制中提取文本，支持 PDF/DOCX，图片不提取。"""
    try:
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if ext == 'pdf' and pdfplumber is not None:
            from io import BytesIO
            with pdfplumber.open(BytesIO(file_bytes)) as pdf:
                return ''.join(page.extract_text() or '' for page in pdf.pages)
        if ext == 'docx':
            try:
                import docx2txt
                from tempfile import NamedTemporaryFile
                with NamedTemporaryFile(suffix='.docx', delete=True) as tmp:
                    tmp.write(file_bytes)
                    tmp.flush()
                    return (docx2txt.process(tmp.name) or '').strip()
            except Exception:
                return ''
    except Exception as e:
        logging.warning(f'extract_text_from_resume failed: {e}')
    return ''

def convert_keys_to_strings(data):
    """
    Recursively converts all dictionary keys to strings.

    Args:
        data (dict or list): The input dictionary or list to process.

    Returns:
        dict or list: The processed data with all keys converted to strings.
    """
    if isinstance(data, dict):
        return {str(k): convert_keys_to_strings(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_strings(i) for i in data]
    else:
        return data

def extract_score(feedback):
    """
    Extracts the score from the feedback text using multiple patterns.

    Args:
        feedback (str): The feedback text containing the score.

    Returns:
        int: The extracted score or None if no score was found.
    """
    patterns = [
        r'\b(\d{1,2})\s*/\s*10\b',                # Matches "3/10", "3 / 10", etc.
        r'\b(\d{1,2})\s*out\s+of\s+10\b',         # Matches "3 out of 10", etc.
        r'\b(\d{1,2})\s*over\s*10\b',             # Matches "3 over 10", etc.
        r'\bscore\s+is\s+(\d{1,2})\b',            # Matches "score is 10", "score is 3", etc.
        r'\brated\s+(\d{1,2})\s*/\s*10\b',        # Matches "rated 7/10", etc.
        r'\brating\s+of\s+(\d{1,2})\s*/\s*10\b',  # Matches "rating of 8/10", etc.
        r'\bgave\s+it\s+a\s+(\d{1,2})\b',         # Matches "gave it a 5", etc.
        r'\b(\d{1,2})\b\s+(?:points|stars)\s*/\s*10\b' # Matches "5 points / 10", "5 stars / 10", etc.
    ]

    for pattern in patterns:
        match = re.search(pattern, feedback, re.IGNORECASE)
        if match:
            return int(match.group(1))

    logging.warning("No score found in feedback.")
    return None

def get_allowed_cv_extensions():
    """
    Returns a set of allowed CV file extensions.
    
    Returns:
        set: A set of allowed file extensions for CV uploads.
    """
    return {'pdf', 'docx', 'png', 'jpg', 'jpeg', 'mp4', 'webm', 'ogg', 'mov', 'avi', 'mkv'}

def extract_text_from_file(file_path):
    """
    Extracts text from various file types (PDF, DOCX, images).
    
    Args:
        file_path (str): Path to the file to extract text from.
        
    Returns:
        str: Extracted text from the file.
        
    Raises:
        Exception: If text extraction fails or file type is not supported.
    """
    import os
    from PIL import Image
    import pytesseract
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext == '.pdf':
            if pdfplumber is None:
                raise Exception("PDF processing library (pdfplumber) not available")
            
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
                
        elif file_ext == '.docx':
            try:
                import docx2txt
                text = docx2txt.process(file_path)
                return text.strip()
            except ImportError:
                raise Exception("DOCX processing library (docx2txt) not available")
                
        elif file_ext in {'.png', '.jpg', '.jpeg'}:
            try:
                # Try to use pytesseract for OCR
                image = Image.open(file_path)
                text = pytesseract.image_to_string(image)
                return text.strip()
            except ImportError:
                raise Exception("Image processing libraries (PIL, pytesseract) not available")
            except Exception as e:
                raise Exception(f"Failed to extract text from image: {e}")
                
        else:
            raise Exception(f"Unsupported file type: {file_ext}")
            
    except Exception as e:
        logging.error(f"Failed to extract text from {file_path}: {e}")
        raise Exception(f"Text extraction failed: {e}")
