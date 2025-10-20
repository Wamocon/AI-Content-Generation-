'use client'

import React, { useState, useEffect, useRef } from 'react'
import { 
  Terminal, 
  Play, 
  Pause, 
  Square, 
  Trash2, 
  Filter,
  Search,
  AlertCircle,
  CheckCircle,
  Clock,
  Activity
} from 'lucide-react'

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
  size?: number
}

interface APIFilter {
  method: string
  status: string
  search: string
}

export default function APIDebugConsole() {
  const [apiCalls, setApiCalls] = useState<APICall[]>([])
  const [isRecording, setIsRecording] = useState(true)
  const [filter, setFilter] = useState<APIFilter>({
    method: 'all',
    status: 'all',
    search: ''
  })
  const [selectedCall, setSelectedCall] = useState<APICall | null>(null)
  const [isExpanded, setIsExpanded] = useState(false)
  const callId = useRef(0)

  // Intercept fetch requests
  useEffect(() => {
    if (!isRecording) return

    const originalFetch = window.fetch
    window.fetch = async (...args) => {
      const startTime = Date.now()
      const callIdValue = callId.current++
      
      const [url, options] = args
      const method = options?.method || 'GET'
      
      try {
        const response = await originalFetch(...args)
        const endTime = Date.now()
        const duration = endTime - startTime
        
        // Clone response to read body
        const responseClone = response.clone()
        let responseData = null
        try {
          responseData = await responseClone.json()
        } catch {
          responseData = await responseClone.text()
        }
        
        const apiCall: APICall = {
          id: `call-${callIdValue}`,
          method,
          url: url.toString(),
          status: response.status,
          duration,
          timestamp: new Date().toISOString(),
          requestData: options?.body ? JSON.parse(options.body as string) : null,
          responseData,
          size: JSON.stringify(responseData).length
        }
        
        setApiCalls(prev => [apiCall, ...prev].slice(0, 100)) // Keep last 100 calls
        
        return response
      } catch (error) {
        const endTime = Date.now()
        const duration = endTime - startTime
        
        const apiCall: APICall = {
          id: `call-${callIdValue}`,
          method,
          url: url.toString(),
          status: 0,
          duration,
          timestamp: new Date().toISOString(),
          requestData: options?.body ? JSON.parse(options.body as string) : null,
          error: error instanceof Error ? error.message : 'Unknown error'
        }
        
        setApiCalls(prev => [apiCall, ...prev].slice(0, 100))
        throw error
      }
    }

    return () => {
      window.fetch = originalFetch
    }
  }, [isRecording])

  const clearCalls = () => {
    setApiCalls([])
  }

  const getStatusColor = (status: number) => {
    if (status >= 200 && status < 300) return 'text-green-400'
    if (status >= 300 && status < 400) return 'text-yellow-400'
    if (status >= 400) return 'text-red-400'
    return 'text-gray-400'
  }

  const getStatusIcon = (status: number) => {
    if (status >= 200 && status < 300) return <CheckCircle className="w-4 h-4 text-green-400" />
    if (status >= 400) return <AlertCircle className="w-4 h-4 text-red-400" />
    return <Clock className="w-4 h-4 text-gray-400" />
  }

  const getMethodColor = (method: string) => {
    switch (method.toUpperCase()) {
      case 'GET': return 'bg-blue-500'
      case 'POST': return 'bg-green-500'
      case 'PUT': return 'bg-yellow-500'
      case 'DELETE': return 'bg-red-500'
      case 'PATCH': return 'bg-purple-500'
      default: return 'bg-gray-500'
    }
  }

  const filteredCalls = apiCalls.filter(call => {
    if (filter.method !== 'all' && call.method.toUpperCase() !== filter.method) return false
    if (filter.status !== 'all') {
      const statusGroup = filter.status === 'success' ? '2xx' : 
                         filter.status === 'client-error' ? '4xx' : 
                         filter.status === 'server-error' ? '5xx' : 'all'
      if (statusGroup !== 'all') {
        const statusCode = Math.floor(call.status / 100)
        if (statusGroup === '2xx' && statusCode !== 2) return false
        if (statusGroup === '4xx' && statusCode !== 4) return false
        if (statusGroup === '5xx' && statusCode !== 5) return false
      }
    }
    if (filter.search && !call.url.toLowerCase().includes(filter.search.toLowerCase())) return false
    return true
  })

  const exportCalls = () => {
    const dataStr = JSON.stringify(apiCalls, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement('a')
    link.href = url
    link.download = `api-calls-${new Date().toISOString().split('T')[0]}.json`
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="bg-gray-900/90 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <Terminal className="w-6 h-6 text-red-400" />
          <h3 className="text-lg font-bold text-white">API Debug Console</h3>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setIsRecording(!isRecording)}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition-all duration-300 ${
              isRecording 
                ? 'bg-red-500 hover:bg-red-600 text-white' 
                : 'bg-gray-700 hover:bg-gray-600 text-white'
            }`}
          >
            {isRecording ? (
              <>
                <Pause className="w-4 h-4 inline mr-1" />
                Recording
              </>
            ) : (
              <>
                <Play className="w-4 h-4 inline mr-1" />
                Start Recording
              </>
            )}
          </button>
          
          <button
            onClick={clearCalls}
            className="bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded-lg text-sm font-medium transition-all duration-300"
          >
            <Trash2 className="w-4 h-4 inline mr-1" />
            Clear
          </button>
          
          <button
            onClick={exportCalls}
            className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded-lg text-sm font-medium transition-all duration-300"
          >
            Export
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="flex items-center space-x-4 mb-4">
        <div className="flex items-center space-x-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <select
            value={filter.method}
            onChange={(e) => setFilter(prev => ({ ...prev, method: e.target.value }))}
            className="bg-gray-700 text-white px-2 py-1 rounded text-sm border border-gray-600"
          >
            <option value="all">All Methods</option>
            <option value="GET">GET</option>
            <option value="POST">POST</option>
            <option value="PUT">PUT</option>
            <option value="DELETE">DELETE</option>
            <option value="PATCH">PATCH</option>
          </select>
        </div>
        
        <select
          value={filter.status}
          onChange={(e) => setFilter(prev => ({ ...prev, status: e.target.value }))}
          className="bg-gray-700 text-white px-2 py-1 rounded text-sm border border-gray-600"
        >
          <option value="all">All Status</option>
          <option value="success">2xx Success</option>
          <option value="client-error">4xx Client Error</option>
          <option value="server-error">5xx Server Error</option>
        </select>
        
        <div className="flex items-center space-x-2">
          <Search className="w-4 h-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search URL..."
            value={filter.search}
            onChange={(e) => setFilter(prev => ({ ...prev, search: e.target.value }))}
            className="bg-gray-700 text-white px-2 py-1 rounded text-sm border border-gray-600 w-48"
          />
        </div>
      </div>

      {/* API Calls List */}
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {filteredCalls.length === 0 ? (
          <div className="text-center py-8 text-gray-400">
            {isRecording ? 'No API calls recorded yet' : 'Recording is paused'}
          </div>
        ) : (
          filteredCalls.map((call) => (
            <div
              key={call.id}
              className={`p-3 rounded-lg border cursor-pointer transition-all duration-300 hover:bg-gray-800/50 ${
                selectedCall?.id === call.id ? 'bg-gray-800/50 border-red-500/50' : 'bg-gray-800/30 border-gray-700/50'
              }`}
              onClick={() => setSelectedCall(call)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className={`px-2 py-1 rounded text-xs font-bold text-white ${getMethodColor(call.method)}`}>
                    {call.method}
                  </span>
                  
                  <div className="flex items-center space-x-2">
                    {getStatusIcon(call.status)}
                    <span className={`text-sm font-medium ${getStatusColor(call.status)}`}>
                      {call.status || 'Error'}
                    </span>
                  </div>
                  
                  <span className="text-sm text-gray-300 truncate max-w-md">
                    {call.url}
                  </span>
                </div>
                
                <div className="flex items-center space-x-4 text-sm text-gray-400">
                  <span>{call.duration}ms</span>
                  <span>{new Date(call.timestamp).toLocaleTimeString()}</span>
                  {call.size && <span>{call.size} bytes</span>}
                </div>
              </div>
              
              {call.error && (
                <div className="mt-2 text-sm text-red-400">
                  Error: {call.error}
                </div>
              )}
            </div>
          ))
        )}
      </div>

      {/* Call Details */}
      {selectedCall && (
        <div className="mt-4 border-t border-gray-700/50 pt-4">
          <div className="flex items-center justify-between mb-2">
            <h4 className="text-sm font-bold text-white">Call Details</h4>
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-sm text-gray-400 hover:text-white"
            >
              {isExpanded ? 'Collapse' : 'Expand'}
            </button>
          </div>
          
          <div className="bg-black/50 rounded-lg p-3 font-mono text-sm">
            <div className="space-y-2">
              <div>
                <span className="text-gray-400">Method:</span>
                <span className="ml-2 text-white">{selectedCall.method}</span>
              </div>
              
              <div>
                <span className="text-gray-400">URL:</span>
                <span className="ml-2 text-white break-all">{selectedCall.url}</span>
              </div>
              
              <div>
                <span className="text-gray-400">Status:</span>
                <span className={`ml-2 ${getStatusColor(selectedCall.status)}`}>
                  {selectedCall.status || 'Error'}
                </span>
              </div>
              
              <div>
                <span className="text-gray-400">Duration:</span>
                <span className="ml-2 text-white">{selectedCall.duration}ms</span>
              </div>
              
              <div>
                <span className="text-gray-400">Timestamp:</span>
                <span className="ml-2 text-white">{new Date(selectedCall.timestamp).toLocaleString()}</span>
              </div>
              
              {isExpanded && (
                <>
                  {selectedCall.requestData && (
                    <div>
                      <span className="text-gray-400">Request:</span>
                      <pre className="mt-1 text-green-400 overflow-x-auto">
                        {JSON.stringify(selectedCall.requestData, null, 2)}
                      </pre>
                    </div>
                  )}
                  
                  {selectedCall.responseData && (
                    <div>
                      <span className="text-gray-400">Response:</span>
                      <pre className="mt-1 text-blue-400 overflow-x-auto">
                        {JSON.stringify(selectedCall.responseData, null, 2)}
                      </pre>
                    </div>
                  )}
                  
                  {selectedCall.error && (
                    <div>
                      <span className="text-gray-400">Error:</span>
                      <pre className="mt-1 text-red-400 overflow-x-auto">
                        {selectedCall.error}
                      </pre>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Stats */}
      <div className="mt-4 pt-4 border-t border-gray-700/50">
        <div className="flex items-center justify-between text-sm text-gray-400">
          <span>Total Calls: {apiCalls.length}</span>
          <span>Filtered: {filteredCalls.length}</span>
          <span>Success Rate: {apiCalls.length > 0 ? Math.round((apiCalls.filter(c => c.status >= 200 && c.status < 300).length / apiCalls.length) * 100) : 0}%</span>
        </div>
      </div>
    </div>
  )
}







