"""Isolation Forest based risk scorer for Guardian project."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

import numpy as np
from sklearn.ensemble import IsolationForest

from backend.app.services.explain.reasons import default_reasons

FEATURE_KEYS: List[str] = [
    "amount",
    "hour",
    "is_foreign",
    "merchant_risk",
    "user_txn_rate",
]


@dataclass
class _ScalerState:
    """Container for min/max statistics used during scaling."""

    mins: np.ndarray
    ranges: np.ndarray


class RiskScorer:
    """Wraps an :class:`IsolationForest` model to score transaction risk.

    The scorer expects features ordered according to :data:`FEATURE_KEYS`.
    Feature vectors are min-max scaled prior to fitting and scoring. Missing
    feature values default to ``0.0``.
    """

    def __init__(self, contamination: float = 0.02, seed: int = 42) -> None:
        self.contamination = contamination
        self.seed = seed
        self._forest: IsolationForest | None = None
        self._scaler: _ScalerState | None = None
        self._fitted: bool = False

    # ------------------------------------------------------------------
    def fit(self, X: np.ndarray) -> None:
        """Fit the scorer on the provided feature matrix.

        Parameters
        ----------
        X:
            Two dimensional array-like structure containing feature vectors in
            the order specified by :data:`FEATURE_KEYS`.
        """

        array = np.asarray(X, dtype=float)
        if array.ndim != 2 or array.size == 0:
            self._forest = None
            self._scaler = None
            self._fitted = False
            return

        expected = len(FEATURE_KEYS)
        if array.shape[1] != expected:
            if array.shape[1] > expected:
                array = array[:, :expected]
            else:
                padding = np.zeros((array.shape[0], expected - array.shape[1]))
                array = np.hstack([array, padding])

        mins = array.min(axis=0)
        maxs = array.max(axis=0)
        ranges = maxs - mins
        ranges[ranges <= 0.0] = 1.0
        scaled = (array - mins) / ranges

        forest = IsolationForest(
            n_estimators=200,
            contamination=self.contamination,
            random_state=self.seed,
            n_jobs=1,
        )
        forest.fit(scaled)

        self._forest = forest
        self._scaler = _ScalerState(mins=mins, ranges=ranges)
        self._fitted = True

    # ------------------------------------------------------------------
    def _to_array(self, feats: Dict[str, object] | None) -> np.ndarray:
        """Convert a feature mapping to a scaled numpy array.

        Missing features default to ``0.0``. Scaling is skipped when the
        instance has not been fitted.
        """

        vector = np.zeros(len(FEATURE_KEYS), dtype=float)
        if not isinstance(feats, dict):
            feats = {}

        for idx, key in enumerate(FEATURE_KEYS):
            raw_value = feats.get(key, 0.0)
            try:
                vector[idx] = float(raw_value)
            except (TypeError, ValueError):
                vector[idx] = 0.0

        if self._fitted and self._scaler is not None:
            vector = (vector - self._scaler.mins) / self._scaler.ranges
            vector = np.clip(vector, 0.0, 1.0)

        return vector

    # ------------------------------------------------------------------
    def _score_array(self, Xs: np.ndarray) -> np.ndarray:
        """Compute scores for the provided scaled feature vectors."""

        matrix = np.asarray(Xs, dtype=float)
        if matrix.ndim == 1:
            matrix = matrix.reshape(1, -1)

        if not self._fitted or self._forest is None:
            return np.full(matrix.shape[0], 0.5, dtype=float)

        raw_scores = self._forest.decision_function(matrix)
        return np.clip(raw_scores + 0.5, 0.0, 1.0)

    # ------------------------------------------------------------------
    def score_one(self, txn: Dict[str, object]) -> Tuple[float, List[Dict[str, object]]]:
        """Score a single transaction.

        Parameters
        ----------
        txn:
            Mapping with transaction details. Feature values are expected under
            the ``"features"`` key or at the top level.

        Returns
        -------
        tuple
            A tuple containing the risk score in ``[0, 1]`` and a list of
            contributing reasons.
        """

        features = txn.get("features") if isinstance(txn, dict) else None
        if not isinstance(features, dict):
            features = {k: txn.get(k) for k in FEATURE_KEYS if isinstance(txn, dict)}

        vector = self._to_array(features)
        score = float(self._score_array(vector)[0])
        reasons = default_reasons(features, FEATURE_KEYS)
        reasons = self._complete_reasons(reasons, features)
        return score, reasons

    # ------------------------------------------------------------------
    def score_batch(self, txns: Iterable[Dict[str, object]]) -> List[Dict[str, object]]:
        """Score a batch of transactions.

        Parameters
        ----------
        txns:
            Iterable of transaction payloads. Each entry should include an
            ``"id"`` and ``"features"`` mapping.

        Returns
        -------
        list of dict
            Scored transactions conforming to the expected API response shape.
        """

        prepared: List[np.ndarray] = []
        original: List[Tuple[int, Dict[str, object], Dict[str, object]]] = []

        if txns is None:
            txns = []

        for index, txn in enumerate(txns):
            txn_dict = txn if isinstance(txn, dict) else {}
            features = txn_dict.get("features")
            if not isinstance(features, dict):
                features = {}
            prepared.append(self._to_array(features))
            original.append((index, txn_dict, features))

        if prepared:
            matrix = np.vstack(prepared)
            scores = self._score_array(matrix)
        else:
            scores = np.array([], dtype=float)

        results: List[Dict[str, object]] = []
        for (index, txn_dict, features), score in zip(original, scores):
            txn_id = txn_dict.get("id", f"txn_{index}")
            reasons = default_reasons(features, FEATURE_KEYS)
            reasons = self._complete_reasons(reasons, features)
            results.append(
                {
                    "id": str(txn_id),
                    "score": float(score),
                    "reasons": reasons,
                }
            )

        return results

    # ------------------------------------------------------------------
    def _complete_reasons(
        self, reasons: List[Dict[str, object]], features: Dict[str, object]
    ) -> List[Dict[str, object]]:
        """Ensure we always return up to three reasons when possible."""

        completed: List[Dict[str, object]] = list(reasons)
        seen = {reason["feature"] for reason in completed if "feature" in reason}

        for key in FEATURE_KEYS:
            if len(completed) >= 3:
                break
            if key in seen:
                continue
            value = features.get(key, 0.0) if isinstance(features, dict) else 0.0
            try:
                numeric = float(value)
            except (TypeError, ValueError):
                numeric = 0.0
            completed.append({"feature": key, "value": numeric})

        return completed[:3]


SCORER = RiskScorer()


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    synthetic = np.column_stack(
        [
            rng.lognormal(mean=4.5, sigma=0.4, size=64),
            rng.integers(0, 24, size=64),
            rng.binomial(1, 0.05, size=64),
            rng.beta(2.0, 5.0, size=64),
            rng.gamma(2.0, 3.0, size=64),
        ]
    )
    SCORER.fit(synthetic)
    sample_txn = {
        "id": "demo",
        "features": {
            "amount": float(synthetic[0, 0]),
            "hour": int(synthetic[0, 1]),
            "is_foreign": int(synthetic[0, 2]),
            "merchant_risk": float(synthetic[0, 3]),
            "user_txn_rate": float(synthetic[0, 4]),
        },
    }
    score, reasons = SCORER.score_one(sample_txn)
    print({"id": sample_txn["id"], "score": score, "reasons": reasons})
