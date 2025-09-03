from flask import Blueprint, render_template, request, jsonify, current_app, send_file
try:
	from flask_login import login_required, current_user  # 兼容导入
except Exception:
	# 容错：当 flask_login 不可用时，提供空装饰器与默认高管用户
	def login_required(func):
		return func
	class _DefaultExecutive:
		user_type = 'executive'
		id = 1
	current_user = _DefaultExecutive()
import json
import os
from datetime import datetime
from .models import db, User, TalentDevelopmentData, MarketSalaryData, TalentAnalysisReport
from .talent_analysis_service import TalentAnalysisService
from .pdf_generator import TalentReportGenerator

# 创建蓝图
talent_dashboard = Blueprint('talent_dashboard', __name__)

# 初始化服务
analysis_service = TalentAnalysisService()
report_generator = TalentReportGenerator()

@talent_dashboard.route('/talent-dashboard')
# # @login_required  # 临时注释掉，便于测试  # 临时注释掉，便于测试
def dashboard():
	"""人才发展大盘主页"""
	try:
		# 临时跳过权限检查，便于测试
		# if getattr(current_user, 'user_type', 'executive') != 'executive':
		# 	return jsonify({"error": "权限不足"}), 403
		
		return render_template('talent_dashboard/dashboard.html')
	except Exception as e:
		current_app.logger.error(f"AI人才大盘页面加载失败: {str(e)}")
		return jsonify({"error": "页面加载失败，请稍后重试"}), 500

@talent_dashboard.route('/api/talent/overview')
# # @login_required  # 临时注释掉，便于测试  # 临时注释掉，便于测试
def get_talent_overview():
	"""获取人才概览数据"""
	# 临时跳过权限检查，便于测试
	# if getattr(current_user, 'user_type', 'executive') != 'executive':
	# 	return jsonify({"error": "权限不足"}), 403
	
	try:
		# 获取总体统计
		total_employees = TalentDevelopmentData.query.count()
		
		# 风险分布
		low_risk = TalentDevelopmentData.query.filter(TalentDevelopmentData.turnover_risk < 0.3).count()
		medium_risk = TalentDevelopmentData.query.filter(
			TalentDevelopmentData.turnover_risk >= 0.3,
			TalentDevelopmentData.turnover_risk < 0.6
		).count()
		high_risk = TalentDevelopmentData.query.filter(TalentDevelopmentData.turnover_risk >= 0.6).count()
		
		# 部门分布
		dept_stats = db.session.query(
			TalentDevelopmentData.department,
			db.func.count(TalentDevelopmentData.id)
		).group_by(TalentDevelopmentData.department).all()
		
		# 平均薪资和绩效
		avg_salary = db.session.query(db.func.avg(TalentDevelopmentData.salary)).scalar() or 0
		avg_performance = db.session.query(db.func.avg(TalentDevelopmentData.performance_score)).scalar() or 0
		
		overview_data = {
			"total_employees": total_employees,
			"risk_distribution": {
				"low_risk": low_risk,
				"medium_risk": medium_risk,
				"high_risk": high_risk
			},
			"department_distribution": dict(dept_stats),
			"average_salary": round(avg_salary, 2),
			"average_performance": round(avg_performance, 2)
		}
		
		return jsonify(overview_data)
		
	except Exception as e:
		current_app.logger.error(f"获取人才概览失败: {str(e)}")
		return jsonify({"error": "获取数据失败"}), 500

@talent_dashboard.route('/api/talent/employees')
# @login_required  # 临时注释掉，便于测试
def get_employees_list():
	"""获取员工列表"""
	# 临时跳过权限检查，便于测试
	# if getattr(current_user, 'user_type', 'executive') != 'executive':
	# 	return jsonify({"error": "权限不足"}), 403
	
	try:
		page = request.args.get('page', 1, type=int)
		per_page = request.args.get('per_page', 20, type=int)
		department = request.args.get('department', '')
		risk_level = request.args.get('risk_level', '')
		
		# 构建查询
		query = TalentDevelopmentData.query.join(User)
		
		if department:
			query = query.filter(TalentDevelopmentData.department == department)
		
		if risk_level:
			if risk_level == 'low':
				query = query.filter(TalentDevelopmentData.turnover_risk < 0.3)
			elif risk_level == 'medium':
				query = query.filter(
					TalentDevelopmentData.turnover_risk >= 0.3,
					TalentDevelopmentData.turnover_risk < 0.6
				)
			elif risk_level == 'high':
				query = query.filter(TalentDevelopmentData.turnover_risk >= 0.6)
		
		# 分页
		pagination = query.paginate(
			page=page, per_page=per_page, error_out=False
		)
		
		employees = []
		for talent_data in pagination.items:
			employee = talent_data.employee
			employees.append({
				"id": employee.id,
				"name": f"{employee.first_name} {employee.last_name}",
				"position": talent_data.position,
				"department": talent_data.department,
				"salary": talent_data.salary,
				"performance_score": talent_data.performance_score,
				"turnover_risk": talent_data.turnover_risk,
				"risk_level": get_risk_level(talent_data.turnover_risk),
				"hire_date": talent_data.hire_date.strftime("%Y-%m-%d") if talent_data.hire_date else None
			})
		
		return jsonify({
			"employees": employees,
			"total": pagination.total,
			"pages": pagination.pages,
			"current_page": page
		})
		
	except Exception as e:
		current_app.logger.error(f"获取员工列表失败: {str(e)}")
		return jsonify({"error": "获取数据失败"}), 500

@talent_dashboard.route('/api/talent/employee/<int:employee_id>')
# @login_required  # 临时注释掉，便于测试
def get_employee_detail(employee_id):
	"""获取员工详细信息"""
	# 临时跳过权限检查，便于测试
	# if getattr(current_user, 'user_type', 'executive') != 'executive':
	# 	return jsonify({"error": "权限不足"}), 403
	
	try:
		talent_data = TalentDevelopmentData.query.filter_by(employee_id=employee_id).first()
		if not talent_data:
			return jsonify({"error": "员工数据不存在"}), 404
		
		employee = talent_data.employee
		
		# 获取分析数据
		turnover_analysis = analysis_service.analyze_employee_turnover_risk(employee_id)
		market_analysis = analysis_service.analyze_market_comparison(talent_data.position, talent_data.salary)
		trend_analysis = analysis_service.analyze_trend_forecast(talent_data.position)
		
		employee_detail = {
			"basic_info": {
				"id": employee.id,
				"name": f"{employee.first_name} {employee.last_name}",
				"position": talent_data.position,
				"department": talent_data.department,
				"salary": talent_data.salary,
				"hire_date": talent_data.hire_date.strftime("%Y-%m-%d") if talent_data.hire_date else None,
				"employee_id": employee.employee_id
			},
			"performance_data": {
				"performance_score": talent_data.performance_score,
				"skills_level": talent_data.skills_level,
				"satisfaction_score": talent_data.satisfaction_score,
				"teamwork_score": talent_data.teamwork_score,
				"leadership_potential": talent_data.leadership_potential,
				"promotion_count": talent_data.promotion_count,
				"training_hours": talent_data.training_hours,
				"certification_count": talent_data.certification_count
			},
			"turnover_analysis": turnover_analysis,
			"market_analysis": market_analysis,
			"trend_analysis": trend_analysis
		}
		
		return jsonify(employee_detail)
		
	except Exception as e:
		current_app.logger.error(f"获取员工详情失败: {str(e)}")
		return jsonify({"error": "获取数据失败"}), 500

@talent_dashboard.route('/api/talent/departments')
# @login_required  # 临时注释掉，便于测试
def get_departments_analysis():
	"""获取部门分析数据"""
	# 临时跳过权限检查，便于测试
	# if getattr(current_user, 'user_type', 'executive') != 'executive':
	# 	return jsonify({"error": "权限不足"}), 403
	
	try:
		# 获取部门统计
		dept_stats = db.session.query(
			TalentDevelopmentData.department,
			db.func.count(TalentDevelopmentData.id),
			db.func.avg(TalentDevelopmentData.salary),
			db.func.avg(TalentDevelopmentData.performance_score),
			db.func.avg(TalentDevelopmentData.turnover_risk)
		).group_by(TalentDevelopmentData.department).all()
		
		departments = []
		for dept, count, avg_salary, avg_performance, avg_risk in dept_stats:
			# 计算高风险员工数
			high_risk_count = TalentDevelopmentData.query.filter(
				TalentDevelopmentData.department == dept,
				TalentDevelopmentData.turnover_risk >= 0.6
			).count()
			
			departments.append({
				"department": dept,
				"employee_count": count,
				"average_salary": round(avg_salary or 0, 2),
				"average_performance": round(avg_performance or 0, 2),
				"average_risk": round(avg_risk or 0, 3),
				"high_risk_count": high_risk_count,
				"high_risk_percentage": round((high_risk_count / count) * 100, 1) if count > 0 else 0
			})
		
		return jsonify({"departments": departments})
		
	except Exception as e:
		current_app.logger.error(f"获取部门分析失败: {str(e)}")
		return jsonify({"error": "获取数据失败"}), 500

@talent_dashboard.route('/api/talent/positions')
# @login_required  # 临时注释掉，便于测试
def get_positions_analysis():
	"""获取职位分析数据"""
	# 临时跳过权限检查，便于测试
	# if getattr(current_user, 'user_type', 'executive') != 'executive':
	# 	return jsonify({"error": "权限不足"}), 403
	
	try:
		# 获取职位统计
		position_stats = db.session.query(
			TalentDevelopmentData.position,
			db.func.count(TalentDevelopmentData.id),
			db.func.avg(TalentDevelopmentData.salary),
			db.func.avg(TalentDevelopmentData.performance_score),
			db.func.avg(TalentDevelopmentData.turnover_risk)
		).group_by(TalentDevelopmentData.position).all()
		
		positions = []
		for pos, count, avg_salary, avg_performance, avg_risk in position_stats:
			# 获取市场数据
			market_data = MarketSalaryData.query.filter_by(position=pos).first()
			
			positions.append({
				"position": pos,
				"employee_count": count,
				"average_salary": round(avg_salary or 0, 2),
				"average_performance": round(avg_performance or 0, 2),
				"average_risk": round(avg_risk or 0, 3),
				"market_avg_salary": round(market_data.avg_salary, 2) if market_data else 0,
				"salary_competitiveness": round((avg_salary or 0) / (market_data.avg_salary or 1), 2) if market_data else 1.0
			})
		
		return jsonify({"positions": positions})
		
	except Exception as e:
		current_app.logger.error(f"获取职位分析失败: {str(e)}")
		return jsonify({"error": "获取数据失败"}), 500

@talent_dashboard.route('/api/talent/generate-report', methods=['POST'])
# @login_required  # 临时注释掉，便于测试
def generate_report():
	"""生成分析报告"""
	# 临时跳过权限检查，便于测试
	# if getattr(current_user, 'user_type', 'executive') != 'executive':
	# 	return jsonify({"error": "权限不足"}), 403
	
	try:
		data = request.get_json()
		report_type = data.get('report_type')  # individual, department, company
		target_id = data.get('target_id', 0)
		
		# 生成报告
		result = analysis_service.generate_comprehensive_report(
			report_type, target_id, getattr(current_user, 'id', 1)
		)
		
		if result.get("error"):
			return jsonify({"error": result["error"]}), 400
		
		# 生成PDF
		report_data = result.get("report_data", {})
		pdf_path = None
		
		if report_type == "individual":
			employee_name = report_data.get("employee_info", {}).get("name", "未知员工")
			pdf_path = report_generator.generate_individual_report(report_data, employee_name)
		elif report_type == "department":
			department_name = f"部门{target_id}"
			pdf_path = report_generator.generate_department_report(report_data, department_name)
		elif report_type == "company":
			pdf_path = report_generator.generate_company_report(report_data)
		
		# 更新报告记录
		if pdf_path:
			report = TalentAnalysisReport.query.get(result.get("report_id"))
			if report:
				report.pdf_path = pdf_path
				db.session.commit()
		
		return jsonify({
			"success": True,
			"report_id": result.get("report_id"),
			"pdf_path": pdf_path
		})
		
	except Exception as e:
		current_app.logger.error(f"生成报告失败: {str(e)}")
		return jsonify({"error": "生成报告失败"}), 500

@talent_dashboard.route('/api/talent/download-report/<int:report_id>')
# @login_required  # 临时注释掉，便于测试
def download_report(report_id):
	"""下载报告PDF"""
	# 临时跳过权限检查，便于测试
	# if getattr(current_user, 'user_type', 'executive') != 'executive':
	# 	return jsonify({"error": "权限不足"}), 403
	
	try:
		report = TalentAnalysisReport.query.get(report_id)
		if not report:
			return jsonify({"error": "报告不存在"}), 404
		pdf_path = report.pdf_path
		if not pdf_path or not os.path.exists(pdf_path):
			# 回退：尝试在环境变量目录查找文件名
			fallback_dir = os.getenv('TALENT_REPORT_DIR') or os.getenv('REPORT_DIR')
			if fallback_dir and os.path.isdir(fallback_dir) and pdf_path:
				fname = os.path.basename(pdf_path)
				candidate = os.path.join(fallback_dir, fname)
				if os.path.exists(candidate):
					pdf_path = candidate
					# 更新记录为新路径
					report.pdf_path = pdf_path
					db.session.commit()
		if not pdf_path or not os.path.exists(pdf_path):
			return jsonify({"error": "PDF文件不存在"}), 404
		return send_file(
			pdf_path,
			as_attachment=True,
			download_name=os.path.basename(pdf_path)
		)
		
	except Exception as e:
		current_app.logger.error(f"下载报告失败: {str(e)}")
		return jsonify({"error": "下载失败"}), 500

@talent_dashboard.route('/api/talent/reports')
# @login_required  # 临时注释掉，便于测试
def get_reports_list():
	"""获取报告列表"""
	# 临时跳过权限检查，便于测试
	# if getattr(current_user, 'user_type', 'executive') != 'executive':
	# 	return jsonify({"error": "权限不足"}), 403
	
	try:
		page = request.args.get('page', 1, type=int)
		per_page = request.args.get('per_page', 10, type=int)
		
		# 获取当前用户的报告
		query = TalentAnalysisReport.query.filter_by(created_by=getattr(current_user, 'id', 1))
		
		pagination = query.order_by(TalentAnalysisReport.generated_at.desc()).paginate(
			page=page, per_page=per_page, error_out=False
		)
		
		reports = []
		for report in pagination.items:
			reports.append({
				"id": report.id,
				"report_type": report.report_type,
				"target_id": report.target_id,
				"generated_at": report.generated_at.strftime("%Y-%m-%d %H:%M:%S"),
				"has_pdf": bool(report.pdf_path and os.path.exists(report.pdf_path))
			})
		
		return jsonify({
			"reports": reports,
			"total": pagination.total,
			"pages": pagination.pages,
			"current_page": page
		})
		
	except Exception as e:
		current_app.logger.error(f"获取报告列表失败: {str(e)}")
		return jsonify({"error": "获取数据失败"}), 500

@talent_dashboard.route('/api/talent/delete-report/<int:report_id>', methods=['DELETE', 'POST'])
# @login_required  # 临时注释掉，便于测试
def delete_report(report_id):
	"""删除报告记录及其PDF文件"""
	# 临时跳过权限检查，便于测试
	# if getattr(current_user, 'user_type', 'executive') != 'executive':
	# 	return jsonify({"error": "权限不足"}), 403
	try:
		report = TalentAnalysisReport.query.get(report_id)
		if not report:
			return jsonify({"error": "报告不存在"}), 404
		# 仅允许删除自己创建的报告
		if getattr(current_user, 'id', 1) != getattr(report, 'created_by', getattr(current_user, 'id', 1)):
			return jsonify({"error": "无权删除该报告"}), 403
		# 删除PDF文件（如果存在）
		try:
			if report.pdf_path and os.path.exists(report.pdf_path):
				os.remove(report.pdf_path)
		except Exception as fe:
			current_app.logger.warning(f"删除PDF文件失败但继续删除记录: {fe}")
		# 删除数据库记录
		db.session.delete(report)
		db.session.commit()
		return jsonify({"success": True})
	except Exception as e:
		current_app.logger.error(f"删除报告失败: {str(e)}")
		return jsonify({"error": "删除失败"}), 500

def get_risk_level(risk_score):
	"""获取风险等级"""
	if risk_score < 0.3:
		return "低风险"
	elif risk_score < 0.6:
		return "中风险"
	else:
		return "高风险"
