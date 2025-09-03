#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度调试500错误的脚本
"""

import os
import sys
import traceback
import logging

# 设置详细日志
logging.basicConfig(level=logging.DEBUG)

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_with_real_session():
    """测试真实的用户会话"""
    try:
        print("=== 测试真实用户会话 ===")
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # 模拟真实的登录会话
            with client.session_transaction() as sess:
                sess['user_id'] = 1  # 假设用户ID为1
                sess['user_type'] = 'candidate'
            
            print("✅ 模拟登录会话成功")
            
            # 测试pre_apply路由
            print("\n测试 /smartrecruit/candidate/applications/pre_apply/4")
            response = client.get('/smartrecruit/candidate/applications/pre_apply/4')
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 500:
                print("❌ 500错误 - 服务器内部错误")
                print(f"响应内容: {response.data.decode('utf-8', errors='ignore')[:2000]}")
                
                # 尝试获取更详细的错误信息
                try:
                    # 检查是否有错误日志
                    print("\n检查应用日志...")
                    with app.app_context():
                        from flask import current_app
                        print(f"应用名称: {current_app.name}")
                        print(f"调试模式: {current_app.debug}")
                        
                        # 检查数据库连接
                        try:
                            from app.models import db
                            db.session.execute("SELECT 1")
                            print("✅ 数据库连接正常")
                        except Exception as e:
                            print(f"❌ 数据库连接问题: {e}")
                            
                except Exception as e:
                    print(f"无法获取详细错误信息: {e}")
                
                return False
            elif response.status_code == 200:
                print("✅ 200成功 - 路由工作正常")
                print(f"响应内容长度: {len(response.data)}")
                return True
            else:
                print(f"其他状态码: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ 真实会话测试失败: {e}")
        traceback.print_exc()
        return False

def test_database_schema():
    """测试数据库架构"""
    try:
        print("\n=== 测试数据库架构 ===")
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from app.models import db
            
            # 检查application表结构
            try:
                result = db.session.execute("PRAGMA table_info(application)")
                columns = result.fetchall()
                print(f"✅ application表结构检查成功，找到 {len(columns)} 列:")
                
                for col in columns:
                    print(f"  {col[1]} ({col[2]}) - 默认值: {col[4]}")
                    
                # 检查是否有缺失的列
                required_columns = [
                    'id', 'user_id', 'job_id', 'message', 'timestamp', 
                    'status', 'is_active'
                ]
                
                existing_columns = [col[1] for col in columns]
                missing_columns = [col for col in required_columns if col not in existing_columns]
                
                if missing_columns:
                    print(f"⚠️ 缺失的必需列: {missing_columns}")
                else:
                    print("✅ 所有必需列都存在")
                    
            except Exception as e:
                print(f"❌ 表结构检查失败: {e}")
                traceback.print_exc()
                
    except Exception as e:
        print(f"❌ 数据库架构测试失败: {e}")
        traceback.print_exc()

def test_job_data():
    """测试职位数据"""
    try:
        print("\n=== 测试职位数据 ===")
        from app import create_app
        app = create_app()
        
        with app.app_context():
            from app.models import Job
            
            # 检查职位ID=4是否存在
            try:
                job = Job.query.get(4)
                if job:
                    print(f"✅ 职位ID=4存在: {job.title}")
                    print(f"   公司: {job.company_name}")
                    print(f"   地点: {job.location}")
                else:
                    print("❌ 职位ID=4不存在")
                    # 列出所有可用的职位
                    jobs = Job.query.limit(5).all()
                    print(f"可用的职位: {[(j.id, j.title) for j in jobs]}")
                    
            except Exception as e:
                print(f"❌ 职位查询失败: {e}")
                traceback.print_exc()
                
    except Exception as e:
        print(f"❌ 职位数据测试失败: {e}")
        traceback.print_exc()

def test_template_rendering_with_context():
    """测试带上下文的模板渲染"""
    try:
        print("\n=== 测试带上下文的模板渲染 ===")
        from app import create_app
        app = create_app()
        
        with app.test_request_context('/test'):
            with app.app_context():
                from flask import render_template
                from app.models import Job
                
                # 获取一个职位
                job = Job.query.first()
                if not job:
                    print("❌ 没有找到职位数据")
                    return False
                
                print(f"使用职位: ID={job.id}, 标题={job.title}")
                
                # 测试upload_resume_apply.html
                try:
                    result = render_template('smartrecruit/candidate/upload_resume_apply.html', job=job)
                    print(f"✅ upload_resume_apply.html 渲染成功，长度: {len(result)}")
                except Exception as e:
                    print(f"❌ upload_resume_apply.html 渲染失败: {e}")
                    traceback.print_exc()
                
                # 测试apply_resume.html
                try:
                    result = render_template('smartrecruit/candidate/apply_resume.html', 
                                          job=job, 
                                          has_saved_cv=False, 
                                          saved_cv_filename='')
                    print(f"✅ apply_resume.html 渲染成功，长度: {len(result)}")
                except Exception as e:
                    print(f"❌ apply_resume.html 渲染失败: {e}")
                    traceback.print_exc()
                    
    except Exception as e:
        print(f"❌ 模板渲染测试失败: {e}")
        traceback.print_exc()

def test_route_with_error_handling():
    """测试带错误处理的路由"""
    try:
        print("\n=== 测试带错误处理的路由 ===")
        from app import create_app
        app = create_app()
        
        with app.test_client() as client:
            # 模拟登录会话
            with client.session_transaction() as sess:
                sess['user_id'] = 1
                sess['user_type'] = 'candidate'
            
            # 测试pre_apply路由，捕获详细错误
            try:
                response = client.get('/smartrecruit/candidate/applications/pre_apply/4')
                print(f"状态码: {response.status_code}")
                
                if response.status_code == 500:
                    print("❌ 500错误 - 分析错误内容...")
                    
                    # 尝试解析错误响应
                    error_content = response.data.decode('utf-8', errors='ignore')
                    print(f"错误响应长度: {len(error_content)}")
                    print(f"错误响应前500字符: {error_content[:500]}")
                    
                    # 检查是否是HTML错误页面
                    if '<html' in error_content.lower():
                        print("错误响应包含HTML内容")
                        if 'traceback' in error_content.lower():
                            print("包含Python traceback信息")
                        if 'error' in error_content.lower():
                            print("包含错误信息")
                    else:
                        print("错误响应不包含HTML内容")
                        
                elif response.status_code == 200:
                    print("✅ 200成功")
                    print(f"响应长度: {len(response.data)}")
                else:
                    print(f"其他状态码: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ 路由测试异常: {e}")
                traceback.print_exc()
                
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        traceback.print_exc()

def main():
    """主函数"""
    print("开始深度调试500错误...")
    
    # 测试真实会话
    test_with_real_session()
    
    # 测试数据库架构
    test_database_schema()
    
    # 测试职位数据
    test_job_data()
    
    # 测试模板渲染
    test_template_rendering_with_context()
    
    # 测试错误处理
    test_route_with_error_handling()
    
    print("\n=== 深度调试完成 ===")

if __name__ == "__main__":
    main()
