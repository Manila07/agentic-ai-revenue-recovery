import { useState, useEffect } from "react";

const API = "http://localhost:8000/api";

export default function Dashboard() {
  const [payments, setPayments] = useState([]);
  const [stats, setStats] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [events, setEvents] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  function loadData() {
    fetch(`${API}/payments?limit=10`)
      .then(r => r.json())
      .then(d => setPayments(d.payments || []))
      .catch(() => {});
    fetch(`${API}/payments/stats`)
      .then(r => r.json())
      .then(d => setStats(d))
      .catch(() => {});
    fetch(`${API}/analytics/overview`)
      .then(r => r.json())
      .then(d => setAnalytics(d))
      .catch(() => {});
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-white mb-6">Dashboard</h1>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <Card
          title="Total Failed Payments"
          value={stats?.total_payments || 0}
          color="text-red-400"
        />
        <Card
          title="Total At-Risk Revenue"
          value={`₹${(stats?.total_amount || 0).toLocaleString()}`}
          color="text-yellow-400"
        />
        <Card
          title="Revenue Recovered"
          value={`₹${(analytics?.total_recovered_amount || 0).toLocaleString()}`}
          color="text-green-400"
        />
        <Card
          title="Recovery Rate"
          value={`${analytics?.recovery_rate || 0}%`}
          color="text-blue-400"
        />
      </div>

      {/* Live Events */}
      {events.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-white mb-4">🔴 Live Events</h2>
          <div className="bg-gray-800 rounded-lg border border-gray-700 p-4 max-h-48 overflow-auto">
            {events.map((e, i) => (
              <div key={i} className="text-sm py-1 border-b border-gray-700 last:border-0">
                <span className="text-green-400">{e.type}</span>
                <span className="text-gray-400 ml-2">{e.data?.payment_id}</span>
                <span className="text-gray-500 ml-2 text-xs">
                  {new Date().toLocaleTimeString()}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Failed Payments */}
      <h2 className="text-lg font-semibold text-white mb-4">Recent Failed Payments</h2>
      <div className="bg-gray-800 rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-gray-900 text-gray-400">
            <tr>
              <th className="px-4 py-3 text-left">Payment ID</th>
              <th className="px-4 py-3 text-left">Amount</th>
              <th className="px-4 py-3 text-left">Failure Reason</th>
              <th className="px-4 py-3 text-left">Method</th>
            </tr>
          </thead>
          <tbody>
            {payments.map(p => (
              <tr key={p.id} className="border-t border-gray-700 hover:bg-gray-750">
                <td className="px-4 py-3 text-blue-400 font-mono">{p.id}</td>
                <td className="px-4 py-3 text-white font-semibold">
                  ₹{p.amount?.toLocaleString()}
                </td>
                <td className="px-4 py-3 text-red-400">
                  {p.failure_reason?.replace(/_/g, " ")}
                </td>
                <td className="px-4 py-3 text-gray-300">
                  {p.payment_method?.replace(/_/g, " ")}
                </td>
              </tr>
            ))}
            {payments.length === 0 && (
              <tr>
                <td colSpan="4" className="px-4 py-8 text-gray-500 text-center">
                  No failed payments found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <p className="text-gray-500 mt-4 text-sm">
        Go to Payments page to analyze and execute recoveries.
      </p>
    </div>
  );
}

function Card({ title, value, color }) {
  return (
    <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
      <p className="text-gray-400 text-sm">{title}</p>
      <p className={`text-2xl font-bold mt-2 ${color}`}>{value}</p>
    </div>
  );
}
