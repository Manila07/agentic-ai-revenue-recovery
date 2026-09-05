import { useState, useEffect } from "react";

const API = "http://localhost:8000/api";

export default function Agent() {
  const [activities, setActivities] = useState([]);
  const [stats, setStats] = useState(null);
  const [paymentId, setPaymentId] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [batchRunning, setBatchRunning] = useState(false);
  const [batchResult, setBatchResult] = useState(null);

  useEffect(() => {
    loadActivity();
  }, []);

  async function loadActivity() {
    try {
      const res = await fetch(`${API}/analytics/overview`);
      const data = await res.json();
      setStats(data);
    } catch (e) {
      console.error(e);
    }
    try {
      const res = await fetch(`${API}/recovery/`);
      const data = await res.json();
      setActivities(data.recoveries || data.attempts || []);
    } catch (e) {
      console.error(e);
    }
  }

  async function handleAnalyze() {
    if (!paymentId.trim()) return;
    try {
      const res = await fetch(`${API}/recovery/${paymentId}/analyze`, {
        method: "POST",
      });
      const data = await res.json();
      setAnalysis(data);
    } catch (e) {
      console.error(e);
    }
  }

  async function handleBatchRecovery() {
    setBatchRunning(true);
    setBatchResult(null);
    try {
      const res = await fetch(`${API}/agent/batch-recovery`, { method: "POST" });
      const data = await res.json();
      setBatchResult(data);
      loadActivity();
    } catch (e) {
      console.error(e);
    }
    setBatchRunning(false);
  }

  function fmt(a) {
    return `₹${Number(a || 0).toLocaleString()}`;
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-white mb-6">AI Agent Dashboard</h1>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <Card
          title="Total Recovery Attempts"
          value={stats?.total_recovery_attempts || 0}
          color="text-blue-400"
        />
        <Card
          title="Recovery Rate"
          value={`${stats?.recovery_rate || 0}%`}
          color="text-green-400"
        />
        <Card
          title="Revenue Recovered"
          value={fmt(stats?.total_recovered_amount)}
          color="text-green-400"
        />
        <Card
          title="Pending Human Review"
          value={stats?.pending_human_review || 0}
          color="text-yellow-400"
        />
      </div>

      {/* Manual Analysis + Batch Recovery */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Manual Analysis */}
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
          <h3 className="text-white font-semibold mb-3">Manual Analysis</h3>
          <div className="flex gap-2 mb-4">
            <input
              type="text"
              placeholder="Enter Payment ID (e.g. PAY_321626B1)"
              value={paymentId}
              onChange={(e) => setPaymentId(e.target.value)}
              className="flex-1 bg-gray-900 border border-gray-600 rounded px-3 py-2 text-white text-sm"
            />
            <button
              onClick={handleAnalyze}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded"
            >
              Analyze
            </button>
          </div>
          {analysis && (
            <div className="bg-gray-900 rounded p-3 text-sm">
              <p className="text-gray-400">Result for: {paymentId}</p>
              <p className="text-white font-bold mt-1">
                Probability:{" "}
                <span className="text-blue-400">
                  {((analysis.recovery_probability || 0) * 100).toFixed(1)}%
                </span>
              </p>
              <p className="text-gray-300 mt-1">
                Strategy: {analysis.selected_strategy?.name}
              </p>
              <p className="text-gray-400 mt-1 text-xs">{analysis.explanation}</p>
            </div>
          )}
        </div>

        {/* Batch Recovery */}
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
          <h3 className="text-white font-semibold mb-3">Batch Recovery</h3>
          <p className="text-gray-400 text-sm mb-3">
            Process up to 10 unprocessed failed payments at once.
          </p>
          <button
            onClick={handleBatchRecovery}
            disabled={batchRunning}
            className={`w-full py-2 rounded font-bold text-white ${
              batchRunning ? "bg-gray-600" : "bg-green-600 hover:bg-green-500"
            }`}
          >
            {batchRunning ? "Running..." : "🚀 Run Batch Recovery"}
          </button>
          {batchResult && (
            <div className="mt-3 bg-gray-900 rounded p-3 text-sm">
              <p className="text-white">
                Processed: <span className="text-blue-400">{batchResult.processed}</span>
              </p>
              <p className="text-green-400">
                Successful: <span>{batchResult.successful}</span>
              </p>
              <p className="text-gray-300">
                Revenue Recovered: {fmt(batchResult.total_recovered)}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Activity Feed */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-4">
        <h3 className="text-white font-semibold mb-3">Agent Activity Feed</h3>
        {activities.length === 0 ? (
          <p className="text-gray-500 text-sm">
            No activity yet — run a recovery from the Payments page or batch recovery
            above.
          </p>
        ) : (
          <div className="space-y-2 max-h-96 overflow-auto">
            {activities.map((a, i) => (
              <div
                key={i}
                className="bg-gray-900 rounded p-3 flex items-center justify-between"
              >
                <div>
                  <span className="text-blue-400 font-mono text-sm">{a.payment_id}</span>
                  <span className="text-gray-400 mx-2">→</span>
                  <span className="text-gray-300 text-sm">{a.strategy}</span>
                </div>
                <div className="flex items-center gap-3">
                  <span
                    className={`text-xs px-2 py-1 rounded ${
                      a.status === "success"
                        ? "bg-green-500/20 text-green-400"
                        : a.status === "failed"
                        ? "bg-red-500/20 text-red-400"
                        : "bg-yellow-500/20 text-yellow-400"
                    }`}
                  >
                    {a.status}
                  </span>
                  <span className="text-gray-500 text-xs">
                    {a.created_at
                      ? new Date(a.created_at).toLocaleString()
                      : "just now"}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
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
