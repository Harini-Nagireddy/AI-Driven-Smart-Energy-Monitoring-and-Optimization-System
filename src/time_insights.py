import pandas as pd

def time_insights():
    df = pd.read_csv("data/processed/energy_features.csv")

    hourly = df.groupby("hour")["Global_active_power"].mean()
    weekday = df.groupby("weekday")["Global_active_power"].mean()

    print("\nAverage Consumption by Hour:")
    print(hourly)

    print("\nAverage Consumption by Weekday (0=Mon):")
    print(weekday)

if __name__ == "__main__":
    time_insights()
