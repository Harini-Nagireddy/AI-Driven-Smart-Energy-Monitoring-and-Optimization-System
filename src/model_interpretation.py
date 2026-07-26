import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

def model_interpretation():
    print("Loading model and data...")

    # Load data
    df = pd.read_csv("data/processed/energy_features.csv")

    # Separate features & target
    X = df.drop(columns=["Global_active_power"])
    y = df["Global_active_power"]

    # Load trained model
    model = joblib.load("data/models/energy_model_final.pkl")

    # -------------------------------
    # Feature Importance
    # -------------------------------
    importances = model.feature_importances_
    feature_names = X.columns

    feature_importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances
    }).sort_values(by="Importance", ascending=False)

    # Plot feature importance
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x="Importance",
        y="Feature",
        data=feature_importance_df
    )
    plt.title("Feature Importance - Energy Consumption Prediction")
    plt.tight_layout()
    plt.show()

    print("\nTop Important Features:")
    print(feature_importance_df.head(10))

if __name__ == "__main__":
    model_interpretation()
