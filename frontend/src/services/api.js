const API_BASE = "http://localhost:8000/api";

export async function fetchPayments(skip = 0, limit = 50, status = null) {
  const params = new URLSearchParams({ skip, limit });
  if (status) params.append("status", status);
  const res = await fetch(`${API_BASE}/payments?${params}`);
  return res.json();
}

export async function fetchPaymentStats() {
  const res = await fetch(`${API_BASE}/payments/stats`);
  return res.json();
}

export async function fetchPayment(paymentId) {
  const res = await fetch(`${API_BASE}/payments/${paymentId}`);
  return res.json();
}

export async function analyzePayment(paymentId) {
  const res = await fetch(`${API_BASE}/recovery/${paymentId}/analyze`, { method: "POST" });
  return res.json();
}

export async function executeRecovery(paymentId, humanApproved = false) {
  const res = await fetch(
    `${API_BASE}/recovery/${paymentId}/execute?human_approved=${humanApproved}`,
    { method: "POST" }
  );
  return res.json();
}

export async function fetchAnalyticsOverview() {
  const res = await fetch(`${API_BASE}/analytics/overview`);
  return res.json();
}

export async function fetchFailureReasons() {
  const res = await fetch(`${API_BASE}/analytics/failure-reasons`);
  return res.json();
}

export async function fetchPaymentMethods() {
  const res = await fetch(`${API_BASE}/analytics/payment-methods`);
  return res.json();
}

export async function fetchAmountDistribution() {
  const res = await fetch(`${API_BASE}/analytics/amount-distribution`);
  return res.json();
}

export async function fetchRevenueByStrategy() {
  const res = await fetch(`${API_BASE}/analytics/revenue-by-strategy`);
  return res.json();
}

export async function fetchAgentActivity() {
  const res = await fetch(`${API_BASE}/analytics/agent-activity`);
  return res.json();
}
