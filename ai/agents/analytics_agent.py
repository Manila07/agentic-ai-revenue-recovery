from typing import Dict, List

class AnalyticsAgent:
    def summarize(self, payments: List) -> Dict:
        total = len(payments)
        recovered = sum(1 for p in payments if p.recovered)
        revenue_recovered = sum(p.recovered_amount for p in payments)
        revenue_at_risk = sum(p.amount for p in payments if not p.recovered)
        return {
            "total": total,
            "recovered": recovered,
            "recovery_rate": (recovered / total * 100) if total else 0,
            "revenue_recovered": revenue_recovered,
            "revenue_at_risk": revenue_at_risk,
        }