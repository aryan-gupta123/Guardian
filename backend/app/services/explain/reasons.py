"""Utilities for generating textual reasons for model predictions."""
from __future__ import annotations

from typing import Dict, List

import numpy as np


def _safe_numeric(value: object) -> float:
    """Best-effort conversion of arbitrary inputs to ``float``."""

    if isinstance(value, (int, float, np.number)):
        return float(value)
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0


def default_reasons(features: Dict[str, object] | None, keys: List[str]) -> List[Dict[str, object]]:
    """Generate ranked reasons for a prediction.

    Parameters
    ----------
    features:
        Mapping of feature names to raw values.
    keys:
        Feature ordering used to maintain deterministic tie-breaking.

    Returns
    -------
    list of dict
        The top three reason dictionaries. When fewer than three meaningful
        reasons exist, the list may be shorter.
    """

    feature_map = features or {}
    ranked: List[Dict[str, object]] = []
    ordering = {key: idx for idx, key in enumerate(keys)}

    for name in keys:
        value = feature_map.get(name, 0.0)
        numeric = _safe_numeric(value)
        score = float(np.clip(abs(numeric), 0.0, 1.0))
        note = None

        if name == "is_foreign" and numeric >= 0.5:
            score += 1.0
            note = "foreign transaction"
        elif name == "hour" and 0 <= numeric <= 5:
            score += 0.3
            note = "night-time activity"
        elif name == "merchant_risk" and numeric > 0.7:
            score += 0.5
            note = "historically risky merchant"

        ranked.append(
            {
                "feature": name,
                "value": value if value is not None else 0.0,
                "_score": score,
                "_order": ordering.get(name, len(keys)),
                "note": note,
            }
        )

    ranked.sort(key=lambda item: (-item["_score"], item["_order"]))

    top_reasons: List[Dict[str, object]] = []
    for item in ranked[:3]:
        reason = {"feature": item["feature"], "value": item["value"]}
        if item["note"]:
            reason["note"] = item["note"]
        top_reasons.append(reason)

    return top_reasons
