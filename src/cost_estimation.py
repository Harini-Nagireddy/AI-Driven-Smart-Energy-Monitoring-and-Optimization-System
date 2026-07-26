import pandas as pd

def cost_estimation():
    print("Loading feature data...")
    df = pd.read_csv("data/processed/energy_features.csv")

    # Electricity rate (India average ₹ per kWh)
    COST_PER_KWH = 6.0  

    # Total energy in watt-hour per minute
    df["total_energy_wh"] = (
        df["Sub_metering_1"] +
        df["Sub_metering_2"] +
        df["Sub_metering_3"]
    )

    # Convert to kWh
    total_kwh = df["total_energy_wh"].sum() / 1000

    total_cost = total_kwh * COST_PER_KWH

    print("\n----- Electricity Cost Estimation -----")
    print(f"Total Energy Used: {total_kwh:.2f} kWh")
    print(f"Estimated Bill: ₹{total_cost:.2f}")

    # Appliance-wise cost
    print("\nAppliance-wise Cost:")
    for name, col in {
        "Kitchen": "Sub_metering_1",
        "Laundry": "Sub_metering_2",
        "HVAC": "Sub_metering_3"
    }.items():
        kwh = df[col].sum() / 1000
        cost = kwh * COST_PER_KWH
        print(f"{name}: ₹{cost:.2f}")

if __name__ == "__main__":
    cost_estimation()
