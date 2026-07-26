import pandas as pd
import matplotlib.pyplot as plt

def behavioral_insights():
    df = pd.read_csv("data/processed/energy_processed.csv")

    df["hour"] = pd.to_datetime(df["DateTime"]).dt.hour

    hourly = df.groupby("hour")["Global_active_power"].mean()

    hourly.plot(figsize=(10,4))
    plt.title("Hourly Energy Usage Pattern")
    plt.xlabel("Hour of Day")
    plt.ylabel("Avg Power (kW)")
    plt.show()

if __name__ == "__main__":
    behavioral_insights()
