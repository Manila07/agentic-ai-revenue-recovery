import sys
import os

# Add project root to sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from ai.agents.recovery_agent import RecoveryAgent
from ai.guardrails.guardrail_policy import GuardrailPolicy
from evaluation.scenarios import SCENARIOS

def run_evaluation():
    agent = RecoveryAgent()
    policy = GuardrailPolicy()

    results = []
    for scenario in SCENARIOS:
        # 1. Agent reasoning
        agent_result = agent.analyze(scenario["payment"])
        # 2. Guardrail validation
        is_allowed, decision_type, reason = policy.validate(agent_result["decision"], scenario["payment"])
        
        actual_decision = agent_result["decision"]
        if decision_type == "BLOCK":
            actual_decision = "BLOCKED"
        elif decision_type == "NEEDS_APPROVAL":
            actual_decision = "ESCALATE"
        
        expected = scenario["expected_decision"]
        correct = actual_decision == expected
        
        results.append({
            "scenario": scenario["id"],
            "expected": expected,
            "actual": actual_decision,
            "correct": correct,
            "guardrail": decision_type,
            "reason": reason,
        })

    # Metrics
    accuracy = sum(1 for r in results if r["correct"]) / len(results)
    print(f"\n== Evaluation Results ==")
    print(f"Decision Accuracy: {accuracy:.2%}")
    for r in results:
        print(f"  {r['scenario']}: Expected={r['expected']}, Actual={r['actual']} -> {'✅' if r['correct'] else '❌'}")
    print(f"\nGuardrail Analysis:")
    for r in results:
        print(f"  {r['scenario']}: {r['guardrail']} ({r['reason']})")

if __name__ == "__main__":
    run_evaluation()