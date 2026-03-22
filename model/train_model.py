"""
train_model.py
Trains a Linear Regression model to predict monthly sales
based on retail features: discount %, units sold, category encoding.
Saves the trained model as model.pkl
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# ── Reproducibility ──────────────────────────────────────────────
np.random.seed(42)

# ── Synthetic retail dataset ─────────────────────────────────────
categories   = ["Electronics", "Clothing", "Groceries", "Furniture", "Sports"]
n_samples    = 500

category_col = np.random.choice(categories, n_samples)
units_sold   = np.random.randint(10, 500, n_samples)
discount_pct = np.random.uniform(0, 40, n_samples)
price        = np.random.uniform(100, 5000, n_samples)

le = LabelEncoder()
category_enc = le.fit_transform(category_col)

# Revenue = units × price × (1 - discount/100) + noise
noise   = np.random.normal(0, 500, n_samples)
revenue = units_sold * price * (1 - discount_pct / 100) / 100 + noise
revenue = np.clip(revenue, 0, None)

df = pd.DataFrame({
    "category_enc": category_enc,
    "units_sold":   units_sold,
    "discount_pct": discount_pct,
    "price":        price,
    "revenue":      revenue,
})

# ── Train / Test split ───────────────────────────────────────────
X = df[["category_enc", "units_sold", "discount_pct", "price"]]
y = df["revenue"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Model ────────────────────────────────────────────────────────
model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mae    = mean_absolute_error(y_test, y_pred)
r2     = r2_score(y_test, y_pred)

print(f"Model trained  →  MAE: {mae:.2f}  |  R²: {r2:.4f}")

# ── Save artefacts ───────────────────────────────────────────────
os.makedirs(os.path.dirname(__file__), exist_ok=True)
joblib.dump({"model": model, "label_encoder": le}, 
            os.path.join(os.path.dirname(__file__), "model.pkl"))

print("model.pkl saved successfully.")
