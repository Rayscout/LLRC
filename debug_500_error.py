#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试500错误的全面脚本
"""

import os
import sys
import traceback
import requests
from urllib.parse import urljoin

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_flask_app():
    """测试Flask应用"""
    try:
        print("=== 测试Flask应用 ===")
        from app import create_app
        app = create_app()
        print("✅ Flask应用创建成功")
        return app
    except Exception as e:
        print(f"❌ Flask应用创建失败: {e}")
        traceback.print_exc()
        return None

def test_route_with_auth(app):
    """测试带认证的路由"""
    if not app:
        return False
    
    try:
        print("\n=== 测试带认证的路由 ===")
        with app.test_client() as client:
            # 模拟登录会话
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # 假设用户ID为1
                sess['user_type'] = 'candidate'
            
            print("测试 /smartrecruit/candidate/applications/pre_apply/4 (已登录)")
            response = client.get('/smartrecruit/candidate/applications/pre_apply/4')
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 500:
                print("❌ 500错误 - 服务器内部错误")
                print(f"响应内容: {response.data.decode('utf-8', errors='ignore')[:1000]}")
                return False
            elif response.status_code == 200:
                print("✅ 200成功 - 路由工作正常")
                return True
            else:
                print(f"其他状态码: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ 路由测试失败: {e}")
        traceback.print_exc()
        return False

def test_database_models(app):
    """测试数据库模型"""
    if not app:
        return False
    
    try:
        print("\n=== 测试数据库模型 ===")
        with app.app_context():
            from app.models import Job, User, Application
            
            # 测试Job模型
            try:
                jobs = Job.query.limit(1).all()
                print(f"✅ Job模型查询成功，找到 {len(jobs)} 个职位")
                if jobs:
                    job = jobs[0]
                    print(f"   示例职位: ID={job.id}, 标题={job.title}")
            except Exception as e:
                print(f"❌ Job模型查询失败: {e}")
                traceback.print_exc()
            
            # 测试User模型
            try:
                users = User.query.limit(1).all()
                print(f"✅ User模型查询成功，找到 {len(users)} 个用户")
                if users:
                    user = users[0]
                    print(f"   示例用户: ID={user.id}, 邮箱={user.email}")
            except Exception as e:
                print(f"❌ User模型查询失败: {e}")
                traceback.print_exc()
            
            # 测试Application模型
            try:
                apps = Application.query.limit(1).all()
                print(f"✅ Application模型查询成功，找到 {len(apps)} 个申请")
            except Exception as e:
                print(f"❌ Application模型查询失败: {e}")
                traceback.print_exc()
        
        return True
    except Exception as e:
        print(f"❌ 数据库模型测试失败: {e}")
        traceback.print_exc()
        return False

def test_template_rendering(app):
    """测试模板渲染"""
    if not app:
        return False
    
    try:
        print("\n=== 测试模板渲染 ===")
        with app.app_context():
            from flask import render_template
            
            # 测试upload_resume_apply.html
            try:
                from app.models import Job
                job = Job.query.first()
                if job:
                    result = render_template('smartrecruit/candidate/upload_resume_apply.html', job=job)
                    print(f"✅ upload_resume_apply.html 渲染成功，长度: {len(result)}")
                else:
                    print("⚠️ 没有找到职位数据，无法测试模板渲染")
            except Exception as e:
                print(f"❌ upload_resume_apply.html 渲染失败: {e}")
                traceback.print_exc()
            
            # 测试apply_resume.html
            try:
                if job:
                    result = render_template('smartrecruit/candidate/apply_resume.html', 
                                          job=job, 
                                          has_saved_cv=False, 
                                          saved_cv_filename='')
                    print(f"✅ apply_resume.html 渲染成功，长度: {len(result)}")
                else:
                    print("⚠️ 没有找到职位数据，无法测试模板渲染")
            except Exception as e:
                print(f"❌ apply_resume.html 渲染失败: {e}")
                traceback.print_exc()
        
        return True
    except Exception as e:
        print(f"❌ 模板渲染测试失败: {e}")
        traceback.print_exc()
        return False

def test_blueprint_routes(app):
    """测试蓝图路由"""
    if not app:
        return False
    
    try:
        print("\n=== 测试蓝图路由 ===")
        
        # 检查applications蓝图
        if 'smartrecruit.candidate.applications' in app.blueprints:
            print("✅ applications蓝图已注册")
            
            # 获取蓝图对象
            applications_bp = app.blueprints['smartrecruit.candidate.applications']
            
            # 检查路由规则
            routes = []
            for rule in app.url_map.iter_rules():
                if 'applications' in rule.rule:
                    routes.append({
                        'rule': rule.rule,
                        'methods': list(rule.methods),
                        'endpoint': rule.endpoint
                    })
            
            print(f"找到 {len(routes)} 个applications相关路由:")
            for route in routes:
                print(f"  {route['rule']} -> {route['endpoint']} [{', '.join(route['methods'])}]")
        else:
            print("❌ applications蓝图未注册")
        
        return True
    except Exception as e:
        print(f"❌ 蓝图路由测试失败: {e}")
        traceback.print_exc()
        return False

def test_specific_route(app):
    """测试特定的申请路由"""
    if not app:
        return False
    
    try:
        print("\n=== 测试特定申请路由 ===")
        with app.test_client() as client:
            # 测试pre_apply路由
            print("测试 /smartrecruit/candidate/applications/pre_apply/4")
            response = client.get('/smartrecruit/candidate/applications/pre_apply/4')
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 500:
                print("❌ 500错误 - 服务器内部错误")
                print(f"响应内容: {response.data.decode('utf-8', errors='ignore')[:1000]}")
                
                # 尝试获取更详细的错误信息
                try:
                    from flask import current_app
                    with current_app.app_context():
                        print("应用上下文中的错误信息:")
                        # 这里可以添加更多的错误诊断逻辑
                except Exception as e:
                    print(f"无法获取详细错误信息: {e}")
                
                return False
            elif response.status_code == 302:
                print("✅ 302重定向 - 认证问题")
                print(f"重定向到: {response.headers.get('Location', 'Unknown')}")
                return True
            elif response.status_code == 200:
                print("✅ 200成功")
                return True
            else:
                print(f"其他状态码: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ 特定路由测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("开始全面调试500错误...")
    
    # 测试Flask应用创建
    app = test_flask_app()
    
    if app:
        # 测试蓝图路由
        test_blueprint_routes(app)
        
        # 测试数据库模型
        test_database_models(app)
        
        # 测试模板渲染
        test_template_rendering(app)
        
        # 测试特定路由
        test_specific_route(app)
        
        # 测试带认证的路由
        test_route_with_auth(app)
    
    print("\n=== 调试完成 ===")

if __name__ == "__main__":
    main()
