def recovery_rate(payments):
    eligible = [p for p in payments if p["failure_category"] in ["INSUFFICIENT_FUNDS", "NETWORK_ERROR", "BANK_UNAVAILABLE"]]
    recovered = sum(1 for p in eligible if p["recovered"])
    return recovered / len(eligible) if eligible else 0