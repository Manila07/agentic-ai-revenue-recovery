from typing import List, Dict

class ToolEvaluator:
    def evaluate(self, tool_results: List[Dict]) -> Dict:
        success = sum(1 for r in tool_results if r.get("success"))
        total = len(tool_results)
        return {"success_rate": success / total if total else 0}