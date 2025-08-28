#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
表情识别集成测试脚本

用于测试YOLO表情识别模块是否正确集成到candidate_module中
"""

import os
import sys
import logging
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """测试模块导入"""
    try:
        logger.info("测试模块导入...")
        
        # 测试AI配置模块
        from smartrecruit_system.candidate_module.ai_config import get_ai_config
        ai_config = get_ai_config()
        logger.info("✓ AI配置模块导入成功")
        
        # 测试表情识别模块
        from smartrecruit_system.candidate_module.emotion_recognition import get_emotion_recognition_ai
        emotion_ai = get_emotion_recognition_ai()
        logger.info("✓ 表情识别模块导入成功")
        
        # 测试增强的AI分析模块
        from smartrecruit_system.candidate_module.candidate_ai import (
            analyze_candidate_emotion_from_image,
            analyze_interview_performance
        )
        logger.info("✓ 增强AI分析模块导入成功")
        
        return True
        
    except ImportError as e:
        logger.error(f"✗ 模块导入失败: {e}")
        return False
    except Exception as e:
        logger.error(f"✗ 导入过程中发生错误: {e}")
        return False

def test_configuration():
    """测试配置管理"""
    try:
        logger.info("测试配置管理...")
        
        from smartrecruit_system.candidate_module.ai_config import get_ai_config
        ai_config = get_ai_config()
        
        # 检查项目根目录
        logger.info(f"项目根目录: {ai_config.project_root}")
        logger.info(f"YOLO基础路径: {ai_config.yolo_base_path}")
        
        # 检查模型可用性
        models_status = ai_config.check_models_availability()
        logger.info(f"模型状态: {models_status}")
        
        # 检查配置参数
        model_config = ai_config.get_model_config()
        logger.info(f"模型配置: {model_config}")
        
        file_config = ai_config.get_file_config()
        logger.info(f"文件配置: {file_config}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ 配置测试失败: {e}")
        return False

def test_emotion_ai_initialization():
    """测试表情识别AI初始化"""
    try:
        logger.info("测试表情识别AI初始化...")
        
        from smartrecruit_system.candidate_module.emotion_recognition import get_emotion_recognition_ai
        emotion_ai = get_emotion_recognition_ai()
        
        # 检查系统状态
        status = emotion_ai.get_system_status()
        logger.info(f"系统状态: {status}")
        
        # 检查模型加载状态
        models_loaded = status["models_loaded"]
        logger.info(f"模型加载状态: {models_loaded}")
        
        # 检查配置信息
        config = status["config"]
        logger.info(f"配置信息: {config}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ 表情识别AI初始化测试失败: {e}")
        return False

def test_file_validation():
    """测试文件验证功能"""
    try:
        logger.info("测试文件验证功能...")
        
        from smartrecruit_system.candidate_module.ai_config import get_ai_config
        ai_config = get_ai_config()
        
        # 测试图片文件验证
        image_validation = ai_config.validate_file_upload(
            "test.jpg", 1024 * 1024, "image"
        )
        logger.info(f"图片验证结果: {image_validation}")
        
        # 测试视频文件验证
        video_validation = ai_config.validate_file_upload(
            "test.mp4", 50 * 1024 * 1024, "video"
        )
        logger.info(f"视频验证结果: {video_validation}")
        
        # 测试无效文件
        invalid_validation = ai_config.validate_file_upload(
            "test.txt", 1024, "image"
        )
        logger.info(f"无效文件验证结果: {invalid_validation}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ 文件验证测试失败: {e}")
        return False

def test_system_info():
    """测试系统信息获取"""
    try:
        logger.info("测试系统信息获取...")
        
        from smartrecruit_system.candidate_module.ai_config import get_ai_config
        ai_config = get_ai_config()
        
        system_info = ai_config.get_system_info()
        logger.info(f"系统信息: {system_info}")
        
        return True
        
    except Exception as e:
        logger.error(f"✗ 系统信息测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    logger.info("开始运行表情识别集成测试...")
    logger.info("=" * 50)
    
    tests = [
        ("模块导入测试", test_imports),
        ("配置管理测试", test_configuration),
        ("表情识别AI初始化测试", test_emotion_ai_initialization),
        ("文件验证测试", test_file_validation),
        ("系统信息测试", test_system_info)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n运行测试: {test_name}")
        try:
            if test_func():
                logger.info(f"✓ {test_name} 通过")
                passed += 1
            else:
                logger.error(f"✗ {test_name} 失败")
        except Exception as e:
            logger.error(f"✗ {test_name} 异常: {e}")
    
    logger.info("=" * 50)
    logger.info(f"测试完成: {passed}/{total} 通过")
    
    if passed == total:
        logger.info("🎉 所有测试通过！表情识别模块集成成功！")
        return True
    else:
        logger.error("❌ 部分测试失败，请检查配置和依赖")
        return False

def main():
    """主函数"""
    try:
        success = run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        logger.info("测试被用户中断")
        return 1
    except Exception as e:
        logger.error(f"测试过程中发生未预期的错误: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
