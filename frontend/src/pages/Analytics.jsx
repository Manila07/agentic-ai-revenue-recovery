import { useState, useEffect } from "react";

const API = "http://localhost:8000/api";

export default function Analytics() {
  const [overview, setOverview] = useState(null);
  const [failureReasons, setFailureReasons] = useState([]);
  const [paymentMethods, setPaymentMethods] = useState([]);
  const [revenueByStrategy, setRevenueByStrategy] = useState([]);
  const [agentActivity, setAgentActivity] = useState([]);

  useEffect(() => {
    fetch(`${API}/analytics/overview`)
      .then((r) => r.json())
      .then(setOverview)
      .catch(() => {});
    fetch(`${API}/analytics/failure-reasons`)
      .then((r) => r.json())
      .then(setFailureReasons)
      .catch(() => {});
    fetch(`${API}/analytics/payment-methods`)
      .then((r) => r.json())
      .then(setPaymentMethods)
      .catch(() => {});
    fetch(`${API}/analytics/revenue-by-strategy`)
      .then((r) => r.json())
      .then(setRevenueByStrategy)
      .catch(() => {});
    fetch(`${API}/analytics/agent-activity`)
      .then((r) => r.json())
      .then(setAgentActivity)
      .catch(() => {});
  }, []);

  const maxFailure = Math.max(...failureReasons.map((f) => f.count), 1);
  const maxMethod = Math.max(...paymentMethods.map((m) => m.count), 1);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-white mb-6">Analytics</h1>

      {/* Overview Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <Card
          title="Total Payments"
          value={overview?.total_payments || 0}
          color="text-blue-400"
        />
        <Card
          title="Total At-Risk"
          value={`₹${(overview?.total_at_risk_amount || 0).toLocaleString()}`}
          color="text-red-400"
        />
        <Card
          title="Recovered"
          value={`₹${(overview?.total_recovered_amount || 0).toLocaleString()}`}
          color="text-green-400"
        />
        <Card
          title="Recovery Rate"
          value={`${overview?.recovery_rate || 0}%`}
          color="text-yellow-400"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Failure Reasons Chart */}
        <ChartCard title="Failure Reasons">
          {failureReasons.length === 0 ? (
            <p className="text-gray-500 text-sm">No data yet</p>
          ) : (
            failureReasons.map((f, i) => (
              <div key={i} className="mb-2">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-300">
                    {f.reason?.replace(/_/g, " ")}
                  </span>
                  <span className="text-gray-400">{f.count}</span>
                </div>
                <div className="bg-gray-700 rounded-full h-3">
                  <div
                    className="bg-red-500 h-3 rounded-full"
                    style={{ width: `${(f.count / maxFailure) * 100}%` }}
                  />
                </div>
              </div>
            ))
          )}
        </ChartCard>

        {/* Payment Methods Chart */}
        <ChartCard title="Payment Methods">
          {paymentMethods.length === 0 ? (
            <p className="text-gray-500 text-sm">No data yet</p>
          ) : (
            paymentMethods.map((m, i) => (
              <div key={i} className="mb-2">
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-300">
                    {m.method?.replace(/_/g, " ")}
                  </span>
                  <span className="text-gray-400">{m.count}</span>
                </div>
                <div className="bg-gray-700 rounded-full h-3">
                  <div
                    className="bg-blue-500 h-3 rounded-full"
                    style={{ width: `${(m.count / maxMethod) * 100}%` }}
                  />
                </div>
              </div>
            ))
          )}
        </ChartCard>
      </div>

      {/* Revenue by Strategy */}
      <ChartCard title="Revenue Recovered by Strategy">
        {revenueByStrategy.length === 0 ? (
          <p className="text-gray-500 text-sm">No recovery data yet — run some recoveries first</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {revenueByStrategy.map((s, i) => (
              <div key={i} className="bg-gray-900 rounded p-3">
                <p className="text-blue-400 font-semibold text-sm">
                  {s.strategy?.replace(/_/g, " ")}
                </p>
                <p className="text-gray-500 text-xs">
                  {s.attempts} attempt(s)
                </p>
                <p className="text-green-400 font-bold mt-1">
                  ₹{Number(s.recovered || 0).toLocaleString()}
                </p>
              </div>
            ))}
          </div>
        )}
      </ChartCard>

      {/* Agent Activity */}
      <div className="mt-6">
        <ChartCard title="Agent Activity Feed">
          {agentActivity.length === 0 ? (
            <p className="text-gray-500 text-sm">
              No activity yet — run some recoveries from the Payments page
            </p>
          ) : (
            <div className="space-y-2 max-h-64 overflow-auto">
              {agentActivity.map((a, i) => (
                <div
                  key={i}
                  className="bg-gray-900 rounded p-2 flex items-center justify-between text-sm"
                >
                  <span className="text-blue-400 font-mono">{a.payment_id}</span>
                  <span className="text-gray-300">{a.strategy}</span>
                  <span
                    className={`px-2 py-1 rounded text-xs ${
                      a.status === "success"
                        ? "bg-green-500/20 text-green-400"
                        : a.status === "failed"
                        ? "bg-red-500/20 text-red-400"
                        : "bg-gray-500/20 text-gray-400"
                    }`}
                  >
                    {a.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </ChartCard>
      </div>
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

function ChartCard({ title, children }) {
  return (
    <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
      <h3 className="text-white font-semibold mb-3">{title}</h3>
      {children}
    </div>
  );
}
