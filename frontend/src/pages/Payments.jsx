import React, { useState, useEffect } from 'react'

const demoPayments = [
  { id: 'pay_demo_001', customer_id: 'cust_001', amount: 8500, status: 'FAILED', failure_reason: 'insufficient_funds', recovery_probability: 0.85 },
  { id: 'pay_demo_002', customer_id: 'cust_002', amount: 24500, status: 'FAILED', failure_reason: 'network_error', recovery_probability: 0.62 },
  { id: 'pay_demo_003', customer_id: 'cust_003', amount: 125000, status: 'FAILED', failure_reason: 'bank_unavailable', recovery_probability: 0.74 },
]

export default function Payments() {
  const [payments, setPayments] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/payments?limit=100')
      .then(res => res.json())
      .then(data => setPayments(data))
      .catch(() => {
        console.warn('Using demo payments')
        setPayments(demoPayments)
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="text-center py-20">Loading...</div>

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Payments</h1>
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Customer</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Amount</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Reason</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Prob.</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {payments.map((p) => (
              <tr key={p.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-sm">{p.id}</td>
                <td className="px-6 py-4 text-sm">{p.customer_id}</td>
                <td className="px-6 py-4 text-sm font-medium">₹{Number(p.amount).toLocaleString('en-IN')}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 rounded-full text-xs ${p.status === 'SUCCESS' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {p.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">{p.failure_reason || '-'}</td>
                <td className="px-6 py-4 text-sm">
                  {p.recovery_probability ? `${(p.recovery_probability * 100).toFixed(0)}%` : '-'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}