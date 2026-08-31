import React, { useState, useEffect } from 'react'

const demoData = {
  total_payments: 1042,
  failed_payments: 178,
  recovered_payments: 52,
  revenue_at_risk: 2450000,
  recovered_revenue: 680000,
  recovery_rate: 29.2,
  pending_recovery: 126
}

export default function Dashboard() {
  const [overview, setOverview] = useState(null)
  const [loading, setLoading] = useState(true)
  const [isLive, setIsLive] = useState(false)

  useEffect(() => {
    // Try to fetch from backend, fall back to demo data
    fetch('http://127.0.0.1:8000/api/v1/analytics/overview')
      .then(res => res.json())
      .then(data => {
        setOverview(data)
        setIsLive(true)
      })
      .catch(() => {
        console.warn('Backend not available, using demo data')
        setOverview(demoData)
        setIsLive(false)
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20">Loading...</div>
  if (!overview) return <div className="text-center py-20">No data</div>

  const kpis = [
    { label: 'Revenue at Risk', value: `₹${overview.revenue_at_risk.toLocaleString('en-IN')}`, color: 'text-orange-600' },
    { label: 'Recovered Revenue', value: `₹${overview.recovered_revenue.toLocaleString('en-IN')}`, color: 'text-green-600' },
    { label: 'Recovery Rate', value: `${overview.recovery_rate.toFixed(1)}%`, color: 'text-blue-600' },
    { label: 'Failed Payments', value: overview.failed_payments, color: 'text-red-600' },
  ]

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${isLive ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
          {isLive ? '● Live' : '● Demo Data'}
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpis.map((kpi) => (
          <div key={kpi.label} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <p className="text-sm text-gray-500">{kpi.label}</p>
            <p className={`text-2xl font-bold ${kpi.color}`}>{kpi.value}</p>
          </div>
        ))}
      </div>

      <Chart />
    </div>
  )
}

function Chart() {
  const bars = [
    { label: 'Mon', failed: 4000, recovered: 2400 },
    { label: 'Tue', failed: 3000, recovered: 1398 },
    { label: 'Wed', failed: 2000, recovered: 3800 },
    { label: 'Thu', failed: 2780, recovered: 3908 },
    { label: 'Fri', failed: 1890, recovered: 4800 },
    { label: 'Sat', failed: 2390, recovered: 3800 },
    { label: 'Sun', failed: 3490, recovered: 4300 },
  ]

  const max = Math.max(...bars.map(b => Math.max(b.failed, b.recovered)))

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h3 className="text-lg font-semibold mb-4">Revenue Trend (7D)</h3>
      <div className="flex items-end justify-between h-48">
        {bars.map((bar) => (
          <div key={bar.label} className="flex flex-col items-center flex-1">
            <div className="flex items-end gap-1" style={{ height: '100%' }}>
              <div className="bg-red-400 w-4 rounded-t" style={{ height: `${(bar.failed / max) * 100}%` }} />
              <div className="bg-green-400 w-4 rounded-t" style={{ height: `${(bar.recovered / max) * 100}%` }} />
            </div>
            <span className="text-xs mt-2">{bar.label}</span>
          </div>
        ))}
      </div>
    </div>
  )
}