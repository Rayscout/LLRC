import os
import re
import sys
import hashlib
import random
from datetime import datetime, timedelta, time

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

ALLOWED_EXTENSIONS = {".py", ".js", ".css", ".html", ".ts"}

SKIP_DIR_NAMES = {
    "venv", "node_modules", "__pycache__", ".git", "logs", "flask_session_data",
    "reports", "app\\reports", "backups", "tmp", "YOLO", "testing_resumes",
    "instance", "database\\migrations", "database\\scripts", "database\\tools",
}

SKIP_PATH_SUBSTRINGS = [
    os.sep + "static" + os.sep + "Images" + os.sep,
    os.sep + "static" + os.sep + "uploads" + os.sep,
    os.sep + "reports" + os.sep,
    os.sep + "flask_session_data" + os.sep,
    os.sep + "venv" + os.sep,
]

AUTHORS = [
    "潘显雨",
    "张宇成",
    "苏杰",
    "谢佳悦",
    "李雨梦",
    "侯东杨",
]

HEADER_START = "LLRC Header Start"
HEADER_END = "LLRC Header End"


def generate_seed_from_path(path: str) -> int:
    """函数 generate_seed_from_path：处理 path 相关逻辑。"""
    digest = hashlib.sha256(path.encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def daytime_random(dt_from: datetime, dt_to: datetime, rng: random.Random) -> datetime:
    """函数 daytime_random：处理 dt_from, dt_to, rng 相关逻辑。"""
    # Pick a random day between dt_from and dt_to (inclusive), then a time between 09:00-18:00
    if dt_from > dt_to:
        dt_from, dt_to = dt_to, dt_from
    days = (dt_to.date() - dt_from.date()).days
    day_offset = rng.randint(0, days)
    day = dt_from.date() + timedelta(days=day_offset)
    start = datetime.combine(day, time(9, 0))
    end = datetime.combine(day, time(18, 0))
    total_seconds = int((end - start).total_seconds())
    sec_offset = rng.randint(0, total_seconds)
    return start + timedelta(seconds=sec_offset)


def get_comment_style(ext: str):
    """函数 get_comment_style：处理 ext 相关逻辑。"""
    if ext in {".js", ".css", ".ts"}:
        return "block", "/*", "*/"
    if ext == ".html":
        return "block", "<!--", "-->"
    if ext == ".py":
        # Use a module docstring so it is valid and harmless
        return "docstring", "\"\"\"", "\"\"\""
    return None, None, None


def infer_description(file_path: str) -> str:
    """函数 infer_description：处理 file_path 相关逻辑。"""
    # Heuristic Chinese description based on path and extension
    rel = os.path.relpath(file_path, PROJECT_ROOT).replace("\\", "/")
    name = os.path.basename(file_path)
    ext = os.path.splitext(name)[1].lower()
    if ext == ".py":
        if "smartrecruit_system" in rel:
            return f"SmartRecruit 子系统 Python 模块：{rel}"
        if "talent_management_system" in rel:
            return f"人才管理子系统 Python 模块：{rel}"
        if "app/templates" in rel:
            return f"应用模板相关的辅助 Python 模块：{rel}"
        if "app/" in rel:
            return f"应用后端 Python 模块：{rel}"
        return f"通用 Python 脚本/模块：{rel}"
    if ext == ".html":
        return f"前端 HTML 模板页面：{rel}"
    if ext == ".js":
        return f"前端 JavaScript 脚本：{rel}"
    if ext == ".css":
        return f"前端样式表（CSS）：{rel}"
    if ext == ".ts":
        return f"前端 TypeScript 脚本：{rel}"
    return f"代码文件：{rel}"


def build_header(ext: str, desc: str, creator: str, created_at: datetime, updates: list[tuple[datetime, str]]) -> str:
    """函数 build_header：处理 ext, desc, creator, created_at, updates 相关逻辑。"""
    style, open_tok, close_tok = get_comment_style(ext)
    created_str = created_at.strftime("%Y-%m-%d %H:%M")
    updates_lines = "\n".join(f"- {dt.strftime('%Y-%m-%d %H:%M')} by {author}" for dt, author in updates)

    if style == "docstring":
        # Python docstring
        body = (
            f"{open_tok}\n"
            f"{HEADER_START}\n"
            f"文件功能: {desc}\n"
            f"创建时间: {created_str}\n"
            f"创建人: {creator}\n"
            f"更新记录:\n{updates_lines}\n"
            f"{HEADER_END}\n"
            f"{close_tok}\n"
        )
        return body
    elif style == "block":
        # C-style block or HTML comment
        return (
            f"{open_tok}\n"
            f" {HEADER_START}\n"
            f" 文件功能: {desc}\n"
            f" 创建时间: {created_str}\n"
            f" 创建人: {creator}\n"
            f" 更新记录:\n {updates_lines}\n"
            f" {HEADER_END}\n"
            f"{close_tok}\n"
        )
    else:
        return ""


def has_header(content: str) -> bool:
    """函数 has_header：处理 content 相关逻辑。"""
    return (HEADER_START in content) and (HEADER_END in content)


def choose_creator(rng: random.Random) -> str:
    """函数 choose_creator：处理 rng 相关逻辑。"""
    return rng.choice(AUTHORS)


def generate_updates(rng: random.Random) -> list[tuple[datetime, str]]:
    """函数 generate_updates：处理 rng 相关逻辑。"""
    # 1-3 update entries within 2025-08-19 to 2025-09-03, daytime
    start = datetime(2025, 8, 19, 0, 0)
    end = datetime(2025, 9, 3, 23, 59)
    num = rng.randint(1, 3)
    entries = []
    for _ in range(num):
        dt = daytime_random(start, end, rng)
        who = rng.choice(AUTHORS)
        entries.append((dt, who))
    # sort chronologically
    entries.sort(key=lambda x: x[0])
    return entries


def get_file_created_time(path: str, rng: random.Random) -> datetime:
    """函数 get_file_created_time：处理 path, rng 相关逻辑。"""
    # Try to use filesystem created time if available; otherwise, pick a stable random time in window
    try:
        stat = os.stat(path)
        # On Windows, st_ctime is creation time
        created_ts = getattr(stat, "st_ctime", None) or getattr(stat, "st_mtime", None)
        if created_ts:
            dt = datetime.fromtimestamp(created_ts)
            # Clamp into range if outside
            low = datetime(2025, 8, 19, 9, 0)
            high = datetime(2025, 9, 3, 18, 0)
            if dt < low or dt > high:
                return daytime_random(low, high, rng)
            return dt
    except Exception:
        pass
    # Fallback: deterministic daytime random in range
    return daytime_random(datetime(2025, 8, 19, 9, 0), datetime(2025, 9, 3, 18, 0), rng)


def should_skip_dir(dir_path: str) -> bool:
    """函数 should_skip_dir：处理 dir_path 相关逻辑。"""
    base = os.path.basename(dir_path)
    if base in SKIP_DIR_NAMES:
        return True
    # skip common large/static folders anywhere in path
    for sub in SKIP_PATH_SUBSTRINGS:
        if sub in dir_path:
            return True
    return False


def should_process_file(file_path: str) -> bool:
    """函数 should_process_file：处理 file_path 相关逻辑。"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
    rel = os.path.relpath(file_path, PROJECT_ROOT)
    for sub in SKIP_PATH_SUBSTRINGS:
        if sub in file_path:
            return False
    # Skip minified assets
    if ".min." in os.path.basename(file_path):
        return False
    return True


def prepend_header_to_file(file_path: str) -> bool:
    """函数 prepend_header_to_file：处理 file_path 相关逻辑。"""
    ext = os.path.splitext(file_path)[1].lower()
    style, _, _ = get_comment_style(ext)
    if style is None:
        return False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try gbk as fallback for potential Chinese encodings
        try:
            with open(file_path, "r", encoding="gbk") as f:
                content = f.read()
        except Exception:
            return False
    except Exception:
        return False

    if has_header(content):
        return False

    rng = random.Random(generate_seed_from_path(os.path.relpath(file_path, PROJECT_ROOT)))

    desc = infer_description(file_path)
    creator = choose_creator(rng)
    created_at = get_file_created_time(file_path, rng)
    updates = generate_updates(rng)
    header = build_header(ext, desc, creator, created_at, updates)
    if not header:
        return False

    # For HTML, if file starts with <!DOCTYPE or <html>, keep doctype first then header
    new_content = header + content
    if ext == ".html":
        doctype_match = re.match(r"^(\s*<!DOCTYPE[^>]*>\s*)", content, re.IGNORECASE)
        if doctype_match:
            prefix = doctype_match.group(1)
            rest = content[len(prefix):]
            new_content = prefix + "\n" + header + rest

    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    except Exception:
        return False


def main():
    """函数 main：核心业务逻辑。"""
    root = PROJECT_ROOT
    processed = 0
    skipped = 0
    for dirpath, dirnames, filenames in os.walk(root):
        # mutate dirnames in-place to prune traversal
        dirnames[:] = [d for d in dirnames if not should_skip_dir(os.path.join(dirpath, d))]

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if not should_process_file(file_path):
                skipped += 1
                continue
            if prepend_header_to_file(file_path):
                processed += 1
            else:
                skipped += 1

    print(f"Headers inserted: {processed}; skipped: {skipped}")


if __name__ == "__main__":
    main()


