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
