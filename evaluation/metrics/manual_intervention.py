def manual_intervention_rate(payments):
    escalated = sum(1 for p in payments if p.get("escalated", False))
    return escalated / len(payments) if payments else 0