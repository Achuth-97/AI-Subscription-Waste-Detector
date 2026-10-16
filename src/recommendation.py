# Subscription information
subscription_name = "Netflix"
monthly_cost = 649

# Results from our AI/ML analysis
waste_probability = 99.0
usage_change = -88.89
current_usage_days = 2

print("\n======================================")
print("      AI SUBSCRIPTION INVESTIGATOR")
print("======================================")

print(f"\nSubscription: {subscription_name}")
print(f"Monthly Cost: ₹{monthly_cost}")
print(f"Current Usage: {current_usage_days} days/month")

print(f"\nWaste Risk: {waste_probability:.2f}%")
print(f"Usage Change: {usage_change:.2f}%")

# Recommendation logic
if waste_probability >= 80 and usage_change <= -20:

    print("\n🔴 HIGH WASTE RISK")

    print("\nAI Analysis:")
    print(
        "Your subscription has high waste risk "
        "and your usage is decreasing significantly."
    )

    print("\n💡 Recommendation:")
    print(
        "Consider cancelling the subscription "
        "or switching to a lower-cost plan."
    )

    monthly_saving = monthly_cost
    yearly_saving = monthly_cost * 12

    print("\n💰 Potential Savings:")
    print(f"Monthly: ₹{monthly_saving}")
    print(f"Yearly: ₹{yearly_saving}")

elif waste_probability >= 50:

    print("\n🟠 MODERATE WASTE RISK")

    print("\n💡 Recommendation:")
    print(
        "Monitor your usage for another month "
        "before making a decision."
    )

else:

    print("\n🟢 LOW WASTE RISK")

    print("\n💡 Recommendation:")
    print(
        "Your current usage suggests that "
        "the subscription is being used regularly."
    )