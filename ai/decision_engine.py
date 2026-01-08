import pandas as pd

# -------------------------------
# Load digital twin data
# -------------------------------
df = pd.read_csv("../data/processed/merged_data.csv")

# -------------------------------
# Decision logic
# -------------------------------
def generate_decision(row):
    predicted = row["predicted_power_kw"]
    consumption = row["consumption_kw"]
    pattern = row["consumption_pattern"]
    waste = row["waste_period"]

    # Case 1: Energy surplus
    if predicted > consumption:
        if waste:
            return "SURPLUS: Shift flexible loads (pumps, EV charging) to this time"
        else:
            return "SURPLUS: Store energy or export to grid"

    # Case 2: Energy deficit
    if predicted < consumption:
        if pattern == "PEAK_USAGE":
            return "DEFICIT: Reduce non-critical loads or import from grid"
        else:
            return "DEFICIT: Monitor usage closely"

    # Case 3: Balanced
    return "BALANCED: No action needed"

# -------------------------------
# Apply decision engine
# -------------------------------
df["energy_decision"] = df.apply(generate_decision, axis=1)

# -------------------------------
# Save updated digital twin state
# -------------------------------
df.to_csv("../data/processed/merged_data.csv", index=False)

# -------------------------------
# Output for demo
# -------------------------------
print("✅ Decision engine executed successfully\n")
print(df[[
    "timestamp",
    "predicted_power_kw",
    "consumption_kw",
    "consumption_pattern",
    "energy_decision"
]])
