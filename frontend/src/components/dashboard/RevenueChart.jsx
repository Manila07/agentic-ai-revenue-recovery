import React from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

const data = [
  { name: 'Mon', recovered: 4000, atRisk: 2000 },
  { name: 'Tue', recovered: 3000, atRisk: 1398 },
  { name: 'Wed', recovered: 2000, atRisk: 3800 },
  { name: 'Thu', recovered: 2780, atRisk: 3908 },
  { name: 'Fri', recovered: 1890, atRisk: 4800 },
]

export default function RevenueChart() {
  return (
    <div className="bg-white rounded-lg p-6 shadow h-72">
      <h3 className="text-lg font-semibold mb-4">Revenue Trend</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="recovered" stroke="#10B981" />
          <Line type="monotone" dataKey="atRisk" stroke="#F59E0B" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}