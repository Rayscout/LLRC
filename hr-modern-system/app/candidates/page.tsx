'use client'

import { useState } from 'react'
import { MainLayout } from '@/components/layout/main-layout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  Search, 
  Filter, 
  Eye, 
  MessageSquare, 
  Calendar,
  Star,
  MoreHorizontal,
  UserPlus,
  Download
} from 'lucide-react'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'

const candidates = [
  {
    id: 1,
    name: '李四',
    email: 'lisi@email.com',
    position: '前端开发工程师',
    skills: ['React', 'TypeScript', 'Node.js'],
    skillsMatch: 95,
    status: 'interview',
    experience: '3年',
    location: '北京',
    avatar: '李',
    appliedDate: '2024-01-15',
    lastContact: '2天前'
  },
  {
    id: 2,
    name: '王五',
    email: 'wangwu@email.com',
    position: '后端开发工程师',
    skills: ['Python', 'Django', 'PostgreSQL'],
    skillsMatch: 88,
    status: 'applied',
    experience: '5年',
    location: '上海',
    avatar: '王',
    appliedDate: '2024-01-14',
    lastContact: '1周前'
  },
  {
    id: 3,
    name: '赵六',
    email: 'zhaoliu@email.com',
    position: 'UI/UX设计师',
    skills: ['Figma', 'Sketch', 'Adobe XD'],
    skillsMatch: 92,
    status: 'offer',
    experience: '4年',
    location: '深圳',
    avatar: '赵',
    appliedDate: '2024-01-10',
    lastContact: '今天'
  },
  {
    id: 4,
    name: '孙七',
    email: 'sunqi@email.com',
    position: '产品经理',
    skills: ['产品规划', '用户研究', '数据分析'],
    skillsMatch: 78,
    status: 'hired',
    experience: '6年',
    location: '杭州',
    avatar: '孙',
    appliedDate: '2024-01-08',
    lastContact: '3天前'
  }
]

const statusColors = {
  applied: 'bg-blue-100 text-blue-800',
  interview: 'bg-purple-100 text-purple-800',
  offer: 'bg-orange-100 text-orange-800',
  hired: 'bg-green-100 text-green-800',
  rejected: 'bg-red-100 text-red-800'
}

const statusLabels = {
  applied: '已申请',
  interview: '面试中',
  offer: '已发Offer',
  hired: '已录用',
  rejected: '已拒绝'
}

export default function CandidatesPage() {
  const [searchTerm, setSearchTerm] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')

  const filteredCandidates = candidates.filter(candidate => {
    const matchesSearch = candidate.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         candidate.position.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         candidate.skills.some(skill => skill.toLowerCase().includes(searchTerm.toLowerCase()))
    
    const matchesStatus = statusFilter === 'all' || candidate.status === statusFilter
    
    return matchesSearch && matchesStatus
  })

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">候选人管理</h1>
            <p className="text-gray-600">管理所有候选人信息，跟踪招聘进度。</p>
          </div>
          <div className="flex space-x-3">
            <Button variant="outline">
              <Download className="mr-2 h-4 w-4" />
              导出数据
            </Button>
            <Button className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
              <UserPlus className="mr-2 h-4 w-4" />
              添加候选人
            </Button>
          </div>
        </div>

        {/* Filters and Search */}
        <Card>
          <CardContent className="p-6">
            <div className="flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="搜索候选人姓名、职位或技能..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full h-11 pl-10 pr-4 rounded-xl border border-gray-200 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
                />
              </div>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="h-11 px-4 rounded-xl border border-gray-200 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              >
                <option value="all">所有状态</option>
                <option value="applied">已申请</option>
                <option value="interview">面试中</option>
                <option value="offer">已发Offer</option>
                <option value="hired">已录用</option>
                <option value="rejected">已拒绝</option>
              </select>
            </div>
          </CardContent>
        </Card>

        {/* Candidates Table */}
        <Card>
          <CardHeader>
            <CardTitle>候选人列表 ({filteredCandidates.length})</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium text-gray-700">候选人</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">职位</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">技能匹配</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">状态</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">经验</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">申请时间</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">操作</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredCandidates.map((candidate) => (
                    <tr key={candidate.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-3">
                          <Avatar className="h-10 w-10">
                            <AvatarFallback className="bg-gradient-to-br from-blue-400 to-purple-500 text-white">
                              {candidate.avatar}
                            </AvatarFallback>
                          </Avatar>
                          <div>
                            <p className="font-medium text-gray-900">{candidate.name}</p>
                            <p className="text-sm text-gray-500">{candidate.email}</p>
                          </div>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <p className="font-medium text-gray-900">{candidate.position}</p>
                        <p className="text-sm text-gray-500">{candidate.location}</p>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-2">
                          <div className="w-16 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full"
                              style={{ width: `${candidate.skillsMatch}%` }}
                            />
                          </div>
                          <span className="text-sm font-medium text-gray-700">{candidate.skillsMatch}%</span>
                        </div>
                        <div className="flex flex-wrap gap-1 mt-1">
                          {candidate.skills.slice(0, 2).map((skill, index) => (
                            <Badge key={index} variant="secondary" className="text-xs">
                              {skill}
                            </Badge>
                          ))}
                          {candidate.skills.length > 2 && (
                            <Badge variant="secondary" className="text-xs">
                              +{candidate.skills.length - 2}
                            </Badge>
                          )}
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <Badge className={statusColors[candidate.status as keyof typeof statusColors]}>
                          {statusLabels[candidate.status as keyof typeof statusLabels]}
                        </Badge>
                      </td>
                      <td className="py-4 px-4">
                        <p className="text-sm text-gray-700">{candidate.experience}</p>
                      </td>
                      <td className="py-4 px-4">
                        <p className="text-sm text-gray-700">{candidate.appliedDate}</p>
                        <p className="text-xs text-gray-500">{candidate.lastContact}</p>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-2">
                          <Button variant="ghost" size="sm">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <MessageSquare className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <Calendar className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm">
                            <MoreHorizontal className="h-4 w-4" />
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </CardContent>
        </Card>

        {/* Skills Overview */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>热门技能需求</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {['React', 'Python', 'UI/UX设计', '产品管理', '数据分析'].map((skill, index) => (
                  <div key={skill} className="flex items-center justify-between">
                    <span className="text-sm text-gray-700">{skill}</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full"
                          style={{ width: `${85 - index * 10}%` }}
                        />
                      </div>
                      <span className="text-xs text-gray-500 w-8 text-right">
                        {85 - index * 10}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>招聘进度概览</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(statusLabels).map(([key, label]) => {
                  const count = candidates.filter(c => c.status === key).length
                  const percentage = (count / candidates.length) * 100
                  return (
                    <div key={key} className="flex items-center justify-between">
                      <span className="text-sm text-gray-700">{label}</span>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-medium text-gray-900">{count}</span>
                        <span className="text-xs text-gray-500">({percentage.toFixed(0)}%)</span>
                      </div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </MainLayout>
  )
}
