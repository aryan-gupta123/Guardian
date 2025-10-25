"""
Bootstrap utilities to warm-start the RiskScorer model with synthetic data.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from .scorer import RiskScorer

logger = logging.getLogger(__name__)


def bootstrap_fit(scorer: "RiskScorer") -> None:
    """
    Train the provided scorer on synthetic yet realistic transaction data.
    """
    if scorer is None:
        logger.error("bootstrap_fit received None scorer; skipping.")
        return

    try:
        rng = np.random.default_rng(42)
        n_samples = 5000

        amount = rng.lognormal(mean=5.0, sigma=0.6, size=n_samples)

        # Daytime bias: heavier weights during business hours.
        hour_weights = np.array(
            [
                0.8, 0.6, 0.6, 0.6, 0.8, 1.0,  # 0-5
                1.5, 1.8, 2.0, 2.1, 2.1, 2.0,  # 6-11
                2.0, 2.0, 1.9, 1.7, 1.5, 1.3,  # 12-17
                1.1, 1.0, 0.9, 0.8, 0.7, 0.6,  # 18-23
            ],
            dtype=float,
        )
        hour_prob = hour_weights / hour_weights.sum()
        hour = rng.choice(np.arange(24), size=n_samples, p=hour_prob)

        is_foreign = rng.binomial(1, 0.10, size=n_samples).astype(float)
        merchant_risk = rng.beta(2.0, 5.0, size=n_samples)
        user_txn_rate = rng.gamma(shape=2.0, scale=1.2, size=n_samples)

        data = np.column_stack((amount, hour, is_foreign, merchant_risk, user_txn_rate))

        n_fraud = max(1, int(n_samples * 0.05))
        fraud_indices = rng.choice(n_samples, size=n_fraud, replace=False)
        data[fraud_indices, 0] = rng.uniform(5000.0, 20000.0, size=n_fraud)
        data[fraud_indices, 1] = rng.integers(0, 6, size=n_fraud)
        data[fraud_indices, 2] = 1.0
        data[fraud_indices, 3] = rng.uniform(0.85, 1.0, size=n_fraud)
        data[fraud_indices, 4] = rng.uniform(8.0, 20.0, size=n_fraud)

        scorer.fit(data.astype(float))
        logger.info(
            "Bootstrap training complete on %d synthetic transactions.",
            n_samples,
        )
    except Exception as exc:  # noqa: BLE001 - callers rely on failure resilience.
        logger.exception("Failed during bootstrap_fit: %s", exc)
