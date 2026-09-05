# 🤖 Agentic AI Revenue Recovery Platform

An autonomous AI agent that identifies recoverable failed payments, predicts recovery likelihood, selects bounded recovery strategies, executes simulated actions, and measures recovered revenue.

> Built for the **Razorpay AI Buildathon**

---

## 🎯 Problem

When a payment fails, businesses lose revenue even though the customer may still be willing to pay. Most systems just show failed transactions. This platform **intelligently recovers** them.

## 🧠 How It Works — The Agentic Loop

Failed Payment
      ↓
   OBSERVE     (Analyze payment context, customer history, failure type)
      ↓
   REASON      (Classify failure, predict recovery probability, assess risk)
      ↓
   DECIDE      (Select best strategy with explanation)
      ↓
   ACT         (Execute simulated recovery action)
      ↓
   EVALUATE    (Record outcome, update metrics, learn)

## 🔄 Recovery Strategies

| Strategy | When Used | Risk Level |
|----------|-----------|------------|
| 🔄 Retry Payment | Network timeout, temporary failure | 🟢 Low |
| 🔔 Send Payment Reminder | Insufficient funds, pending | 🟢 Low |
| ⏰ Schedule Retry | Timing-based failures | 🟢 Low |
| 🔗 Generate Payment Link | Card declined, method issue | 🟡 Medium |
| ✉️ Send Email Notification | Customer context suggests | 🟡 Medium |
| 👤 Escalate to Human | Fraud suspected, high value | 🔴 High |
| 🚫 No Action | Recovery probability too low | ⚪ — |

## 📊 Features

- **Dashboard** — Real-time metrics: at-risk revenue, recovery rate, AI actions executed
- **Payments** — Analyze individual failed payments with AI reasoning
- **Recovery Queue** — Priority-sorted pending recoveries with human approval flow
- **AI Agent** — Batch recovery processing + agent activity feed
- **Analytics** — Charts: failure reasons, strategy effectiveness, amount distribution
- **Live Demo** — Step-by-step walkthrough of the agentic loop
- **Settings** — Configurable agent thresholds and strategy weights

## 🏗️ Architecture

┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│   Frontend   │─────▶│    Backend   │─────▶│   SQLite     │
│  React+Vite  │      │   FastAPI    │      │   Database   │
└──────────────┘      └──────┬───────┘      └──────────────┘
                             │
                             │
                    ┌────────▼────────┐
                    │   Recovery AI   │
                    │     Engine      │
                    │                 │
                    │ ┌─────────────┐ │
                    │ │    Agent    │ │
                    │ │  (Decision) │ │
                    │ └─────────────┘ │
                    │ ┌─────────────┐ │
                    │ │  Guardrails │ │
                    │ │  (Policy)   │ │
                    │ └─────────────┘ │
                    │ ┌─────────────┐ │
                    │ │  Tools/API  │ │
                    │ └─────────────┘ │
                    └─────────────────┘
                    
## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+

### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
python seed_data.py
python -m uvicorn main:app --reload
# Agentic AI Revenue Recovery Platform

**Razorpay AI Buildathon submission** — an agentic system that analyzes failed
payments, predicts recoverability, selects a bounded recovery strategy, passes it
through deterministic guardrails, executes safely, and tracks recovered revenue.

```
Failed Payment
    ↓  Payment Intelligence Agent — analyze context, failure category
    ↓  Recovery Prediction — recovery probability + risk score
    ↓  Strategy Agent — pick a bounded recovery strategy
    ↓  Risk / Guardrail Engine — SAFE → execute | UNSAFE → human review
    ↓  Execution → observe result → update state → revenue analytics
```

---


## Setup

```powershell
# Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1       # Windows
pip install -r requirements.txt

# Frontend
cd frontend
npm install
cd ..
```

---

## Run

### 1. Backend API — http://localhost:8000

```powershell
cd backend
uvicorn main:app --reload --port 8000
```

Interactive docs: http://localhost:8000/docs

### 2. Frontend — http://localhost:5173

```powershell
cd frontend
npm run dev
```

> The frontend calls the backend at `http://localhost:8000/api` (CORS enabled).

### 3. Seed demo data (first run only)

```powershell
python backend/seed.py        # adjust to your seed script name if different
```

Creates ~50 failed payments with realistic failure categories and customer history.

---

## API Routes

| Method | Route                                  | Description                        |
|--------|----------------------------------------|------------------------------------|
| GET    | `/api/health`                          | Health check                       |
| GET    | `/api/payments`                        | List payments                      |
| GET    | `/api/payments/{payment_id}`           | Payment detail                     |
| POST   | `/api/payments/simulate-failure`       | Create a simulated failed payment  |
| GET    | `/api/recovery/`                       | Recovery attempts queue            |
| POST   | `/api/recovery/{payment_id}/analyze`   | Run agent analysis                 |
| POST   | `/api/recovery/{payment_id}/execute`   | Execute (guardrail-approved)       |
| GET    | `/api/recovery/{payment_id}/history`   | Attempt history                    |
| GET    | `/api/agent/activity`                  | Agent activity feed                |
| POST   | `/api/agent/batch-recovery`            | Batch run over recoverable queue   |
| GET    | `/api/agent/stats`                     | Agent stats                        |
| GET    | `/api/analytics/overview`              | KPIs (recovered ₹, recovery rate)  |
| GET    | `/api/analytics/failure-reasons`       | Failure breakdown                  |
| GET    | `/api/analytics/payment-methods`       | Method breakdown                   |
| GET    | `/api/analytics/revenue-by-strategy`   | Revenue by strategy                |
| GET    | `/api/analytics/agent-activity`        | Recent agent decisions             |
| POST   | `/api/webhooks/payment`                | Razorpay-style failed-payment hook |
| GET    | `/api/webhooks/events`                 | Recent webhook events              |

---

## Agent Workflow

1. **Observe** — a payment fails (directly or via webhook).
2. **Analyze** — `POST /api/recovery/{id}/analyze` runs the Payment Intelligence
   Agent: failure category, customer history, retry count, amount.
3. **Predict** — the agent returns a recovery probability and risk score.
4. **Plan** — a Strategy Agent picks one bounded strategy (retry, card update,
   dunning email, etc.).
5. **Validate** — the deterministic Guardrail / Action Validator checks the
   recommendation (retry limits, cooldowns, non-retryable categories,
   high-value thresholds). Unsafe actions are **blocked → human review**.
6. **Execute** — safe actions run through the simulated payment executor.
7. **Observe outcome** — success updates `recovered_amount` and revenue analytics;
   failure feeds the learning signal for future decisions.

The AI/agent never executes unrestricted payment operations — every action passes
through guardrails first.

---

## Tests

```powershell
pytest backend/tests -v
```

All **8 tests pass**:

- `test_recovery_agent_high_probability` ✅
- `test_recovery_agent_low_probability` ✅
- `test_action_validator_non_retryable` ✅
- `test_health` ✅
- `test_list_payments` ✅
- `test_simulate_failure` ✅
- `test_analyze_payment` ✅
- `test_execute_recovery` ✅
- `test_webhook_failed_payment` ✅

---

## CI

`.github/workflows/tests.yml` runs on every push/PR to `main`:

- **Backend job** — Python 3.11: `pip install -r requirements.txt` →
  `pytest backend/tests -v`
- **Frontend job** — Node 18: `npm install` → `npm run build`

---

## Notes

- SQLite schema is created automatically at app import
  (`Base.metadata.create_all`).
- `httpx==0.27.2` is pinned for Starlette `TestClient` compatibility in CI.
- Routes are versioned as `/api/*` (no `/api/v1` prefix).
