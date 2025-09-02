"""
智能推荐系统配置文件
"""

# 推荐算法权重配置
RECOMMENDATION_WEIGHTS = {
    'skill_match': 0.6,      # 技能匹配权重 60%
    'experience_match': 0.2,  # 经验匹配权重 20%
    'salary_match': 0.1,      # 薪资匹配权重 10%
    'location_match': 0.1     # 地理位置匹配权重 10%
}

# 技能分类配置
SKILL_CATEGORIES = {
    'programming_languages': [
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 
        'ruby', 'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab'
    ],
    'frontend_technologies': [
        'react', 'vue', 'angular', 'html', 'css', 'sass', 'less', 
        'bootstrap', 'jquery', 'webpack', 'vite', 'next.js', 'nuxt.js'
    ],
    'backend_technologies': [
        'node.js', 'express', 'spring', 'django', 'flask', 'fastapi', 
        'laravel', 'rails', 'asp.net', 'gin', 'echo', 'fiber'
    ],
    'databases': [
        'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 
        'oracle', 'sql server', 'sqlite', 'mariadb', 'cassandra'
    ],
    'cloud_services': [
        'aws', 'azure', 'gcp', 'aliyun', 'tencent cloud', 'huawei cloud',
        'docker', 'kubernetes', 'jenkins', 'gitlab', 'github'
    ],
    'development_tools': [
        'git', 'svn', 'jira', 'confluence', 'postman', 'swagger', 
        'maven', 'gradle', 'npm', 'yarn', 'pip', 'composer'
    ],
    'methodologies': [
        'agile', 'scrum', 'kanban', 'devops', 'ci/cd', 'tdd', 'bdd', 
        'lean', 'six sigma', 'waterfall', 'spiral'
    ],
    'design_tools': [
        'ui/ux', 'design', 'figma', 'sketch', 'adobe', 'photoshop', 
        'illustrator', 'invision', 'zeplin', 'principle'
    ],
    'business_skills': [
        'marketing', 'sales', 'management', 'leadership', 'project management', 
        'product management', 'business analysis', 'data analysis', 
        'financial analysis', 'risk management'
    ],
    'soft_skills': [
        'communication', 'teamwork', 'problem solving', 'critical thinking', 
        'creativity', 'time management', 'customer service', 'negotiation', 
        'presentation', 'adaptability'
    ]
}

# 中文技能关键词
CHINESE_SKILLS = {
    '技术技能': [
        '编程', '开发', '设计', '技术', '算法', '人工智能', '机器学习', '深度学习',
        '大数据', '云计算', '区块链', '物联网', '移动开发', '前端开发', '后端开发',
        '全栈开发', '测试', '运维', '安全', '架构', '系统', '数据库', '网络',
        '服务器', '客户端', '服务端', '接口', 'api', '微服务', '分布式', '高并发',
        '性能优化', '代码质量', '版本控制', '持续集成'
    ],
    '业务技能': [
        '管理', '分析', '运营', '营销', '销售', '客服', '财务', '人力资源',
        '行政', '法务', '产品', '项目', '数据', '商业', '市场', '客户',
        '供应链', '物流', '采购', '质量', '生产', '研发', '创新'
    ],
    '行业领域': [
        '互联网', '金融', '教育', '医疗', '制造', '零售', '房地产', '汽车',
        '能源', '环保', '农业', '旅游', '娱乐', '媒体', '咨询', '政府'
    ]
}

# 经验水平映射
EXPERIENCE_LEVELS = {
    '初级': {
        'keywords': ['初级', 'junior', 'entry', 'associate', 'trainee', 'intern'],
        'years': '0-2年',
        'level': 1
    },
    '中级': {
        'keywords': ['中级', 'middle', 'intermediate', 'mid-level', 'experienced'],
        'years': '2-5年',
        'level': 2
    },
    '高级': {
        'keywords': ['高级', 'senior', 'advanced', 'expert', 'lead'],
        'years': '5-8年',
        'level': 3
    },
    '专家': {
        'keywords': ['专家', 'expert', 'principal', 'architect', 'director'],
        'years': '8年以上',
        'level': 4
    }
}

# 职位类型映射
JOB_TYPES = {
    '全职': ['全职', 'full-time', 'full time', 'permanent'],
    '兼职': ['兼职', 'part-time', 'part time', 'casual'],
    '实习': ['实习', 'internship', 'intern', 'trainee'],
    '远程': ['远程', 'remote', 'work from home', 'wfh'],
    '合同': ['合同', 'contract', 'freelance', 'consultant']
}

# 推荐算法参数
RECOMMENDATION_PARAMS = {
    'max_recommendations': 8,        # 最大推荐数量
    'min_match_score': 30,           # 最小匹配分数
    'skill_boost_factor': 1.2,       # 技能匹配提升因子
    'experience_penalty': 0.8,       # 经验不匹配惩罚因子
    'location_boost': 1.1,           # 地理位置匹配提升因子
    'salary_boost': 1.05,            # 薪资匹配提升因子
    'fresh_job_boost': 1.15,         # 新职位提升因子（7天内）
    'popular_job_boost': 1.1         # 热门职位提升因子（申请人数多）
}

# 公司类型技能映射
COMPANY_SKILL_MAPPING = {
    '科技公司': {
        'keywords': ['科技', '技术', '软件', '互联网', 'digital', 'tech', 'software', 'ai', '人工智能'],
        'skills': ['编程', '软件开发', '技术管理', '产品设计', '数据分析', '算法', '云计算']
    },
    '金融公司': {
        'keywords': ['银行', '金融', '保险', '投资', 'finance', 'bank', 'insurance', '证券', '基金'],
        'skills': ['金融分析', '风险管理', '财务建模', '投资分析', '合规', '审计', '精算']
    },
    '咨询公司': {
        'keywords': ['咨询', '顾问', '咨询', 'consulting', 'advisory', '管理咨询'],
        'skills': ['商业分析', '战略规划', '项目管理', '客户关系', '市场研究', '流程优化']
    },
    '制造业': {
        'keywords': ['制造', '工业', '生产', 'manufacturing', 'industrial', '工厂', '制造'],
        'skills': ['生产管理', '质量控制', '供应链管理', '工艺优化', '设备维护', '安全']
    },
    '教育机构': {
        'keywords': ['教育', '学校', '大学', 'education', 'university', 'college', '培训'],
        'skills': ['教学', '课程设计', '教育管理', '学生服务', '研究', '学术']
    },
    '医疗健康': {
        'keywords': ['医疗', '健康', '医院', 'healthcare', 'medical', 'pharma', '生物'],
        'skills': ['医疗管理', '临床研究', '药物开发', '健康数据分析', '护理', '康复']
    },
    '零售电商': {
        'keywords': ['零售', '电商', '购物', 'retail', 'e-commerce', 'online', '商城'],
        'skills': ['销售管理', '客户服务', '供应链', '数据分析', '营销', '运营']
    }
}

# 推荐算法优化配置
OPTIMIZATION_CONFIG = {
    'enable_skill_boost': True,           # 启用技能匹配提升
    'enable_experience_penalty': True,    # 启用经验不匹配惩罚
    'enable_location_boost': True,        # 启用地理位置匹配提升
    'enable_salary_boost': True,          # 启用薪资匹配提升
    'enable_fresh_job_boost': True,       # 启用新职位提升
    'enable_popular_job_boost': True,     # 启用热门职位提升
    'enable_company_type_boost': True,    # 启用公司类型匹配提升
    'enable_user_preference_boost': True  # 启用用户偏好提升
}
