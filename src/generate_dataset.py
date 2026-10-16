import pandas as pd
import numpy as np

# Make the random data reproducible
np.random.seed(42)

# Number of records
num_records = 5000

# Subscription categories
categories = [
    "Entertainment",
    "Music",
    "Education",
    "Cloud Storage",
    "Software",
    "Fitness",
    "News"
]

# Generate data
data = {
    "monthly_cost": np.random.randint(50, 1500, num_records),
    "usage_days": np.random.randint(0, 31, num_records),
    "usage_hours": np.random.randint(0, 101, num_records),
    "months_subscribed": np.random.randint(1, 37, num_records),
    "previous_usage_days": np.random.randint(0, 31, num_records),
    "category": np.random.choice(categories, num_records)
}

df = pd.DataFrame(data)

# Calculate usage percentage
df["usage_percentage"] = (df["usage_days"] / 30) * 100

# Calculate usage trend
df["usage_change"] = (
    df["usage_days"] - df["previous_usage_days"]
)

# Create a simple initial waste label
# Higher cost + low usage = higher chance of waste
df["waste_score"] = (
    (df["monthly_cost"] / 1500) * 0.4
    + ((30 - df["usage_days"]) / 30) * 0.4
    + ((30 - df["previous_usage_days"]) / 30) * 0.2
)

# Convert score into label
df["waste_label"] = (df["waste_score"] > 0.55).astype(int)

# Remove the temporary score
df.drop(columns=["waste_score"], inplace=True)

# Save dataset
df.to_csv("dataset/subscriptions.csv", index=False)

print("Dataset created successfully!")
print(f"Number of records: {len(df)}")
print("\nFirst 10 records:")
print(df.head(10))