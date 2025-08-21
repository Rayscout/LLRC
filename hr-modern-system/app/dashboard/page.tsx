'use client'

import { MainLayout } from '@/components/layout/main-layout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  Users, 
  Calendar, 
  CheckCircle, 
  TrendingUp,
  ArrowUpRight,
  ArrowDownRight,
  UserPlus,
  Clock,
  Star,
  BarChart3
} from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const metrics = [
  {
    title: '总候选人',
    value: '1,234',
    change: '+12%',
    changeType: 'up',
    icon: Users,
    color: 'from-blue-500 to-blue-600'
  },
  {
    title: '已安排面试',
    value: '89',
    change: '+5%',
    changeType: 'up',
    icon: Calendar,
    color: 'from-purple-500 to-purple-600'
  },
  {
    title: '已发出Offer',
    value: '23',
    change: '+18%',
    changeType: 'up',
    icon: CheckCircle,
    color: 'from-green-500 to-green-600'
  },
  {
    title: '已完成招聘',
    value: '18',
    change: '-2%',
    changeType: 'down',
    icon: TrendingUp,
    color: 'from-orange-500 to-orange-600'
  }
]

const funnelData = [
  { name: '已申请', value: 1234, color: '#3B82F6' },
  { name: '已筛选', value: 856, color: '#8B5CF6' },
  { name: '已面试', value: 234, color: '#10B981' },
  { name: '已录用', value: 18, color: '#F59E0B' }
]

const recentActivity = [
  {
    id: 1,
    type: 'candidate_applied',
    message: '李四申请了前端开发工程师职位',
    time: '2分钟前',
    avatar: '李',
    status: 'new'
  },
  {
    id: 2,
    type: 'interview_scheduled',
    message: '王五的面试已安排在明天下午2点',
    time: '15分钟前',
    avatar: '王',
    status: 'scheduled'
  },
  {
    id: 3,
    type: 'feedback_submitted',
    message: '赵六的面试反馈已提交',
    time: '1小时前',
    avatar: '赵',
    status: 'completed'
  },
  {
    id: 4,
    type: 'offer_sent',
    message: '孙七的Offer已发出',
    time: '2小时前',
    avatar: '孙',
    status: 'offer'
  }
]

export default function DashboardPage() {
  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">仪表板</h1>
            <p className="text-gray-600">欢迎回来，张三！这是您的招聘概览。</p>
          </div>
          <Button className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
            <UserPlus className="mr-2 h-4 w-4" />
            添加候选人
          </Button>
        </div>

        {/* Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {metrics.map((metric) => (
            <Card key={metric.title} className="overflow-hidden">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-gray-600">{metric.title}</p>
                    <p className="text-3xl font-bold text-gray-900 mt-1">{metric.value}</p>
                  </div>
                  <div className={`h-12 w-12 rounded-xl bg-gradient-to-br ${metric.color} flex items-center justify-center`}>
                    <metric.icon className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="flex items-center mt-4">
                  {metric.changeType === 'up' ? (
                    <ArrowUpRight className="h-4 w-4 text-green-500" />
                  ) : (
                    <ArrowDownRight className="h-4 w-4 text-red-500" />
                  )}
                  <span className={`text-sm font-medium ml-1 ${
                    metric.changeType === 'up' ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {metric.change}
                  </span>
                  <span className="text-sm text-gray-500 ml-1">较上月</span>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Charts and Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recruitment Funnel */}
          <Card>
            <CardHeader>
              <CardTitle>招聘漏斗</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={funnelData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#8884d8" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle>最近活动</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentActivity.map((activity) => (
                  <div key={activity.id} className="flex items-start space-x-3">
                    <div className="h-8 w-8 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white text-sm font-medium">
                      {activity.avatar}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-gray-900">{activity.message}</p>
                      <p className="text-xs text-gray-500 mt-1">{activity.time}</p>
                    </div>
                    <div className={`h-2 w-2 rounded-full mt-2 ${
                      activity.status === 'new' ? 'bg-blue-500' :
                      activity.status === 'scheduled' ? 'bg-purple-500' :
                      activity.status === 'completed' ? 'bg-green-500' :
                      'bg-orange-500'
                    }`} />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>快速操作</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Button variant="outline" className="h-20 flex-col space-y-2">
                <Calendar className="h-6 w-6" />
                <span>安排面试</span>
              </Button>
              <Button variant="outline" className="h-20 flex-col space-y-2">
                <Users className="h-6 w-6" />
                <span>查看候选人</span>
              </Button>
              <Button variant="outline" className="h-20 flex-col space-y-2">
                <BarChart3 className="h-6 w-6" />
                <span>生成报告</span>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </MainLayout>
  )
}
