"""Utility for fitting the shared IsolationForest scorer with synthetic data."""
from __future__ import annotations

import numpy as np

from backend.app.services.ml.iso_forest import FEATURE_KEYS, SCORER

_BOOTSTRAPPED = False


def bootstrap_fit(n: int = 5000, seed: int = 7) -> None:
    """Initialise the shared scorer with synthetic-but-realistic data."""

    global _BOOTSTRAPPED
    if _BOOTSTRAPPED:
        return

    rng = np.random.default_rng(seed)

    amount = rng.lognormal(mean=4.5, sigma=0.6, size=n)
    hour = rng.integers(0, 24, size=n)
    is_foreign = rng.binomial(1, 0.05, size=n)
    merchant_risk = rng.beta(2.0, 4.0, size=n)
    user_txn_rate = rng.gamma(shape=2.0, scale=3.0, size=n)

    feature_map = {
        "amount": amount,
        "hour": hour,
        "is_foreign": is_foreign,
        "merchant_risk": merchant_risk,
        "user_txn_rate": user_txn_rate,
    }

    matrix = np.column_stack([feature_map[key] for key in FEATURE_KEYS])
    SCORER.fit(matrix)
    _BOOTSTRAPPED = True


bootstrap_fit()
