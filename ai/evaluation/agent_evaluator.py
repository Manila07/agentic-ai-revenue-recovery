from typing import List, Dict

class AgentEvaluator:
    def evaluate(self, scenarios: List[Dict]) -> Dict:
        correct = sum(1 for s in scenarios if s["expected"] == s["actual"])
        total = len(scenarios)
        return {"accuracy": correct / total if total else 0, "correct": correct, "total": total}