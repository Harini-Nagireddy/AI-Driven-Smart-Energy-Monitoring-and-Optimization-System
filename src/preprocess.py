import pandas as pd
import os

def preprocess():
    print("Loading raw data...")

    df = pd.read_csv(
        "data/raw/household_power_consumption.csv",
        sep=","
    )

    print("Initial shape:", df.shape)
    print("Columns:", df.columns.tolist())

    # Combine Date + Time safely
    df["DateTime"] = pd.to_datetime(
        df["Date"] + " " + df["Time"],
        dayfirst=True,
        errors="coerce"
    )

    # Drop original columns
    df.drop(columns=["Date", "Time"], inplace=True)

    # Convert all numeric columns properly
    numeric_cols = [
        "Global_active_power",
        "Global_reactive_power",
        "Voltage",
        "Global_intensity",
        "Sub_metering_1",
        "Sub_metering_2",
        "Sub_metering_3"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Handle missing values
    df.fillna(method="ffill", inplace=True)
    df.dropna(inplace=True)

    # Save processed data
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/energy_processed.csv", index=False)

    print("Preprocessing completed.")
    print("Final shape:", df.shape)

if __name__ == "__main__":
    preprocess()
