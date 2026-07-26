import pandas as pd
import os

def feature_engineering():
    print("Loading processed data...")
    df = pd.read_csv("data/processed/energy_processed.csv")

    # Convert DateTime if exists
    if "DateTime" in df.columns:
        df["DateTime"] = pd.to_datetime(df["DateTime"])
        df["hour"] = df["DateTime"].dt.hour
        df["day"] = df["DateTime"].dt.day
        df["weekday"] = df["DateTime"].dt.weekday
        df["month"] = df["DateTime"].dt.month
        df.drop(columns=["DateTime"], inplace=True)

    # Appliance total usage
    df["total_sub_metering"] = (
        df["Sub_metering_1"] +
        df["Sub_metering_2"] +
        df["Sub_metering_3"]
    )

    # Appliance usage ratios
    df["kitchen_ratio"] = df["Sub_metering_1"] / (df["total_sub_metering"] + 1)
    df["laundry_ratio"] = df["Sub_metering_2"] / (df["total_sub_metering"] + 1)
    df["hvac_ratio"] = df["Sub_metering_3"] / (df["total_sub_metering"] + 1)

    # Save
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/energy_features.csv", index=False)

    print("Feature engineering completed.")
    print("New shape:", df.shape)

if __name__ == "__main__":
    feature_engineering()
