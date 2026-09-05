import { useState } from "react";

const API = "http://localhost:8000/api";

const STEPS = [
  {
    id: 1,
    title: "Observe",
    icon: "👁️",
    description: "Agent observes a failed payment and collects context",
  },
  {
    id: 2,
    title: "Reason",
    icon: "🧠",
    description: "AI reasons about failure type and recovery probability",
  },
  {
    id: 3,
    title: "Decide",
    icon: "🎯",
    description: "Agent selects the best recovery strategy",
  },
  {
    id: 4,
    title: "Act",
    icon: "⚡",
    description: "Agent executes the chosen recovery action",
  },
  {
    id: 5,
    title: "Evaluate",
    icon: "📊",
    description: "Result is recorded and metrics updated",
  },
];

export default function LiveDemo() {
  const [paymentId, setPaymentId] = useState("");
  const [currentStep, setCurrentStep] = useState(0);
  const [analysis, setAnalysis] = useState(null);
  const [execution, setExecution] = useState(null);
  const [error, setError] = useState(null);

  async function startDemo() {
    if (!paymentId.trim()) return;
    setCurrentStep(1);
    setAnalysis(null);
    setExecution(null);
    setError(null);

    // Step 1: Observe
    await delay(1000);
    setCurrentStep(2);

    // Step 2: Reason — call analyze
    try {
      const res = await fetch(`${API}/recovery/${paymentId}/analyze`, {
        method: "POST",
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      setAnalysis(data);
      setCurrentStep(3);
      await delay(1000);
      setCurrentStep(4);

      // Step 3: Decide
      await delay(1000);
      setCurrentStep(5);

      // Step 4: Act — call execute
      const execRes = await fetch(`${API}/recovery/${paymentId}/execute`, {
        method: "POST",
      });
      const execData = await execRes.json();
      setExecution(execData);
      setCurrentStep(6);
    } catch (e) {
      setError(e.message);
      setCurrentStep(0);
    }
  }

  function reset() {
    setCurrentStep(0);
    setAnalysis(null);
    setExecution(null);
    setError(null);
  }

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold text-white mb-2">🎬 Live Demo</h1>
      <p className="text-gray-400 mb-6">
        Walk through the full Agentic AI loop: Observe → Reason → Decide → Act →
        Evaluate
      </p>

      {/* Input */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 p-6 mb-8">
        <h3 className="text-white font-semibold mb-3">Enter a Failed Payment ID</h3>
        <div className="flex gap-3">
          <input
            type="text"
            placeholder="e.g. PAY_321626B1"
            value={paymentId}
            onChange={(e) => setPaymentId(e.target.value)}
            className="flex-1 bg-gray-900 border border-gray-600 rounded px-4 py-2 text-white"
          />
          <button
            onClick={startDemo}
            disabled={currentStep > 0 && currentStep < 6}
            className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded font-bold"
          >
            {currentStep > 0 && currentStep < 6 ? "Running..." : "Start Demo"}
          </button>
          {currentStep >= 1 && (
            <button
              onClick={reset}
              className="px-4 py-2 bg-gray-600 hover:bg-gray-500 text-white rounded"
            >
              Reset
            </button>
          )}
        </div>
      </div>

      {/* Steps */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
        {STEPS.map((step) => (
          <div
            key={step.id}
            className={`rounded-lg p-4 border text-center transition-all ${
              currentStep > step.id
                ? "bg-green-900/30 border-green-500"
                : currentStep === step.id
                ? "bg-blue-900/30 border-blue-500 animate-pulse"
                : "bg-gray-800 border-gray-700"
            }`}
          >
            <p className="text-3xl mb-2">{step.icon}</p>
            <p
              className={`font-bold ${
                currentStep >= step.id ? "text-white" : "text-gray-500"
              }`}
            >
              {step.title}
            </p>
            <p className="text-gray-400 text-xs mt-1">{step.description}</p>
          </div>
        ))}
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-900/30 border border-red-500 rounded-lg p-4 mb-6">
          <p className="text-red-400 font-bold">Error</p>
          <p className="text-gray-300 text-sm">{error}</p>
        </div>
      )}

      {/* Analysis Result */}
      {analysis && currentStep >= 3 && (
        <div className="bg-gray-800 rounded-lg border border-gray-700 p-6 mb-6">
          <h3 className="text-white font-semibold mb-4">🧠 AI Analysis</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
            <div className="bg-gray-900 rounded p-3">
              <p className="text-gray-400 text-sm">Recovery Probability</p>
              <p
                className={`text-2xl font-bold ${
                  analysis.recovery_probability >= 0.7
                    ? "text-green-400"
                    : analysis.recovery_probability >= 0.4
                    ? "text-yellow-400"
                    : "text-red-400"
                }`}
              >
                {((analysis.recovery_probability || 0) * 100).toFixed(1)}%
              </p>
            </div>
            <div className="bg-gray-900 rounded p-3">
              <p className="text-gray-400 text-sm">Selected Strategy</p>
              <p className="text-blue-400 font-bold">
                {analysis.selected_strategy?.name}
              </p>
            </div>
            <div className="bg-gray-900 rounded p-3">
              <p className="text-gray-400 text-sm">Risk Score</p>
              <p className="text-yellow-400 font-bold">
                {((analysis.risk_score || 0) * 100).toFixed(0)}%
              </p>
            </div>
          </div>
          <div className="bg-gray-900 rounded p-3">
            <p className="text-gray-400 text-sm mb-1">AI Reasoning</p>
            <p className="text-gray-300 text-sm">{analysis.explanation}</p>
          </div>
        </div>
      )}

      {/* Execution Result */}
      {execution && currentStep >= 6 && (
        <div
          className={`rounded-lg border p-6 ${
            execution.success
              ? "bg-green-900/20 border-green-500"
              : "bg-red-900/20 border-red-500"
          }`}
        >
          <h3 className={`font-bold text-lg mb-2 ${
            execution.success ? "text-green-400" : "text-red-400"
          }`}>
            {execution.success
              ? "✅ Recovery Successful!"
              : "❌ Recovery Failed"}
          </h3>
          <p className="text-gray-300">
            Amount Recovered: ₹{(execution.recovered_amount || 0).toLocaleString()}
          </p>
          <p className="text-gray-400 text-sm mt-1">{execution.message}</p>
        </div>
      )}
    </div>
  );
}

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
