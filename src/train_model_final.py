import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import os

def train_model():
    print("Loading feature-engineered data...")
    df = pd.read_csv("data/processed/energy_features.csv")

    # Target variable
    y = df["Global_active_power"]

    # Drop non-feature columns
    X = df.drop(columns=[
        "Global_active_power",
        "DateTime"
    ], errors="ignore")

    print("Features shape:", X.shape)
    print("Target shape:", y.shape)

    # Train-test split (time-aware: no shuffle)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    print("Training RandomForest model...")
    model = RandomForestRegressor(
        n_estimators=50,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)

    print("\nModel Evaluation")
    print("----------------")
    print("MAE:", mean_absolute_error(y_test, y_pred))
    print("R2 Score:", r2_score(y_test, y_pred))

    # Save model
    os.makedirs("data/models", exist_ok=True)
    joblib.dump(model, "data/models/energy_model_final.pkl")
    print("\nModel saved to data/models/energy_model_final.pkl")

if __name__ == "__main__":
    train_model()
