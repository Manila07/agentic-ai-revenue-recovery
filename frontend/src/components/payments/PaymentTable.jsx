import React from 'react'

export default function PaymentTable({ payments, loading }) {
  if (loading) return <div className="text-center py-10">Loading...</div>

  return (
    <table className="min-w-full bg-white shadow rounded">
      <thead>
        <tr>
          <th className="px-4 py-2 text-left">ID</th>
          <th className="px-4 py-2 text-left">Customer</th>
          <th className="px-4 py-2 text-left">Amount</th>
          <th className="px-4 py-2 text-left">Status</th>
          <th className="px-4 py-2 text-left">Failure Reason</th>
          <th className="px-4 py-2 text-left">Recovery Prob.</th>
        </tr>
      </thead>
      <tbody>
        {payments.map((p) => (
          <tr key={p.id} className="border-t">
            <td className="px-4 py-2">{p.id}</td>
            <td className="px-4 py-2">{p.customer_id}</td>
            <td className="px-4 py-2">₹{p.amount.toLocaleString()}</td>
            <td className="px-4 py-2">{p.status}</td>
            <td className="px-4 py-2">{p.failure_reason || '-'}</td>
            <td className="px-4 py-2">{p.recovery_probability ? (p.recovery_probability * 100).toFixed(0) + '%' : '-'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  )
}