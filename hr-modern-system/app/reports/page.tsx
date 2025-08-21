'use client'

import { MainLayout } from '@/components/layout/main-layout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  Download,
  TrendingUp,
  TrendingDown,
  Users,
  Clock,
  DollarSign,
  Target,
  BarChart3,
  PieChart as PieChartIcon
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
  PieChart, 
  Pie, 
  Cell,
  AreaChart,
  Area
} from 'recharts'

const kpiData = [
  {
    title: '平均招聘时间',
    value: '23天',
    change: '-12%',
    changeType: 'down',
    icon: Clock,
    color: 'from-blue-500 to-blue-600'
  },
  {
    title: '平均招聘成本',
    value: '¥8,500',
    change: '+5%',
    changeType: 'up',
    icon: DollarSign,
    color: 'from-green-500 to-green-600'
  },
  {
    title: 'Offer接受率',
    value: '78%',
    change: '+8%',
    changeType: 'up',
    icon: Target,
    color: 'from-purple-500 to-purple-600'
  },
  {
    title: '招聘质量评分',
    value: '4.2/5',
    change: '+15%',
    changeType: 'up',
    icon: Users,
    color: 'from-orange-500 to-orange-600'
  }
]

const timeToHireData = [
  { month: '1月', engineering: 25, design: 18, product: 22, marketing: 20 },
  { month: '2月', engineering: 22, design: 16, product: 19, marketing: 18 },
  { month: '3月', engineering: 20, design: 15, product: 17, marketing: 16 },
  { month: '4月', engineering: 18, design: 14, product: 15, marketing: 15 },
  { month: '5月', engineering: 16, design: 13, product: 14, marketing: 14 },
  { month: '6月', engineering: 15, design: 12, product: 13, marketing: 13 }
]

const funnelData = [
  { stage: '已申请', count: 1234, percentage: 100 },
  { stage: '已筛选', count: 856, percentage: 69 },
  { stage: '已面试', count: 234, percentage: 19 },
  { stage: '已发Offer', count: 45, percentage: 4 },
  { stage: '已录用', count: 18, percentage: 1.5 }
]

const recruiterPerformance = [
  { name: '张经理', hires: 12, avgTime: 20, quality: 4.3 },
  { name: '李总监', hires: 8, avgTime: 18, quality: 4.5 },
  { name: '王主管', hires: 15, avgTime: 22, quality: 4.1 },
  { name: '赵经理', hires: 10, avgTime: 19, quality: 4.2 }
]

const offerAcceptanceData = [
  { month: '1月', rate: 65 },
  { month: '2月', rate: 72 },
  { month: '3月', rate: 68 },
  { month: '4月', rate: 75 },
  { month: '5月', rate: 78 },
  { month: '6月', rate: 82 }
]

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

export default function ReportsPage() {
  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">报告分析</h1>
            <p className="text-gray-600">深入了解招聘数据，优化招聘策略。</p>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline">
              <Download className="mr-2 h-4 w-4" />
              导出PDF
            </Button>
            <Button variant="outline">
              <Download className="mr-2 h-4 w-4" />
              导出CSV
            </Button>
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {kpiData.map((kpi) => (
            <Card key={kpi.title} className="overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{kpi.title}</p>
                    <p className="text-3xl font-bold text-gray-900 mt-1">{kpi.value}</p>
                  </div>
                  <div className={`h-12 w-12 rounded-xl bg-gradient-to-br ${kpi.color} flex items-center justify-center`}>
                    <kpi.icon className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="flex items-center mt-4">
                  {kpi.changeType === 'down' ? (
                    <TrendingDown className="h-4 w-4 text-green-500" />
                  ) : (
                    <TrendingUp className="h-4 w-4 text-red-500" />
                  )}
                  <span className={`text-sm font-medium ml-1 ${
                    kpi.changeType === 'down' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {kpi.change}
                  </span>
                  <span className="text-sm text-gray-500 ml-1">较上月</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Charts Row 1 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Time to Hire Trend */}
          <Card>
            <CardHeader>
              <CardTitle>招聘时间趋势</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={timeToHireData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="engineering" stroke="#3B82F6" strokeWidth={2} name="技术岗" />
                  <Line type="monotone" dataKey="design" stroke="#8B5CF6" strokeWidth={2} name="设计岗" />
                  <Line type="monotone" dataKey="product" stroke="#10B981" strokeWidth={2} name="产品岗" />
                  <Line type="monotone" dataKey="marketing" stroke="#F59E0B" strokeWidth={2} name="市场岗" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Recruitment Funnel */}
          <Card>
            <CardHeader>
              <CardTitle>招聘漏斗分析</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={funnelData} layout="horizontal">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="stage" type="category" width={80} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#8884d8" radius={[0, 4, 4, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Charts Row 2 */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recruiter Performance */}
          <Card>
            <CardHeader>
              <CardTitle>招聘官绩效对比</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={recruiterPerformance}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="hires" fill="#3B82F6" name="招聘人数" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="avgTime" fill="#8B5CF6" name="平均时间" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Offer Acceptance Rate */}
          <Card>
            <CardHeader>
              <CardTitle>Offer接受率趋势</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={offerAcceptanceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Area 
                    type="monotone" 
                    dataKey="rate" 
                    stroke="#10B981" 
                    fill="#10B981" 
                    fillOpacity={0.3}
                    strokeWidth={2}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Detailed Metrics */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Department Performance */}
          <Card>
            <CardHeader>
              <CardTitle>部门招聘表现</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { dept: '技术部', hires: 25, avgTime: 18, quality: 4.3 },
                  { dept: '设计部', hires: 12, avgTime: 15, quality: 4.5 },
                  { dept: '产品部', hires: 18, avgTime: 20, quality: 4.2 },
                  { dept: '市场部', hires: 15, avgTime: 22, quality: 4.0 }
                ].map((dept) => (
                  <div key={dept.dept} className="flex items-center justify-between p-3 rounded-lg bg-gray-50">
                    <div>
                      <p className="font-medium text-gray-900">{dept.dept}</p>
                      <p className="text-sm text-gray-500">{dept.hires}人 · {dept.avgTime}天</p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm font-medium text-gray-900">{dept.quality}/5</p>
                      <p className="text-xs text-gray-500">质量评分</p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Skills Gap Analysis */}
          <Card>
            <CardHeader>
              <CardTitle>技能缺口分析</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {[
                  { skill: 'React开发', demand: 85, supply: 60, gap: 25 },
                  { skill: 'Python开发', demand: 78, supply: 65, gap: 13 },
                  { skill: 'UI/UX设计', demand: 72, supply: 55, gap: 17 },
                  { skill: '产品管理', demand: 68, supply: 45, gap: 23 },
                  { skill: '数据分析', demand: 75, supply: 50, gap: 25 }
                ].map((item) => (
                  <div key={item.skill} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-700">{item.skill}</span>
                      <span className="text-gray-500">{item.gap}% 缺口</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-gradient-to-r from-red-500 to-orange-500 h-2 rounded-full"
                        style={{ width: `${item.gap}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Cost Analysis */}
          <Card>
            <CardHeader>
              <CardTitle>招聘成本分析</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={[
                      { name: '招聘平台', value: 35, color: '#3B82F6' },
                      { name: '猎头服务', value: 25, color: '#8B5CF6' },
                      { name: '内部推荐', value: 20, color: '#10B981' },
                      { name: '校园招聘', value: 15, color: '#F59E0B' },
                      { name: '其他渠道', value: 5, color: '#EF4444' }
                    ]}
                    cx="50%"
                    cy="50%"
                    outerRadius={60}
                    dataKey="value"
                    label={({ name, value }) => `${name}: ${value}%`}
                  >
                    {[
                      { name: '招聘平台', value: 35, color: '#3B82F6' },
                      { name: '猎头服务', value: 25, color: '#8B5CF6' },
                      { name: '内部推荐', value: 20, color: '#10B981' },
                      { name: '校园招聘', value: 15, color: '#F59E0B' },
                      { name: '其他渠道', value: 5, color: '#EF4444' }
                    ].map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Recommendations */}
        <Card>
          <CardHeader>
            <CardTitle>AI优化建议</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <h4 className="font-semibold text-gray-900">招聘效率提升</h4>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                    <span>技术岗位平均招聘时间可缩短至15天</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                    <span>优化面试流程，减少重复环节</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                    <span>加强内部推荐激励政策</span>
                  </li>
                </ul>
              </div>
              <div className="space-y-4">
                <h4 className="font-semibold text-gray-900">成本控制建议</h4>
                <ul className="space-y-2 text-sm text-gray-600">
                  <li className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                    <span>减少猎头服务依赖，节省25%成本</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                    <span>优化招聘平台使用策略</span>
                  </li>
                  <li className="flex items-start space-x-2">
                    <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                    <span>建立人才库，降低重复招聘成本</span>
                  </li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
