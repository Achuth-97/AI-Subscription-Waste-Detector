import pandas as pd

# Load the dataset
df = pd.read_csv("dataset/subscriptions.csv")

print("Dataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nBasic statistics:")
print(df.describe())

print("\nWaste label distribution:")
print(df["waste_label"].value_counts())