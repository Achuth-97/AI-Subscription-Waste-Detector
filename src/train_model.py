
from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "dataset" / "subscriptions.csv"
MODEL_PATH = ROOT / "models" / "subscription_model.pkl"

print("Loading subscription dataset...")

df = pd.read_csv(DATA_PATH)

# Features expected by the dashboard
feature_columns = [
    "monthly_cost",
    "usage_days",
    "usage_hours",
    "months_subscribed",
    "previous_usage_days",
    "category",
    "usage_percentage",
    "usage_change"
]

target_column = "waste_label"

missing = [
    col for col in feature_columns + [target_column]
    if col not in df.columns
]

if missing:
    raise ValueError(
        f"Dataset is missing required columns: {missing}"
    )

X = df[feature_columns].copy()
y = df[target_column].astype(int)

numeric_features = [
    "monthly_cost",
    "usage_days",
    "usage_hours",
    "months_subscribed",
    "previous_usage_days",
    "usage_percentage",
    "usage_change"
]

categorical_features = ["category"]

preprocessor = ColumnTransformer([
    ("numeric", "passthrough", numeric_features),
    (
        "category",
        OneHotEncoder(handle_unknown="ignore"),
        categorical_features
    )
])

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    (
        "classifier",
        RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced"
        )
    )
])

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training model...")

pipeline.fit(X_train, y_train)

predictions = pipeline.predict(X_test)
probabilities = pipeline.predict_proba(X_test)[:, 1]

print("\n===== MODEL EVALUATION =====")

print(
    f"Test accuracy: "
    f"{accuracy_score(y_test, predictions) * 100:.2f}%"
)

print("\nClassification report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

print("\nConfusion matrix:")
print(confusion_matrix(y_test, predictions))

if y_test.nunique() == 2:
    print(
        "\nROC-AUC:",
        round(roc_auc_score(y_test, probabilities), 3)
    )

MODEL_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(pipeline, MODEL_PATH)

print(f"\nModel saved to: {MODEL_PATH}")

print(
    "\nIMPORTANT: The dataset contains synthetic labels. "
    "These metrics do not establish real-world performance."
)
