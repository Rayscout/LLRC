"""
LLRC Header Start
文件功能: 通用 Python 脚本/模块：scripts/auto_smoke_all_endpoints.py
创建时间: 2025-08-29 12:09
创建人: 张宇成
更新记录:
- 2025-08-29 12:39 by 侯东杨
LLRC Header End
"""
import sys
import json
import re
from typing import List, Dict, Any

sys.path.append('.')
from app import create_app


def is_public_get_rule(rule) -> bool:
    """函数 is_public_get_rule：处理 rule 相关逻辑。"""
    if 'GET' not in rule.methods:
        return False
    # skip static and favicon
    if rule.rule.startswith('/static') or rule.rule == '/favicon.ico':
        return False
    return True


def guess_min_payload(endpoint: str) -> Dict[str, Any]:
    """函数 guess_min_payload：处理 endpoint 相关逻辑。"""
    # Heuristics for minimal JSON payloads
    if 'generate-report' in endpoint:
        return {"title": "smoke", "filters": {}}
    if endpoint.endswith('/login') or endpoint.endswith('/api/login'):
        return {"email": "hr@test.com", "password": "123456"}
    if 'analysis' in endpoint:
        return {"query": "test"}
    return {}


def main() -> None:
    """函数 main：核心业务逻辑。"""
    app = create_app()
    client = app.test_client()

    # Collect all GET routes
    rules = list(app.url_map.iter_rules())
    get_rules = [r for r in rules if is_public_get_rule(r)]

    results: List[Dict[str, Any]] = []

    # Probe GET endpoints
    for r in sorted(get_rules, key=lambda x: x.rule):
        try:
            resp = client.get(r.rule)
            results.append({
                "method": "GET",
                "url": r.rule,
                "status": resp.status_code,
                "ok": 200 <= resp.status_code < 400,
                "content_type": resp.headers.get("Content-Type"),
            })
        except Exception as e:
            results.append({
                "method": "GET",
                "url": r.rule,
                "status": None,
                "ok": False,
                "error": str(e),
            })

    # Heuristic: test JSON POST endpoints by name
    post_like = [r for r in rules if 'POST' in r.methods and re.search(r'/api/.+|generate-report', r.rule)]
    for r in sorted(post_like, key=lambda x: x.rule):
        payload = guess_min_payload(r.rule)
        try:
            resp = client.post(r.rule, json=payload or {})
            results.append({
                "method": "POST",
                "url": r.rule,
                "status": resp.status_code,
                "ok": 200 <= resp.status_code < 400,
                "content_type": resp.headers.get("Content-Type"),
                "payload_used": payload,
            })
        except Exception as e:
            results.append({
                "method": "POST",
                "url": r.rule,
                "status": None,
                "ok": False,
                "error": str(e),
                "payload_used": payload,
            })

    print(json.dumps({
        "total": len(results),
        "passed": sum(1 for r in results if r.get("ok")),
        "failed": [r for r in results if not r.get("ok")],
        "sample": results[:10],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
