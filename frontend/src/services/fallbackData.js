export const demoPayments = [
  {
    id: 'pay_demo_001',
    customer_id: 'cust_001',
    amount: 8500,
    currency: 'INR',
    method: 'card',
    status: 'FAILED',
    failure_reason: 'insufficient_funds',
    failure_category: 'INSUFFICIENT_FUNDS',
    created_at: new Date().toISOString(),
    recovered: false,
    recovered_amount: 0,
    recovery_probability: 0.85
  },
  {
    id: 'pay_demo_002',
    customer_id: 'cust_002',
    amount: 24500,
    currency: 'INR',
    method: 'upi',
    status: 'FAILED',
    failure_reason: 'network_error',
    failure_category: 'NETWORK_ERROR',
    created_at: new Date().toISOString(),
    recovered: false,
    recovered_amount: 0,
    recovery_probability: 0.62
  },
  {
    id: 'pay_demo_003',
    customer_id: 'cust_003',
    amount: 125000,
    currency: 'INR',
    method: 'card',
    status: 'FAILED',
    failure_reason: 'bank_unavailable',
    failure_category: 'BANK_UNAVAILABLE',
    created_at: new Date().toISOString(),
    recovered: false,
    recovered_amount: 0,
    recovery_probability: 0.74
  },
  {
    id: 'pay_demo_004',
    customer_id: 'cust_004',
    amount: 5600,
    currency: 'INR',
    method: 'netbanking',
    status: 'FAILED',
    failure_reason: 'card_declined',
    failure_category: 'CARD_DECLINED',
    created_at: new Date().toISOString(),
    recovered: false,
    recovered_amount: 0,
    recovery_probability: 0.34
  }
]

export const demoAnalyticsOverview = {
  total_payments: 1042,
  failed_payments: 178,
  recovered_payments: 52,
  revenue_at_risk: 2450000,
  recovered_revenue: 680000,
  recovery_rate: 29.2,
  pending_recovery: 126
}

export const demoAgentActions = [
  {
    id: 1,
    payment_id: 'pay_demo_001',
    decision: 'RETRY',
    reasoning: 'High recovery probability (85%). Attempting immediate retry.',
    confidence: 0.85,
    tool_name: 'retry_payment',
    status: 'EXECUTED',
    created_at: new Date().toISOString()
  },
  {
    id: 2,
    payment_id: 'pay_demo_002',
    decision: 'NOTIFY',
    reasoning: 'Moderate recovery probability (62%). Notify customer to resolve issue.',
    confidence: 0.62,
    tool_name: 'send_notification',
    status: 'PROPOSED',
    created_at: new Date().toISOString()
  }
]