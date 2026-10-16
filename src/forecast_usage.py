
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "dataset" / "usage_history.csv"

# Load historical usage
df = pd.read_csv(DATA_PATH)

# Select one subscription for the first experiment
name = "Netflix"

history = (
    df[df["subscription_name"] == name]
    .sort_values("month")["usage_days"]
    .to_numpy(dtype=float)
)

if len(history) < 5:
    raise ValueError("At least five months of usage are required.")

# Normalize usage values to a 0–1 range
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(history.reshape(-1, 1))

# Use the previous 3 months to predict the next month
window = 3
X, y = [], []

for i in range(len(scaled) - window):
    X.append(scaled[i:i + window, 0])
    y.append(scaled[i + window, 0])

X = np.array(X).reshape(-1, window, 1)
y = np.array(y)

# Build a small LSTM model
model = Sequential([
    Input(shape=(window, 1)),
    LSTM(16),
    Dense(1)
])

model.compile(optimizer="adam", loss="mse")

# Train the demonstration model
model.fit(X, y, epochs=100, verbose=0)

# Predict next month's usage
last_window = scaled[-window:].reshape(1, window, 1)
predicted_scaled = model.predict(last_window, verbose=0)

predicted_days = scaler.inverse_transform(
    predicted_scaled
)[0, 0]

predicted_days = float(np.clip(predicted_days, 0, 30))

print("===== DEEP LEARNING USAGE FORECAST =====")
print(f"Subscription: {name}")
print(f"Historical usage: {history.astype(int).tolist()}")
print(f"Predicted usage next month: {predicted_days:.1f} days")

if predicted_days < 5:
    print("Insight: Very low usage is forecast.")
    print("Recommendation: Review whether this subscription is still needed.")
elif predicted_days < 12:
    print("Insight: Relatively low usage is forecast.")
    print("Recommendation: Monitor usage and compare it with the subscription cost.")
else:
    print("Insight: Moderate or high usage is forecast.")
    print("Recommendation: Continue monitoring actual usage against this forecast.")

print(
    "\nNote: This is an experimental forecast trained on a tiny "
    "simulated history. It is not a reliable real-world prediction yet."
)
