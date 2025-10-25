"""
Core scoring logic for the Guardian anomaly detection system.

This module exposes a singleton `SCORER` that can be imported by the Django
application to score transaction batches deterministically and efficiently.
"""

from __future__ import annotations

import logging
from typing import Dict, Iterable, List, Mapping, Optional, Sequence

import numpy as np
from sklearn.ensemble import IsolationForest

from .explainer import default_reasons

logger = logging.getLogger(__name__)


class RiskScorer:
    """
    Wraps an IsolationForest to produce normalized risk scores for transactions.

    The scorer performs min-max scaling on the five expected features, trains an
    IsolationForest, and maps raw anomaly scores onto [0, 1]. Inference is
    deterministic and resilient to malformed input.
    """

    FEATURES: Sequence[str] = (
        "amount",
        "hour",
        "is_foreign",
        "merchant_risk",
        "user_txn_rate",
    )

    DEFAULT_FEATURES: Mapping[str, float] = {
        "amount": 0.0,
        "hour": 12,
        "is_foreign": 0.0,
        "merchant_risk": 0.0,
        "user_txn_rate": 0.0,
    }

    def __init__(self) -> None:
        self._model: Optional[IsolationForest] = None
        self.feature_min: np.ndarray = np.zeros(len(self.FEATURES), dtype=float)
        self.feature_max: np.ndarray = np.ones(len(self.FEATURES), dtype=float)
        self.score_min: float = 0.0
        self.score_max: float = 1.0
        self._fitted: bool = False

    def fit(self, X: np.ndarray) -> None:
        """
        Fit the internal IsolationForest and scaling parameters.

        Args:
            X: Training array with shape (n_samples, 5).
        """
        try:
            if X is None:
                logger.error("Provided training data is None; skipping fit.")
                return

            X = np.asarray(X, dtype=float)
            if X.ndim != 2 or X.shape[1] != len(self.FEATURES):
                logger.error(
                    "Training data must have shape (n_samples, %d); received %s",
                    len(self.FEATURES),
                    X.shape,
                )
                return

            self.feature_min = np.min(X, axis=0)
            self.feature_max = np.max(X, axis=0)

            scaled = self._scale_array(X)

            self._model = IsolationForest(
                n_estimators=200,
                contamination=0.02,
                random_state=42,
                n_jobs=1,
            )
            self._model.fit(scaled)

            raw_scores = -self._model.decision_function(scaled)
            self.score_min = float(np.min(raw_scores))
            self.score_max = float(np.max(raw_scores))
            if self.score_max <= self.score_min:
                # Degenerate case: collapse range to a default span.
                self.score_max = self.score_min + 1.0

            self._fitted = True
            logger.info(
                "RiskScorer fitted on %d samples with feature ranges recorded.",
                X.shape[0],
            )
        except Exception as exc:  # noqa: BLE001 - we must never raise upstream.
            logger.exception("Failed to fit RiskScorer: %s", exc)
            self._fitted = False

    def score_batch(
        self, transactions: Optional[Iterable[Mapping[str, object]]]
    ) -> List[Dict[str, object]]:
        """
        Score a batch of transactions.

        Args:
            transactions: Iterable of items with keys `id` and `features`.

        Returns:
            List of dictionaries containing id, normalized score, and top reasons.
        """
        results: List[Dict[str, object]] = []
        if transactions is None:
            logger.warning("score_batch received None; returning empty result.")
            return results

        for index, txn in enumerate(transactions):
            txn_id = self._extract_id(txn, index)
            features_dict = self._prepare_features_dict(txn)
            feature_vector = self._dict_to_vector(features_dict)

            if self._fitted and self._model is not None:
                scaled_vector = self._scale_row(feature_vector)
                try:
                    raw_score = float(-self._model.decision_function([scaled_vector])[0])
                except Exception as exc:  # noqa: BLE001 - guard upstream consumers.
                    logger.exception(
                        "Scoring failure for transaction %s: %s", txn_id, exc
                    )
                    raw_score = 0.0
                normalized_score = self._normalize_score(raw_score)
            else:
                normalized_score = 0.0
                logger.warning(
                    "RiskScorer is not fitted. Returning default score for %s.",
                    txn_id,
                )

            reasons = default_reasons(features_dict, normalized_score)
            results.append(
                {"id": txn_id, "score": normalized_score, "reasons": reasons}
            )

        return results

    def _normalize_score(self, raw_score: float) -> float:
        """
        Map the raw anomaly score onto [0, 1] using the learned score range.
        """
        adjusted = float(np.clip(raw_score, self.score_min, self.score_max))
        denom = self.score_max - self.score_min
        if denom <= 0:
            return 0.5
        normalized = (adjusted - self.score_min) / denom
        return float(np.clip(normalized, 0.0, 1.0))

    def _scale_array(self, data: np.ndarray) -> np.ndarray:
        """
        Apply min-max scaling to a 2D array using stored feature ranges.
        """
        scaled = np.zeros_like(data, dtype=float)
        for idx, (min_val, max_val) in enumerate(zip(self.feature_min, self.feature_max)):
            denom = max_val - min_val
            if denom <= 0:
                scaled[:, idx] = 0.5
            else:
                scaled[:, idx] = np.clip(
                    (data[:, idx] - min_val) / denom,
                    0.0,
                    1.0,
                )
        return scaled

    def _scale_row(self, row: np.ndarray) -> np.ndarray:
        """
        Scale a single feature row while handling degenerate ranges gracefully.
        """
        scaled = np.zeros_like(row, dtype=float)
        for idx, value in enumerate(row):
            min_val = self.feature_min[idx]
            max_val = self.feature_max[idx]
            denom = max_val - min_val
            if denom <= 0:
                scaled[idx] = 0.5
            else:
                scaled[idx] = float(
                    np.clip((value - min_val) / denom, 0.0, 1.0)
                )
        return scaled

    def _prepare_features_dict(
        self, txn: Mapping[str, object]
    ) -> Dict[str, float]:
        """
        Extract and sanitize feature values from a transaction mapping.
        """
        features = txn.get("features") if isinstance(txn, Mapping) else None
        if not isinstance(features, Mapping):
            logger.debug("Transaction missing 'features'; using defaults.")
            features = {}

        clean: Dict[str, float] = {}
        for name in self.FEATURES:
            raw_value = features.get(name, self.DEFAULT_FEATURES[name])
            clean[name] = self._sanitize_feature(name, raw_value)
        return clean

    def _sanitize_feature(self, name: str, value: object) -> float:
        """
        Coerce incoming feature values to floats and clip to valid ranges.
        """
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            logger.debug("Feature %s has invalid value %r; using default.", name, value)
            numeric = float(self.DEFAULT_FEATURES[name])

        if name == "hour":
            return float(np.clip(round(numeric), 0, 23))
        if name == "is_foreign":
            return float(1.0 if numeric >= 0.5 else 0.0)
        if name == "merchant_risk":
            return float(np.clip(numeric, 0.0, 1.0))
        if name == "amount":
            return float(max(numeric, 0.0))
        if name == "user_txn_rate":
            return float(max(numeric, 0.0))

        return float(numeric)

    def _dict_to_vector(self, features: Mapping[str, float]) -> np.ndarray:
        """
        Convert a feature mapping into a numpy array matching the feature order.
        """
        return np.array([features.get(name, 0.0) for name in self.FEATURES], dtype=float)

    def _extract_id(self, txn: Mapping[str, object], index: int) -> str:
        """
        Safely derive a transaction identifier from the input mapping.
        """
        identifier = None
        if isinstance(txn, Mapping):
            identifier = txn.get("id")
        if not isinstance(identifier, str) or not identifier:
            identifier = f"txn_{index}"
        return identifier


SCORER = RiskScorer()
