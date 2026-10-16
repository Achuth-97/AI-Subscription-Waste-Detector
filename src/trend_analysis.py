import pandas as pd
import matplotlib.pyplot as plt

# Example historical usage for one subscription
data = {
    "month": [
        "March",
        "April",
        "May",
        "June",
        "July"
    ],
    "usage_days": [
        18,
        15,
        11,
        6,
        2
    ]
}

df = pd.DataFrame(data)

print("===== SUBSCRIPTION USAGE TREND =====")

print(df)

# Calculate change from first month to last month
first_usage = df["usage_days"].iloc[0]
last_usage = df["usage_days"].iloc[-1]

percentage_change = (
    (last_usage - first_usage) / first_usage
) * 100

print(f"\nUsage change: {percentage_change:.2f}%")

# Determine trend
if percentage_change < -20:
    trend = "Strongly Decreasing"
elif percentage_change < 0:
    trend = "Decreasing"
elif percentage_change > 20:
    trend = "Increasing"
else:
    trend = "Stable"

print(f"Usage Trend: {trend}")

# Plot the trend
plt.figure(figsize=(8, 5))

plt.plot(
    df["month"],
    df["usage_days"],
    marker="o"
)

plt.title("Subscription Usage Trend")
plt.xlabel("Month")
plt.ylabel("Usage Days")

plt.grid(True)

plt.show()