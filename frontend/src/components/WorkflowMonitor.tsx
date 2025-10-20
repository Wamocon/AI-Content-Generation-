'use client'

import React, { useState, useEffect, useRef } from 'react'
import { 
  Play, 
  Pause, 
  Square, 
  RefreshCw, 
  CheckCircle, 
  AlertCircle, 
  Clock, 
  FileText,
  Database,
  Users,
  BarChart3,
  Zap,
  Activity,
  Terminal,
  Eye,
  EyeOff
} from 'lucide-react'

interface WorkflowStep {
  id: string
  name: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  startTime?: string
  endTime?: string
  duration?: number
  message?: string
  agent?: string
  progress?: number
}

interface WorkflowMetrics {
  totalSteps: number
  completedSteps: number
  failedSteps: number
  totalDuration: number
  averageStepDuration: number
  successRate: number
}

interface APICall {
  id: string
  method: string
  url: string
  status: number
  duration: number
  timestamp: string
  requestData?: any
  responseData?: any
  error?: string
}

export default function WorkflowMonitor() {
  const [isRunning, setIsRunning] = useState(false)
  const [workflowSteps, setWorkflowSteps] = useState<WorkflowStep[]>([])
  const [metrics, setMetrics] = useState<WorkflowMetrics | null>(null)
  const [apiCalls, setApiCalls] = useState<APICall[]>([])
  const [showDebugConsole, setShowDebugConsole] = useState(false)
  const [wsConnected, setWsConnected] = useState(false)
  const [currentStep, setCurrentStep] = useState<string | null>(null)
  const wsRef = useRef<WebSocket | null>(null)
  const apiCallId = useRef(0)

  // Mock workflow steps for demonstration
  const mockSteps: WorkflowStep[] = [
    { id: 'discover', name: 'Document Discovery', status: 'pending', agent: 'Document Discovery Agent' },
    { id: 'analyze', name: 'Content Analysis', status: 'pending', agent: 'Content Analyst' },
    { id: 'generate', name: 'Content Generation', status: 'pending', agent: 'Presentation Creator' },
    { id: 'validate', name: 'Quality Validation', status: 'pending', agent: 'Quality Assurance' },
    { id: 'upload', name: 'Content Upload', status: 'pending', agent: 'Content Distribution Agent' },
    { id: 'track', name: 'Progress Tracking', status: 'pending', agent: 'Monitoring Agent' }
  ]

  // WebSocket connection for real-time updates
  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://localhost:8000/ws')
      wsRef.current = ws

      ws.onopen = () => {
        setWsConnected(true)
        console.log('🔌 Workflow Monitor WebSocket connected')
      }

      ws.onclose = () => {
        setWsConnected(false)
        console.log('🔌 Workflow Monitor WebSocket disconnected')
        // Reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000)
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          handleWebSocketMessage(data)
        } catch (error) {
          console.log('📨 Raw WebSocket message:', event.data)
        }
      }

      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
        setWsConnected(false)
      }
    }

    connectWebSocket()

    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  const handleWebSocketMessage = (data: any) => {
    console.log('📨 WebSocket message received:', data)

    if (data.type === 'workflow_step_start') {
      setWorkflowSteps(prev => prev.map(step => 
        step.id === data.stepId 
          ? { ...step, status: 'running', startTime: new Date().toISOString(), progress: 0 }
          : step
      ))
      setCurrentStep(data.stepId)
    } else if (data.type === 'workflow_step_progress') {
      setWorkflowSteps(prev => prev.map(step => 
        step.id === data.stepId 
          ? { ...step, progress: data.progress, message: data.message }
          : step
      ))
    } else if (data.type === 'workflow_step_complete') {
      setWorkflowSteps(prev => prev.map(step => 
        step.id === data.stepId 
          ? { 
              ...step, 
              status: 'completed', 
              endTime: new Date().toISOString(),
              duration: data.duration,
              message: data.message
            }
          : step
      ))
      setCurrentStep(null)
    } else if (data.type === 'workflow_step_error') {
      setWorkflowSteps(prev => prev.map(step => 
        step.id === data.stepId 
          ? { 
              ...step, 
              status: 'failed', 
              endTime: new Date().toISOString(),
              message: data.error
            }
          : step
      ))
      setCurrentStep(null)
    } else if (data.type === 'workflow_complete') {
      setIsRunning(false)
      setCurrentStep(null)
      updateMetrics()
    }
  }

  const updateMetrics = () => {
    const completed = workflowSteps.filter(s => s.status === 'completed').length
    const failed = workflowSteps.filter(s => s.status === 'failed').length
    const total = workflowSteps.length
    
    const newMetrics: WorkflowMetrics = {
      totalSteps: total,
      completedSteps: completed,
      failedSteps: failed,
      totalDuration: workflowSteps.reduce((sum, step) => sum + (step.duration || 0), 0),
      averageStepDuration: workflowSteps.reduce((sum, step) => sum + (step.duration || 0), 0) / total,
      successRate: total > 0 ? (completed / total) * 100 : 0
    }
    
    setMetrics(newMetrics)
  }

  const startWorkflow = async () => {
    setIsRunning(true)
    setWorkflowSteps(mockSteps.map(step => ({ ...step, status: 'pending' })))
    setCurrentStep(null)
    setMetrics(null)

    // Simulate workflow execution
    for (let i = 0; i < mockSteps.length; i++) {
      const step = mockSteps[i]
      
      // Start step
      setWorkflowSteps(prev => prev.map(s => 
        s.id === step.id 
          ? { ...s, status: 'running', startTime: new Date().toISOString(), progress: 0 }
          : s
      ))
      setCurrentStep(step.id)

      // Simulate progress
      for (let progress = 0; progress <= 100; progress += 20) {
        await new Promise(resolve => setTimeout(resolve, 200))
        setWorkflowSteps(prev => prev.map(s => 
          s.id === step.id 
            ? { ...s, progress, message: `Processing ${step.name}...` }
            : s
        ))
      }

      // Complete step
      const duration = Math.random() * 2000 + 1000 // 1-3 seconds
      setWorkflowSteps(prev => prev.map(s => 
        s.id === step.id 
          ? { 
              ...s, 
              status: 'completed', 
              endTime: new Date().toISOString(),
              duration,
              progress: 100,
              message: `${step.name} completed successfully`
            }
          : s
      ))
      setCurrentStep(null)
    }

    setIsRunning(false)
    updateMetrics()
  }

  const stopWorkflow = () => {
    setIsRunning(false)
    setCurrentStep(null)
    setWorkflowSteps(prev => prev.map(step => 
      step.status === 'running' 
        ? { ...step, status: 'failed', endTime: new Date().toISOString(), message: 'Workflow stopped by user' }
        : step
    ))
  }

  const resetWorkflow = () => {
    setIsRunning(false)
    setCurrentStep(null)
    setWorkflowSteps(mockSteps.map(step => ({ ...step, status: 'pending' })))
    setMetrics(null)
  }

  const getStepStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-400" />
      case 'running':
        return <Activity className="w-5 h-5 text-blue-400 animate-pulse" />
      case 'failed':
        return <AlertCircle className="w-5 h-5 text-red-400" />
      default:
        return <Clock className="w-5 h-5 text-gray-400" />
    }
  }

  const getStepStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'border-green-500/30 bg-green-500/10'
      case 'running':
        return 'border-blue-500/30 bg-blue-500/10'
      case 'failed':
        return 'border-red-500/30 bg-red-500/10'
      default:
        return 'border-gray-500/30 bg-gray-500/10'
    }
  }

  return (
    <div className="space-y-6">
      {/* Workflow Controls */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <Zap className="w-6 h-6 text-red-400" />
            <h2 className="text-xl font-bold text-white">Workflow Monitor</h2>
          </div>
          
          <div className="flex items-center space-x-2">
            <div className={`w-3 h-3 rounded-full animate-pulse ${
              wsConnected ? 'bg-green-400 shadow-lg shadow-green-400/50' : 'bg-red-400 shadow-lg shadow-red-400/50'
            }`} />
            <span className="text-sm text-gray-300">
              {wsConnected ? 'Live' : 'Offline'}
            </span>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <button
            onClick={startWorkflow}
            disabled={isRunning}
            className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 disabled:from-gray-500 disabled:to-gray-600 text-white font-semibold py-2 px-4 rounded-xl transition-all duration-300 hover:scale-105 flex items-center space-x-2"
          >
            <Play className="w-4 h-4" />
            <span>Start Workflow</span>
          </button>

          <button
            onClick={stopWorkflow}
            disabled={!isRunning}
            className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 disabled:from-gray-500 disabled:to-gray-600 text-white font-semibold py-2 px-4 rounded-xl transition-all duration-300 hover:scale-105 flex items-center space-x-2"
          >
            <Square className="w-4 h-4" />
            <span>Stop</span>
          </button>

          <button
            onClick={resetWorkflow}
            className="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded-xl transition-all duration-300 hover:scale-105 flex items-center space-x-2"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Reset</span>
          </button>

          <button
            onClick={() => setShowDebugConsole(!showDebugConsole)}
            className="bg-gray-700 hover:bg-gray-600 text-white font-semibold py-2 px-4 rounded-xl transition-all duration-300 hover:scale-105 flex items-center space-x-2"
          >
            {showDebugConsole ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            <span>Debug Console</span>
          </button>
        </div>
      </div>

      {/* Workflow Steps */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
        <h3 className="text-lg font-bold text-white mb-4">Workflow Steps</h3>
        
        <div className="space-y-3">
          {workflowSteps.map((step, index) => (
            <div key={step.id} className={`p-4 rounded-xl border transition-all duration-300 ${getStepStatusColor(step.status)}`}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center space-x-3">
                  {getStepStatusIcon(step.status)}
                  <div>
                    <h4 className="font-semibold text-white">{step.name}</h4>
                    <p className="text-sm text-gray-400">{step.agent}</p>
                  </div>
                </div>
                
                <div className="text-right">
                  {step.duration && (
                    <p className="text-sm text-gray-300">
                      {(step.duration / 1000).toFixed(2)}s
                    </p>
                  )}
                  {step.status === 'running' && step.progress !== undefined && (
                    <p className="text-sm text-blue-400">{step.progress}%</p>
                  )}
                </div>
              </div>
              
              {step.status === 'running' && step.progress !== undefined && (
                <div className="w-full bg-gray-700 rounded-full h-2 mb-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${step.progress}%` }}
                  />
                </div>
              )}
              
              {step.message && (
                <p className="text-sm text-gray-300">{step.message}</p>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Metrics */}
      {metrics && (
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
          <h3 className="text-lg font-bold text-white mb-4">Workflow Metrics</h3>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-white">{metrics.totalSteps}</div>
              <div className="text-sm text-gray-400">Total Steps</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-green-400">{metrics.completedSteps}</div>
              <div className="text-sm text-gray-400">Completed</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-red-400">{metrics.failedSteps}</div>
              <div className="text-sm text-gray-400">Failed</div>
            </div>
            
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-400">{metrics.successRate.toFixed(1)}%</div>
              <div className="text-sm text-gray-400">Success Rate</div>
            </div>
          </div>
        </div>
      )}

      {/* Debug Console */}
      {showDebugConsole && (
        <div className="bg-gray-900/90 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
          <div className="flex items-center space-x-3 mb-4">
            <Terminal className="w-5 h-5 text-red-400" />
            <h3 className="text-lg font-bold text-white">Debug Console</h3>
          </div>
          
          <div className="bg-black/50 rounded-lg p-4 font-mono text-sm text-green-400 max-h-64 overflow-y-auto">
            <div className="space-y-1">
              <div>[{new Date().toLocaleTimeString()}] WebSocket: {wsConnected ? 'Connected' : 'Disconnected'}</div>
              <div>[{new Date().toLocaleTimeString()}] Workflow Status: {isRunning ? 'Running' : 'Stopped'}</div>
              {currentStep && (
                <div>[{new Date().toLocaleTimeString()}] Current Step: {currentStep}</div>
              )}
              {metrics && (
                <div>[{new Date().toLocaleTimeString()}] Total Duration: {(metrics.totalDuration / 1000).toFixed(2)}s</div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}







