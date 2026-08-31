import numpy as np
import pickle
from pathlib import Path
from typing import Optional

from sklearn.ensemble import RandomForestClassifier


class RecoveryPredictor:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or "ml/models/model.pkl"
        self.model = None
        if Path(self.model_path).exists():
            try:
                with open(self.model_path, "rb") as model_file:
                    loaded_model = pickle.load(model_file)
                if loaded_model is not None and hasattr(loaded_model, "predict_proba"):
                    self.model = loaded_model
            except (pickle.PickleError, EOFError, AttributeError, ImportError, ValueError):
                self.model = None
        if self.model is None:
            self._train_default()

    def _ensure_model(self):
        if self.model is None or not hasattr(self.model, "predict_proba"):
            self._train_default()

    def _train_default(self):
        np.random.seed(42)
        X = np.random.rand(1000, 5)
        y = (X[:, 0] * 0.3 + X[:, 2] * 0.5 + X[:, 4] * 0.2) > 0.5
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X, y)
        Path(self.model_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.model_path, "wb") as model_file:
            pickle.dump(self.model, model_file)

    def _extract_features(self, payment) -> np.ndarray:
        amount_norm = min(payment.amount / 10000, 1.0)
        categories = {
            "INSUFFICIENT_FUNDS": 0,
            "CARD_EXPIRED": 1,
            "CARD_DECLINED": 2,
            "NETWORK_ERROR": 3,
            "BANK_UNAVAILABLE": 4,
            "LIMIT_EXCEEDED": 5,
            "INVALID_CVV": 6,
            "DUPLICATE": 7,
            "UNKNOWN": 8,
        }
        cat_idx = categories.get(payment.failure_category or "UNKNOWN", 8) / 8.0
        customer_success = getattr(payment, "customer_success_rate", 0.8)
        time_since = 1.0
        retries = 0
        return np.array([amount_norm, cat_idx, customer_success, time_since, retries]).reshape(1, -1)

    def predict(self, payment) -> float:
        self._ensure_model()
        if self.model is None or not hasattr(self.model, "predict_proba"):
            raise ValueError("Recovery model is unavailable")

        features = self._extract_features(payment)
        proba = self.model.predict_proba(features)[0][1]
        return float(proba)