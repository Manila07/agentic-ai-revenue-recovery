from ml.models.recovery_predictor import RecoveryPredictor

def predict_recovery_probability(payment) -> float:
    predictor = RecoveryPredictor()
    return predictor.predict(payment)