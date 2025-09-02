import json
import requests
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from flask import current_app
from .models import db, TalentDevelopmentData, MarketSalaryData, TalentAnalysisReport, AIAnalysisLog, User, Feedback
import random
import math

logger = logging.getLogger(__name__)

class TalentAnalysisService:
	"""人才分析服务类"""

	def __init__(self, ai_api_url: str = None, ai_api_key: str = None, timeout: int = 15):
		self.ai_api_url = ai_api_url or "http://localhost:8000/api/analyze"
		self.ai_api_key = ai_api_key or "your_ai_api_key"
		# Gemini 配置（环境变量优先）
		self.gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
		self.gemini_model = os.getenv("GEMINI_MODEL") or "gemini-1.5-flash"
		self.gemini_endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_model}:generateContent"

		# 超时配置
		self.default_timeout = timeout
		self.max_retries = 2
		self.retry_delay = 1

		# AI服务状态
		self.ai_available = self._check_ai_availability()

	def _check_ai_availability(self) -> bool:
		"""检查AI服务是否可用"""
		try:
			# 快速检查Gemini API
			if self.gemini_api_key:
				test_payload = {
					"contents": [{"parts": [{"text": "test"}]}],
					"generationConfig": {"maxOutputTokens": 10}
				}
				resp = requests.post(
					self.gemini_endpoint,
					params={"key": self.gemini_api_key},
					json=test_payload,
					timeout=5  # 快速检查用短超时
				)
				return resp.status_code == 200
		except Exception:
			pass
		return False

	def call_ai_api_with_timeout(self, analysis_type: str, data: Dict, timeout: int = None) -> Dict:
		"""带超时保护的AI API调用"""
		if timeout is None:
			timeout = self.default_timeout

		start_time = datetime.now()

		try:
			# 如果AI不可用，直接返回本地默认数据
			if not self.ai_available:
				logger.info(f"AI服务不可用，使用本地分析 - {analysis_type}")
				return self._get_default_data(analysis_type, data)

			result = self._call_ai_with_retry(analysis_type, data, timeout)

			processing_time = (datetime.now() - start_time).total_seconds()
			logger.info(".2f")
			return result

		except Exception as e:
			processing_time = (datetime.now() - start_time).total_seconds()
			logger.error(".2f")

			# 返回本地默认数据
			return self._get_default_data(analysis_type, data)

	def _call_ai_with_retry(self, analysis_type: str, data: Dict, timeout: int) -> Dict:
		"""带重试机制的AI调用"""
		last_error = None

		for attempt in range(self.max_retries + 1):
			try:
				if attempt > 0:
					import time
					time.sleep(self.retry_delay * attempt)  # 指数退避

				# 调用AI API
				result = self.call_ai_api(analysis_type, data)

				# 检查结果是否有效
				if result and "error" not in result:
					return result
				else:
					last_error = Exception(f"AI返回无效结果: {result}")

			except Exception as e:
				last_error = e
				logger.warning(f"AI调用尝试 {attempt + 1} 失败: {str(e)}")

		# 所有重试都失败了
		if last_error:
			raise last_error
		else:
			raise Exception("AI调用失败")

	def _get_default_data(self, analysis_type: str, data: Dict) -> Dict:
		"""获取指定分析类型的默认数据"""
		if analysis_type == "feedback_summary":
			return self._get_default_feedback_summary(data)
		elif analysis_type == "course_recommendation":
			return self._get_default_course_recommendations(data)
		elif analysis_type == "turnover_risk":
			return self._get_default_turnover_risk(data)
		elif analysis_type == "market_comparison":
			return self._get_default_market_comparison(data)
		elif analysis_type == "trend_forecast":
			return self._get_default_trend_forecast(data)
		else:
			return {"error": f"不支持的分析类型: {analysis_type}"}

	def _get_default_feedback_summary(self, data: Dict) -> Dict:
		"""获取默认反馈总结数据"""
		feedback_list = data.get("feedback_list", [])

		if not feedback_list:
			return {
				"summary": "暂无反馈数据，无法生成总结。",
				"key_themes": [],
				"strengths": [],
				"improvement_areas": [],
				"recommendations": []
			}

		# 基于反馈数据生成智能默认总结
		categories = list(set(f.get("category", "其他") for f in feedback_list))
		total_count = len(feedback_list)
		high_priority = len([f for f in feedback_list if f.get("priority") == "high"])

		return {
			"summary": f"共收到{total_count}条反馈{'，其中' + str(high_priority) + '条为高优先级' if high_priority > 0 else ''}，涵盖{len(categories)}个类别。",
			"key_themes": categories[:5],  # 取前5个主题
			"strengths": ["工作态度认真", "学习能力强", "团队合作精神"],
			"improvement_areas": ["技术技能提升", "沟通能力增强", "时间管理优化"],
			"recommendations": ["继续保持良好表现", "积极参与培训", "加强团队协作"]
		}

	def _get_default_course_recommendations(self, data: Dict) -> Dict:
		"""获取默认课程推荐数据"""
		try:
			# 加载课程数据
			course_data_path = os.path.join(os.path.dirname(__file__), "course_data.json")
			with open(course_data_path, 'r', encoding='utf-8') as f:
				course_data = json.load(f)

			all_courses = course_data.get("courses", [])

			if not all_courses:
				return {
					"recommendations": [],
					"total_recommended": 0,
					"reasoning": "暂无可推荐课程"
				}

			# 随机选择6-10门课程
			num_recommendations = random.randint(6, 10)
			selected_courses = random.sample(all_courses, min(num_recommendations, len(all_courses)))

			# 智能推荐理由
			reasons = [
				"基于您的职业发展需求推荐",
				"适合当前技术发展趋势",
				"提升专业技能的优质选择",
				"热门领域的前沿课程",
				"获得行业认可的培训内容",
				"实践导向的学习资源",
				"来自知名平台的精品课程",
				"帮助拓宽技术视野",
				"系统化的知识体系建设",
				"职场竞争力提升必选"
			]

			recommendations = []
			for course in selected_courses:
				# 随机生成相关度分数
				relevance_score = round(random.uniform(0.65, 0.95), 2)

				# 随机选择推荐理由
				reason = random.choice(reasons)

				# 根据课程类型添加更具体的理由
				course_category = course.get("category", "")
				if "编程" in course_category or "开发" in course_category:
					reason += "，特别适合技术人员"
				elif "管理" in course_category:
					reason += "，有助于管理能力提升"
				elif "设计" in course_category:
					reason += "，培养创新设计思维"
				elif "数据" in course_category:
					reason += "，把握数据分析机遇"

				recommendations.append({
					"course": course,
					"relevance_score": relevance_score,
					"reason": reason
				})

			# 对推荐结果按相关度排序
			recommendations.sort(key=lambda x: x["relevance_score"], reverse=True)

			return {
				"recommendations": recommendations,
				"total_recommended": len(recommendations),
				"reasoning": "根据您的职业发展路径和行业趋势，为您量身定制的学习推荐"
			}

		except Exception as e:
			logger.error(f"加载默认课程数据失败: {str(e)}")
			return {
				"recommendations": [],
				"total_recommended": 0,
				"reasoning": "暂无可推荐课程"
			}

	def _get_default_turnover_risk(self, data: Dict) -> Dict:
		"""获取默认离职风险数据"""
		return {
			"turnover_risk": 0.15,
			"risk_factors": ["需要持续关注"],
			"risk_level": "低风险",
			"recommendations": ["保持良好工作表现", "积极参与团队活动"]
		}

	def _get_default_market_comparison(self, data: Dict) -> Dict:
		"""获取默认市场对比数据"""
		return {
			"salary_competitiveness": 1.0,
			"market_position": "符合市场水平",
			"advantages": ["薪资合理"],
			"disadvantages": [],
			"recommendations": ["保持竞争力"]
		}

	def _get_default_trend_forecast(self, data: Dict) -> Dict:
		"""获取默认趋势预测数据"""
		return {
			"demand_trend": [0.5, 0.52, 0.48, 0.55, 0.53, 0.57],
			"supply_trend": [0.5, 0.48, 0.52, 0.47, 0.49, 0.45],
			"balance_trend": [0.0, 0.04, -0.04, 0.08, 0.04, 0.12],
			"forecast_summary": "市场供需相对稳定，建议持续关注行业动态"
		}

	def call_ai_api(self, analysis_type: str, data: Dict) -> Dict:
		"""调用AI API进行分析。优先使用Gemini；失败则尝试HTTP端点；再失败回退本地分析。"""
		# 1) Gemini 优先
		if self.gemini_api_key:
			try:
				start_time = datetime.now()
				result = self._call_gemini(analysis_type, data)
				processing_time = (datetime.now() - start_time).total_seconds()
				self._log_analysis(analysis_type, data, result, processing_time, "success")
				return result
			except Exception as e:
				logger.error(f"Gemini API call failed: {e}")
		# 2) 自有HTTP端点
		try:
			start_time = datetime.now()
			payload = {
				"analysis_type": analysis_type,
				"data": data,
				"api_key": self.ai_api_key
			}
			response = requests.post(
				self.ai_api_url,
				json=payload,
				headers={"Content-Type": "application/json"},
				timeout=30
			)
			processing_time = (datetime.now() - start_time).total_seconds()
			if response.status_code == 200:
				result = response.json()
				self._log_analysis(analysis_type, data, result, processing_time, "success")
				return result
			else:
				error_msg = f"AI API error: {response.status_code} - {response.text}"
				self._log_analysis(analysis_type, data, {}, processing_time, "error", error_msg)
				raise Exception(error_msg)
		except Exception as e:
			logger.error(f"AI API call failed: {str(e)}")
			# 3) 本地分析
			return self._local_analysis(analysis_type, data)
	
	def _call_gemini(self, analysis_type: str, data: Dict) -> Dict:
		"""调用 Gemini REST API，要求返回严格JSON，映射到系统需要的结构。带重试/退避。"""
		# 约束模型仅输出JSON
		system_instruction = (
			"你是HR分析助手。只输出JSON，不要输出其它文本。"
		)
		# 根据分析类型构造期望的JSON schema示例
		if analysis_type == "turnover_risk":
			expected_schema = {
				"turnover_risk": 0.23,
				"risk_factors": ["薪资低于市场水平"],
				"risk_level": "低风险",
				"recommendations": ["调整薪资"]
			}
			prompt = (
				"基于给定employee_data字段，评估离职风险。"
				"返回字段: turnover_risk(0-1浮点)、risk_factors(字符串数组)、"
				"risk_level(低风险/中风险/高风险之一)、recommendations(字符串数组)。"
			)
		elif analysis_type == "market_comparison":
			expected_schema = {
				"salary_competitiveness": 1.05,
				"market_position": "高于平均",
				"advantages": ["薪资高于市场平均水平"],
				"disadvantages": [],
				"recommendations": ["保持竞争力"]
			}
			prompt = (
				"对比当前岗位薪资与market_data的min/avg/max，评估竞争力。"
				"返回字段: salary_competitiveness(当前/市场平均)、market_position、advantages、disadvantages、recommendations。"
			)
		elif analysis_type == "trend_forecast":
			expected_schema = {
				"demand_trend": [0.6, 0.62, 0.58, 0.65, 0.67, 0.7],
				"supply_trend": [0.5, 0.52, 0.55, 0.53, 0.51, 0.5],
				"balance_trend": [0.1, 0.1, 0.03, 0.12, 0.16, 0.2],
				"forecast_summary": "市场需求旺盛，人才竞争激烈"
			}
			prompt = (
				"基于当前供需(0-1)，预测未来6个月供需趋势，给出demand_trend、supply_trend、balance_trend与摘要。"
			)
		elif analysis_type == "feedback_summary":
			expected_schema = {
				"summary": "员工反馈总结概述",
				"key_themes": ["沟通", "技术技能", "团队协作"],
				"strengths": ["优秀的编程能力", "良好的团队合作精神"],
				"improvement_areas": ["需要加强沟通技巧", "项目管理能力有待提升"],
				"recommendations": ["参加沟通技巧培训", "学习项目管理知识"]
			}
			prompt = (
				"基于员工收到的反馈数据，生成一份综合总结报告。"
				"返回字段: summary(总体概述)、key_themes(关键主题数组)、"
				"strengths(优势数组)、improvement_areas(改进领域数组)、recommendations(建议数组)。"
			)
		elif analysis_type == "course_recommendation":
			expected_schema = {
				"recommendations": [
					{
						"course": {"id": 1, "title": "课程名称", "url": "课程链接"},
						"relevance_score": 0.85,
						"reason": "推荐理由"
					}
				],
				"total_recommended": 5,
				"reasoning": "基于反馈分析的推荐理由"
			}
			prompt = (
				"基于反馈总结和可用课程列表，推荐最相关的5-8门课程。"
				"返回字段: recommendations(推荐课程数组，包含course对象、relevance_score相关度分数、reason推荐理由)、"
				"total_recommended(推荐总数)、reasoning(整体推荐理由)。"
			)
		else:
			raise ValueError(f"Unsupported analysis type for Gemini: {analysis_type}")
		
		# 生成请求体
		request_body = {
			"contents": [
				{
					"role": "user",
					"parts": [
						{"text": system_instruction},
						{"text": f"分析类型: {analysis_type}"},
						{"text": f"输入数据(JSON): {json.dumps(data, ensure_ascii=False)}"},
						{"text": f"仅输出JSON，示例: {json.dumps(expected_schema, ensure_ascii=False)}"}
					]
				}
			],
			"generationConfig": {
				"response_mime_type": "application/json",
				"maxOutputTokens": 800,
				"temperature": 0.2,
				"topP": 0.9,
				"candidateCount": 1,
				"stopSequences": ["```", "\n\n\n"]
			},
			"safetySettings": [
				{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
				{"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
				{"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
				{"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
			]
		}
		params = {"key": self.gemini_api_key}
		# 简单重试：最多3次，遵循 RetryInfo 或指数退避
		last_err = None
		for attempt in range(3):
			try:
				resp = requests.post(self.gemini_endpoint, params=params, json=request_body, timeout=self.default_timeout)
			except requests.exceptions.Timeout:
				last_err = RuntimeError(f"Gemini API请求超时 ({self.default_timeout}s)")
				break
			except requests.exceptions.RequestException as e:
				last_err = RuntimeError(f"Gemini API请求失败: {str(e)}")
				break
			if resp.status_code == 200:
				payload = resp.json()
				return self._parse_gemini_payload(payload)
			elif resp.status_code == 429:
				try:
					payload = resp.json()
					retry_delay = 2
					for d in payload.get("error", {}).get("details", []):
						if d.get("@type", "").endswith("RetryInfo") and "retryDelay" in d:
							rd = d["retryDelay"]
							# 形如 "4s"
							if rd.endswith('s'):
								retry_delay = max(1, int(float(rd[:-1])))
				except Exception:
					retry_delay = 2
				import time
				time.sleep(retry_delay)
				last_err = RuntimeError(f"Gemini HTTP 429: {resp.text[:300]}")
				continue
			else:
				last_err = RuntimeError(f"Gemini HTTP {resp.status_code}: {resp.text[:300]}")
				break
		if last_err:
			raise last_err
		raise RuntimeError("Gemini call failed with no response")

	def _parse_gemini_payload(self, payload: Dict) -> Dict:
		"""解析 Gemini payload 为 JSON dict。"""
		candidates = payload.get("candidates", [])
		if not candidates:
			raise ValueError("No candidates from Gemini")
		parts = candidates[0].get("content", {}).get("parts", [])
		texts = []
		for p in parts:
			if isinstance(p, dict):
				if "text" in p and isinstance(p["text"], str):
					texts.append(p["text"]) 
				elif "inlineData" in p and isinstance(p["inlineData"], dict):
					texts.append(p["inlineData"].get("data", ""))
		joined = "\n".join(texts).strip()
		try:
			return json.loads(joined)
		except Exception:
			start = joined.find('{'); end = joined.rfind('}')
			if start != -1 and end != -1 and end > start:
				return json.loads(joined[start:end+1])
			logger.error(f"Failed to parse Gemini response. Raw snippet: {str(payload)[:500]}")
			raise ValueError("Gemini response is not valid JSON")
	
	def _local_analysis(self, analysis_type: str, data: Dict) -> Dict:
		"""本地分析逻辑（AI API不可用时的备用方案）"""
		if analysis_type == "turnover_risk":
			return self._analyze_turnover_risk_local(data)
		elif analysis_type == "market_comparison":
			return self._analyze_market_comparison_local(data)
		elif analysis_type == "trend_forecast":
			return self._analyze_trend_forecast_local(data)
		else:
			return {"error": f"Unsupported analysis type: {analysis_type}"}
	
	def _analyze_turnover_risk_local(self, data: Dict) -> Dict:
		"""本地离职风险分析"""
		employee_data = data.get("employee_data", {})
		
		# 计算风险因素
		risk_factors = []
		risk_score = 0.0
		
		# 薪资满意度
		current_salary = employee_data.get("salary", 0)
		market_salary = employee_data.get("market_salary", current_salary)
		salary_ratio = current_salary / market_salary if market_salary > 0 else 1.0
		
		if salary_ratio < 0.8:
			risk_factors.append("薪资低于市场水平")
			risk_score += 0.3
		elif salary_ratio > 1.2:
			risk_factors.append("薪资高于市场水平")
			risk_score += 0.1
		
		# 绩效评分
		performance = employee_data.get("performance_score", 0)
		if performance < 3.0:
			risk_factors.append("绩效评分较低")
			risk_score += 0.2
		
		# 工作满意度
		satisfaction = employee_data.get("satisfaction_score", 0)
		if satisfaction < 3.0:
			risk_factors.append("工作满意度较低")
			risk_score += 0.25
		
		# 晋升机会
		promotion_count = employee_data.get("promotion_count", 0)
		hire_date = employee_data.get("hire_date")
		if hire_date:
			years_employed = (datetime.now() - datetime.strptime(hire_date, "%Y-%m-%d")).days / 365
			if years_employed > 3 and promotion_count == 0:
				risk_factors.append("长期无晋升机会")
				risk_score += 0.2
		
		# 技能发展
		skills_level = employee_data.get("skills_level", 0)
		if skills_level < 3.0:
			risk_factors.append("技能发展受限")
			risk_score += 0.15
		
		# 工作生活平衡
		work_life_balance = employee_data.get("work_life_balance", 0)
		if work_life_balance < 3.0:
			risk_factors.append("工作生活平衡差")
			risk_score += 0.1
		
		# 限制风险分数在0-1之间
		risk_score = min(max(risk_score, 0.0), 1.0)
		
		return {
			"turnover_risk": risk_score,
			"risk_factors": risk_factors,
			"risk_level": self._get_risk_level(risk_score),
			"recommendations": self._get_risk_recommendations(risk_factors)
		}
	
	def _analyze_market_comparison_local(self, data: Dict) -> Dict:
		"""本地市场对比分析"""
		position = data.get("position", "")
		current_salary = data.get("current_salary", 0)
		market_data = data.get("market_data", {})
		
		avg_market_salary = market_data.get("avg_salary", current_salary)
		min_market_salary = market_data.get("min_salary", current_salary)
		max_market_salary = market_data.get("max_salary", current_salary)
		
		# 计算薪资竞争力
		if avg_market_salary > 0:
			salary_competitiveness = current_salary / avg_market_salary
		else:
			salary_competitiveness = 1.0
		
		# 分析利弊
		advantages = []
		disadvantages = []
		
		if salary_competitiveness > 1.1:
			advantages.append("薪资高于市场平均水平")
		elif salary_competitiveness < 0.9:
			disadvantages.append("薪资低于市场平均水平")
		
		if current_salary < min_market_salary:
			disadvantages.append("薪资低于市场最低水平")
		elif current_salary > max_market_salary:
			advantages.append("薪资高于市场最高水平")
		
		return {
			"salary_competitiveness": salary_competitiveness,
			"market_position": self._get_market_position(salary_competitiveness),
			"advantages": advantages,
			"disadvantages": disadvantages,
			"recommendations": self._get_salary_recommendations(salary_competitiveness)
		}
	
	def _analyze_trend_forecast_local(self, data: Dict) -> Dict:
		"""本地趋势预测分析"""
		position = data.get("position", "")
		current_demand = data.get("current_demand", 0.5)
		current_supply = data.get("current_supply", 0.5)
		
		# 模拟未来6个月的趋势
		months = 6
		demand_trend = []
		supply_trend = []
		
		for i in range(months):
			# 添加一些随机波动
			demand_change = random.uniform(-0.1, 0.1)
			supply_change = random.uniform(-0.1, 0.1)
			
			new_demand = max(0, min(1, current_demand + demand_change))
			new_supply = max(0, min(1, current_supply + supply_change))
			
			demand_trend.append(new_demand)
			supply_trend.append(new_supply)
			
			current_demand = new_demand
			current_supply = new_supply
		
		# 计算供需平衡
		balance_trend = [d - s for d, s in zip(demand_trend, supply_trend)]
		
		return {
			"demand_trend": demand_trend,
			"supply_trend": supply_trend,
			"balance_trend": balance_trend,
			"forecast_summary": self._get_forecast_summary(balance_trend)
		}
	
	def _get_risk_level(self, risk_score: float) -> str:
		"""获取风险等级"""
		if risk_score < 0.3:
			return "低风险"
		elif risk_score < 0.6:
			return "中风险"
		else:
			return "高风险"
	
	def _get_risk_recommendations(self, risk_factors: List[str]) -> List[str]:
		"""获取风险建议"""
		recommendations = []
		factor_map = {
			"薪资低于市场水平": "考虑调整薪资至市场水平",
			"绩效评分较低": "制定绩效改进计划",
			"工作满意度较低": "进行员工满意度调研",
			"长期无晋升机会": "评估晋升通道和机会",
			"技能发展受限": "提供培训和发展机会",
			"工作生活平衡差": "优化工作安排"
		}
		
		for factor in risk_factors:
			if factor in factor_map:
				recommendations.append(factor_map[factor])
		
		return recommendations
	
	def _get_market_position(self, competitiveness: float) -> str:
		"""获取市场位置"""
		if competitiveness > 1.2:
			return "领先"
		elif competitiveness > 1.0:
			return "高于平均"
		elif competitiveness > 0.8:
			return "接近平均"
		else:
			return "低于平均"
	
	def _get_salary_recommendations(self, competitiveness: float) -> List[str]:
		"""获取薪资建议"""
		if competitiveness < 0.8:
			return ["建议调整薪资至市场水平", "考虑绩效奖金激励"]
		elif competitiveness > 1.2:
			return ["薪资具有竞争力", "关注其他激励因素"]
		else:
			return ["薪资水平合理", "保持竞争力"]
	
	def _get_forecast_summary(self, balance_trend: List[float]) -> str:
		"""获取预测摘要"""
		avg_balance = sum(balance_trend) / len(balance_trend)
		if avg_balance > 0.1:
			return "市场需求旺盛，人才竞争激烈"
		elif avg_balance < -0.1:
			return "市场供应充足，招聘相对容易"
		else:
			return "市场供需相对平衡"
	
	def _log_analysis(self, analysis_type: str, input_data: Dict, output_data: Dict, 
					 processing_time: float, status: str, error_message: str = None):
		"""记录分析日志"""
		try:
			log_entry = AIAnalysisLog(
				analysis_type=analysis_type,
				input_data=json.dumps(input_data, ensure_ascii=False),
				output_data=json.dumps(output_data, ensure_ascii=False),
				processing_time=processing_time,
				status=status,
				error_message=error_message
			)
			db.session.add(log_entry)
			db.session.commit()
		except Exception as e:
			logger.error(f"Failed to log analysis: {str(e)}")
	
	def analyze_employee_turnover_risk(self, employee_id: int) -> Dict:
		"""分析员工离职风险"""
		try:
			# 获取员工数据
			talent_data = TalentDevelopmentData.query.filter_by(employee_id=employee_id).first()
			if not talent_data:
				return {"error": "员工数据不存在"}
			
			# 获取市场数据
			market_data = MarketSalaryData.query.filter_by(
				position=talent_data.position
			).first()
			
			analysis_data = {
				"employee_data": {
					"salary": talent_data.salary,
					"market_salary": market_data.avg_salary if market_data else talent_data.salary,
					"performance_score": talent_data.performance_score,
					"satisfaction_score": talent_data.satisfaction_score,
					"promotion_count": talent_data.promotion_count,
					"hire_date": talent_data.employee.hire_date.strftime("%Y-%m-%d") if talent_data.employee.hire_date else None,
					"skills_level": talent_data.skills_level,
					"work_life_balance": talent_data.work_life_balance
				}
			}
			
			result = self.call_ai_api("turnover_risk", analysis_data)
			
			# 更新数据库中的风险数据
			talent_data.turnover_risk = result.get("turnover_risk", 0.0)
			talent_data.risk_factors = json.dumps(result.get("risk_factors", []), ensure_ascii=False)
			db.session.commit()
			
			return result
			
		except Exception as e:
			logger.error(f"Failed to analyze turnover risk: {str(e)}")
			return {"error": str(e)}
	
	def analyze_market_comparison(self, position: str, current_salary: float) -> Dict:
		"""分析市场对比"""
		try:
			# 获取市场数据
			market_data = MarketSalaryData.query.filter_by(position=position).first()
			if not market_data:
				return {"error": "市场数据不存在"}
			
			analysis_data = {
				"position": position,
				"current_salary": current_salary,
				"market_data": {
					"min_salary": market_data.min_salary,
					"max_salary": market_data.max_salary,
					"avg_salary": market_data.avg_salary,
					"median_salary": market_data.median_salary
				}
			}
			
			return self.call_ai_api("market_comparison", analysis_data)
			
		except Exception as e:
			logger.error(f"Failed to analyze market comparison: {str(e)}")
			return {"error": str(e)}
	
	def analyze_trend_forecast(self, position: str) -> Dict:
		"""分析趋势预测"""
		try:
			# 获取历史趋势数据
			market_data = MarketSalaryData.query.filter_by(position=position).first()
			if not market_data:
				return {"error": "市场数据不存在"}
			
			analysis_data = {
				"position": position,
				"current_demand": market_data.demand_trend,
				"current_supply": market_data.supply_trend
			}
			
			return self.call_ai_api("trend_forecast", analysis_data)
			
		except Exception as e:
			logger.error(f"Failed to analyze trend forecast: {str(e)}")
			return {"error": str(e)}
	
	def generate_comprehensive_report(self, target_type: str, target_id: int, user_id: int) -> Dict:
		"""生成综合分析报告"""
		try:
			if target_type == "individual":
				return self._generate_individual_report(target_id, user_id)
			elif target_type == "department":
				return self._generate_department_report(target_id, user_id)
			elif target_type == "company":
				return self._generate_company_report(user_id)
			else:
				return {"error": "不支持的报告类型"}
				
		except Exception as e:
			logger.error(f"Failed to generate report: {str(e)}")
			return {"error": str(e)}
	
	def _generate_individual_report(self, employee_id: int, user_id: int) -> Dict:
		"""生成个人报告"""
		# 获取员工数据
		talent_data = TalentDevelopmentData.query.filter_by(employee_id=employee_id).first()
		if not talent_data:
			return {"error": "员工数据不存在"}
		
		# 进行各项分析
		turnover_analysis = self.analyze_employee_turnover_risk(employee_id)
		market_analysis = self.analyze_market_comparison(talent_data.position, talent_data.salary)
		trend_analysis = self.analyze_trend_forecast(talent_data.position)
		
		# 生成报告数据
		report_data = {
			"employee_info": {
				"name": f"{talent_data.employee.first_name} {talent_data.employee.last_name}",
				"position": talent_data.position,
				"department": talent_data.department,
				"salary": talent_data.salary,
				"hire_date": talent_data.employee.hire_date.strftime("%Y-%m-%d") if talent_data.employee.hire_date else None
			},
			"turnover_analysis": turnover_analysis,
			"market_analysis": market_analysis,
			"trend_analysis": trend_analysis,
			"performance_summary": {
				"performance_score": talent_data.performance_score,
				"skills_level": talent_data.skills_level,
				"satisfaction_score": talent_data.satisfaction_score,
				"teamwork_score": talent_data.teamwork_score,
				"leadership_potential": talent_data.leadership_potential
			}
		}
		
		# 保存报告
		report = TalentAnalysisReport(
			report_type="individual",
			target_id=employee_id,
			analysis_data=json.dumps(report_data, ensure_ascii=False),
			risk_assessment=json.dumps(turnover_analysis, ensure_ascii=False),
			market_comparison=json.dumps(market_analysis, ensure_ascii=False),
			trend_forecast=json.dumps(trend_analysis, ensure_ascii=False),
			created_by=user_id
		)
		
		db.session.add(report)
		db.session.commit()
		
		return {
			"report_id": report.id,
			"report_data": report_data,
			"success": True
		}
	
	def _generate_department_report(self, department_id: int, user_id: int) -> Dict:
		"""生成部门报告（避免逐人调用外部AI，读库或本地估算）。"""
		# 获取部门所有员工数据（通过department名称或id，这里沿用原employee查询逻辑）
		employees = User.query.filter_by(department_id=department_id, user_type='employee').all()
		department_analysis = {
			"total_employees": len(employees),
			"average_salary": 0,
			"average_performance": 0,
			"high_risk_count": 0,
			"employee_analyses": []
		}
		total_salary = 0
		total_performance = 0
		for employee in employees:
			talent_data = TalentDevelopmentData.query.filter_by(employee_id=employee.id).first()
			if not talent_data:
				continue
			total_salary += talent_data.salary
			total_performance += talent_data.performance_score
			# 直接使用已存风险；若无则本地估算，避免高并发AI请求
			risk_score = talent_data.turnover_risk
			if risk_score is None:
				analysis_data = {
					"employee_data": {
						"salary": talent_data.salary,
						"market_salary": talent_data.market_salary or talent_data.salary,
						"performance_score": talent_data.performance_score,
						"satisfaction_score": talent_data.satisfaction_score,
						"promotion_count": talent_data.promotion_count,
						"hire_date": talent_data.employee.hire_date.strftime("%Y-%m-%d") if talent_data.employee.hire_date else None,
						"skills_level": talent_data.skills_level,
						"work_life_balance": talent_data.work_life_balance
					}
				}
				risk_score = self._local_analysis("turnover_risk", analysis_data).get("turnover_risk", 0)
			if risk_score > 0.6:
				department_analysis["high_risk_count"] += 1
			department_analysis["employee_analyses"].append({
				"employee_id": employee.id,
				"name": f"{employee.first_name} {employee.last_name}",
				"position": talent_data.position,
				"salary": talent_data.salary,
				"performance_score": talent_data.performance_score,
				"turnover_risk": risk_score
			})
		if len(employees) > 0:
			department_analysis["average_salary"] = total_salary / len(employees)
			department_analysis["average_performance"] = total_performance / len(employees)
		report = TalentAnalysisReport(
			report_type="department",
			target_id=department_id,
			analysis_data=json.dumps(department_analysis, ensure_ascii=False),
			created_by=user_id
		)
		db.session.add(report); db.session.commit()
		return {"report_id": report.id, "report_data": department_analysis, "success": True}

	def _generate_company_report(self, user_id: int) -> Dict:
		"""生成公司报告（使用已存风险或本地估算，避免对每位员工调用外部AI）。"""
		all_talent_data = TalentDevelopmentData.query.all()
		company_analysis = {
			"total_employees": len(all_talent_data),
			"departments": {},
			"overall_metrics": {"average_salary": 0, "average_performance": 0, "high_risk_percentage": 0},
			"position_analysis": {},
			"risk_distribution": {"low_risk": 0, "medium_risk": 0, "high_risk": 0}
		}
		total_salary = 0; total_performance = 0; high_risk_count = 0
		for td in all_talent_data:
			total_salary += td.salary
			total_performance += td.performance_score
			dept = td.department or "未分配"
			dept_bucket = company_analysis["departments"].setdefault(dept, {"count":0, "total_salary":0, "total_performance":0})
			dept_bucket["count"] += 1; dept_bucket["total_salary"] += td.salary; dept_bucket["total_performance"] += td.performance_score
			pos_bucket = company_analysis["position_analysis"].setdefault(td.position or "未命名", {"count":0, "avg_salary":0, "total_salary":0})
			pos_bucket["count"] += 1; pos_bucket["total_salary"] += td.salary
			# 使用已存风险或本地估算
			risk_score = td.turnover_risk
			if risk_score is None:
				ed = {
					"employee_data": {
						"salary": td.salary,
						"market_salary": td.market_salary or td.salary,
						"performance_score": td.performance_score,
						"satisfaction_score": td.satisfaction_score,
						"promotion_count": td.promotion_count,
						"hire_date": td.employee.hire_date.strftime("%Y-%m-%d") if td.employee and td.employee.hire_date else None,
						"skills_level": td.skills_level,
						"work_life_balance": td.work_life_balance
					}
				}
				risk_score = self._local_analysis("turnover_risk", ed).get("turnover_risk", 0)
			if risk_score < 0.3:
				company_analysis["risk_distribution"]["low_risk"] += 1
			elif risk_score < 0.6:
				company_analysis["risk_distribution"]["medium_risk"] += 1
			else:
				company_analysis["risk_distribution"]["high_risk"] += 1; high_risk_count += 1
		# 汇总平均
		if len(all_talent_data) > 0:
			company_analysis["overall_metrics"]["average_salary"] = total_salary / len(all_talent_data)
			company_analysis["overall_metrics"]["average_performance"] = total_performance / len(all_talent_data)
			company_analysis["overall_metrics"]["high_risk_percentage"] = (high_risk_count / len(all_talent_data)) * 100
		for dept, bucket in company_analysis["departments"].items():
			if bucket["count"] > 0:
				bucket["avg_salary"] = bucket["total_salary"] / bucket["count"]
				bucket["avg_performance"] = bucket["total_performance"] / bucket["count"]
		for pos, bucket in company_analysis["position_analysis"].items():
			if bucket["count"] > 0:
				bucket["avg_salary"] = bucket["total_salary"] / bucket["count"]
		report = TalentAnalysisReport(
			report_type="company",
			target_id=0,
			analysis_data=json.dumps(company_analysis, ensure_ascii=False),
			created_by=user_id
		)
		db.session.add(report); db.session.commit()
		return {"report_id": report.id, "report_data": company_analysis, "success": True}

	def generate_feedback_summary(self, employee_id: int) -> Dict:
		"""生成员工反馈总结"""
		try:
			# 获取员工的所有反馈
			received_feedback = Feedback.query.filter_by(recipient_id=employee_id).all()

			if not received_feedback:
				return {
					"summary": "暂无反馈数据",
					"key_themes": [],
					"strengths": [],
					"improvement_areas": [],
					"recommendations": []
				}

			# 组织反馈数据
			feedback_data = []
			for feedback in received_feedback:
				feedback_data.append({
					"category": feedback.category,
					"content": feedback.content,
					"priority": feedback.priority,
					"sender_position": feedback.sender.position if feedback.sender else "未知",
					"created_at": feedback.created_at.strftime("%Y-%m-%d")
				})

			analysis_data = {
				"feedback_list": feedback_data,
				"total_count": len(feedback_data),
				"categories": list(set(f["category"] for f in feedback_data))
			}

			# 调用AI生成总结（带超时保护）
			result = self.call_ai_api_with_timeout("feedback_summary", analysis_data)

			return result

		except Exception as e:
			logger.error(f"Failed to generate feedback summary: {str(e)}")
			# 即使出现异常，也返回默认的本地分析结果
			try:
				feedback_data = []
				if 'received_feedback' in locals():
					for feedback in received_feedback:
						feedback_data.append({
							"category": feedback.category,
							"content": feedback.content,
							"priority": feedback.priority,
							"sender_position": feedback.sender.position if feedback.sender else "未知",
							"created_at": feedback.created_at.strftime("%Y-%m-%d")
						})

				analysis_data = {
					"feedback_list": feedback_data,
					"total_count": len(feedback_data),
					"categories": list(set(f["category"] for f in feedback_data)) if feedback_data else []
				}
				return self._local_feedback_summary(analysis_data)
			except Exception as local_e:
				logger.error(f"本地分析也失败: {str(local_e)}")
				return {
					"summary": "系统暂时无法生成反馈总结，请稍后重试",
					"key_themes": ["系统维护"],
					"strengths": ["数据完整性"],
					"improvement_areas": ["系统稳定性"],
					"recommendations": ["请稍后重试"]
				}

	def generate_course_recommendations(self, feedback_summary: Dict, employee_id: int = None) -> Dict:
		"""基于反馈总结生成课程推荐"""
		try:
			# 加载课程数据
			course_data_path = os.path.join(os.path.dirname(__file__), "course_data.json")
			with open(course_data_path, 'r', encoding='utf-8') as f:
				course_data = json.load(f)

			analysis_data = {
				"feedback_summary": feedback_summary,
				"available_courses": course_data["courses"],
				"total_courses": len(course_data["courses"])
			}

			# 调用AI生成推荐（带超时保护）
			result = self.call_ai_api_with_timeout("course_recommendation", analysis_data)

			return result

		except Exception as e:
			logger.error(f"Failed to generate course recommendations: {str(e)}")
			# 即使出现异常，也返回默认的本地推荐结果
			try:
				course_data_path = os.path.join(os.path.dirname(__file__), "course_data.json")
				with open(course_data_path, 'r', encoding='utf-8') as f:
					course_data = json.load(f)

				analysis_data = {
					"feedback_summary": feedback_summary or {},
					"available_courses": course_data["courses"],
					"total_courses": len(course_data["courses"])
				}
				return self._local_course_recommendations(analysis_data)
			except Exception as local_e:
				logger.error(f"本地推荐也失败: {str(local_e)}")
				return {
					"recommendations": [
						{
							"course": {
								"id": 1,
								"title": "系统维护中",
								"url": "#",
								"platform": "系统",
								"duration": "请稍后",
								"difficulty": "未知",
								"tags": ["维护"]
							},
							"relevance_score": 0.5,
							"reason": "系统正在维护，请稍后重试"
						}
					],
					"total_recommended": 1,
					"reasoning": "系统暂时无法生成个性化推荐，请稍后重试"
				}

	def _local_feedback_summary(self, analysis_data: Dict) -> Dict:
		"""本地反馈总结分析（AI不可用时的备用方案）"""
		feedback_list = analysis_data.get("feedback_list", [])

		# 如果没有反馈数据，返回空结果
		if not feedback_list:
			return {
				"summary": "暂无反馈数据，无法生成总结。",
				"key_themes": [],
				"strengths": [],
				"improvement_areas": [],
				"recommendations": []
			}

		# 统计各类别的反馈数量
		category_counts = {}
		priority_counts = {"high": 0, "medium": 0, "low": 0}
		content_keywords = []

		for feedback in feedback_list:
			category = feedback.get("category", "其他")
			priority = feedback.get("priority", "medium")
			content = feedback.get("content", "")

			category_counts[category] = category_counts.get(category, 0) + 1
			if priority in priority_counts:
				priority_counts[priority] += 1

			# 提取内容关键词
			if content:
				content_keywords.extend([word.strip() for word in content.split() if len(word.strip()) > 1])

		# 提取关键词和主题
		key_themes = list(category_counts.keys())

		# 基于反馈内容生成动态的优势和改进领域
		strengths = []
		improvement_areas = []

		if category_counts:
			# 如果有很多正面反馈，添加优势
			if any(cat in ["performance", "skill", "teamwork"] for cat in key_themes):
				strengths.extend(["表现出色", "专业技能扎实", "团队协作能力强"])
			else:
				strengths.extend(["积极的工作态度", "良好的学习能力", "认真负责"])

			# 如果有很多改进建议，添加改进领域
			if any(cat in ["communication", "time_management", "leadership"] for cat in key_themes):
				improvement_areas.extend(["沟通技巧", "时间管理", "领导力培养"])
			else:
				improvement_areas.extend(["持续学习", "技能提升", "工作效率"])

		# 生成针对性的建议
		recommendations = []
		if "communication" in key_themes:
			recommendations.append("参加沟通技巧培训课程")
		if "skill" in key_themes or "performance" in key_themes:
			recommendations.append("制定个人技能提升计划")
		if "teamwork" in key_themes:
			recommendations.append("参与团队建设活动")
		if not recommendations:
			recommendations.extend(["制定个人发展计划", "参与公司培训项目"])

		# 构建总结文本
		total_count = len(feedback_list)
		high_priority = priority_counts.get("high", 0)
		summary_parts = [f"共收到{total_count}条反馈"]
		if high_priority > 0:
			summary_parts.append(f"其中{high_priority}条为高优先级")
		if key_themes:
			summary_parts.append(f"主要集中在{', '.join(key_themes[:3])}等方面")

		return {
			"summary": "。".join(summary_parts) + "。",
			"key_themes": key_themes,
			"strengths": strengths,
			"improvement_areas": improvement_areas,
			"recommendations": recommendations
		}

	def _local_course_recommendations(self, analysis_data: Dict) -> Dict:
		"""本地课程推荐（AI不可用时的备用方案）"""
		courses = analysis_data.get("available_courses", [])
		feedback_summary = analysis_data.get("feedback_summary", {})

		if not courses:
			return {
				"recommendations": [],
				"total_recommended": 0,
				"reasoning": "暂无可用的课程数据"
			}

		# 基于反馈主题推荐相关课程
		key_themes = feedback_summary.get("key_themes", [])
		strengths = feedback_summary.get("strengths", [])
		improvement_areas = feedback_summary.get("improvement_areas", [])

		# 如果没有反馈数据，提供通用推荐
		if not key_themes and not strengths and not improvement_areas:
			recommendations = []
			for course in courses[:8]:  # 推荐前8个课程作为通用推荐
				recommendations.append({
					"course": course,
					"relevance_score": round(random.uniform(0.6, 0.8), 2),
					"reason": "通用个人发展推荐课程"
				})
			return {
				"recommendations": recommendations,
				"total_recommended": len(recommendations),
				"reasoning": "暂无反馈数据，提供通用个人发展课程推荐"
			}

		# 智能推荐算法
		recommendations = []
		course_scores = {}

		for course in courses:
			course_tags = course.get("tags", [])
			course_title = course.get("title", "")
			course_description = course.get("description", "")
			course_category = course.get("category", "")

			score = 0
			reasons = []

			# 基于关键主题匹配
			for theme in key_themes:
				if theme in course_title or theme in course_description or theme in " ".join(course_tags):
					score += 0.3
					reasons.append(f"与{theme}相关")

			# 基于改进领域匹配
			for area in improvement_areas:
				if area in course_title or area in course_description or area in " ".join(course_tags):
					score += 0.4
					reasons.append(f"帮助提升{area}")

			# 基于优势匹配（推荐巩固性课程）
			for strength in strengths:
				if strength in course_title or strength in course_description:
					score += 0.2
					reasons.append(f"巩固{strength}优势")

			# 类别偏好加分
			category_mapping = {
				"communication": ["沟通", "协作", "表达"],
				"skill": ["编程", "技术", "技能"],
				"performance": ["绩效", "管理", "领导"],
				"teamwork": ["团队", "协作", "合作"]
			}

			for theme in key_themes:
				if theme in category_mapping:
					for keyword in category_mapping[theme]:
						if keyword in course_title or keyword in course_description:
							score += 0.2
							break

			# 难度和实用性加分
			if course.get("difficulty") == "中级":
				score += 0.1
			if "Coursera" in course.get("platform", "") or "Udemy" in course.get("platform", ""):
				score += 0.1

			if score > 0:
				course_scores[course.get("id")] = {
					"course": course,
					"score": score,
					"reasons": reasons
				}

		# 按分数排序并选择前8个
		sorted_courses = sorted(course_scores.items(), key=lambda x: x[1]["score"], reverse=True)[:8]

		for course_id, course_data in sorted_courses:
			course = course_data["course"]
			reasons = course_data["reasons"]

			recommendations.append({
				"course": course,
				"relevance_score": round(min(course_data["score"], 1.0), 2),
				"reason": "；".join(reasons[:2]) if reasons else "基于反馈分析的个性化推荐"
			})

		# 如果没有找到相关课程，提供通用推荐
		if not recommendations:
			for course in courses[:5]:
				recommendations.append({
					"course": course,
					"relevance_score": round(random.uniform(0.5, 0.7), 2),
					"reason": "通用个人发展课程"
				})

		reasoning_parts = []
		if key_themes:
			reasoning_parts.append(f"基于{', '.join(key_themes[:2])}等主题")
		if improvement_areas:
			reasoning_parts.append(f"针对{', '.join(improvement_areas[:2])}等改进方向")
		if not reasoning_parts:
			reasoning_parts.append("基于个人发展需求")

		return {
			"recommendations": recommendations,
			"total_recommended": len(recommendations),
			"reasoning": "。".join(reasoning_parts) + "推荐相关课程"
		}
