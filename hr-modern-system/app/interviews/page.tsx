'use client'

import { useState } from 'react'
import { MainLayout } from '@/components/layout/main-layout'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { 
  Calendar,
  Clock,
  Users,
  Plus,
  Video,
  MapPin,
  MessageSquare,
  CheckCircle,
  XCircle,
  MoreHorizontal
} from 'lucide-react'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'

const timeSlots = [
  '09:00', '09:30', '10:00', '10:30', '11:00', '11:30',
  '14:00', '14:30', '15:00', '15:30', '16:00', '16:30'
]

const interviews = [
  {
    id: 1,
    candidate: '李四',
    position: '前端开发工程师',
    interviewer: '张经理',
    date: '2024-01-16',
    time: '14:00',
    duration: '60分钟',
    type: 'online',
    status: 'scheduled',
    avatar: '李'
  },
  {
    id: 2,
    candidate: '王五',
    position: '后端开发工程师',
    interviewer: '李总监',
    date: '2024-01-16',
    time: '15:30',
    duration: '90分钟',
    type: 'in-person',
    status: 'completed',
    avatar: '王'
  },
  {
    id: 3,
    candidate: '赵六',
    position: 'UI/UX设计师',
    interviewer: '王主管',
    date: '2024-01-17',
    time: '10:00',
    duration: '60分钟',
    type: 'online',
    status: 'scheduled',
    avatar: '赵'
  }
]

const weekDays = [
  { date: '2024-01-15', day: '周一', label: '1月15日' },
  { date: '2024-01-16', day: '周二', label: '1月16日' },
  { date: '2024-01-17', day: '周三', label: '1月17日' },
  { date: '2024-01-18', day: '周四', label: '1月18日' },
  { date: '2024-01-19', day: '周五', label: '1月19日' }
]

export default function InterviewsPage() {
  const [selectedDate, setSelectedDate] = useState('2024-01-16')
  const [showScheduleModal, setShowScheduleModal] = useState(false)

  const getInterviewsForDate = (date: string) => {
    return interviews.filter(interview => interview.date === date)
  }

  const getInterviewsForTimeSlot = (date: string, time: string) => {
    return interviews.filter(interview => 
      interview.date === date && interview.time === time
    )
  }

  return (
    <MainLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">面试安排</h1>
            <p className="text-gray-600">管理和安排候选人面试，跟踪面试进度。</p>
          </div>
          <Button 
            className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
            onClick={() => setShowScheduleModal(true)}
          >
            <Plus className="mr-2 h-4 w-4" />
            安排面试
          </Button>
        </div>

        {/* Calendar View */}
        <Card>
          <CardHeader>
            <CardTitle>本周面试安排</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <div className="min-w-[800px]">
                {/* Time slots header */}
                <div className="grid grid-cols-6 gap-2 mb-4">
                  <div className="h-12"></div>
                  {weekDays.map((day) => (
                    <div key={day.date} className="text-center">
                      <div className="text-sm font-medium text-gray-900">{day.day}</div>
                      <div className="text-xs text-gray-500">{day.label}</div>
                    </div>
                  ))}
                </div>

                {/* Time slots */}
                {timeSlots.map((time) => (
                  <div key={time} className="grid grid-cols-6 gap-2 mb-2">
                    <div className="h-16 flex items-center text-sm text-gray-500 font-medium">
                      {time}
                    </div>
                    {weekDays.map((day) => {
                      const dayInterviews = getInterviewsForTimeSlot(day.date, time)
                      return (
                        <div key={day.date} className="h-16 border border-gray-200 rounded-lg p-2 relative">
                          {dayInterviews.map((interview) => (
                            <div
                              key={interview.id}
                              className={`absolute inset-1 rounded-md p-2 text-xs ${
                                interview.type === 'online' 
                                  ? 'bg-blue-100 border border-blue-200' 
                                  : 'bg-purple-100 border border-purple-200'
                              }`}
                            >
                              <div className="flex items-center space-x-1 mb-1">
                                {interview.type === 'online' ? (
                                  <Video className="h-3 w-3 text-blue-600" />
                                ) : (
                                  <MapPin className="h-3 w-3 text-purple-600" />
                                )}
                                <span className="font-medium text-gray-900">{interview.candidate}</span>
                              </div>
                              <div className="text-gray-600">{interview.position}</div>
                              <div className="text-gray-500">{interview.duration}</div>
                            </div>
                          ))}
                        </div>
                      )
                    })}
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Upcoming Interviews */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card>
            <CardHeader>
              <CardTitle>即将到来的面试</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {interviews
                  .filter(interview => interview.status === 'scheduled')
                  .slice(0, 3)
                  .map((interview) => (
                    <div key={interview.id} className="flex items-center space-x-3 p-3 rounded-lg border border-gray-100 hover:bg-gray-50">
                      <Avatar className="h-10 w-10">
                        <AvatarFallback className="bg-gradient-to-br from-blue-400 to-purple-500 text-white">
                          {interview.avatar}
                        </AvatarFallback>
                      </Avatar>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-gray-900">{interview.candidate}</p>
                        <p className="text-sm text-gray-500">{interview.position}</p>
                        <div className="flex items-center space-x-2 mt-1">
                          <Clock className="h-3 w-3 text-gray-400" />
                          <span className="text-xs text-gray-500">
                            {interview.date} {interview.time} ({interview.duration})
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Badge className={
                          interview.type === 'online' 
                            ? 'bg-blue-100 text-blue-800' 
                            : 'bg-purple-100 text-purple-800'
                        }>
                          {interview.type === 'online' ? '在线' : '现场'}
                        </Badge>
                        <Button variant="ghost" size="sm">
                          <MessageSquare className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>面试统计</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">本周已安排</span>
                  <span className="text-lg font-semibold text-gray-900">12</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">已完成</span>
                  <span className="text-lg font-semibold text-green-600">8</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">待进行</span>
                  <span className="text-lg font-semibold text-blue-600">4</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">在线面试</span>
                  <span className="text-lg font-semibold text-purple-600">7</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">现场面试</span>
                  <span className="text-lg font-semibold text-orange-600">5</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Interview History */}
        <Card>
          <CardHeader>
            <CardTitle>面试历史</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200">
                    <th className="text-left py-3 px-4 font-medium text-gray-700">候选人</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">职位</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">面试官</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">时间</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">类型</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">状态</th>
                    <th className="text-left py-3 px-4 font-medium text-gray-700">操作</th>
                  </tr>
                </thead>
                <tbody>
                  {interviews.map((interview) => (
                    <tr key={interview.id} className="border-b border-gray-100 hover:bg-gray-50">
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-3">
                          <Avatar className="h-8 w-8">
                            <AvatarFallback className="bg-gradient-to-br from-blue-400 to-purple-500 text-white text-sm">
                              {interview.avatar}
                            </AvatarFallback>
                          </Avatar>
                          <span className="font-medium text-gray-900">{interview.candidate}</span>
                        </div>
                      </td>
                      <td className="py-4 px-4">
                        <p className="text-sm text-gray-700">{interview.position}</p>
                      </td>
                      <td className="py-4 px-4">
                        <p className="text-sm text-gray-700">{interview.interviewer}</p>
                      </td>
                      <td className="py-4 px-4">
                        <p className="text-sm text-gray-700">{interview.date}</p>
                        <p className="text-xs text-gray-500">{interview.time}</p>
                      </td>
                      <td className="py-4 px-4">
                        <Badge className={
                          interview.type === 'online' 
                            ? 'bg-blue-100 text-blue-800' 
                            : 'bg-purple-100 text-purple-800'
                        }>
                          {interview.type === 'online' ? '在线' : '现场'}
                        </Badge>
                      </td>
                      <td className="py-4 px-4">
                        <Badge className={
                          interview.status === 'scheduled' 
                            ? 'bg-blue-100 text-blue-800' 
                            : 'bg-green-100 text-green-800'
                        }>
                          {interview.status === 'scheduled' ? '已安排' : '已完成'}
                        </Badge>
                      </td>
                      <td className="py-4 px-4">
                        <div className="flex items-center space-x-2">
                          <Button variant="ghost" size="sm">
                            <MessageSquare className="h-4 w-4" />
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
      </div>

      {/* Schedule Interview Modal */}
      {showScheduleModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">安排面试</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">候选人</label>
                <select className="w-full h-10 px-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                  <option>选择候选人</option>
                  <option>李四</option>
                  <option>王五</option>
                  <option>赵六</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">面试官</label>
                <select className="w-full h-10 px-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                  <option>选择面试官</option>
                  <option>张经理</option>
                  <option>李总监</option>
                  <option>王主管</option>
                </select>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">日期</label>
                  <input type="date" className="w-full h-10 px-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500" />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">时间</label>
                  <select className="w-full h-10 px-3 rounded-lg border border-gray-200 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500">
                    <option>09:00</option>
                    <option>09:30</option>
                    <option>10:00</option>
                    <option>14:00</option>
                    <option>14:30</option>
                    <option>15:00</option>
                  </select>
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">面试类型</label>
                <div className="flex space-x-4">
                  <label className="flex items-center">
                    <input type="radio" name="type" value="online" className="mr-2" />
                    <span className="text-sm text-gray-700">在线</span>
                  </label>
                  <label className="flex items-center">
                    <input type="radio" name="type" value="in-person" className="mr-2" />
                    <span className="text-sm text-gray-700">现场</span>
                  </label>
                </div>
              </div>
              <div className="flex space-x-3 pt-4">
                <Button 
                  variant="outline" 
                  className="flex-1"
                  onClick={() => setShowScheduleModal(false)}
                >
                  取消
                </Button>
                <Button className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700">
                  安排面试
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </MainLayout>
  )
}
