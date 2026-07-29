import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os
from datetime import date

st.set_page_config(page_title="Smart Energy Optimizer", layout="wide")
st.title("⚡ Smart Energy Monitoring & Optimization System")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "data", "models", "energy_model_final.pkl")
PROFILE_PATH = os.path.join(BASE_DIR, "data", "processed", "monthly_hourly_profile.csv")


# ---------------- LOAD ML MODEL + SEASONAL PROFILE (cached) ----------------
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_profile():
    return pd.read_csv(PROFILE_PATH)


if not os.path.exists(MODEL_PATH):
    st.warning("Training ML model for the first time... Please wait.")

    import subprocess
    import sys

    train_script = os.path.join(BASE_DIR, "src", "train_model_final.py")

    subprocess.run(
        [sys.executable, train_script],
        check=True
    )

model = load_model()
seasonal_profile = load_profile()
FEATURE_COLS = list(model.feature_names_in_)


def predicted_monthly_kwh_for_month(month: int) -> float:
    """
    Uses the trained RandomForest model together with a precomputed hourly
    seasonal profile (built from real smart-meter data) to estimate a
    reference household's expected monthly kWh for a given calendar month.
    """
    sub = seasonal_profile[seasonal_profile["month"] == month].copy()
    if sub.empty:
        sub = seasonal_profile.copy()
    X = sub[FEATURE_COLS]
    hourly_kw = model.predict(X)      # predicted avg kW per hour of a typical day
    daily_kwh = hourly_kw.sum()       # 24 hourly averages ~ kWh for that day
    return float(daily_kwh * 30)


# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("🏠 Household Inputs")

ac_count = st.sidebar.number_input("Number of ACs", 0, 10, 1)
ac_hours = st.sidebar.slider("AC usage (hours/day)", 0, 24, 6)

fridge = st.sidebar.selectbox("Refrigerator", ["Yes", "No"])
wm_uses = st.sidebar.slider("Washing Machine uses/week", 0, 14, 3)

lights = st.sidebar.number_input("Number of Lights", 0, 50, 8)
fans = st.sidebar.number_input("Number of Fans", 0, 20, 4)

rate = st.sidebar.number_input("Electricity rate (₹/unit)", 1.0, 20.0, 6.0)

calculate = st.sidebar.button("🔎 Calculate", use_container_width=True)

if calculate:
    st.session_state["calculated"] = True
    st.session_state["inputs"] = dict(
        ac_count=ac_count, ac_hours=ac_hours, fridge=fridge,
        wm_uses=wm_uses, lights=lights, fans=fans, rate=rate,
    )

if not st.session_state.get("calculated"):
    st.info("👈 Set your household details in the sidebar and click **Calculate** to see your energy summary.")
    st.stop()

inp = st.session_state["inputs"]
ac_count, ac_hours, fridge = inp["ac_count"], inp["ac_hours"], inp["fridge"]
wm_uses, lights, fans, rate = inp["wm_uses"], inp["lights"], inp["fans"], inp["rate"]

# ---------------- ENERGY LOGIC ----------------
AC_POWER = 1.5          # kWh per hour
FRIDGE_DAILY = 1.2
WM_PER_USE = 0.8
LIGHT_PER_DAY = 0.05
FAN_PER_DAY = 0.07

ac_energy = ac_count * ac_hours * AC_POWER * 30
fridge_energy = FRIDGE_DAILY * 30 if fridge == "Yes" else 0
wm_energy = wm_uses * WM_PER_USE * 4
light_energy = lights * LIGHT_PER_DAY * 30
fan_energy = fans * FAN_PER_DAY * 30

total_energy = ac_energy + fridge_energy + wm_energy + light_energy + fan_energy
bill = total_energy * rate

# ---------------- DASHBOARD ----------------
st.subheader("📊 Energy Summary")

col1, col2 = st.columns(2)
col1.metric("Monthly Consumption (kWh)", f"{total_energy:.2f}")
col2.metric("Estimated Bill (₹)", f"₹ {bill:.2f}")

# Appliance-wise chart
st.subheader("🔌 Appliance-wise Consumption")

appliance_df = pd.DataFrame({
    "Appliance": ["AC", "Refrigerator", "Washing Machine", "Lights", "Fans"],
    "Energy (kWh)": [ac_energy, fridge_energy, wm_energy, light_energy, fan_energy],
})

fig, ax = plt.subplots()
bars = ax.bar(appliance_df["Appliance"], appliance_df["Energy (kWh)"], color="#1f77b4")
ax.set_ylabel("kWh / Month")
ax.bar_label(bars, fmt="%.1f")
st.pyplot(fig)

# ---------------- ML-DRIVEN FUTURE PREDICTION ----------------
st.subheader("🔮 Next Month Prediction (ML-driven)")

today = date.today()
current_month = today.month
next_month = 1 if current_month == 12 else current_month + 1

baseline_current = predicted_monthly_kwh_for_month(current_month)
baseline_next = predicted_monthly_kwh_for_month(next_month)
seasonal_trend = (baseline_next / baseline_current) if baseline_current else 1.0
seasonal_trend = float(np.clip(seasonal_trend, 0.85, 1.20))  # keep projections sane

future_energy = total_energy * seasonal_trend
future_bill = future_energy * rate

st.success(f"🔹 Predicted Consumption: **{future_energy:.2f} kWh**")
st.success(f"🔹 Predicted Bill: **₹ {future_bill:.2f}**")

trend_pct = (seasonal_trend - 1) * 100
direction = "increase" if trend_pct >= 0 else "decrease"
st.caption(
    f"📈 A RandomForest model trained on real household smart-meter data predicts a "
    f"seasonal **{direction} of {abs(trend_pct):.1f}%** heading into next month, "
    f"applied to your current usage profile."
)

# ---------------- DATA-DRIVEN OPTIMIZATION SUGGESTIONS ----------------
st.subheader("💡 Optimization Suggestions")

contributions = {
    "AC": ac_energy,
    "Refrigerator": fridge_energy,
    "Washing Machine": wm_energy,
    "Lights": light_energy,
    "Fans": fan_energy,
}
top_appliance = max(contributions, key=contributions.get)
top_share = (contributions[top_appliance] / total_energy * 100) if total_energy else 0

tips = []

if ac_hours > 8 and ac_count > 0:
    saving = ac_count * 1 * AC_POWER * 30 * rate
    tips.append(f"Your AC runs {ac_hours} hrs/day — cutting just 1 hr/day would save ≈ ₹{saving:.0f}/month.")

if lights > 10:
    saving = light_energy * 0.6 * rate
    tips.append(f"Switching your {lights} bulbs to LED could cut lighting cost by ~60% (≈ ₹{saving:.0f}/month saved).")

if fans > 6:
    tips.append(f"You're running {fans} fans — turning off fans in unoccupied rooms will reduce this load.")

if fridge == "Yes":
    tips.append("Keep the refrigerator door seal clean and thermostat setting optimal to avoid energy creep.")

if top_share > 40:
    tips.append(
        f"**{top_appliance}** is your single biggest energy driver at {top_share:.0f}% of total usage — "
        f"optimizing it first will have the biggest impact on your bill."
    )

if trend_pct > 5:
    tips.append("Historical seasonal patterns suggest usage typically rises around this time of year — budget for a slightly higher bill.")

if not tips:
    tips.append("Your usage is already fairly optimized 👍")

for t in tips:
    st.write("✔️", t)

st.caption("Prediction model: RandomForestRegressor trained on the UCI Individual Household Electric Power Consumption dataset.")
