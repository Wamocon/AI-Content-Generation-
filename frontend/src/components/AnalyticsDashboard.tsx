'use client'

import React, { useState, useEffect } from 'react'
import { 
  BarChart3, 
  TrendingUp, 
  Clock, 
  CheckCircle, 
  AlertCircle,
  Activity,
  Database,
  Users,
  Zap
} from 'lucide-react'

interface AnalyticsData {
  totalDocuments: number
  processedDocuments: number
  averageQuality: number
  processingTimeAvg: number
  errorRate: number
  dailyStats: Array<{
    date: string
    processed: number
    quality: number
    errors: number
  }>
  agentPerformance: Array<{
    agent: string
    tasksCompleted: number
    averageTime: number
    successRate: number
  }>
  systemMetrics: {
    cpuUsage: number
    memoryUsage: number
    diskUsage: number
    activeConnections: number
  }
}

export default function AnalyticsDashboard() {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [timeRange, setTimeRange] = useState<'24h' | '7d' | '30d'>('24h')

  useEffect(() => {
    fetchAnalytics()
    const interval = setInterval(fetchAnalytics, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [timeRange])

  const fetchAnalytics = async () => {
    try {
      setIsLoading(true)
      
      // Fetch analytics from multiple endpoints
      const [contentAnalytics, systemMetrics, batchStatus] = await Promise.all([
        fetch(`http://localhost:8000/content-intelligence/analytics?days=${timeRange === '24h' ? 1 : timeRange === '7d' ? 7 : 30}`).then(r => r.json()),
        fetch('http://localhost:8000/monitoring/metrics').then(r => r.json()),
        fetch('http://localhost:8000/batch-status').then(r => r.json())
      ])

      // Mock data for demonstration (replace with real data)
      const mockData: AnalyticsData = {
        totalDocuments: batchStatus.total_documents || 0,
        processedDocuments: batchStatus.total_processed || 0,
        averageQuality: batchStatus.average_quality || 0,
        processingTimeAvg: contentAnalytics.analytics?.processing_time_avg || 0,
        errorRate: contentAnalytics.analytics?.error_rate || 0,
        dailyStats: generateMockDailyStats(),
        agentPerformance: [
          { agent: 'Content Analyst', tasksCompleted: 45, averageTime: 2.3, successRate: 98.5 },
          { agent: 'Presentation Creator', tasksCompleted: 42, averageTime: 3.1, successRate: 96.2 },
          { agent: 'Use Case Developer', tasksCompleted: 38, averageTime: 1.8, successRate: 99.1 },
          { agent: 'Quiz Master', tasksCompleted: 40, averageTime: 1.5, successRate: 97.8 },
          { agent: 'Trainer Writer', tasksCompleted: 35, averageTime: 2.7, successRate: 95.4 },
          { agent: 'Quality Assurance', tasksCompleted: 43, averageTime: 1.2, successRate: 99.7 }
        ],
        systemMetrics: {
          cpuUsage: systemMetrics.metrics?.cpu_usage || 0,
          memoryUsage: systemMetrics.metrics?.memory_usage || 0,
          diskUsage: systemMetrics.metrics?.disk_usage || 0,
          activeConnections: systemMetrics.metrics?.active_jobs || 0
        }
      }

      setAnalyticsData(mockData)
    } catch (error) {
      console.error('Failed to fetch analytics:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const generateMockDailyStats = () => {
    const days = timeRange === '24h' ? 1 : timeRange === '7d' ? 7 : 30
    const stats = []
    
    for (let i = days - 1; i >= 0; i--) {
      const date = new Date()
      date.setDate(date.getDate() - i)
      
      stats.push({
        date: date.toISOString().split('T')[0],
        processed: Math.floor(Math.random() * 20) + 5,
        quality: Math.random() * 20 + 80,
        errors: Math.floor(Math.random() * 3)
      })
    }
    
    return stats
  }

  const getQualityColor = (quality: number) => {
    if (quality >= 90) return 'text-green-400'
    if (quality >= 80) return 'text-yellow-400'
    return 'text-red-400'
  }

  const getPerformanceColor = (rate: number) => {
    if (rate >= 95) return 'text-green-400'
    if (rate >= 90) return 'text-yellow-400'
    return 'text-red-400'
  }

  if (isLoading) {
    return (
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-400"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <BarChart3 className="w-6 h-6 text-red-400" />
            <h2 className="text-xl font-bold text-white">Real-time Analytics</h2>
          </div>
          
          <div className="flex items-center space-x-2">
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value as '24h' | '7d' | '30d')}
              className="bg-gray-700 text-white px-3 py-1 rounded-lg text-sm border border-gray-600"
            >
              <option value="24h">Last 24 Hours</option>
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
            </select>
          </div>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-white">{analyticsData?.totalDocuments || 0}</div>
            <div className="text-sm text-gray-400">Total Documents</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-green-400">{analyticsData?.processedDocuments || 0}</div>
            <div className="text-sm text-gray-400">Processed</div>
          </div>
          
          <div className="text-center">
            <div className={`text-3xl font-bold ${getQualityColor(analyticsData?.averageQuality || 0)}`}>
              {(analyticsData?.averageQuality || 0).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-400">Avg Quality</div>
          </div>
          
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-400">
              {(analyticsData?.processingTimeAvg || 0).toFixed(1)}s
            </div>
            <div className="text-sm text-gray-400">Avg Processing Time</div>
          </div>
        </div>
      </div>

      {/* System Metrics */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
        <h3 className="text-lg font-bold text-white mb-4">System Performance</h3>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-white">
              {(analyticsData?.systemMetrics.cpuUsage || 0).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-400">CPU Usage</div>
            <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
              <div 
                className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${analyticsData?.systemMetrics.cpuUsage || 0}%` }}
              />
            </div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-white">
              {(analyticsData?.systemMetrics.memoryUsage || 0).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-400">Memory Usage</div>
            <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
              <div 
                className="bg-green-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${analyticsData?.systemMetrics.memoryUsage || 0}%` }}
              />
            </div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-white">
              {(analyticsData?.systemMetrics.diskUsage || 0).toFixed(1)}%
            </div>
            <div className="text-sm text-gray-400">Disk Usage</div>
            <div className="w-full bg-gray-700 rounded-full h-2 mt-2">
              <div 
                className="bg-yellow-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${analyticsData?.systemMetrics.diskUsage || 0}%` }}
              />
            </div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-white">
              {analyticsData?.systemMetrics.activeConnections || 0}
            </div>
            <div className="text-sm text-gray-400">Active Jobs</div>
          </div>
        </div>
      </div>

      {/* Agent Performance */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
        <h3 className="text-lg font-bold text-white mb-4">Agent Performance</h3>
        
        <div className="space-y-4">
          {analyticsData?.agentPerformance.map((agent, index) => (
            <div key={agent.agent} className="flex items-center justify-between p-4 bg-gray-700/50 rounded-xl">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-red-500/20 to-red-600/20 rounded-lg flex items-center justify-center">
                  <Users className="w-5 h-5 text-red-400" />
                </div>
                <div>
                  <h4 className="font-semibold text-white">{agent.agent}</h4>
                  <p className="text-sm text-gray-400">{agent.tasksCompleted} tasks completed</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-6">
                <div className="text-center">
                  <div className="text-lg font-bold text-white">{agent.averageTime.toFixed(1)}s</div>
                  <div className="text-xs text-gray-400">Avg Time</div>
                </div>
                
                <div className="text-center">
                  <div className={`text-lg font-bold ${getPerformanceColor(agent.successRate)}`}>
                    {agent.successRate.toFixed(1)}%
                  </div>
                  <div className="text-xs text-gray-400">Success Rate</div>
                </div>
                
                <div className="w-16 bg-gray-600 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${agent.successRate}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Daily Stats Chart */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
        <h3 className="text-lg font-bold text-white mb-4">Processing Trends</h3>
        
        <div className="space-y-3">
          {analyticsData?.dailyStats.slice(-7).map((day, index) => (
            <div key={day.date} className="flex items-center justify-between p-3 bg-gray-700/30 rounded-lg">
              <div className="text-sm text-gray-300">
                {new Date(day.date).toLocaleDateString()}
              </div>
              
              <div className="flex items-center space-x-4">
                <div className="text-center">
                  <div className="text-sm font-bold text-white">{day.processed}</div>
                  <div className="text-xs text-gray-400">Processed</div>
                </div>
                
                <div className="text-center">
                  <div className={`text-sm font-bold ${getQualityColor(day.quality)}`}>
                    {day.quality.toFixed(1)}%
                  </div>
                  <div className="text-xs text-gray-400">Quality</div>
                </div>
                
                <div className="text-center">
                  <div className="text-sm font-bold text-red-400">{day.errors}</div>
                  <div className="text-xs text-gray-400">Errors</div>
                </div>
                
                <div className="w-20 bg-gray-600 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${(day.processed / 25) * 100}%` }}
                  />
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}







