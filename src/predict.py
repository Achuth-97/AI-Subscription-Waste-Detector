import pandas as pd
import joblib

# Load our trained model
model = joblib.load("models/subscription_model.pkl")

# New subscription to analyze
new_subscription = pd.DataFrame([
    {
        "monthly_cost": 649,
        "usage_days": 2,
        "usage_hours": 4,
        "months_subscribed": 8,
        "previous_usage_days": 5,
        "category": "Entertainment",
        "usage_percentage": (2 / 30) * 100,
        "usage_change": 2 - 5
    }
])

# Make prediction
prediction = model.predict(new_subscription)[0]

# Get waste probability
waste_probability = model.predict_proba(new_subscription)[0][1]

print("\n===== AI SUBSCRIPTION ANALYSIS =====")

if prediction == 1:
    print("⚠️ Potentially Wasteful Subscription")
else:
    print("✅ Subscription Appears Useful")

print(f"Waste Risk: {waste_probability * 100:.2f}%")

print("\nSubscription Details:")
print("Monthly Cost: ₹649")
print("Usage: 2 days")
print("Previous Month Usage: 5 days")
monthly_cost = 649

if prediction == 1:
    monthly_saving = monthly_cost
    yearly_saving = monthly_saving * 12

    print("\n💰 Potential Savings:")
    print(f"Monthly Saving: ₹{monthly_saving}")
    print(f"Yearly Saving: ₹{yearly_saving}")
else:
    print("\n✅ No significant potential saving detected.")