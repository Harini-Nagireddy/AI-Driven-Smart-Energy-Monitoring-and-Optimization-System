import pandas as pd

def appliance_insights():
    print("Loading feature engineered data...")
    df = pd.read_csv("data/processed/energy_features.csv")

    appliance_usage = {
        "Kitchen Appliances": df["Sub_metering_1"].sum(),
        "Laundry + Fridge": df["Sub_metering_2"].sum(),
        "HVAC (AC/Heater)": df["Sub_metering_3"].sum()
    }

    print("\nAppliance-wise Energy Consumption:")
    for k, v in appliance_usage.items():
        print(f"{k}: {v:.2f} Wh")

    max_appliance = max(appliance_usage, key=appliance_usage.get)
    print(f"\n⚠️ Highest Energy Consumer: {max_appliance}")

    if max_appliance == "HVAC (AC/Heater)":
        print("Recommendation: Reduce AC/Heater usage, especially during mild weather.")
    elif max_appliance == "Kitchen Appliances":
        print("Recommendation: Use energy-efficient cooking practices.")
    else:
        print("Recommendation: Optimize laundry cycles and switch to LED lighting.")

if __name__ == "__main__":
    appliance_insights()
