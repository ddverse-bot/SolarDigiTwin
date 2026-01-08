import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# -------------------------------
# Load merged digital twin data
# -------------------------------
df = pd.read_csv("../data/processed/merged_data.csv")

# -------------------------------
# Features (what the AI learns from)
# -------------------------------
X = df[["sunlight_index", "temperature_c"]]

# Target (what the AI predicts)
y = df["power_kw"]

# -------------------------------
# Train-test split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# Train forecasting model
# -------------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# -------------------------------
# Predict solar power
# -------------------------------
df["predicted_power_kw"] = model.predict(X)

# Physical constraint:
# Solar power cannot be negative
df["predicted_power_kw"] = df["predicted_power_kw"].clip(lower=0)

# -------------------------------
# Save updated digital twin state
# -------------------------------
df.to_csv("../data/processed/merged_data.csv", index=False)

# -------------------------------
# Output for demo / debugging
# -------------------------------
print("✅ Solar forecasting model trained successfully\n")
print(df[["timestamp", "power_kw", "predicted_power_kw"]])
