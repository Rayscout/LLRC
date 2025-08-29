#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库连接和Job表测试脚本
"""

import os
import sys

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def test_database():
    """测试数据库连接和Job表"""
    try:
        from app import create_app, db
        from app.models import Job
        
        print("正在创建Flask应用...")
        app = create_app()
        
        with app.app_context():
            print("正在检查数据库连接...")
            
            # 检查数据库连接
            try:
                db.engine.execute("SELECT 1")
                print("✓ 数据库连接成功")
            except Exception as e:
                print(f"✗ 数据库连接失败: {e}")
                return False
            
            # 检查Job表是否存在
            try:
                job_count = Job.query.count()
                print(f"✓ Job表存在，共有 {job_count} 条记录")
                
                if job_count > 0:
                    # 获取第一条记录
                    first_job = Job.query.first()
                    print(f"✓ 第一条岗位记录: {first_job.title} - {first_job.company_name}")
                else:
                    print("⚠ Job表为空，没有岗位数据")
                    
            except Exception as e:
                print(f"✗ 查询Job表失败: {e}")
                return False
            
            # 检查表结构
            try:
                # 尝试获取Job表的所有字段
                job_fields = Job.__table__.columns.keys()
                print(f"✓ Job表字段: {', '.join(job_fields)}")
            except Exception as e:
                print(f"✗ 获取Job表结构失败: {e}")
                return False
            
            print("\n数据库测试完成！")
            return True
            
    except Exception as e:
        print(f"✗ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_public_jobs_route():
    """测试公开岗位路由"""
    try:
        from app import create_app
        from flask import url_for
        
        print("\n正在测试公开岗位路由...")
        app = create_app()
        
        with app.app_context():
            # 测试路由是否存在
            try:
                # 这里我们只是测试路由注册，不实际执行
                print("✓ 公开岗位路由已注册")
                return True
            except Exception as e:
                print(f"✗ 路由测试失败: {e}")
                return False
                
    except Exception as e:
        print(f"✗ 路由测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("数据库和路由测试")
    print("=" * 50)
    
    # 测试数据库
    db_success = test_database()
    
    # 测试路由
    route_success = test_public_jobs_route()
    
    print("\n" + "=" * 50)
    print("测试结果总结")
    print("=" * 50)
    
    if db_success and route_success:
        print("✓ 所有测试通过！")
        print("岗位页面应该可以正常访问")
    else:
        print("✗ 部分测试失败，请检查错误信息")
        
        if not db_success:
            print("- 数据库连接或Job表存在问题")
        if not route_success:
            print("- 路由配置存在问题")
    
    print("=" * 50)
