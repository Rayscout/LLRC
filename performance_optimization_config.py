#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
面试安排功能性能优化配置
"""

# MongoDB连接优化配置
MONGO_OPTIMIZATION_CONFIG = {
    'max_time_ms': 3000,  # 查询超时时间（毫秒）
    'max_pool_size': 10,  # 连接池大小
    'min_pool_size': 1,   # 最小连接数
    'max_idle_time_ms': 30000,  # 连接最大空闲时间
    'server_selection_timeout_ms': 5000,  # 服务器选择超时
    'connect_timeout_ms': 2000,  # 连接超时
    'socket_timeout_ms': 3000,   # Socket超时
}

# 缓存配置
CACHE_CONFIG = {
    'ai_candidates_ttl': 300,  # AI候选人缓存时间（秒）
    'interview_details_ttl': 180,  # 面试详情缓存时间（秒）
    'max_cache_size': 1000,  # 最大缓存条目数
}

# 查询限制配置
QUERY_LIMITS = {
    'max_candidates_per_page': 50,  # 每页最大候选人数
    'max_feedback_per_candidate': 10,  # 每个候选人最大反馈数
    'max_interview_schedules': 100,  # 最大面试安排数
}

# 性能监控配置
PERFORMANCE_MONITORING = {
    'enable_query_logging': True,  # 启用查询日志
    'enable_performance_metrics': True,  # 启用性能指标
    'slow_query_threshold_ms': 1000,  # 慢查询阈值（毫秒）
}

# 降级策略配置
FALLBACK_STRATEGIES = {
    'mongo_fallback_enabled': True,  # 启用MongoDB降级策略
    'cache_fallback_enabled': True,  # 启用缓存降级策略
    'default_ai_status': False,  # MongoDB失败时的默认AI状态
}

def get_mongo_optimization_config():
    """获取MongoDB优化配置"""
    return MONGO_OPTIMIZATION_CONFIG

def get_cache_config():
    """获取缓存配置"""
    return CACHE_CONFIG

def get_query_limits():
    """获取查询限制配置"""
    return QUERY_LIMITS

def get_performance_monitoring_config():
    """获取性能监控配置"""
    return PERFORMANCE_MONITORING

def get_fallback_strategies():
    """获取降级策略配置"""
    return FALLBACK_STRATEGIES



