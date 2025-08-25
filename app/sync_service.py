"""
数据同步服务
用于HR端和求职者端之间的数据同步
"""
import logging
from datetime import datetime
from flask import current_app
from .models import db, Job, Application, User
from . import applications_collection

logger = logging.getLogger(__name__)

class DataSyncService:
    """数据同步服务类"""
    
    @staticmethod
    def sync_job_to_candidates(job_id):
        """
        同步HR发布的职位到求职者端
        当HR发布、更新或删除职位时调用
        """
        try:
            job = Job.query.get(job_id)
            if not job:
                logger.warning(f"职位 {job_id} 不存在，无法同步")
                return False
            
            # 记录同步日志
            logger.info(f"开始同步职位 {job_id} ({job.title}) 到求职者端")
            
            # 这里可以添加其他同步逻辑，比如：
            # 1. 发送通知给匹配的求职者
            # 2. 更新推荐系统
            # 3. 同步到其他系统
            
            # 记录同步状态
            job.last_synced = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"职位 {job_id} 同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步职位 {job_id} 失败: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def sync_application_to_hr(application_id):
        """
        同步求职者的申请到HR端
        当求职者提交申请时调用
        """
        try:
            application = Application.query.get(application_id)
            if not application:
                logger.warning(f"申请 {application_id} 不存在，无法同步")
                return False
            
            # 获取相关数据
            user = User.query.get(application.user_id)
            job = Job.query.get(application.job_id)
            
            if not user or not job:
                logger.warning(f"申请 {application_id} 的相关数据不完整，无法同步")
                return False
            
            # 记录同步日志
            logger.info(f"开始同步申请 {application_id} (用户: {user.email}, 职位: {job.title}) 到HR端")
            
            # 同步到MongoDB（如果配置了的话）
            try:
                if applications_collection is not None:
                    # 检查是否已存在
                    existing = applications_collection.find_one({
                        'user_id': str(application.user_id),
                        'job_id': str(application.job_id)
                    })
                    
                    if existing:
                        # 更新现有记录
                        applications_collection.update_one(
                            {'user_id': str(application.user_id), 'job_id': str(application.job_id)},
                            {
                                '$set': {
                                    'status': application.status,
                                    'message': application.message,
                                    'timestamp': application.timestamp,
                                    'is_active': application.is_active,
                                    'last_updated': datetime.utcnow()
                                }
                            }
                        )
                    else:
                        # 创建新记录
                        applications_collection.insert_one({
                            'user_id': str(application.user_id),
                            'job_id': str(application.job_id),
                            'status': application.status,
                            'message': application.message,
                            'timestamp': application.timestamp,
                            'is_active': application.is_active,
                            'user_info': {
                                'first_name': user.first_name,
                                'last_name': user.last_name,
                                'email': user.email,
                                'phone_number': user.phone_number,
                                'cv_file': user.cv_file,
                                'profile_photo': user.profile_photo
                            },
                            'job_info': {
                                'title': job.title,
                                'company_name': job.company_name,
                                'location': job.location,
                                'department': job.department
                            },
                            'created_at': datetime.utcnow(),
                            'last_updated': datetime.utcnow()
                        })
                        
                    logger.info(f"申请 {application_id} 已同步到MongoDB")
                    
            except Exception as e:
                logger.warning(f"同步到MongoDB失败: {e}")
            
            # 记录同步状态
            application.last_synced = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"申请 {application_id} 同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步申请 {application_id} 失败: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def sync_cv_update_to_hr(user_id):
        """
        同步求职者简历更新到HR端
        当求职者更新简历时调用
        """
        try:
            user = User.query.get(user_id)
            if not user:
                logger.warning(f"用户 {user_id} 不存在，无法同步简历")
                return False
            
            # 记录同步日志
            logger.info(f"开始同步用户 {user_id} ({user.email}) 的简历更新到HR端")
            
            # 同步到MongoDB
            try:
                if applications_collection is not None:
                    # 更新所有相关申请记录中的用户信息
                    applications_collection.update_many(
                        {'user_id': str(user_id)},
                        {
                            '$set': {
                                'user_info': {
                                    'first_name': user.first_name,
                                    'last_name': user.last_name,
                                    'email': user.email,
                                    'phone_number': user.phone_number,
                                    'cv_file': user.cv_file,
                                    'profile_photo': user.profile_photo,
                                    'skills': user.skills,
                                    'education': user.education,
                                    'experience': user.experience
                                },
                                'cv_last_updated': datetime.utcnow()
                            }
                        }
                    )
                    
                    logger.info(f"用户 {user_id} 的简历信息已同步到MongoDB")
                    
            except Exception as e:
                logger.warning(f"同步简历到MongoDB失败: {e}")
            
            # 记录同步状态
            user.cv_last_synced = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"用户 {user_id} 的简历同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步用户 {user_id} 简历失败: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def sync_application_status_update(application_id):
        """
        同步申请状态更新
        当HR更新申请状态时调用
        """
        try:
            application = Application.query.get(application_id)
            if not application:
                logger.warning(f"申请 {application_id} 不存在，无法同步状态")
                return False
            
            # 记录同步日志
            logger.info(f"开始同步申请 {application_id} 状态更新: {application.status}")
            
            # 同步到MongoDB
            try:
                if applications_collection:
                    applications_collection.update_one(
                        {'user_id': str(application.user_id), 'job_id': str(application.job_id)},
                        {
                            '$set': {
                                'status': application.status,
                                'message': application.message,
                                'last_updated': datetime.utcnow(),
                                'status_updated_at': datetime.utcnow()
                            }
                        }
                    )
                    
                    logger.info(f"申请 {application_id} 状态已同步到MongoDB")
                    
            except Exception as e:
                logger.warning(f"同步状态到MongoDB失败: {e}")
            
            # 记录同步状态
            application.last_synced = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"申请 {application_id} 状态同步完成")
            return True
            
        except Exception as e:
            logger.error(f"同步申请 {application_id} 状态失败: {e}")
            db.session.rollback()
            return False
    
    @staticmethod
    def get_sync_status():
        """
        获取数据同步状态
        """
        try:
            # 统计各表的同步状态
            total_jobs = Job.query.count()
            synced_jobs = Job.query.filter(Job.last_synced.isnot(None)).count()
            
            total_applications = Application.query.count()
            synced_applications = Application.query.filter(Application.last_synced.isnot(None)).count()
            
            total_users = User.query.count()
            synced_users = User.query.filter(User.cv_last_synced.isnot(None)).count()
            
            return {
                'jobs': {
                    'total': total_jobs,
                    'synced': synced_jobs,
                    'sync_rate': round((synced_jobs / total_jobs * 100) if total_jobs > 0 else 0, 2)
                },
                'applications': {
                    'total': total_applications,
                    'synced': synced_applications,
                    'sync_rate': round((synced_applications / total_applications * 100) if total_applications > 0 else 0, 2)
                },
                'users': {
                    'total': total_users,
                    'synced': synced_users,
                    'sync_rate': round((synced_users / total_users * 100) if total_users > 0 else 0, 2)
                },
                'last_sync': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"获取同步状态失败: {e}")
            return {
                'error': str(e),
                'last_sync': datetime.utcnow().isoformat()
            }
    
    @staticmethod
    def force_sync_all():
        """
        强制同步所有数据
        """
        try:
            logger.info("开始强制同步所有数据")
            
            # 同步所有职位
            jobs = Job.query.all()
            for job in jobs:
                DataSyncService.sync_job_to_candidates(job.id)
            
            # 同步所有申请
            applications = Application.query.all()
            for app in applications:
                DataSyncService.sync_application_to_hr(app.id)
            
            # 同步所有用户简历
            users = User.query.filter(User.cv_file.isnot(None)).all()
            for user in users:
                DataSyncService.sync_cv_update_to_hr(user.id)
            
            logger.info("强制同步所有数据完成")
            return True
            
        except Exception as e:
            logger.error(f"强制同步所有数据失败: {e}")
            return False
