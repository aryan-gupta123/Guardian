"""Generate synthetic Guardian transactions as JSON."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path
from typing import Dict, List

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.services.ml.iso_forest import FEATURE_KEYS


def _generate_transactions(n: int, seed: int) -> List[Dict[str, object]]:
    rng = np.random.default_rng(seed)
    base_time = dt.datetime(2024, 1, 1, tzinfo=dt.timezone.utc)
    transactions: List[Dict[str, object]] = []

    for idx in range(n):
        amount = float(rng.lognormal(mean=4.5, sigma=0.7))
        hour = int(rng.integers(0, 24))
        is_foreign = int(rng.binomial(1, 0.05))
        merchant_risk = float(rng.beta(2.0, 4.5))
        user_txn_rate = float(rng.gamma(shape=2.0, scale=3.0))

        timestamp = base_time + dt.timedelta(minutes=int(idx % (24 * 60)))
        merchant = f"merchant_{rng.integers(1, 2000):04d}"

        features = {
            "amount": amount,
            "hour": hour,
            "is_foreign": is_foreign,
            "merchant_risk": merchant_risk,
            "user_txn_rate": user_txn_rate,
        }

        risk_signal = 0.0
        risk_signal += 0.4 if amount > 200 else 0.0
        risk_signal += 0.6 if is_foreign else 0.0
        risk_signal += 0.3 if 0 <= hour <= 5 else 0.0
        risk_signal += 0.5 * merchant_risk
        noise = rng.normal(0.0, 0.15)
        label = int(risk_signal + noise > 0.8)

        transactions.append(
            {
                "id": f"txn_{idx:05d}",
                "amount": amount,
                "merchant": merchant,
                "ts": timestamp.isoformat(),
                "label": label,
                "features": {key: features[key] for key in FEATURE_KEYS},
            }
        )

    return transactions


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic Guardian data")
    parser.add_argument("-n", "--count", type=int, default=50000, help="Number of transactions")
    parser.add_argument("--seed", type=int, default=2024, help="Random seed")
    args = parser.parse_args()

    transactions = _generate_transactions(args.count, args.seed)
    payload = {"transactions": transactions}
    json.dump(payload, sys.stdout)


if __name__ == "__main__":
    main()
