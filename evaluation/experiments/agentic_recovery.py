def run_agentic(payments, predictor, agent):
    """Agentic: use ML + agent to decide."""
    recovered = 0
    for p in payments:
        prob = predictor.predict(p)
        decision = agent.analyze(p, prob)["decision"]
        if decision == "RETRY":
            recovered += 1
    return recovered / len(payments)