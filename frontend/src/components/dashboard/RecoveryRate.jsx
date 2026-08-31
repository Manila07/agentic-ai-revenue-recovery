import React from 'react'

export default function RecoveryRate({ rate }) {
  return (
    <div className="bg-white rounded-lg p-6 shadow">
      <h3 className="text-sm text-gray-500">Recovery Rate</h3>
      <p className="text-2xl font-bold text-success">{rate.toFixed(1)}%</p>
    </div>
  )
}