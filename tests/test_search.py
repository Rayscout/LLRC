#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_search_api():
    """测试智能搜索API"""
    base_url = "http://localhost:5000"
    
    print("=== 智能搜索功能测试 ===")
    
    # 测试推荐职位API
    print("\n1. 测试推荐职位API...")
    try:
        response = requests.get(f"{base_url}/api/recommend_jobs", timeout=10)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                jobs = data.get('jobs', [])
                skills = data.get('user_skills', [])
                print(f"✅ 成功获取 {len(jobs)} 个推荐职位")
                print(f"📋 用户技能: {skills}")
                
                for i, job in enumerate(jobs[:3], 1):
                    print(f"  {i}. {job['title']} - {job['company_name']} (匹配度: {job['match_score']}%)")
            else:
                print(f"❌ 获取推荐失败: {data.get('message')}")
        else:
            print(f"❌ API调用失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    # 测试搜索职位API
    print("\n2. 测试搜索职位API...")
    try:
        search_data = {
            "query": "python",
            "location": "",
            "salary_min": 0,
            "salary_max": 999999,
            "job_type": "",
            "experience_level": ""
        }
        
        response = requests.post(
            f"{base_url}/api/search_jobs",
            json=search_data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                jobs = data.get('jobs', [])
                print(f"✅ 搜索成功，找到 {len(jobs)} 个职位")
                
                for i, job in enumerate(jobs[:3], 1):
                    print(f"  {i}. {job['title']} - {job['company_name']} (匹配度: {job['match_score']}%)")
            else:
                print(f"❌ 搜索失败: {data.get('message')}")
        else:
            print(f"❌ API调用失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 测试失败: {e}")
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    test_search_api()
