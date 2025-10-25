"""
Human-readable explanation helpers for the Guardian anomaly detection system.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Mapping

import numpy as np

logger = logging.getLogger(__name__)


DEFAULT_FEATURES: Mapping[str, float] = {
    "amount": 0.0,
    "hour": 12.0,
    "is_foreign": 0.0,
    "merchant_risk": 0.0,
    "user_txn_rate": 0.0,
}


def default_reasons(features: Mapping[str, object], score: float) -> List[Dict[str, object]]:
    """
    Derive a ranked list of reasons contributing to the computed risk score.

    Args:
        features: Mapping of feature names to values.
        score: Normalized risk score in [0, 1].

    Returns:
        A list of up to three reason dictionaries sorted by strongest contribution.
    """
    sanitized = _sanitize_features(features)
    contributions = _compute_contributions(sanitized, score)

    # Sort by descending contribution; fall back to feature name for determinism.
    contributions.sort(key=lambda item: (-item["weight"], item["feature"]))

    reasons: List[Dict[str, object]] = []
    for entry in contributions[:3]:
        reason: Dict[str, object] = {
            "feature": entry["feature"],
            "value": entry["value"],
        }
        if entry.get("note"):
            reason["note"] = entry["note"]
        reasons.append(reason)

    return reasons


def _sanitize_features(features: Mapping[str, object]) -> Dict[str, float]:
    """
    Ensure all expected features are present and coerced to floats.
    """
    clean: Dict[str, float] = {}
    for key, default_value in DEFAULT_FEATURES.items():
        value = features.get(key, default_value) if isinstance(features, Mapping) else default_value
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            logger.debug("Invalid value for %s: %r; using default.", key, value)
            numeric = float(default_value)

        if key == "hour":
            numeric = float(np.clip(round(numeric), 0, 23))
        elif key == "is_foreign":
            numeric = 1.0 if numeric >= 0.5 else 0.0
        elif key == "merchant_risk":
            numeric = float(np.clip(numeric, 0.0, 1.0))
        elif key in {"amount", "user_txn_rate"}:
            numeric = float(max(numeric, 0.0))

        clean[key] = numeric
    return clean


def _compute_contributions(features: Mapping[str, float], score: float) -> List[Dict[str, object]]:
    """
    Compute heuristic risk contributions for each feature.
    """
    contributions: List[Dict[str, object]] = []

    amount = features["amount"]
    hour = features["hour"]
    is_foreign = features["is_foreign"]
    merchant_risk = features["merchant_risk"]
    txn_rate = features["user_txn_rate"]

    amount_weight = float(np.tanh(amount / 600.0))
    contributions.append({
        "feature": "amount",
        "value": amount,
        "weight": max(amount_weight, 0.0),
    })

    if is_foreign >= 1.0:
        contrib_weight = 1.0
        note = "foreign transaction"
    else:
        contrib_weight = 0.1 * score
        note = None
    contributions.append({
        "feature": "is_foreign",
        "value": int(is_foreign),
        "weight": contrib_weight,
        "note": note,
    })

    if 0 <= hour <= 5:
        hour_weight = 0.3
        note = "night-time activity"
    else:
        hour_weight = max(0.05 * score, 0.01)
        note = None
    contributions.append({
        "feature": "hour",
        "value": int(hour),
        "weight": hour_weight,
        "note": note,
    })

    if merchant_risk > 0.7:
        merchant_weight = 0.5 + 0.5 * merchant_risk
        note = "historically risky merchant"
    else:
        merchant_weight = float(merchant_risk * 0.4)
        note = None
    contributions.append({
        "feature": "merchant_risk",
        "value": round(merchant_risk, 3),
        "weight": merchant_weight,
        "note": note,
    })

    txn_rate_weight = float(np.tanh(txn_rate / 4.0))
    contributions.append({
        "feature": "user_txn_rate",
        "value": round(txn_rate, 3),
        "weight": max(txn_rate_weight, 0.0),
    })

    return contributions
