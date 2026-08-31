import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def generate_synthetic_data(n_samples=2000):
    np.random.seed(42)
    data = {
        "amount": np.random.uniform(100, 10000, n_samples),
        "failure_category": np.random.randint(0, 9, n_samples),
        "customer_success_rate": np.random.uniform(0.3, 1.0, n_samples),
        "time_since_failure": np.random.uniform(0, 24, n_samples),
        "retry_count": np.random.randint(0, 4, n_samples),
        "is_high_value": np.random.randint(0, 2, n_samples),
        "is_premium_customer": np.random.randint(0, 2, n_samples),
    }
    df = pd.DataFrame(data)
    prob = (
        (1 - df["amount"] / 10000) * 0.3 +
        df["customer_success_rate"] * 0.4 +
        (1 - df["retry_count"] / 3) * 0.2 +
        (1 - df["failure_category"] / 8) * 0.1
    )
    df["recovered"] = (prob > 0.5).astype(int)
    return df

def train():
    df = generate_synthetic_data()
    X = df.drop("recovered", axis=1)
    y = df["recovered"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
    }
    model_path = Path("ml/models/model.pkl")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    pickle.dump(model, open(model_path, "wb"))
    import json
    with open("ml/models/model_metadata.json", "w") as f:
        json.dump({"metrics": metrics, "features": list(X.columns), "n_samples": len(df)}, f, indent=2)
    print(f"Model trained. Metrics: {metrics}")

if __name__ == "__main__":
    train()