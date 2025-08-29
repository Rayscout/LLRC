#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试AI面试结果审核按钮功能
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_ai_review_button():
    """测试AI面试结果审核按钮功能"""
    
    print("🧪 开始测试AI面试结果审核按钮功能...")
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无头模式
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # 启动浏览器
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        
        # 访问候选人管理页面
        print("1. 访问候选人管理页面...")
        driver.get("http://localhost:5000/smartrecruit/hr/candidates")
        
        # 等待页面加载
        time.sleep(3)
        
        # 检查是否有"审核AI面试结果"按钮
        print("2. 检查'审核AI面试结果'按钮...")
        try:
            ai_review_button = driver.find_element(By.XPATH, "//a[contains(text(), '审核AI面试结果')]")
            print("✅ 找到'审核AI面试结果'按钮")
            
            # 检查按钮样式
            button_class = ai_review_button.get_attribute("class")
            if "ios-btn-ai-review" in button_class:
                print("✅ 按钮样式正确")
            else:
                print("⚠️  按钮样式可能不正确")
            
            # 点击按钮
            print("3. 点击'审核AI面试结果'按钮...")
            ai_review_button.click()
            
            # 等待页面跳转
            time.sleep(3)
            
            # 检查是否跳转到正确的页面
            current_url = driver.current_url
            if "review_all_ai_interviews_global" in current_url:
                print("✅ 成功跳转到AI面试结果审核页面")
                
                # 检查页面标题
                page_title = driver.find_element(By.TAG_NAME, "h1").text
                if "审核AI面试结果" in page_title:
                    print("✅ 页面标题正确")
                else:
                    print("⚠️  页面标题不正确")
                
                # 检查统计信息
                try:
                    stats_section = driver.find_element(By.CLASS_NAME, "stats-section")
                    print("✅ 统计信息区域存在")
                except:
                    print("⚠️  统计信息区域不存在")
                
                # 检查返回按钮
                try:
                    back_button = driver.find_element(By.XPATH, "//a[contains(text(), '返回候选人管理')]")
                    print("✅ 返回按钮存在")
                except:
                    print("⚠️  返回按钮不存在")
                
            else:
                print("❌ 页面跳转失败")
                
        except Exception as e:
            print(f"❌ 未找到'审核AI面试结果'按钮: {e}")
        
        # 关闭浏览器
        driver.quit()
        
        print("\n🎉 AI面试结果审核按钮功能测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    test_ai_review_button()

