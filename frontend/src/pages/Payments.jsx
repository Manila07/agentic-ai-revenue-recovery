import { useState, useEffect } from "react";

const API = "http://localhost:8000/api";

export default function Payments() {
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selected, setSelected] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [executing, setExecuting] = useState(false);
  const [result, setResult] = useState(null);

  useEffect(() => {
    loadPayments();
  }, []);

  async function loadPayments() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/payments`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setPayments(data.payments || []);
    } catch (e) {
      console.error("Failed to load payments:", e);
      setError(e.message);
    }
    setLoading(false);
  }

  async function handleAnalyze(payment) {
    setSelected(payment);
    setAnalysis(null);
    setResult(null);
    try {
      const res = await fetch(`${API}/recovery/${payment.id}/analyze`, {
        method: "POST",
      });
      const data = await res.json();
      setAnalysis(data);
    } catch (e) {
      console.error("Analyze failed:", e);
    }
  }

  async function handleExecute() {
    if (!selected) return;
    setExecuting(true);
    try {
      const res = await fetch(`${API}/recovery/${selected.id}/execute`, {
        method: "POST",
      });
      const data = await res.json();
      setResult(data);
      loadPayments();
    } catch (e) {
      console.error("Execute failed:", e);
    }
    setExecuting(false);
  }

  function fmt(a) {
    return `₹${Number(a).toLocaleString("en-IN", { minimumFractionDigits: 0 })}`;
  }

  if (loading) {
    return (
      <div className="p-8">
        <p className="text-gray-400">Loading payments...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <h1 className="text-2xl font-bold text-white mb-4">Payments</h1>
        <div className="bg-red-900/30 border border-red-500 rounded-lg p-4">
          <p className="text-red-400 font-bold">Error loading payments</p>
          <p className="text-gray-300 text-sm mt-1">{error}</p>
          <button
            onClick={loadPayments}
            className="mt-3 px-4 py-2 bg-red-600 hover:bg-red-500 text-white rounded"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-[calc(100vh-0rem)]">
      {/* Payment List */}
      <div
        className={`${
          selected ? "w-1/2" : "w-full"
        } transition-all overflow-auto p-6`}
      >
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold text-white">
            Failed Payments ({payments.length})
          </h1>
          <button
            onClick={loadPayments}
            className="px-3 py-1 bg-gray-700 hover:bg-gray-600 text-white rounded text-sm"
          >
            Refresh
          </button>
        </div>

        <div className="bg-gray-800 rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-900 text-gray-400">
              <tr>
                <th className="px-4 py-3 text-left">Payment ID</th>
                <th className="px-4 py-3 text-left">Amount</th>
                <th className="px-4 py-3 text-left">Failure Reason</th>
                <th className="px-4 py-3 text-left">Method</th>
                <th className="px-4 py-3 text-left">Retries</th>
                <th className="px-4 py-3 text-left">Action</th>
              </tr>
            </thead>
            <tbody>
              {payments.map((p) => (
                <tr
                  key={p.id}
                  className={`border-t border-gray-700 hover:bg-gray-750 cursor-pointer ${
                    selected?.id === p.id ? "bg-gray-700" : ""
                  }`}
                  onClick={() => handleAnalyze(p)}
                >
                  <td className="px-4 py-3 text-blue-400 font-mono">{p.id}</td>
                  <td className="px-4 py-3 text-white font-semibold">
                    {fmt(p.amount)}
                  </td>
                  <td className="px-4 py-3 text-red-400">
                    {p.failure_reason?.replace(/_/g, " ")}
                  </td>
                  <td className="px-4 py-3 text-gray-300">
                    {p.payment_method?.replace(/_/g, " ")}
                  </td>
                  <td className="px-4 py-3 text-gray-400">{p.retry_count || 0}</td>
                  <td className="px-4 py-3">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleAnalyze(p);
                      }}
                      className="px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs"
                    >
                      Analyze
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Analysis Panel */}
      {selected && (
        <div className="w-1/2 bg-gray-900 border-l border-gray-700 p-6 overflow-auto">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl font-bold text-white">AI Analysis</h2>
            <button
              onClick={() => {
                setSelected(null);
                setAnalysis(null);
                setResult(null);
              }}
              className="text-gray-400 hover:text-white text-xl"
            >
              ✕
            </button>
          </div>

          {/* Payment Info */}
          <div className="bg-gray-800 rounded-lg p-4 mb-4">
            <p className="text-gray-400 text-sm">Payment</p>
            <p className="text-white font-mono">{selected.id}</p>
            <p className="text-2xl font-bold text-green-400 mt-1">
              {fmt(selected.amount)}
            </p>
            <p className="text-red-400 text-sm mt-1">
              Failure: {selected.failure_reason?.replace(/_/g, " ")}
            </p>
          </div>

          {/* Customer History */}
          <div className="bg-gray-800 rounded-lg p-4 mb-4">
            <p className="text-gray-400 text-sm mb-2">Customer History</p>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-white font-bold">
                  {selected.customer_total_payments || 0}
                </p>
                <p className="text-gray-500 text-xs">Total Payments</p>
              </div>
              <div>
                <p className="text-green-400 font-bold">
                  {((selected.customer_success_rate || 0) * 100).toFixed(0)}%
                </p>
                <p className="text-gray-500 text-xs">Success Rate</p>
              </div>
              <div>
                <p className="text-yellow-400 font-bold">
                  {selected.customer_previous_retries || 0}
                </p>
                <p className="text-gray-500 text-xs">Previous Retries</p>
              </div>
            </div>
          </div>

          {/* Analysis Results */}
          {analysis && (
            <>
              {/* Recovery Probability */}
              <div className="bg-gray-800 rounded-lg p-4 mb-4">
                <p className="text-gray-400 text-sm mb-2">Recovery Probability</p>
                <div className="flex items-center gap-4">
                  <div className="flex-1 bg-gray-700 rounded-full h-4">
                    <div
                      className={`h-4 rounded-full ${
                        analysis.recovery_probability >= 0.7
                          ? "bg-green-500"
                          : analysis.recovery_probability >= 0.4
                          ? "bg-yellow-500"
                          : "bg-red-500"
                      }`}
                      style={{
                        width: `${(analysis.recovery_probability || 0) * 100}%`,
                      }}
                    />
                  </div>
                  <span
                    className={`text-2xl font-bold ${
                      analysis.recovery_probability >= 0.7
                        ? "text-green-400"
                        : analysis.recovery_probability >= 0.4
                        ? "text-yellow-400"
                        : "text-red-400"
                    }`}
                  >
                    {((analysis.recovery_probability || 0) * 100).toFixed(1)}%
                  </span>
                </div>
                <p className="text-gray-500 text-xs mt-2">
                  Risk Score: {((analysis.risk_score || 0) * 100).toFixed(0)}%
                </p>
              </div>

              {/* Selected Strategy */}
              <div className="bg-gray-800 rounded-lg p-4 mb-4">
                <p className="text-gray-400 text-sm mb-2">AI Selected Strategy</p>
                <p className="text-blue-400 font-bold text-lg">
                  {analysis.selected_strategy?.name}
                </p>
                <p className="text-gray-300 text-sm mt-1">
                  {analysis.selected_strategy?.description}
                </p>
                {analysis.selected_strategy?.requires_human_approval && (
                  <span className="inline-block mt-2 px-2 py-1 bg-yellow-500/20 text-yellow-400 rounded text-xs">
                    ⚠️ Requires Human Approval
                  </span>
                )}
              </div>

              {/* Reasoning */}
              <div className="bg-gray-800 rounded-lg p-4 mb-4">
                <p className="text-gray-400 text-sm mb-2">AI Reasoning</p>
                <p className="text-gray-300 text-sm leading-relaxed">
                  {analysis.explanation}
                </p>
              </div>

              {/* Execute Button */}
              {!result && (
                <button
                  onClick={handleExecute}
                  disabled={executing}
                  className={`w-full py-3 rounded-lg font-bold text-white ${
                    executing ? "bg-gray-600" : "bg-green-600 hover:bg-green-500"
                  }`}
                >
                  {executing ? "Executing..." : "Execute Recovery"}
                </button>
              )}

              {/* Result */}
              {result && (
                <div
                  className={`rounded-lg p-4 ${
                    result.success
                      ? "bg-green-900/30 border border-green-500"
                      : "bg-red-900/30 border border-red-500"
                  }`}
                >
                  <p
                    className={`font-bold text-lg ${
                      result.success ? "text-green-400" : "text-red-400"
                    }`}
                  >
                    {result.success ? "✅ Recovery Successful" : "❌ Recovery Failed"}
                  </p>
                  <p className="text-gray-300 text-sm mt-1">
                    Strategy: {result.strategy}
                  </p>
                  <p className="text-gray-300 text-sm">
                    Amount: {fmt(result.recovered_amount || 0)}
                  </p>
                  <p className="text-gray-400 text-xs mt-2">{result.message}</p>
                  <button
                    onClick={() => {
                      setResult(null);
                      setAnalysis(null);
                    }}
                    className="mt-4 px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded"
                  >
                    Analyze Another
                  </button>
                </div>
              )}
            </>
          )}

          {!analysis && (
            <div className="text-center text-gray-500 mt-12">
              <p className="text-4xl mb-4">🤖</p>
              <p>Click "Analyze" to run AI analysis on this payment</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
