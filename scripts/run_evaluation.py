from evaluation.experiments.comparison import compare
from evaluation.metrics.recovery_rate import recovery_rate
from evaluation.metrics.revenue_recovered import revenue_recovered
import pandas as pd

# Load test data
df = pd.read_csv("evaluation/datasets/test.csv")
payments = df.to_dict("records")

# Simple predictor and agent mock
class SimplePredictor:
    def predict(self, p):
        return 0.8 if p["failure_category"] != "CARD_EXPIRED" else 0.1

class SimpleAgent:
    def analyze(self, p, prob):
        return {"decision": "RETRY" if prob > 0.5 else "STOP"}

result = compare(payments, SimplePredictor(), SimpleAgent())
print(result)