import React from 'react'

export default function RecoveryCard({ payment, onAnalyze, onExecute }) {
  return (
    <div className="bg-white rounded-lg p-4 shadow">
      <h3 className="font-semibold">{payment.id}</h3>
      <p className="text-sm text-gray-500">Amount: ₹{payment.amount}</p>
      <p className="text-sm text-gray-500">Category: {payment.failure_category}</p>
      <p className="text-sm text-gray-500">Probability: {payment.recovery_probability ? (payment.recovery_probability * 100).toFixed(0) + '%' : 'N/A'}</p>
      <div className="mt-3 flex gap-2">
        <button onClick={onAnalyze} className="bg-blue-500 text-white px-3 py-1 rounded">Analyze</button>
        <button onClick={() => onExecute('RETRY')} className="bg-green-500 text-white px-3 py-1 rounded">Retry</button>
        <button onClick={() => onExecute('NOTIFY')} className="bg-yellow-500 text-white px-3 py-1 rounded">Notify</button>
      </div>
    </div>
  )
}