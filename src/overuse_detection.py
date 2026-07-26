import pandas as pd

def overuse_detection():
    print("Loading feature data...")
    df = pd.read_csv("data/processed/energy_features.csv")

    # Appliance mapping
    appliances = {
        "Kitchen": "Sub_metering_1",
        "Laundry": "Sub_metering_2",
        "HVAC": "Sub_metering_3"
    }

    print("\nAverage Consumption (Wh per minute):")
    avg_usage = {}

    for name, col in appliances.items():
        avg = df[col].mean()
        avg_usage[name] = avg
        print(f"{name}: {avg:.2f}")

    # Overuse threshold (30% above average)
    print("\nOveruse Alerts:")
    for name, col in appliances.items():
        threshold = avg_usage[name] * 1.3
        overused_count = (df[col] > threshold).sum()

        print(f"{name}: Overused {overused_count} times")

        if overused_count > 0:
            print(f"⚠ Recommendation: Reduce unnecessary usage of {name}")

if __name__ == "__main__":
    overuse_detection()
