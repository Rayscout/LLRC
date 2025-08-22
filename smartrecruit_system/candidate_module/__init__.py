# 统一从 routes 导出含首页的 candidate_bp，避免重复定义导致路由缺失
from .routes import candidate_bp  # noqa: F401
