from evaluation.experiments.baseline import run_baseline
from evaluation.experiments.agentic_recovery import run_agentic

def compare(payments, predictor, agent):
    baseline_rate = run_baseline(payments)
    agentic_rate = run_agentic(payments, predictor, agent)
    return {
        "baseline_recovery_rate": baseline_rate,
        "agentic_recovery_rate": agentic_rate,
        "improvement": agentic_rate - baseline_rate,
    }