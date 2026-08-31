import React, { useState, useEffect } from 'react'
import api from '../services/api'
import { demoAgentActions } from '../services/fallbackData'

export default function AgentActivity() {
  const [actions, setActions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/agent/activity?limit=100')
      .then(res => setActions(res.data))
      .catch(err => { console.warn('Using demo data:', err.message); setActions(demoAgentActions) })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20">Loading...</div>

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Agent Activity</h1>
      <div className="space-y-4">
        {actions.length === 0 && <p className="text-gray-500">No agent activity yet.</p>}
        {actions.map((action, idx) => (
          <div key={action.id} className="bg-white rounded-lg p-4 shadow-card border border-gray-200 flex items-start gap-3">
            <div className="flex flex-col items-center">
              <div className={`w-3 h-3 rounded-full ${action.status === 'EXECUTED' ? 'bg-success' : 'bg-warning'}`} />
              {idx < actions.length - 1 && <div className="flex-1 border-l border-gray-200 ml-1.5" />}
            </div>
            <div className="flex-1">
              <div className="flex justify-between">
                <span className="font-semibold text-sm">{action.payment_id}</span>
                <span className={`badge ${action.status === 'EXECUTED' ? 'badge-success' : 'badge-warning'}`}>
                  {action.status}
                </span>
              </div>
              <p className="mt-1 text-sm"><strong>Decision:</strong> {action.decision}</p>
              <p className="text-sm"><strong>Confidence:</strong> {(action.confidence * 100).toFixed(0)}%</p>
              {action.reasoning && <p className="text-sm text-gray-600 mt-1">{action.reasoning}</p>}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}