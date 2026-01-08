import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Solar Energy Digital Twin",
    layout="wide"
)

st.title("🌞 Self-Learning Solar Energy Digital Twin")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("../data/processed/merged_data.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])

# -----------------------------
# Base Totals
# -----------------------------
BASE_SOLAR = df["power_kw"].sum()
BASE_CONSUMPTION = df["consumption_kw"].sum()
BASE_PREDICTED = df["predicted_power_kw"].sum()

# -----------------------------
# Overview Metrics
# -----------------------------
m1, m2, m3 = st.columns(3)
m1.metric("Total Solar Generated (kWh)", round(BASE_SOLAR, 2))
m2.metric("Total Energy Consumed (kWh)", round(BASE_CONSUMPTION, 2))
m3.metric("Total Predicted Solar (kWh)", round(BASE_PREDICTED, 2))

st.divider()

# -----------------------------
# 📈 Solar vs Prediction Graph
# -----------------------------
st.subheader("🔮 Solar Power — Actual vs Predicted")

fig1, ax1 = plt.subplots()
ax1.plot(df["timestamp"], df["power_kw"], label="Actual Solar")
ax1.plot(
    df["timestamp"],
    df["predicted_power_kw"],
    linestyle="--",
    label="Predicted Solar"
)
ax1.set_xlabel("Time")
ax1.set_ylabel("Power (kW)")
ax1.legend()
st.pyplot(fig1)

st.divider()

# -----------------------------
# ⚡ Consumption Graph
# -----------------------------
st.subheader("⚡ Energy Consumption")

fig2, ax2 = plt.subplots()
ax2.plot(
    df["timestamp"],
    df["consumption_kw"],
    color="orange",
    label="Consumption"
)
ax2.set_xlabel("Time")
ax2.set_ylabel("Power (kW)")
ax2.legend()
st.pyplot(fig2)

st.divider()

# -----------------------------
# 🔮 WHAT-IF SIMULATION
# -----------------------------
st.subheader("🔮 What-If Energy Simulation")

c1, c2, c3, c4 = st.columns(4)

with c1:
    battery_capacity = st.slider(
        "Battery Capacity (kWh)", 10, 200, 50
    )

with c2:
    initial_battery_pct = st.slider(
        "Initial Battery Charge (%)", 0, 100, 50
    )

with c3:
    panel_increase = st.slider(
        "Solar Panel Capacity Increase (%)", 0, 200, 0
    )

with c4:
    load_reduction = st.slider(
        "Load Reduction (%)", 0, 50, 0
    )

# -----------------------------
# Adjusted Values
# -----------------------------
sim_solar = BASE_SOLAR * (1 + panel_increase / 100)
sim_consumption = BASE_CONSUMPTION * (1 - load_reduction / 100)

# -----------------------------
# 🔋 Battery Logic (REALISTIC)
# -----------------------------
MIN_SOC = 0.20  # 20% reserve protection

reserve_energy = battery_capacity * MIN_SOC
usable_battery = battery_capacity - reserve_energy

initial_total_energy = battery_capacity * (initial_battery_pct / 100)
initial_usable_energy = max(0, initial_total_energy - reserve_energy)

energy_gap = sim_solar - sim_consumption

battery_used = 0.0
battery_charged = 0.0
usable_soc = initial_usable_energy

if energy_gap < 0:
    # Discharge battery
    battery_used = min(abs(energy_gap), usable_soc)
    usable_soc -= battery_used
    net_energy = energy_gap + battery_used
else:
    # Charge battery
    available_space = usable_battery - usable_soc
    battery_charged = min(energy_gap, available_space)
    usable_soc += battery_charged
    net_energy = energy_gap - battery_charged

# -----------------------------
# 🌐 Grid Import / Export
# -----------------------------
grid_import = abs(net_energy) if net_energy < 0 else 0
grid_export = net_energy if net_energy > 0 else 0

# -----------------------------
# 📊 Simulation Results
# -----------------------------
st.divider()
st.subheader("📊 Simulation Results")

r1, r2, r3 = st.columns(3)
r1.metric("Simulated Solar (kWh)", round(sim_solar, 2))
r2.metric("Simulated Consumption (kWh)", round(sim_consumption, 2))
r3.metric("Net Energy After Battery (kWh)", round(net_energy, 2))

g1, g2 = st.columns(2)
g1.metric("Grid Import Required (kWh)", round(grid_import, 2))
g2.metric("Energy Exported to Grid (kWh)", round(grid_export, 2))

# -----------------------------
# 🔋 Battery Status
# -----------------------------
st.divider()
st.subheader("🔋 Battery Status")

total_soc = usable_soc + reserve_energy

b1, b2, b3 = st.columns(3)
b1.metric("Battery State of Charge (kWh)", round(total_soc, 2))
b2.metric("Battery Charged (kWh)", round(battery_charged, 2))
b3.metric("Battery Used (kWh)", round(battery_used, 2))

st.caption(
    f"🔒 Battery reserve protected: {round(reserve_energy, 1)} kWh "
    f"({int(MIN_SOC * 100)}% minimum SOC)"
)

if grid_import > 0:
    st.warning("⚠ Remaining energy demand must be supplied by the grid.")
elif grid_export > 0:
    st.success("✅ Excess energy exported to the grid.")

# -----------------------------
# 🌱 Environmental Impact
# -----------------------------
st.divider()
st.subheader("🌱 Environmental Impact")

EMISSION_FACTOR = 0.82  # kg CO₂ per kWh
co2_saved = sim_solar * EMISSION_FACTOR

st.metric("Estimated CO₂ Saved (kg)", round(co2_saved, 2))

st.info(
    "CO₂ savings are estimated using average grid emissions. "
    "Battery reserve protection mirrors real-world lithium battery constraints."
)

# -----------------------------
# 🧠 AI Decisions Table
# -----------------------------
st.divider()
st.subheader("🧠 AI Energy Decisions")

st.dataframe(
    df[[
        "timestamp",
        "predicted_power_kw",
        "consumption_kw",
        "consumption_pattern",
        "energy_decision"
    ]],
    use_container_width=True
)
