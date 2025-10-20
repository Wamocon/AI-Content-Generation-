'use client'

import React, { useState, useEffect } from 'react'
import { 
  Brain, 
  Upload, 
  Play, 
  Activity, 
  CheckCircle, 
  AlertCircle, 
  Loader2,
  FileText,
  Zap,
  Database,
  Users,
  BarChart3,
  Terminal,
  Eye,
  EyeOff
} from 'lucide-react'
import WorkflowMonitor from '@/components/WorkflowMonitor'
import AnalyticsDashboard from '@/components/AnalyticsDashboard'
import APIDebugConsole from '@/components/APIDebugConsole'
import ReviewQueue from '@/components/ReviewQueue'

// ==========================================
// SIMPLE MODERN UI - SINGLE PAGE APPLICATION
// ==========================================

interface ServiceStatus {
  name: string
  status: 'healthy' | 'unavailable' | 'error' | 'checking'
  message: string
  icon: React.ComponentType<any>
}

interface SystemHealth {
  status: string
  timestamp: string
  dependencies: Record<string, string>
}

export default function FIAEDashboard() {
  // State management
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null)
  const [serviceStatuses, setServiceStatuses] = useState<ServiceStatus[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [processingStatus, setProcessingStatus] = useState<string>('')
  const [wsConnected, setWsConnected] = useState(false)
  const [activeTab, setActiveTab] = useState<'dashboard' | 'workflow' | 'analytics' | 'review' | 'debug'>('dashboard')
  const [currentJobId, setCurrentJobId] = useState<string | null>(null)
  const [isAutomationRunning, setIsAutomationRunning] = useState(false)
  const [showDebugConsole, setShowDebugConsole] = useState(false)

  // Service definitions
  const services: ServiceStatus[] = [
    {
      name: 'CrewAI Orchestrator',
      status: 'checking',
      message: 'Checking status...',
      icon: Users
    },
    {
      name: 'RAG System',
      status: 'checking', 
      message: 'Checking status...',
      icon: Database
    },
    {
      name: 'Content Intelligence',
      status: 'checking',
      message: 'Checking status...',
      icon: BarChart3
    },
    {
      name: 'Google Services',
      status: 'checking',
      message: 'Checking status...',
      icon: CheckCircle
    }
  ]

  // Fetch system health and service statuses
  const fetchSystemStatus = async () => {
    try {
      setIsLoading(true)
      
      // Fetch system health
      const healthResponse = await fetch('http://localhost:8000/health')
      const healthData = await healthResponse.json()
      setSystemHealth(healthData)

      // Fetch individual service statuses
      const crewaiResponse = await fetch('http://localhost:8000/crewai/status')
      const crewaiData = await crewaiResponse.json()
      
      const ragResponse = await fetch('http://localhost:8000/rag/status')
      const ragData = await ragResponse.json()
      
      const contentResponse = await fetch('http://localhost:8000/content-intelligence/analytics')
      const contentData = await contentResponse.json()

      // Update service statuses
      setServiceStatuses([
        {
          name: 'CrewAI Orchestrator',
          status: crewaiData.success ? 'healthy' : 'unavailable',
          message: crewaiData.success ? 'Available with 6 agents' : crewaiData.error || 'Unavailable',
          icon: Users
        },
        {
          name: 'RAG System',
          status: ragData.success ? 'healthy' : 'unavailable',
          message: ragData.success ? 'Available' : ragData.error || 'Unavailable',
          icon: Database
        },
        {
          name: 'Content Intelligence',
          status: contentData.success ? 'healthy' : 'unavailable',
          message: contentData.success ? 'Analytics available' : contentData.error || 'Unavailable',
          icon: BarChart3
        },
        {
          name: 'Google Services',
          status: healthData.dependencies?.google_drive === 'healthy' ? 'healthy' : 'unavailable',
          message: healthData.dependencies?.google_drive === 'healthy' ? 'Drive & Sheets connected' : 'Not connected',
          icon: CheckCircle
        }
      ])

    } catch (error) {
      console.error('Failed to fetch system status:', error)
      setServiceStatuses(services.map(s => ({ ...s, status: 'error', message: 'Connection failed' })))
    } finally {
      setIsLoading(false)
    }
  }

  // Handle Google Drive processing
  const handleGoogleDriveProcessing = async () => {
    setProcessingStatus('Discovering documents in Google Drive...')
    setIsAutomationRunning(true)

    try {
      // Step 1: Discover documents in Google Drive
      const discoverResponse = await fetch('http://localhost:8000/discover-documents')
      const discoverResult = await discoverResponse.json()
      
      if (!discoverResult.success) {
        throw new Error(discoverResult.message || 'Failed to discover documents')
      }

      setProcessingStatus(`✅ Found ${discoverResult.statistics?.total_documents || 0} documents in Google Drive. Starting processing...`)

      // Step 2: Start comprehensive batch processing
      const jobId = `batch_${Date.now()}`
      setCurrentJobId(jobId)
      
      const processResponse = await fetch('http://localhost:8000/process-comprehensive-batch', {
        method: 'POST'
      })

      if (!processResponse.ok) {
        throw new Error('Failed to start batch processing')
      }

      const processResult = await processResponse.json()
      
      if (processResult.success) {
        setProcessingStatus('✅ Google Drive document processing started successfully! Check the logs for real-time progress.')
      } else {
        setProcessingStatus(`❌ Failed to start processing: ${processResult.detail}`)
        setIsAutomationRunning(false)
      }
    } catch (error) {
      setProcessingStatus(`❌ Google Drive processing failed: ${error instanceof Error ? error.message : 'Unknown error'}`)
      setIsAutomationRunning(false)
    }
  }
  
  // Abort automation
  const handleAbortAutomation = async () => {
    if (!currentJobId) return
    
    if (!confirm('Are you sure you want to abort the running automation?\n\nThis will stop all processing immediately.')) {
      return
    }
    
    try {
      const response = await fetch(`http://localhost:8000/abort-automation/${currentJobId}`, {
        method: 'POST'
      })
      
      const result = await response.json()
      
      if (result.success) {
        setProcessingStatus('🛑 Automation aborted successfully')
        setIsAutomationRunning(false)
        setCurrentJobId(null)
      } else {
        setProcessingStatus(`❌ Failed to abort: ${result.message || 'Unknown error'}`)
      }
    } catch (error) {
      setProcessingStatus(`❌ Abort failed: ${error}`)
    }
  }

  // Start CrewAI workflow
  const startWorkflow = async () => {
    setProcessingStatus('Starting CrewAI workflow...')
    
    try {
      const response = await fetch('http://localhost:8000/crewai/run-workflow', {
        method: 'POST'
      })
      
      const result = await response.json()
      
      if (result.success) {
        setProcessingStatus(`✅ Workflow completed in ${result.processing_time_seconds?.toFixed(2)}s`)
      } else {
        setProcessingStatus(`❌ Workflow failed: ${result.error}`)
      }
    } catch (error) {
      setProcessingStatus(`❌ Workflow failed: ${error}`)
    }
  }

  // Enhanced WebSocket connection with progress tracking
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws')
    
    ws.onopen = () => {
      setWsConnected(true)
      console.log('🔌 WebSocket connected to backend')
      setProcessingStatus('🔌 Connected to automation engine')
    }
    
    ws.onclose = () => {
      setWsConnected(false)
      console.log('🔌 WebSocket disconnected from backend')
      setProcessingStatus('🔌 Disconnected from automation engine')
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('📨 WebSocket message received:', data)
        
        if (data.type === 'progress') {
          setProcessingStatus(`🔄 ${data.message}`)
        } else if (data.type === 'complete') {
          setProcessingStatus(`✅ ${data.message}`)
          setIsAutomationRunning(false)
          // Show notification to check Review Queue
          setTimeout(() => {
            setProcessingStatus(`✅ ${data.message} - Check Review Queue tab for approvals!`)
          }, 1000)
        } else if (data.type === 'error') {
          setProcessingStatus(`❌ ${data.message}`)
          setIsAutomationRunning(false)
        }
      } catch (error) {
        console.log('📨 Raw WebSocket message:', event.data)
        setProcessingStatus(`📨 ${event.data}`)
      }
    }

    ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error)
      setProcessingStatus('❌ WebSocket connection error')
    }

    return () => ws.close()
  }, [])

  // Initial load
  useEffect(() => {
    fetchSystemStatus()
    const interval = setInterval(fetchSystemStatus, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  // Render functions
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="w-5 h-5 text-green-400" />
      case 'unavailable':
        return <AlertCircle className="w-5 h-5 text-red-400" />
      case 'error':
        return <AlertCircle className="w-5 h-5 text-red-500" />
      default:
        return <Loader2 className="w-5 h-5 text-gray-400 animate-spin" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'border-green-500/30 bg-green-500/10'
      case 'unavailable':
        return 'border-red-500/30 bg-red-500/10'
      case 'error':
        return 'border-red-500/30 bg-red-500/20'
      default:
        return 'border-gray-500/30 bg-gray-500/10'
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
      {/* Header */}
      <div className="bg-gray-900/95 backdrop-blur-sm border-b border-gray-700/50 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-red-500 to-red-700 rounded-xl flex items-center justify-center shadow-lg border border-red-500/30">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">FIAE AI Content Factory</h1>
                <p className="text-xs text-gray-400">Intelligent Document Processing</p>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full animate-pulse ${
                  wsConnected ? 'bg-green-400 shadow-lg shadow-green-400/50' : 'bg-red-400 shadow-lg shadow-red-400/50'
                }`} />
                <span className="text-sm font-medium text-white">
                  {wsConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Welcome Section */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-white via-red-400 to-red-600 bg-clip-text text-transparent mb-4">
            FIAE AI Content Factory
          </h1>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto">
            Next-generation intelligent document processing and automation platform
          </p>
        </div>

        {/* Navigation Tabs */}
        <div className="flex justify-center mb-8">
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700/50 p-1">
            <div className="flex space-x-1">
              {[
                { id: 'dashboard', label: 'Dashboard', icon: Brain },
                { id: 'workflow', label: 'Workflow', icon: Zap },
                { id: 'analytics', label: 'Analytics', icon: BarChart3 },
                { id: 'review', label: 'Review Queue', icon: CheckCircle },
                { id: 'debug', label: 'Debug', icon: Terminal }
              ].map((tab) => {
                const Icon = tab.icon
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-300 flex items-center space-x-2 ${
                      activeTab === tab.id
                        ? 'bg-red-500 text-white shadow-lg'
                        : 'text-gray-400 hover:text-white hover:bg-gray-700/50'
                    }`}
                  >
                    <Icon className="w-4 h-4" />
                    <span>{tab.label}</span>
                  </button>
                )
              })}
            </div>
          </div>
        </div>

        {/* Tab Content */}
        {activeTab === 'dashboard' && (
          <>
            {/* System Status */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {serviceStatuses.map((service, index) => {
                const Icon = service.icon
                return (
                  <div key={service.name} className={`group relative bg-gray-800/50 backdrop-blur-sm rounded-2xl border p-6 hover:scale-105 transition-all duration-500 hover:shadow-2xl ${getStatusColor(service.status)}`}>
                    <div className="absolute inset-0 bg-gradient-to-br from-red-500/5 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
                    <div className="relative">
                      <div className="flex items-center justify-between mb-4">
                        <div className={`p-3 rounded-xl border ${
                          service.status === 'healthy' ? 'bg-green-500/20 border-green-500/30' :
                          service.status === 'unavailable' ? 'bg-red-500/20 border-red-500/30' :
                          'bg-gray-500/20 border-gray-500/30'
                        }`}>
                          <Icon className={`w-6 h-6 ${
                            service.status === 'healthy' ? 'text-green-400' :
                            service.status === 'unavailable' ? 'text-red-400' :
                            'text-gray-400'
                          }`} />
                        </div>
                        {getStatusIcon(service.status)}
                      </div>
                      <h3 className="font-semibold text-white text-lg mb-2">{service.name}</h3>
                      <p className="text-sm text-gray-300">{service.message}</p>
                    </div>
                  </div>
                )
              })}
            </div>

            {/* Main Actions */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              
              {/* Google Drive Processing */}
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-8">
                <div className="flex items-center space-x-3 mb-6">
                  <Database className="w-6 h-6 text-red-400" />
                  <h2 className="text-xl font-bold text-white">Google Drive Processing</h2>
                </div>
                
                <div className="space-y-4">
                  <div className="bg-gradient-to-r from-red-500/10 to-red-600/10 border border-red-500/30 rounded-xl p-6">
                    <div className="flex items-center space-x-3 mb-4">
                      <CheckCircle className="w-6 h-6 text-green-400" />
                      <h3 className="text-white font-semibold">Automated Workflow</h3>
                    </div>
                    <p className="text-gray-300 text-sm mb-4">
                      Process all .docx documents from your Google Drive source folder automatically. 
                      The system will discover, analyze, and generate comprehensive educational content.
                    </p>
                    <ul className="text-sm text-gray-400 space-y-1">
                      <li>• Auto-discovers .docx files in source folder</li>
                      <li>• Dynamic content generation (no limits)</li>
                      <li>• 100% topic coverage guaranteed</li>
                      <li>• Real-time progress monitoring</li>
                    </ul>
                  </div>
                  
                  <button
                    onClick={handleGoogleDriveProcessing}
                    disabled={isAutomationRunning}
                    className="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 disabled:from-gray-500 disabled:to-gray-600 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 hover:scale-105 hover:shadow-lg flex items-center justify-center space-x-3"
                  >
                    <Play className="w-5 h-5" />
                    <span>{isAutomationRunning ? 'Automation Running...' : 'Start Google Drive Processing'}</span>
                  </button>
                  
                  {isAutomationRunning && (
                    <button
                      onClick={handleAbortAutomation}
                      className="w-full bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 hover:scale-105 hover:shadow-lg flex items-center justify-center space-x-3 border-2 border-red-400"
                    >
                      <AlertCircle className="w-5 h-5" />
                      <span>🛑 Abort Automation</span>
                    </button>
                  )}
                  
                  {processingStatus && (
                    <div className="bg-gray-700/50 rounded-xl p-4">
                      <p className="text-white">{processingStatus}</p>
                    </div>
                  )}
                </div>
              </div>

              {/* Testing Workflow */}
              <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-8">
                <div className="flex items-center space-x-3 mb-6">
                  <Zap className="w-6 h-6 text-red-400" />
                  <h2 className="text-xl font-bold text-white">Testing Workflow</h2>
                </div>
                
                <div className="space-y-4">
                  <div className="bg-gradient-to-r from-yellow-500/10 to-yellow-600/10 border border-yellow-500/30 rounded-xl p-6">
                    <div className="flex items-center space-x-3 mb-4">
                      <AlertCircle className="w-6 h-6 text-yellow-400" />
                      <h3 className="text-white font-semibold">Test Mode</h3>
                    </div>
                    <p className="text-gray-300 text-sm mb-4">
                      This button runs a test workflow with sample content to verify the AI agents are working correctly.
                      For production use, use the Google Drive Processing above.
                    </p>
                  </div>
                  
                  <button
                    onClick={startWorkflow}
                    className="w-full bg-gradient-to-r from-yellow-500 to-yellow-600 hover:from-yellow-600 hover:to-yellow-700 text-white font-semibold py-3 px-6 rounded-xl transition-all duration-300 hover:scale-105 hover:shadow-lg flex items-center justify-center space-x-3"
                  >
                    <Play className="w-5 h-5" />
                    <span>Test CrewAI Workflow</span>
                  </button>
                  
                  <div className="bg-gray-700/50 rounded-xl p-4">
                    <h3 className="text-white font-semibold mb-2">6 AI Agents</h3>
                    <ul className="text-sm text-gray-300 space-y-1">
                      <li>• Content Analyst - Knowledge extraction</li>
                      <li>• Presentation Creator - PowerPoint & Slides</li>
                      <li>• Use Case Developer - IT scenarios</li>
                      <li>• Quiz Master - Assessment questions</li>
                      <li>• Trainer Writer - Presentation scripts</li>
                      <li>• Quality Assurance - Content validation</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            {/* System Information */}
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-8">
              <div className="flex items-center space-x-3 mb-6">
                <Activity className="w-6 h-6 text-red-400" />
                <h2 className="text-xl font-bold text-white">System Information</h2>
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <h3 className="text-white font-semibold mb-2">System Health</h3>
                  <p className={`text-sm ${systemHealth?.status === 'healthy' ? 'text-green-400' : 'text-red-400'}`}>
                    {systemHealth?.status?.toUpperCase() || 'CHECKING...'}
                  </p>
                </div>
                
                <div>
                  <h3 className="text-white font-semibold mb-2">Last Updated</h3>
                  <p className="text-sm text-gray-300">
                    {systemHealth?.timestamp ? new Date(systemHealth.timestamp).toLocaleTimeString() : 'Never'}
                  </p>
                </div>
                
                <div>
                  <h3 className="text-white font-semibold mb-2">API Version</h3>
                  <p className="text-sm text-gray-300">v2.0.0</p>
                </div>
              </div>
            </div>

            {/* Refresh Button */}
            <div className="text-center mt-8">
              <button
                onClick={fetchSystemStatus}
                disabled={isLoading}
                className="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-2 px-6 rounded-xl transition-all duration-300 hover:scale-105 flex items-center space-x-2 mx-auto"
              >
                {isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Activity className="w-4 h-4" />
                )}
                <span>Refresh Status</span>
              </button>
            </div>
          </>
        )}

        {activeTab === 'workflow' && <WorkflowMonitor />}
        {activeTab === 'analytics' && <AnalyticsDashboard />}
        {activeTab === 'review' && <ReviewQueue />}
        {activeTab === 'debug' && <APIDebugConsole />}

      </div>
    </div>
  )
}