import ast
import os
from typing import List, Tuple

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

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


def should_skip_dir(dir_path: str) -> bool:
    """函数 should_skip_dir：处理 dir_path 相关逻辑。"""
    base = os.path.basename(dir_path)
    if base in SKIP_DIR_NAMES:
        return True
    for sub in SKIP_PATH_SUBSTRINGS:
        if sub in dir_path:
            return True
    return False


def list_python_files(root: str) -> List[str]:
    """函数 list_python_files：处理 root 相关逻辑。"""
    files: List[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(os.path.join(dirpath, d))]
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            file_path = os.path.join(dirpath, filename)
            skip = False
            for sub in SKIP_PATH_SUBSTRINGS:
                if sub in file_path:
                    skip = True
                    break
            if skip:
                continue
            files.append(file_path)
    return files


def get_leading_whitespace(s: str) -> str:
    """函数 get_leading_whitespace：处理 s 相关逻辑。"""
    idx = 0
    while idx < len(s) and s[idx] in (" ", "\t"):
        idx += 1
    return s[:idx]


def summarize_function(name: str, args: ast.arguments) -> str:
    """函数 summarize_function：处理 name, args 相关逻辑。"""
    params: List[str] = []
    for a in list(args.posonlyargs) + list(args.args):
        if a.arg not in {"self", "cls"}:
            params.append(a.arg)
    if args.vararg:
        params.append("*" + args.vararg.arg)
    for a in args.kwonlyargs:
        params.append(a.arg)
    if args.kwarg:
        params.append("**" + args.kwarg.arg)
    if params:
        return f"函数 {name}：处理 {', '.join(params)} 相关逻辑。"
    return f"函数 {name}：核心业务逻辑。"


def summarize_class(name: str) -> str:
    """函数 summarize_class：处理 name 相关逻辑。"""
    return f"类 {name}：封装与该模块相关的数据与行为。"


def collect_targets(tree: ast.AST) -> List[Tuple[int, str, str, ast.AST]]:
    """
    Return list of (insert_after_line, indent_hint, docstring_text, node)
    in descending order of line numbers for safe insertion.
    """
    targets: List[Tuple[int, str, str, ast.AST]] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Skip if already has docstring
            if ast.get_docstring(node):
                continue
            # Must have body
            if not node.body:
                continue
            # Decorators may shift lineno; AST lineno is def line
            insert_after_line = node.lineno
            # Create docstring content
            doc = summarize_function(node.name, node.args)
            targets.append((insert_after_line, "func", doc, node))
        elif isinstance(node, ast.ClassDef):
            if ast.get_docstring(node):
                continue
            if not node.body:
                continue
            insert_after_line = node.lineno
            doc = summarize_class(node.name)
            targets.append((insert_after_line, "class", doc, node))

    # Insert bottom-up to keep line numbers valid
    targets.sort(key=lambda t: t[0], reverse=True)
    return targets


def insert_docstrings(source: str) -> Tuple[str, int]:
    """函数 insert_docstrings：处理 source 相关逻辑。"""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return source, 0

    lines = source.splitlines(keepends=True)
    targets = collect_targets(tree)
    added = 0

    for insert_after_line, kind, doc, node in targets:
        # Determine indentation: prefer first body statement indentation
        body_first_line = None
        if node.body and hasattr(node.body[0], 'lineno'):
            body_first_line = node.body[0].lineno - 1
        indent = ""
        if body_first_line is not None and 0 <= body_first_line < len(lines):
            indent = get_leading_whitespace(lines[body_first_line])
        else:
            def_line = insert_after_line - 1
            if 0 <= def_line < len(lines):
                def_indent = get_leading_whitespace(lines[def_line])
                # add one indentation level (reuse same style: spaces or tabs)
                if def_indent.endswith("\t"):
                    indent = def_indent + "\t"
                else:
                    indent = def_indent + "    "

        doc_lines = [f"{indent}\"\"\"{doc}\"\"\"\n"]

        insert_index = insert_after_line  # line numbers are 1-based; insert after def/class line
        # Special case: if next meaningful line is also a string literal -> existing docstring; skip
        if insert_index < len(lines):
            next_line = lines[insert_index].lstrip()
            if next_line.startswith("\"\"\"") or next_line.startswith("'" * 3):
                # already has a docstring as first statement (race due to parsing), skip
                continue

        lines[insert_index:insert_index] = doc_lines
        added += 1

    return "".join(lines), added


def process_file(path: str) -> int:
    """函数 process_file：处理 path 相关逻辑。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
    except Exception:
        try:
            with open(path, "r", encoding="gbk") as f:
                src = f.read()
        except Exception:
            return 0

    new_src, added = insert_docstrings(src)
    if added > 0 and new_src != src:
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_src)
        except Exception:
            return 0
    return added


def main():
    """函数 main：核心业务逻辑。"""
    files = list_python_files(PROJECT_ROOT)
    total_added = 0
    files_changed = 0
    for p in files:
        added = process_file(p)
        if added > 0:
            total_added += added
            files_changed += 1
    print(f"Files changed: {files_changed}")
    print(f"Docstrings added: {total_added}")


if __name__ == "__main__":
    main()


