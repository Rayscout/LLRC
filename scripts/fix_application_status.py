#!/usr/bin/env python3
"""
修复申请状态问题
将错误的Withdrawn状态改为正确的状态
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Application, Job, User
from datetime import datetime

def fix_application_status():
    """修复申请状态问题"""
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 开始修复申请状态问题...")
            print("=" * 50)
            
            # 获取所有申请记录
            applications = Application.query.all()
            print(f"找到 {len(applications)} 个申请记录")
            
            fixed_count = 0
            
            for application in applications:
                print(f"\n检查申请 ID: {application.id}")
                print(f"  当前状态: {application.status}")
                print(f"  是否活跃: {application.is_active}")
                
                # 如果状态是Withdrawn但is_active是True，这是不合理的
                if application.status == 'Withdrawn' and application.is_active:
                    print(f"  ⚠️ 发现状态不一致：Withdrawn但活跃")
                    
                    # 根据时间判断应该是什么状态
                    if application.timestamp:
                        time_diff = datetime.utcnow() - application.timestamp
                        days_old = time_diff.days
                        
                        if days_old < 30:  # 30天内的申请设为Pending
                            new_status = 'Pending'
                        else:  # 30天以上的设为Expired
                            new_status = 'Expired'
                        
                        # 更新状态
                        application.status = new_status
                        application.is_active = (new_status == 'Pending')
                        
                        print(f"  ✅ 修复状态: {application.status} -> {new_status}")
                        print(f"  ✅ 更新活跃状态: {application.is_active}")
                        
                        fixed_count += 1
                    else:
                        print(f"  ⚠️ 无法确定时间，保持原状态")
                
                # 如果状态是Pending但is_active是False，这也是不合理的
                elif application.status == 'Pending' and not application.is_active:
                    print(f"  ⚠️ 发现状态不一致：Pending但不活跃")
                    application.is_active = True
                    print(f"  ✅ 修复活跃状态: False -> True")
                    fixed_count += 1
                
                # 如果状态是Submitted但is_active是False，这也是不合理的
                elif application.status == 'Submitted' and not application.is_active:
                    print(f"  ⚠️ 发现状态不一致：Submitted但不活跃")
                    application.is_active = True
                    print(f"  ✅ 修复活跃状态: False -> True")
                    fixed_count += 1
            
            # 提交更改
            if fixed_count > 0:
                db.session.commit()
                print(f"\n🎉 成功修复了 {fixed_count} 个申请记录")
            else:
                print("\n✅ 所有申请记录状态都正确，无需修复")
            
            # 显示修复后的状态
            print("\n修复后的申请状态:")
            print("-" * 30)
            
            applications = Application.query.all()
            for app in applications:
                user = User.query.get(app.user_id)
                job = Job.query.get(app.job_id)
                print(f"申请 {app.id}: {user.first_name} {user.last_name} -> {job.title if job else '未知职位'} (状态: {app.status}, 活跃: {app.is_active})")
            
            return True
            
        except Exception as e:
            print(f"❌ 修复过程中出现错误: {e}")
            db.session.rollback()
            import traceback
            print(f"错误追踪:\n{traceback.format_exc()}")
            return False

def create_test_application():
    """创建一个测试申请来验证功能"""
    app = create_app()
    
    with app.app_context():
        try:
            print("\n🧪 创建测试申请...")
            
            # 获取一个求职者用户
            candidate = User.query.filter_by(is_hr=False).first()
            if not candidate:
                print("❌ 没有找到求职者用户")
                return False
            
            # 获取一个HR发布的职位
            job = Job.query.filter_by(user_id=4).first()
            if not job:
                print("❌ 没有找到HR发布的职位")
                return False
            
            # 检查是否已有申请
            existing = Application.query.filter_by(
                user_id=candidate.id,
                job_id=job.id,
                is_active=True
            ).first()
            
            if existing:
                print(f"⚠️ 已存在申请: ID {existing.id}")
                return True
            
            # 创建新申请
            test_application = Application(
                user_id=candidate.id,
                job_id=job.id,
                status='Pending',
                message='这是一个测试申请，用于验证同步功能',
                is_active=True,
                timestamp=datetime.utcnow()
            )
            
            db.session.add(test_application)
            db.session.commit()
            
            print(f"✅ 测试申请创建成功: ID {test_application.id}")
            print(f"   求职者: {candidate.first_name} {candidate.last_name}")
            print(f"   职位: {job.title}")
            print(f"   状态: {test_application.status}")
            
            return True
            
        except Exception as e:
            print(f"❌ 创建测试申请失败: {e}")
            db.session.rollback()
            return False

def main():
    """主函数"""
    print("申请状态修复工具")
    print("=" * 50)
    
    # 修复申请状态
    if fix_application_status():
        print("\n✅ 申请状态修复完成")
        
        # 创建测试申请
        if create_test_application():
            print("✅ 测试申请创建完成")
        else:
            print("❌ 测试申请创建失败")
    else:
        print("❌ 申请状态修复失败")
    
    print("\n💡 下一步:")
    print("1. 重新启动Flask应用")
    print("2. 以HR用户身份登录")
    print("3. 查看候选人管理页面")
    print("4. 验证申请是否正常显示")

if __name__ == '__main__':
    main()
