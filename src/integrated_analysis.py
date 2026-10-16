import pandas as pd
import joblib

# ==========================================
# 1. Load trained ML model
# ==========================================

model = joblib.load("models/subscription_model.pkl")


# ==========================================
# 2. New subscription information
# ==========================================

subscription = {
    "name": "Netflix",
    "monthly_cost": 649,
    "usage_days": 2,
    "usage_hours": 4,
    "months_subscribed": 8,
    "previous_usage_days": 5,
    "category": "Entertainment"
}


# ==========================================
# 3. Prepare data for ML model
# ==========================================

usage_percentage = (
    subscription["usage_days"] / 30
) * 100

usage_change = (
    subscription["usage_days"]
    - subscription["previous_usage_days"]
)

new_data = pd.DataFrame([
    {
        "monthly_cost": subscription["monthly_cost"],
        "usage_days": subscription["usage_days"],
        "usage_hours": subscription["usage_hours"],
        "months_subscribed": subscription["months_subscribed"],
        "previous_usage_days": subscription["previous_usage_days"],
        "category": subscription["category"],
        "usage_percentage": usage_percentage,
        "usage_change": usage_change
    }
])


# ==========================================
# 4. ML prediction
# ==========================================

prediction = model.predict(new_data)[0]

waste_probability = (
    model.predict_proba(new_data)[0][1]
) * 100


# ==========================================
# 5. Savings calculation
# ==========================================

monthly_cost = subscription["monthly_cost"]

if prediction == 1:
    monthly_saving = monthly_cost
    yearly_saving = monthly_cost * 12
else:
    monthly_saving = 0
    yearly_saving = 0


# ==========================================
# 6. Display AI analysis
# ==========================================

print("\n======================================")
print("      AI SUBSCRIPTION INVESTIGATOR")
print("======================================")

print(f"\nSubscription: {subscription['name']}")
print(f"Monthly Cost: ₹{monthly_cost}")
print(f"Current Usage: {subscription['usage_days']} days")
print(
    f"Previous Usage: "
    f"{subscription['previous_usage_days']} days"
)

print("\n----- AI ANALYSIS -----")

if prediction == 1:
    print("⚠️ Potentially Wasteful")
else:
    print("✅ Appears Useful")

print(
    f"Waste Risk: "
    f"{waste_probability:.2f}%"
)

print(
    f"Usage Change: "
    f"{usage_change:.2f} days"
)


# ==========================================
# 7. Recommendation
# ==========================================

print("\n----- RECOMMENDATION -----")

if waste_probability >= 80 and usage_change < 0:

    print("🔴 HIGH WASTE RISK")

    print(
        "Your subscription has high waste risk "
        "and your usage has decreased."
    )

    print(
        "\n💡 Recommendation:"
    )

    print(
        "Consider cancelling the subscription "
        "or switching to a lower-cost plan."
    )

    print("\n💰 Potential Savings:")
    print(f"Monthly: ₹{monthly_saving}")
    print(f"Yearly: ₹{yearly_saving}")

elif waste_probability >= 50:

    print("🟠 MODERATE WASTE RISK")

    print(
        "Your subscription is underutilized. "
        "Continue monitoring your usage."
    )

else:

    print("🟢 LOW WASTE RISK")

    print(
        "Your subscription appears to be "
        "used regularly."
    )