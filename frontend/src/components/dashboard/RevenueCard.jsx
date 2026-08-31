import React from 'react'

export default function RevenueCard({ title, value, color }) {
  return (
    <div className="bg-white rounded-lg p-6 shadow">
      <h3 className="text-sm text-gray-500">{title}</h3>
      <p className={`text-2xl font-bold ${color}`}>₹{Number(value).toLocaleString()}</p>
    </div>
  )
}