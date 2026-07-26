import pandas as pd

def bill_estimation():
    df = pd.read_csv("data/processed/energy_features.csv")

    # Convert kW-minute to kWh
    df["energy_kWh"] = df["Global_active_power"] / 60

    monthly_kwh = df.groupby("month")["energy_kWh"].sum()

    COST_PER_KWH = 6.0  # ₹ per unit (India average)

    bill = monthly_kwh * COST_PER_KWH

    print("\nEstimated Monthly Electricity Bill (₹):")
    print(bill)

if __name__ == "__main__":
    bill_estimation()
