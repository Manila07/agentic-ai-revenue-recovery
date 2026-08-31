def revenue_recovered(payments):
    return sum(p["amount"] for p in payments if p["recovered"])