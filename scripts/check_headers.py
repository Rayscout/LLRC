import os
import re

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

HEADER_START = "LLRC Header Start"
HEADER_END = "LLRC Header End"


def should_skip_dir(dir_path: str) -> bool:
    """函数 should_skip_dir：处理 dir_path 相关逻辑。"""
    base = os.path.basename(dir_path)
    if base in SKIP_DIR_NAMES:
        return True
    for sub in SKIP_PATH_SUBSTRINGS:
        if sub in dir_path:
            return True
    return False


def should_process_file(file_path: str) -> bool:
    """函数 should_process_file：处理 file_path 相关逻辑。"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
    for sub in SKIP_PATH_SUBSTRINGS:
        if sub in file_path:
            return False
    if ".min." in os.path.basename(file_path):
        return False
    return True


def has_header_text(content: str) -> bool:
    """函数 has_header_text：处理 content 相关逻辑。"""
    return (HEADER_START in content) and (HEADER_END in content)


def main():
    """函数 main：核心业务逻辑。"""
    root = PROJECT_ROOT
    missing = []
    total = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(os.path.join(dirpath, d))]
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if not should_process_file(file_path):
                continue
            total += 1
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                try:
                    with open(file_path, "r", encoding="gbk") as f:
                        content = f.read()
                except Exception:
                    missing.append(os.path.relpath(file_path, root) + " (无法读取)")
                    continue
            if not has_header_text(content):
                missing.append(os.path.relpath(file_path, root))

    print(f"Total code files checked: {total}")
    print(f"Files missing header: {len(missing)}")
    if missing:
        print("Examples:")
        for p in missing[:50]:
            print(" -", p)


if __name__ == "__main__":
    main()


