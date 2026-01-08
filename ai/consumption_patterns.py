import pandas as pd
import numpy as np

# -------------------------------
# Load merged digital twin data
# -------------------------------
df = pd.read_csv("../data/processed/merged_data.csv")

# -------------------------------
# Basic statistics
# -------------------------------
mean_consumption = df["consumption_kw"].mean()
std_consumption = df["consumption_kw"].std()

# -------------------------------
# Pattern classification logic
# -------------------------------
def classify_consumption(value):
    if value > mean_consumption + std_consumption:
        return "PEAK_USAGE"
    elif value < mean_consumption - std_consumption:
        return "LOW_USAGE"
    else:
        return "NORMAL_USAGE"

df["consumption_pattern"] = df["consumption_kw"].apply(classify_consumption)

# -------------------------------
# Time-based insights
# -------------------------------
df["hour"] = pd.to_datetime(df["timestamp"]).dt.hour

# Identify waste periods:
# Low usage but good solar availability
df["waste_period"] = (
    (df["consumption_pattern"] == "LOW_USAGE") &
    (df["sunlight_index"] > 0.6)
)

# -------------------------------
# Save updated digital twin state
# -------------------------------
df.to_csv("../data/processed/merged_data.csv", index=False)

# -------------------------------
# Output for demo
# -------------------------------
print("✅ Consumption pattern learning completed\n")
print(df[[
    "timestamp",
    "consumption_kw",
    "consumption_pattern",
    "waste_period"
]])
