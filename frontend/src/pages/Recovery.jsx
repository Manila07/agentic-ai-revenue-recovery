import React, { useState, useEffect } from 'react'

const demoPayments = [
  { id: 'pay_demo_001', amount: 8500, failure_category: 'INSUFFICIENT_FUNDS', recovery_probability: 0.85 },
  { id: 'pay_demo_002', amount: 24500, failure_category: 'NETWORK_ERROR', recovery_probability: 0.62 },
  { id: 'pay_demo_003', amount: 125000, failure_category: 'BANK_UNAVAILABLE', recovery_probability: 0.74 },
]

export default function Recovery() {
  const [payments, setPayments] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/payments?status=FAILED&limit=50')
      .then(res => res.json())
      .then(data => setPayments(data))
      .catch(() => {
        console.warn('Using demo data')
        setPayments(demoPayments)
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20">Loading...</div>

  const handleAnalyze = (id) => alert(`Analyze clicked for ${id}`)
  const handleExecute = (id, action) => alert(`Execute ${action} for ${id}`)

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Recovery Center</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {payments.map((payment) => (
          <div key={payment.id} className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <h3 className="font-semibold">{payment.id}</h3>
            <p className="text-sm text-gray-500 mt-1">Amount: ₹{Number(payment.amount).toLocaleString('en-IN')}</p>
            <p className="text-sm text-gray-500">Failure: {payment.failure_category || 'UNKNOWN'}</p>
            <p className="text-sm text-gray-500">Probability: {payment.recovery_probability ? `${(payment.recovery_probability * 100).toFixed(0)}%` : 'N/A'}</p>
            <div className="mt-4 flex gap-2">
              <button onClick={() => handleAnalyze(payment.id)} className="bg-blue-500 text-white px-3 py-1 rounded">Analyze</button>
              <button onClick={() => handleExecute(payment.id, 'RETRY')} className="bg-green-500 text-white px-3 py-1 rounded">Retry</button>
              <button onClick={() => handleExecute(payment.id, 'NOTIFY')} className="bg-yellow-500 text-white px-3 py-1 rounded">Notify</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}