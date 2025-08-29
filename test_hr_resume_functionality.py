#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HR查看候选人简历功能测试脚本

这个脚本用于测试HR模块中新增的简历查看和下载功能。
"""

import os
import sys
import requests
from urllib.parse import urljoin

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_hr_resume_endpoints():
    """测试HR简历相关的API端点"""
    
    # 基础URL（需要根据实际部署情况调整）
    base_url = "http://localhost:5000"
    
    # 测试端点列表
    endpoints = [
        "/smartrecruit/hr/candidates/view_candidate_resume/1",
        "/smartrecruit/hr/candidates/download_candidate_resume/1",
        "/smartrecruit/hr/candidates/preview_candidate_resume/1",
        "/smartrecruit/hr/candidates/get_candidate_info/1"
    ]
    
    print("=== HR简历功能测试 ===\n")
    
    for endpoint in endpoints:
        full_url = urljoin(base_url, endpoint)
        print(f"测试端点: {endpoint}")
        print(f"完整URL: {full_url}")
        
        try:
            # 发送GET请求
            response = requests.get(full_url, timeout=10)
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ 端点可访问")
                if 'application/json' in response.headers.get('content-type', ''):
                    try:
                        data = response.json()
                        print(f"响应数据: {data}")
                    except:
                        print("响应内容: 非JSON格式")
                else:
                    print("响应内容: 非JSON格式")
            elif response.status_code == 401:
                print("❌ 需要认证（这是正常的，未登录用户无法访问）")
            elif response.status_code == 403:
                print("❌ 权限不足（这是正常的，非HR用户无法访问）")
            elif response.status_code == 404:
                print("❌ 端点不存在或候选人不存在")
            else:
                print(f"❌ 其他错误: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ 连接失败 - 请确保Flask应用正在运行")
        except requests.exceptions.Timeout:
            print("❌ 请求超时")
        except Exception as e:
            print(f"❌ 请求失败: {e}")
        
        print("-" * 50)

def test_template_files():
    """测试模板文件是否存在"""
    
    print("=== 模板文件检查 ===\n")
    
    template_files = [
        "app/templates/smartrecruit/hr/view_candidate_resume.html",
        "app/templates/smartrecruit/hr/hr_candidates.html"
    ]
    
    for template_file in template_files:
        file_path = os.path.join(os.path.dirname(__file__), template_file)
        if os.path.exists(file_path):
            print(f"✅ {template_file} - 存在")
        else:
            print(f"❌ {template_file} - 不存在")
    
    print("-" * 50)

def test_python_files():
    """测试Python文件是否存在"""
    
    print("=== Python文件检查 ===\n")
    
    python_files = [
        "smartrecruit_system/hr_module/candidates.py",
        "smartrecruit_system/hr_module/routes.py"
    ]
    
    for python_file in python_files:
        file_path = os.path.join(os.path.dirname(__file__), python_file)
        if os.path.exists(file_path):
            print(f"✅ {python_file} - 存在")
            
            # 检查文件内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 检查关键函数是否存在
                if 'view_candidate_resume' in content:
                    print(f"  ✅ view_candidate_resume 函数存在")
                else:
                    print(f"  ❌ view_candidate_resume 函数不存在")
                    
                if 'download_candidate_resume' in content:
                    print(f"  ✅ download_candidate_resume 函数存在")
                else:
                    print(f"  ❌ download_candidate_resume 函数不存在")
                    
                if 'preview_candidate_resume' in content:
                    print(f"  ✅ preview_candidate_resume 函数存在")
                else:
                    print(f"  ❌ preview_candidate_resume 函数不存在")
                    
            except Exception as e:
                print(f"  ❌ 读取文件失败: {e}")
        else:
            print(f"❌ {python_file} - 不存在")
    
    print("-" * 50)

def test_route_registration():
    """测试路由是否正确注册"""
    
    print("=== 路由注册检查 ===\n")
    
    # 检查routes.py文件
    routes_file = os.path.join(os.path.dirname(__file__), "smartrecruit_system/hr_module/routes.py")
    
    if os.path.exists(routes_file):
        try:
            with open(routes_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if 'candidates_bp' in content:
                print("✅ candidates_bp 蓝图已注册")
            else:
                print("❌ candidates_bp 蓝图未注册")
                
            if 'hr_bp.register_blueprint(candidates_bp)' in content:
                print("✅ candidates_bp 已注册到hr_bp")
            else:
                print("❌ candidates_bp 未注册到hr_bp")
                
        except Exception as e:
            print(f"❌ 读取routes.py失败: {e}")
    else:
        print("❌ routes.py 文件不存在")
    
    print("-" * 50)

def main():
    """主函数"""
    
    print("HR查看候选人简历功能测试")
    print("=" * 50)
    
    # 检查模板文件
    test_template_files()
    
    # 检查Python文件
    test_python_files()
    
    # 检查路由注册
    test_route_registration()
    
    # 测试API端点（需要Flask应用运行）
    print("\n注意: 以下API测试需要Flask应用正在运行")
    print("如果应用未运行，请先启动Flask应用")
    print("=" * 50)
    
    test_hr_resume_endpoints()
    
    print("\n测试完成！")
    print("\n如果所有检查都通过，说明HR简历功能已正确实现。")
    print("如果发现问题，请检查相应的文件内容和配置。")

if __name__ == "__main__":
    main()


