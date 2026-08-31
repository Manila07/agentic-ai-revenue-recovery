def false_retry_rate(attempts):
    """Attempts: list of dicts with action and success."""
    retries = [a for a in attempts if a["action"] == "RETRY"]
    false = [a for a in retries if not a["success"]]
    return len(false) / len(retries) if retries else 0