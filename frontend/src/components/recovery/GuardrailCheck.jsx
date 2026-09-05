export default function GuardrailCheck({ guardrail }) {
  if (!guardrail) return null;
  const styles = {
    ALLOW: "bg-green-100 text-green-800 border-green-300",
    NEEDS_APPROVAL: "bg-yellow-100 text-yellow-800 border-yellow-300",
    BLOCK: "bg-red-100 text-red-800 border-red-300",
  };
  return (
    <div className={`mt-3 p-2 rounded border ${styles[guardrail.decision_type] || "bg-gray-100"}`}>
      <span className="text-xs font-semibold">{guardrail.decision_type}</span>
      <span className="text-xs text-gray-600 ml-2">{guardrail.reason}</span>
    </div>
  );
}