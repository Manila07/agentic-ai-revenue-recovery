import React, { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'
import api from '../services/api'

export default function Analytics() {
  const [data, setData] = useState(null)

  useEffect(() => {
    api.get('/analytics/recovery')
      .then(res => setData(res.data))
      .catch(err => {
        console.warn('Using demo analytics:', err.message)
        setData({
          by_action: { RETRY: 10, NOTIFY: 5, STOP: 3 },
          by_category: { INSUFFICIENT_FUNDS: 8, NETWORK_ERROR: 5, CARD_DECLINED: 3 },
          average_recovery_probability: 0.65,
          success_rate_by_action: { RETRY: 80, NOTIFY: 50 }
        })
      })
  }, [])

  if (!data) return <div className="text-center py-20">Loading...</div>

  const actionData = Object.entries(data.by_action).map(([action, count]) => ({ action, count }))
  const categoryData = Object.entries(data.by_category).map(([category, count]) => ({ category, count }))

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg p-6 shadow-card border border-gray-200">
          <h3 className="text-lg font-semibold mb-4">Recovery by Action</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={actionData}>
              <XAxis dataKey="action" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#4F46E5" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="bg-white rounded-lg p-6 shadow-card border border-gray-200">
          <h3 className="text-lg font-semibold mb-4">Failures by Category</h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={categoryData}>
              <XAxis dataKey="category" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#F59E0B" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div className="bg-white rounded-lg p-6 shadow-card border border-gray-200">
        <h3 className="text-lg font-semibold mb-4">Success Rate by Action</h3>
        <div className="space-y-2">
          {Object.entries(data.success_rate_by_action).map(([action, rate]) => (
            <div key={action} className="flex items-center">
              <span className="w-32 text-sm font-medium">{action}</span>
              <div className="flex-1 bg-gray-200 rounded h-4">
                <div className="bg-success rounded h-4" style={{ width: `${rate}%` }} />
              </div>
              <span className="ml-2 text-sm font-bold">{rate}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}