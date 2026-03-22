"""
predict.py
Loads model.pkl and exposes a predict_revenue() function
used by Flask routes to get ML-based revenue forecasts.
"""

import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

_artifacts = None  # lazy-load cache


def _load():
    global _artifacts
    if _artifacts is None:
        _artifacts = joblib.load(MODEL_PATH)
    return _artifacts


def predict_revenue(category: str, units_sold: int,
                    discount_pct: float, price: float) -> float:
    """
    Returns predicted revenue (float) given retail inputs.

    Parameters
    ----------
    category    : str   – product category name
    units_sold  : int   – number of units
    discount_pct: float – discount percentage (0-40)
    price       : float – unit price in ₹

    Returns
    -------
    float – predicted monthly revenue
    """
    arts = _load()
    model = arts["model"]
    le    = arts["label_encoder"]

    # Encode category (unknown → 0)
    if category in le.classes_:
        cat_enc = le.transform([category])[0]
    else:
        cat_enc = 0

    import pandas as pd
    X = pd.DataFrame([[cat_enc, units_sold, discount_pct, price]],
                     columns=["category_enc", "units_sold", "discount_pct", "price"])
    prediction = model.predict(X)[0]
    return max(0.0, round(float(prediction), 2))
