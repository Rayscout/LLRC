'use client'

import { MainLayout } from '@/components/layout/main-layout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  TrendingUp,
  TrendingDown,
  Users,
  AlertTriangle,
  CheckCircle,
  Clock,
  DollarSign,
  Target,
  BarChart3,
  Lightbulb,
  Shield,
  Heart,
  Brain,
  Zap
} from 'lucide-react'
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  LineChart, 
  Line, 
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from 'recharts'

const attritionRiskData = [
  { name: '技术部', high: 15, medium: 25, low: 60 },
  { name: '设计部', high: 8, medium: 20, low: 72 },
  { name: '产品部', high: 12, medium: 30, low: 58 },
  { name: '市场部', high: 20, medium: 35, low: 45 },
  { name: '运营部', high: 10, medium: 25, low: 65 }
]

const salaryCompetitiveness = [
  { position: '前端开发', market: 25, company: 22, gap: -12 },
  { position: '后端开发', market: 28, company: 25, gap: -11 },
  { position: 'UI设计师', market: 18, company: 16, gap: -11 },
  { position: '产品经理', market: 30, company: 28, gap: -7 },
  { position: '数据分析师', market: 22, company: 20, gap: -9 }
]

const organizationalHealth = [
  { metric: '团队稳定性', score: 85, trend: 'up', color: 'green' },
  { metric: '技能匹配度', score: 72, trend: 'down', color: 'orange' },
  { metric: '员工满意度', score: 78, trend: 'up', color: 'green' },
  { metric: '内部流动性', score: 65, trend: 'stable', color: 'blue' },
  { metric: '知识传承', score: 68, trend: 'down', color: 'orange' }
]

const employeeSatisfaction = [
  { month: '1月', overall: 75, workLife: 70, growth: 80, compensation: 65 },
  { month: '2月', overall: 78, workLife: 72, growth: 82, compensation: 68 },
  { month: '3月', overall: 76, workLife: 71, growth: 79, compensation: 66 },
  { month: '4月', overall: 80, workLife: 75, growth: 85, compensation: 70 },
  { month: '5月', overall: 82, workLife: 78, growth: 87, compensation: 72 },
  { month: '6月', overall: 85, workLife: 80, growth: 90, compensation: 75 }
]

const aiRecommendations = [
  {
    category: '人才保留',
    priority: 'high',
    title: '加强技术团队职业发展路径',
    description: '为技术团队建立清晰的晋升通道和技能认证体系',
    impact: '高',
    effort: '中',
    timeline: '3个月'
  },
  {
    category: '薪酬优化',
    priority: 'high',
    title: '调整前端开发工程师薪资',
    description: '将前端开发工程师薪资提升至市场水平的95%',
    impact: '高',
    effort: '低',
    timeline: '1个月'
  },
  {
    category: '文化建设',
    priority: 'medium',
    title: '建立内部导师制度',
    description: '实施1对1导师配对，提升知识传承效率',
    impact: '中',
    effort: '中',
    timeline: '2个月'
  }
]

export default function InsightsPage() {
  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">员工洞察</h1>
            <p className="text-gray-600">AI驱动的员工分析和预测，助力人才管理决策。</p>
          </div>
          <Button className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
            <Lightbulb className="mr-2 h-4 w-4" />
            生成洞察报告
          </Button>
        </div>

        {/* Key Insights Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border-l-4 border-l-red-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">流失风险</p>
                  <p className="text-3xl font-bold text-red-600">12%</p>
                </div>
                <AlertTriangle className="h-8 w-8 text-red-500" />
              </div>
              <p className="text-xs text-gray-500 mt-2">较上月 +2%</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">组织健康度</p>
                  <p className="text-3xl font-bold text-green-600">78/100</p>
                </div>
                <Heart className="h-8 w-8 text-green-500" />
              </div>
              <p className="text-xs text-gray-500 mt-2">较上月 +3</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-blue-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">技能匹配度</p>
                  <p className="text-3xl font-bold text-blue-600">72%</p>
                </div>
                <Brain className="h-8 w-8 text-blue-500" />
              </div>
              <p className="text-xs text-gray-500 mt-2">较上月 -1%</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-purple-500">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">员工满意度</p>
                  <p className="text-3xl font-bold text-purple-600">85%</p>
                </div>
                <Shield className="h-8 w-8 text-purple-500" />
              </div>
              <p className="text-xs text-gray-500 mt-2">较上月 +2%</p>
            </CardContent>
          </Card>
        </div>

        {/* Attrition Risk Analysis */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>流失风险分析</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={attritionRiskData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="high" stackId="a" fill="#EF4444" name="高风险" />
                  <Bar dataKey="medium" stackId="a" fill="#F59E0B" name="中风险" />
                  <Bar dataKey="low" stackId="a" fill="#10B981" name="低风险" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>薪资竞争力分析</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {salaryCompetitiveness.map((item) => (
                  <div key={item.position} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-700">{item.position}</span>
                      <span className={`font-medium ${
                        item.gap >= -10 ? 'text-green-600' : 
                        item.gap >= -15 ? 'text-orange-600' : 'text-red-600'
                      }`}>
                        {item.gap}% 差距
                      </span>
                    </div>
                    <div className="flex space-x-2">
                      <div className="flex-1 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-blue-500 h-2 rounded-full"
                          style={{ width: `${(item.company / item.market) * 100}%` }}
                        />
                      </div>
                      <span className="text-xs text-gray-500 w-12 text-right">
                        {item.company}k
                      </span>
                    </div>
                    <div className="text-xs text-gray-500">
                      市场平均: {item.market}k
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Organizational Health & Employee Satisfaction */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>组织健康度雷达图</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={organizationalHealth}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="metric" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar
                    name="当前得分"
                    dataKey="score"
                    stroke="#3B82F6"
                    fill="#3B82F6"
                    fillOpacity={0.3}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>员工满意度趋势</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={employeeSatisfaction}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="overall" stroke="#3B82F6" strokeWidth={2} name="整体满意度" />
                  <Line type="monotone" dataKey="workLife" stroke="#8B5CF6" strokeWidth={2} name="工作生活平衡" />
                  <Line type="monotone" dataKey="growth" stroke="#10B981" strokeWidth={2} name="职业发展" />
                  <Line type="monotone" dataKey="compensation" stroke="#F59E0B" strokeWidth={2} name="薪酬福利" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* AI Recommendations */}
        <Card>
          <CardHeader>
            <CardTitle>AI智能建议</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {aiRecommendations.map((recommendation, index) => (
                <div key={index} className="p-4 border border-gray-200 rounded-xl hover:bg-gray-50 transition-colors">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-3">
                      <div className={`w-3 h-3 rounded-full ${
                        recommendation.priority === 'high' ? 'bg-red-500' :
                        recommendation.priority === 'medium' ? 'bg-orange-500' : 'bg-blue-500'
                      }`} />
                      <span className="text-sm font-medium text-gray-500">{recommendation.category}</span>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs px-2 py-1 rounded-full bg-blue-100 text-blue-800">
                        影响: {recommendation.impact}
                      </span>
                      <span className="text-xs px-2 py-1 rounded-full bg-green-100 text-green-800">
                        难度: {recommendation.effort}
                      </span>
                      <span className="text-xs px-2 py-1 rounded-full bg-purple-100 text-purple-800">
                        {recommendation.timeline}
                      </span>
                    </div>
                  </div>
                  
                  <h4 className="font-semibold text-gray-900 mb-2">{recommendation.title}</h4>
                  <p className="text-sm text-gray-600 mb-3">{recommendation.description}</p>
                  
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <Zap className="h-4 w-4 text-yellow-500" />
                      <span className="text-xs text-gray-500">AI生成建议</span>
                    </div>
                    <div className="flex space-x-2">
                      <Button variant="outline" size="sm">了解更多</Button>
                      <Button size="sm" className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
                        实施计划
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Predictive Analytics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>人才流失预测</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-gray-900 mb-2">15%</div>
                  <p className="text-sm text-gray-600">未来3个月预测流失率</p>
                </div>
                <div className="space-y-3">
                  {[
                    { factor: '薪资不满', weight: 35, risk: 'high' },
                    { factor: '职业发展受限', weight: 28, risk: 'medium' },
                    { factor: '工作压力大', weight: 22, risk: 'medium' },
                    { factor: '团队氛围', weight: 15, risk: 'low' }
                  ].map((item) => (
                    <div key={item.factor} className="flex items-center justify-between">
                      <span className="text-sm text-gray-700">{item.factor}</span>
                      <div className="flex items-center space-x-2">
                        <div className="w-20 bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full ${
                              item.risk === 'high' ? 'bg-red-500' :
                              item.risk === 'medium' ? 'bg-orange-500' : 'bg-green-500'
                            }`}
                            style={{ width: `${item.weight}%` }}
                          />
                        </div>
                        <span className="text-xs text-gray-500 w-8 text-right">{item.weight}%</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>技能发展建议</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { skill: 'AI/ML技能', demand: 85, current: 45, priority: 'critical' },
                  { skill: '云原生开发', demand: 78, current: 52, priority: 'high' },
                  { skill: '数据科学', demand: 72, current: 38, priority: 'high' },
                  { skill: 'DevOps实践', demand: 68, current: 55, priority: 'medium' }
                ].map((item) => (
                  <div key={item.skill} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-700">{item.skill}</span>
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        item.priority === 'critical' ? 'bg-red-100 text-red-800' :
                        item.priority === 'high' ? 'bg-orange-100 text-orange-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {item.priority === 'critical' ? '紧急' : 
                         item.priority === 'high' ? '高' : '中'}
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full"
                        style={{ width: `${(item.current / item.demand) * 100}%` }}
                      />
                    </div>
                    <div className="text-xs text-gray-500">
                      当前水平: {item.current}% | 市场需求: {item.demand}%
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </MainLayout>
  )
}
