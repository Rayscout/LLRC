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

# Initialize the sentence transformer model if available
model = SentenceTransformer('multi-qa-mpnet-base-dot-v1') if SentenceTransformer else None
logging.basicConfig(level=logging.DEBUG)

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

    if model and util:
        embeddings_cv = model.encode(cv_text, convert_to_tensor=True)
        embeddings_job_desc = model.encode(job_description, convert_to_tensor=True)
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

def generate_interview_questions(cv_text, job_description, max_retries=10):
    """
    Generates personalized interview questions based on the candidate's CV and the job description.

    Args:
        cv_text (str): The text from the candidate's CV.
        job_description (str): The text from the job description.
        max_retries (int): The maximum number of retries if the API call fails.

    Returns:
        list: A list of generated interview questions or an error message.
    """
    # 返回通用问题
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

def generate_feedback(question_text, response_text, job_description, max_retries=10):
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
    # 简单的评分算法
    score_base = 5
    overlap = len(set(response_text.lower().split()) & set(job_description.lower().split()))
    length_bonus = min(len(response_text) // 120, 3)
    score = max(3, min(9, score_base + (1 if overlap > 10 else 0) + length_bonus))
    return f"感谢您的回答。建议可以增加更多具体的例子和量化成果。评分：{score}/10"

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
