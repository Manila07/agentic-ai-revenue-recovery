import React from 'react'

export default function AgentTimeline({ actions, loading }) {
  if (loading) return <div className="text-center py-10">Loading...</div>

  return (
    <div className="space-y-4">
      {actions.length === 0 && <p className="text-gray-500">No agent activity yet.</p>}
      {actions.map((action) => (
        <div key={action.id} className="bg-white rounded p-4 shadow">
          <div className="flex justify-between">
            <span className="font-semibold">{action.payment_id}</span>
            <span className={`px-2 py-1 rounded text-xs ${action.status === 'EXECUTED' ? 'bg-green-200 text-green-800' : 'bg-yellow-200 text-yellow-800'}`}>{action.status}</span>
          </div>
          <p className="mt-2 text-sm"><strong>Decision:</strong> {action.decision}</p>
          <p className="text-sm"><strong>Confidence:</strong> {(action.confidence * 100).toFixed(0)}%</p>
          {action.reasoning && <p className="text-sm text-gray-600 mt-1">{action.reasoning}</p>}
        </div>
      ))}
    </div>
  )
}