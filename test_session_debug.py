#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试会话状态的调试脚本
"""

import os
import sys
import traceback

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_session_flow():
    """测试完整的会话流程"""
    try:
        print("=== 测试完整会话流程 ===")
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            print("1. 初始状态 - 未登录")
            response = client.get('/smartrecruit/candidate/applications/pre_apply/4')
            print(f"   状态码: {response.status_code}")
            if response.status_code == 302:
                print(f"   重定向到: {response.headers.get('Location', 'Unknown')}")
            
            print("\n2. 模拟登录过程")
            # 模拟登录请求
            login_data = {
                'email': 'candidate@test.com',  # 假设的候选人邮箱
                'password': 'password123',      # 假设的密码
                'user_type': 'candidate'
            }
            
            # 先访问登录页面
            response = client.get('/auth/sign')
            print(f"   登录页面状态码: {response.status_code}")
            
            # 模拟POST登录
            response = client.post('/auth/sign', data=login_data, follow_redirects=False)
            print(f"   登录POST状态码: {response.status_code}")
            
            if response.status_code == 302:
                print(f"   登录后重定向到: {response.headers.get('Location', 'Unknown')}")
            
            print("\n3. 检查会话状态")
            with client.session_transaction() as sess:
                print(f"   会话内容: {dict(sess)}")
                user_id = sess.get('user_id')
                user_type = sess.get('user_type')
                print(f"   user_id: {user_id}")
                print(f"   user_type: {user_type}")
            
            print("\n4. 测试已登录状态下的申请路由")
            response = client.get('/smartrecruit/candidate/applications/pre_apply/4')
            print(f"   状态码: {response.status_code}")
            
            if response.status_code == 500:
                print("❌ 500错误 - 分析错误内容...")
                error_content = response.data.decode('utf-8', errors='ignore')
                print(f"   错误响应长度: {len(error_content)}")
                print(f"   错误响应前1000字符: {error_content[:1000]}")
                
                # 检查是否是数据库问题
                if 'database' in error_content.lower() or 'sql' in error_content.lower():
                    print("   可能涉及数据库问题")
                if 'template' in error_content.lower() or 'jinja' in error_content.lower():
                    print("   可能涉及模板问题")
                if 'import' in error_content.lower() or 'module' in error_content.lower():
                    print("   可能涉及模块导入问题")
                    
            elif response.status_code == 200:
                print("✅ 200成功")
                print(f"   响应长度: {len(response.data)}")
            else:
                print(f"   其他状态码: {response.status_code}")
                
    except Exception as e:
        print(f"❌ 会话流程测试失败: {e}")
        traceback.print_exc()

def test_database_connection():
    """测试数据库连接"""
    try:
        print("\n=== 测试数据库连接 ===")
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from app.models import db, User, Job
            
            # 测试基本连接
            try:
                result = db.session.execute("SELECT 1")
                print("✅ 数据库基本连接正常")
            except Exception as e:
                print(f"❌ 数据库基本连接失败: {e}")
                return False
            
            # 测试User表
            try:
                users = User.query.limit(3).all()
                print(f"✅ User表查询成功，找到 {len(users)} 个用户")
                for user in users:
                    print(f"   用户ID: {user.id}, 邮箱: {user.email}, 类型: {getattr(user, 'user_type', 'N/A')}")
            except Exception as e:
                print(f"❌ User表查询失败: {e}")
                traceback.print_exc()
            
            # 测试Job表
            try:
                jobs = Job.query.limit(3).all()
                print(f"✅ Job表查询成功，找到 {len(jobs)} 个职位")
                for job in jobs:
                    print(f"   职位ID: {job.id}, 标题: {job.title}, 公司: {getattr(job, 'company_name', 'N/A')}")
            except Exception as e:
                print(f"❌ Job表查询失败: {e}")
                traceback.print_exc()
                
    except Exception as e:
        print(f"❌ 数据库连接测试失败: {e}")
        traceback.print_exc()

def test_blueprint_registration():
    """测试蓝图注册"""
    try:
        print("\n=== 测试蓝图注册 ===")
        from app import create_app
        app = create_app()
        
        # 检查applications蓝图
        if 'smartrecruit.candidate.applications' in app.blueprints:
            print("✅ applications蓝图已注册")
            
            # 获取蓝图对象
            applications_bp = app.blueprints['smartrecruit.candidate.applications']
            print(f"   蓝图名称: {applications_bp.name}")
            print(f"   URL前缀: {applications_bp.url_prefix}")
            
            # 检查路由
            routes = []
            for rule in app.url_map.iter_rules():
                if 'applications' in rule.rule and 'pre_apply' in rule.rule:
                    routes.append({
                        'rule': rule.rule,
                        'methods': list(rule.methods),
                        'endpoint': rule.endpoint
                    })
            
            print(f"   找到 {len(routes)} 个pre_apply相关路由:")
            for route in routes:
                print(f"     {route['rule']} -> {route['endpoint']} [{', '.join(route['methods'])}]")
        else:
            print("❌ applications蓝图未注册")
            
    except Exception as e:
        print(f"❌ 蓝图注册测试失败: {e}")
        traceback.print_exc()

def main():
    """主函数"""
    print("开始测试会话状态...")
    
    # 测试蓝图注册
    test_blueprint_registration()
    
    # 测试数据库连接
    test_database_connection()
    
    # 测试会话流程
    test_session_flow()
    
    print("\n=== 会话状态测试完成 ===")

if __name__ == "__main__":
    main()
