def run_baseline(payments):
    """Baseline: retry all payments once."""
    recovered = 0
    for p in payments:
        if p["failure_category"] not in ["CARD_EXPIRED", "INVALID_CVV"]:
            recovered += 1
    return recovered / len(payments)