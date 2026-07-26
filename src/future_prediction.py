import pandas as pd
import joblib

def future_prediction():
    model = joblib.load("data/models/energy_model_final.pkl")
    df = pd.read_csv("data/processed/energy_features.csv")

    feature_cols = model.feature_names_in_

    last_row = df[feature_cols].iloc[-1:].copy()

    predictions = model.predict(last_row)

    print("\nNext Hour Predicted Consumption (kW):")
    print(predictions[0])

if __name__ == "__main__":
    future_prediction()
