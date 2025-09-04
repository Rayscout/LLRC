"""
LLRC Header Start
文件功能: 通用 Python 脚本/模块：scripts/smoke_test_endpoints.py
创建时间: 2025-08-22 14:17
创建人: 张宇成
更新记录:
- 2025-08-26 15:33 by 苏杰
- 2025-08-29 13:25 by 张宇成
- 2025-09-03 11:49 by 张宇成
LLRC Header End
"""
import sys
import json

sys.path.append('.')

from app import create_app


def main() -> None:
    """函数 main：核心业务逻辑。"""
    app = create_app()
    client = app.test_client()

    endpoints = [
        ("GET", "/test"),
        ("GET", "/"),
        ("GET", "/jobs"),
        ("GET", "/talent-dashboard"),
        ("GET", "/api/talent/overview"),
        ("GET", "/api/talent/employees"),
        ("GET", "/api/talent/departments"),
    ]

    results = []
    for method, url in endpoints:
        try:
            resp = client.open(url, method=method)
            results.append({
                "method": method,
                "url": url,
                "status": resp.status_code,
                "ok": 200 <= resp.status_code < 400,
                "content_type": resp.headers.get("Content-Type"),
            })
        except Exception as e:
            results.append({
                "method": method,
                "url": url,
                "status": None,
                "ok": False,
                "error": str(e),
            })

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
