'use client'

import React, { useState, useEffect } from 'react'
import {
  CheckCircle,
  XCircle,
  Clock,
  FileText,
  FolderOpen,
  RefreshCw,
  ExternalLink,
  AlertCircle
} from 'lucide-react'

interface ReviewItem {
  row_number: number
  document_name: string
  source_file_id: string
  processing_date: string
  processing_status: string
  review_status: string
  output_folder_id: string
  output_files: string
  quality_score: number
  processing_time: number
}

interface ReviewStats {
  total_documents: number
  pending_review: number
  approved: number
  rejected: number
}

export default function ReviewQueue() {
  const [reviewItems, setReviewItems] = useState<ReviewItem[]>([])
  const [stats, setStats] = useState<ReviewStats | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [selectedItem, setSelectedItem] = useState<ReviewItem | null>(null)
  const [approveNotes, setApproveNotes] = useState('')

  // Fetch pending reviews
  const fetchReviews = async () => {
    try {
      setIsLoading(true)
      
      // Fetch pending reviews
      const reviewsResponse = await fetch('http://localhost:8000/hitl/pending-approvals')
      const reviewsData = await reviewsResponse.json()
      
      // Fetch statistics
      const statsResponse = await fetch('http://localhost:8000/hitl/statistics')
      const statsData = await statsResponse.json()
      
      setReviewItems(reviewsData.pending_approvals || [])
      setStats(statsData.statistics || null)
      
    } catch (error) {
      console.error('Failed to fetch reviews:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Auto-refresh every 60 seconds (polls Google Sheets - FREE API)
  useEffect(() => {
    fetchReviews()
    const interval = setInterval(fetchReviews, 60000) // 60 seconds
    return () => clearInterval(interval)
  }, [])

  // Approve document
  const handleApprove = async (rowNumber: number, documentName: string) => {
    if (!confirm(`Approve "${documentName}"?\n\nThis will move the files to the Done folder.`)) {
      return
    }

    try {
      const response = await fetch(`http://localhost:8000/hitl/approve/${rowNumber}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          approved_by: 'User',
          notes: approveNotes
        })
      })

      const result = await response.json()

      if (result.success) {
        alert(`✅ Approved: ${documentName}\n\nFiles moved to Done folder!`)
        setApproveNotes('')
        fetchReviews() // Refresh list
      } else {
        alert(`❌ Failed to approve: ${result.message || 'Unknown error'}`)
      }
    } catch (error) {
      alert(`❌ Error approving document: ${error}`)
    }
  }

  // Reject document  
  const handleReject = async (rowNumber: number, documentName: string) => {
    const notes = prompt(`Reject "${documentName}"?\n\nPlease provide a reason:`)
    
    if (!notes) return

    try {
      const response = await fetch(`http://localhost:8000/hitl/reject/${rowNumber}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          approved_by: 'User',
          notes: notes
        })
      })

      const result = await response.json()

      if (result.success) {
        alert(`❌ Rejected: ${documentName}\n\nFiles remain in Review folder for revision.`)
        fetchReviews() // Refresh list
      } else {
        alert(`❌ Failed to reject: ${result.message || 'Unknown error'}`)
      }
    } catch (error) {
      alert(`❌ Error rejecting document: ${error}`)
    }
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
      {/* Header with Stats */}
      <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <CheckCircle className="w-6 h-6 text-red-400" />
            <h2 className="text-xl font-bold text-white">Review Queue</h2>
          </div>
          
          <button
            onClick={fetchReviews}
            className="flex items-center space-x-2 bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-all"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Refresh</span>
          </button>
        </div>

        {/* Statistics */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-3xl font-bold text-white">{stats.total_documents}</div>
              <div className="text-sm text-gray-400">Total Documents</div>
            </div>
            
            <div className="text-center">
              <div className="text-3xl font-bold text-yellow-400">{stats.pending_review}</div>
              <div className="text-sm text-gray-400">Pending Review</div>
            </div>
            
            <div className="text-center">
              <div className="text-3xl font-bold text-green-400">{stats.approved}</div>
              <div className="text-sm text-gray-400">Approved</div>
            </div>
            
            <div className="text-center">
              <div className="text-3xl font-bold text-red-400">{stats.rejected}</div>
              <div className="text-sm text-gray-400">Rejected</div>
            </div>
          </div>
        )}
      </div>

      {/* Review Items */}
      {reviewItems.length === 0 ? (
        <div className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-12 text-center">
          <AlertCircle className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-white mb-2">No Documents Pending Review</h3>
          <p className="text-gray-400">
            Run automation to generate documents, then they'll appear here for review.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {reviewItems.map((item) => (
            <div
              key={item.row_number}
              className="bg-gray-800/50 backdrop-blur-sm rounded-2xl border border-gray-700/50 p-6 hover:border-red-500/50 transition-all"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-3">
                    <FileText className="w-5 h-5 text-red-400" />
                    <h3 className="text-lg font-bold text-white">{item.document_name}</h3>
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                    <div>
                      <div className="text-xs text-gray-500">Processing Date</div>
                      <div className="text-sm text-white">
                        {new Date(item.processing_date).toLocaleDateString()}
                      </div>
                    </div>
                    
                    <div>
                      <div className="text-xs text-gray-500">Quality Score</div>
                      <div className="text-sm font-bold text-green-400">
                        {item.quality_score.toFixed(1)}%
                      </div>
                    </div>
                    
                    <div>
                      <div className="text-xs text-gray-500">Processing Time</div>
                      <div className="text-sm text-white">
                        {item.processing_time.toFixed(1)}s
                      </div>
                    </div>
                    
                    <div>
                      <div className="text-xs text-gray-500">Output Files</div>
                      <div className="text-sm text-white">
                        {item.output_files.split(',').length} files
                      </div>
                    </div>
                  </div>
                  
                  <div className="text-xs text-gray-400 mb-4">
                    Files: {item.output_files}
                  </div>
                  
                  {item.output_folder_id && (
                    <a
                      href={`https://drive.google.com/drive/folders/${item.output_folder_id}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center space-x-2 text-sm text-blue-400 hover:text-blue-300"
                    >
                      <FolderOpen className="w-4 h-4" />
                      <span>Open in Google Drive</span>
                      <ExternalLink className="w-3 h-3" />
                    </a>
                  )}
                </div>
                
                <div className="flex flex-col space-y-2 ml-4">
                  <button
                    onClick={() => handleApprove(item.row_number, item.document_name)}
                    className="flex items-center space-x-2 bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-all"
                  >
                    <CheckCircle className="w-4 h-4" />
                    <span>Approve</span>
                  </button>
                  
                  <button
                    onClick={() => handleReject(item.row_number, item.document_name)}
                    className="flex items-center space-x-2 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-all"
                  >
                    <XCircle className="w-4 h-4" />
                    <span>Reject</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

