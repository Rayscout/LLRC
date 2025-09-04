import os
import re
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

HEADER_START = "LLRC Header Start"
HEADER_END = "LLRC Header End"

CREATED_RE = re.compile(r"^\s*创建时间:\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*$", re.M)
UPDATE_RE = re.compile(r"^\s*-\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s+by\s+.+$", re.M)

WINDOW_START = datetime(2025, 8, 19, 9, 0)
WINDOW_END = datetime(2025, 9, 3, 18, 0)


def should_skip_dir(dir_path: str) -> bool:
    base = os.path.basename(dir_path)
    if base in SKIP_DIR_NAMES:
        return True
    for sub in SKIP_PATH_SUBSTRINGS:
        if sub in dir_path:
            return True
    return False


def should_process_file(file_path: str) -> bool:
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False
    for sub in SKIP_PATH_SUBSTRINGS:
        if sub in file_path:
            return False
    if ".min." in os.path.basename(file_path):
        return False
    return True


def clamp_to_daytime(dt: datetime) -> datetime:
    start = datetime.combine(dt.date(), time(9, 0))
    end = datetime.combine(dt.date(), time(18, 0))
    if dt < start:
        return start
    if dt > end:
        return end
    return dt


def fix_content(content: str) -> tuple[str, bool]:
    if HEADER_START not in content or HEADER_END not in content:
        return content, False

    created_match = CREATED_RE.search(content)
    if not created_match:
        return content, False
    try:
        created_dt = datetime.strptime(created_match.group(1), "%Y-%m-%d %H:%M")
    except ValueError:
        return content, False

    update_strs = UPDATE_RE.findall(content)
    if not update_strs:
        return content, False
    try:
        update_dts = [datetime.strptime(s, "%Y-%m-%d %H:%M") for s in update_strs]
    except ValueError:
        return content, False

    earliest_update = min(update_dts)

    # If creation is later than earliest update, adjust creation to before it
    if created_dt > earliest_update:
        new_created = earliest_update - timedelta(minutes=30)
        # keep within same day daytime window
        new_created = clamp_to_daytime(new_created)
        # also clamp to global window
        if new_created < WINDOW_START:
            new_created = WINDOW_START
        if new_created > WINDOW_END:
            new_created = WINDOW_END

        new_created_str = new_created.strftime("%Y-%m-%d %H:%M")
        new_content = content[:created_match.start(1)] + new_created_str + content[created_match.end(1):]
        return new_content, True

    return content, False


def main():
    fixed_files = 0
    scanned = 0
    for dirpath, dirnames, filenames in os.walk(PROJECT_ROOT):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(os.path.join(dirpath, d))]
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if not should_process_file(file_path):
                continue
            scanned += 1
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                try:
                    with open(file_path, "r", encoding="gbk") as f:
                        content = f.read()
                except Exception:
                    continue

            new_content, changed = fix_content(content)
            if changed:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    fixed_files += 1
                except Exception:
                    pass

    print(f"Scanned files: {scanned}")
    print(f"Fixed headers: {fixed_files}")


if __name__ == "__main__":
    main()


