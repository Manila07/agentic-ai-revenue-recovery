import pickle
import numpy as np
from sklearn.metrics import classification_report
from ml.training.train import generate_synthetic_data
from sklearn.model_selection import train_test_split

def evaluate():
    df = generate_synthetic_data(1000)
    X = df.drop("recovered", axis=1)
    y = df["recovered"]
    _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = pickle.load(open("ml/models/model.pkl", "rb"))
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    evaluate()