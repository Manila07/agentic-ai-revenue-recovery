// frontend/src/pages/Recovery.jsx
import React, { useState, useEffect } from "react";
import { 
  RotateCcw, Search, AlertTriangle, CheckCircle2, 
  Clock, XCircle, Zap, Shield, ChevronRight 
} from "lucide-react";

const API_BASE = "http://localhost:8000/api";

export default function Recovery() {
  const [recoveries, setRecoveries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchId, setSearchId] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  useEffect(() => {
    fetchRecoveries();
  }, []);

  const fetchRecoveries = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await fetch(`${API_BASE}/recovery/`);
      if (!res.ok) throw new Error(`Server returned ${res.status}`);
      const data = await res.json();
      setRecoveries(data.recoveries || []);
    } catch (err) {
      console.error("Failed to fetch recoveries:", err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const analyzePayment = async () => {
    if (!searchId.trim()) return;
    try {
      setAnalyzing(true);
      setAnalysisResult(null);
      setError(null);
      const res = await fetch(`${API_BASE}/recovery/${searchId.trim()}/analyze`, {
        method: "POST",
      });
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || `Server returned ${res.status}`);
      }
      const data = await res.json();
      setAnalysisResult(data);
      fetchRecoveries(); // Refresh list
    } catch (err) {
      setError(err.message);
    } finally {
      setAnalyzing(false);
    }
  };

  const executeRecovery = async (paymentId) => {
    try {
      const res = await fetch(
        `${API_BASE}/recovery/${paymentId}/execute?human_approved=false`,
        { method: "POST" }
      );
      if (!res.ok) throw new Error(`Execution failed: ${res.status}`);
      fetchRecoveries();
    } catch (err) {
      setError(err.message);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case "success": return <CheckCircle2 size={16} className="text-green-400" />;
      case "failed": return <XCircle size={16} className="text-red-400" />;
      case "pending": return <Clock size={16} className="text-yellow-400" />;
      default: return <RotateCcw size={16} className="text-gray-400" />;
    }
  };

  const getRiskBadge = (risk) => {
    const colors = {
      low: "bg-green-900/50 text-green-300 border-green-700",
      medium: "bg-yellow-900/50 text-yellow-300 border-yellow-700",
      high: "bg-red-900/50 text-red-300 border-red-700",
    };
    return (
      <span className={`px-2 py-0.5 rounded text-xs border ${colors[risk] || colors.medium}`}>
        {risk?.toUpperCase() || "N/A"}
      </span>
    );
  };

  return (
    <div style={{ padding: 24 }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: 24, fontWeight: "bold", color: "#e2e8f0" }}>
            <RotateCcw style={{ display: "inline", marginRight: 8 }} size={24} />
            Recovery Queue
          </h1>
          <p style={{ color: "#94a3b8", marginTop: 4 }}>
            Analyze failed payments and execute recovery strategies
          </p>
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div style={{
          padding: 12, marginBottom: 16, borderRadius: 8,
          backgroundColor: "#7f1d1d", border: "1px solid #dc2626", color: "#fecaca"
        }}>
          <AlertTriangle style={{ display: "inline", marginRight: 8 }} size={16} />
          {error}
          <button 
            onClick={() => setError(null)}
            style={{ float: "right", background: "none", border: "none", color: "#fecaca", cursor: "pointer" }}
          >
            ✕
          </button>
        </div>
      )}

      {/* Analyze Payment Section */}
      <div style={{
        padding: 20, marginBottom: 24, borderRadius: 12,
        backgroundColor: "#1e293b", border: "1px solid #334155"
      }}>
        <h2 style={{ fontSize: 16, fontWeight: 600, color: "#e2e8f0", marginBottom: 12 }}>
          <Zap style={{ display: "inline", marginRight: 8 }} size={16} />
          Analyze Payment
        </h2>
        <div style={{ display: "flex", gap: 12 }}>
          <input
            type="text"
            placeholder="Enter Payment ID (e.g., PAY_739464)"
            value={searchId}
            onChange={(e) => setSearchId(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && analyzePayment()}
            style={{
              flex: 1, padding: "10px 14px", borderRadius: 8,
              backgroundColor: "#0f172a", border: "1px solid #475569",
              color: "#e2e8f0", fontSize: 14, outline: "none"
            }}
          />
          <button
            onClick={analyzePayment}
            disabled={analyzing || !searchId.trim()}
            style={{
              padding: "10px 20px", borderRadius: 8, border: "none",
              backgroundColor: analyzing ? "#4f46e5aa" : "#4f46e5",
              color: "white", fontWeight: 600, cursor: analyzing ? "not-allowed" : "pointer"
            }}
          >
            {analyzing ? "Analyzing..." : "Analyze"}
          </button>
        </div>

        {/* Analysis Result */}
        {analysisResult && (
          <div style={{
            marginTop: 16, padding: 16, borderRadius: 8,
            backgroundColor: "#0f172a", border: "1px solid #334155"
          }}>
            <h3 style={{ color: "#818cf8", marginBottom: 8 }}>
              Analysis Result — {analysisResult.payment_id}
            </h3>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12, marginBottom: 12 }}>
              <div>
                <div style={{ color: "#94a3b8", fontSize: 12 }}>Recovery Probability</div>
                <div style={{ fontSize: 20, fontWeight: "bold", color: "#4ade80" }}>
                  {(analysisResult.recovery_probability * 100).toFixed(0)}%
                </div>
              </div>
              <div>
                <div style={{ color: "#94a3b8", fontSize: 12 }}>Risk Score</div>
                <div style={{ fontSize: 20, fontWeight: "bold", color: "#facc15" }}>
                  {(analysisResult.risk_score * 100).toFixed(0)}%
                </div>
              </div>
              <div>
                <div style={{ color: "#94a3b8", fontSize: 12 }}>Failure Category</div>
                <div style={{ fontSize: 20, fontWeight: "bold", color: "#c084fc" }}>
                  {analysisResult.failure_category}
                </div>
              </div>
            </div>

            {/* Strategy */}
            {analysisResult.selected_strategy && (
              <div style={{
                padding: 12, borderRadius: 8,
                backgroundColor: "#1e293b", border: "1px solid #334155"
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
                  <Shield size={14} className="text-indigo-400" />
                  <span style={{ fontWeight: 600, color: "#e2e8f0" }}>
                    {analysisResult.selected_strategy.name}
                  </span>
                  {getRiskBadge(analysisResult.selected_strategy.risk_level)}
                </div>
                <p style={{ color: "#94a3b8", fontSize: 13 }}>
                  {analysisResult.selected_strategy.description}
                </p>
              </div>
            )}

            {/* Explanation */}
            {analysisResult.explanation && (
              <p style={{ marginTop: 12, color: "#94a3b8", fontSize: 13, lineHeight: 1.5 }}>
                {analysisResult.explanation}
              </p>
            )}

            {/* Execute Button */}
            <button
              onClick={() => executeRecovery(analysisResult.payment_id)}
              style={{
                marginTop: 12, padding: "8px 16px", borderRadius: 8,
                border: "none", backgroundColor: "#16a34a",
                color: "white", fontWeight: 600, cursor: "pointer"
              }}
            >
              Execute Recovery
            </button>
          </div>
        )}
      </div>

      {/* Recovery Attempts Table */}
      <div style={{
        padding: 20, borderRadius: 12,
        backgroundColor: "#1e293b", border: "1px solid #334155"
      }}>
        <h2 style={{ fontSize: 16, fontWeight: 600, color: "#e2e8f0", marginBottom: 16 }}>
          Recovery Attempts ({recoveries.length})
        </h2>

        {loading ? (
          <div style={{ textAlign: "center", padding: 40, color: "#94a3b8" }}>
            Loading recovery attempts...
          </div>
        ) : recoveries.length === 0 ? (
          <div style={{ textAlign: "center", padding: 40, color: "#94a3b8" }}>
            No recovery attempts yet. Analyze a payment above to get started.
          </div>
        ) : (
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #334155" }}>
                <th style={{ padding: "10px 12px", textAlign: "left", color: "#94a3b8", fontSize: 12 }}>Payment ID</th>
                <th style={{ padding: "10px 12px", textAlign: "left", color: "#94a3b8", fontSize: 12 }}>Strategy</th>
                <th style={{ padding: "10px 12px", textAlign: "left", color: "#94a3b8", fontSize: 12 }}>Status</th>
                <th style={{ padding: "10px 12px", textAlign: "left", color: "#94a3b8", fontSize: 12 }}>Recovered</th>
                <th style={{ padding: "10px 12px", textAlign: "left", color: "#94a3b8", fontSize: 12 }}>Created</th>
              </tr>
            </thead>
            <tbody>
              {recoveries.map((r) => (
                <tr key={r.id} style={{ borderBottom: "1px solid #1e293b" }}>
                  <td style={{ padding: "10px 12px", color: "#e2e8f0", fontFamily: "monospace" }}>
                    {r.payment_id}
                  </td>
                  <td style={{ padding: "10px 12px", color: "#c084fc" }}>{r.strategy}</td>
                  <td style={{ padding: "10px 12px", display: "flex", alignItems: "center", gap: 6 }}>
                    {getStatusIcon(r.status)}
                    <span style={{ color: "#e2e8f0" }}>{r.status}</span>
                  </td>
                  <td style={{ padding: "10px 12px", color: "#4ade80" }}>
                    ₹{r.recovered_amount?.toFixed(2) || "0.00"}
                  </td>
                  <td style={{ padding: "10px 12px", color: "#94a3b8", fontSize: 13 }}>
                    {r.created_at}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
