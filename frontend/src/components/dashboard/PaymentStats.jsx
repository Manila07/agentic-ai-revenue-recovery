import React from 'react'

export default function PaymentStats({ failed, recovered }) {
  return (
    <div className="bg-white rounded-lg p-6 shadow">
      <h3 className="text-sm text-gray-500">Payments</h3>
      <div className="flex justify-between mt-2">
        <span className="text-danger">Failed: {failed}</span>
        <span className="text-success">Recovered: {recovered}</span>
      </div>
    </div>
  )
}