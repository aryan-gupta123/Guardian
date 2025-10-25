"""CLI helper to send batch scoring requests to the Guardian API."""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.services.ml.iso_forest import FEATURE_KEYS


def _safe_features(raw: Dict[str, object] | None) -> Dict[str, float]:
    features = {}
    data = raw or {}
    for key in FEATURE_KEYS:
        value = data.get(key, 0.0)
        try:
            features[key] = float(value)
        except (TypeError, ValueError):
            features[key] = 0.0
    return features


def _generate_synthetic(n: int, seed: int) -> List[Dict[str, object]]:
    rng = np.random.default_rng(seed)
    results: List[Dict[str, object]] = []
    for idx in range(n):
        amount = float(rng.lognormal(mean=4.5, sigma=0.7))
        hour = int(rng.integers(0, 24))
        is_foreign = int(rng.binomial(1, 0.05))
        merchant_risk = float(rng.beta(2.0, 4.5))
        user_txn_rate = float(rng.gamma(shape=2.0, scale=3.0))

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

        results.append(
            {
                "id": f"txn_{idx:05d}",
                "features": features,
                "label": label,
            }
        )
    return results


def _load_transactions(path: str) -> Tuple[List[Dict[str, object]], Dict[str, int]]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)

    if isinstance(data, dict) and "transactions" in data:
        items = data["transactions"]
    elif isinstance(data, list):
        items = data
    else:
        raise ValueError("Unsupported JSON format: expected list or {'transactions': [...]}")

    transactions: List[Dict[str, object]] = []
    labels: Dict[str, int] = {}

    for idx, item in enumerate(items):
        txn = item if isinstance(item, dict) else {}
        txn_id = str(txn.get("id", f"txn_{idx:05d}"))
        features = _safe_features(txn.get("features") if isinstance(txn, dict) else None)
        label = txn.get("label")
        if label is not None:
            try:
                labels[txn_id] = int(label)
            except (TypeError, ValueError):
                pass
        transactions.append({"id": txn_id, "features": features, "label": labels.get(txn_id)})

    return transactions, labels


def _prepare_payload(transactions: Iterable[Dict[str, object]]) -> List[Dict[str, object]]:
    payload: List[Dict[str, object]] = []
    for idx, txn in enumerate(transactions):
        txn_id = str(txn.get("id", f"txn_{idx:05d}"))
        features = _safe_features(txn.get("features") if isinstance(txn, dict) else None)
        payload.append({"id": txn_id, "features": features})
    return payload


def _compute_metrics(
    results: List[Dict[str, object]], labels: Dict[str, int], thresholds: Iterable[float]
) -> None:
    if not labels:
        return

    for threshold in thresholds:
        tp = fp = fn = 0
        for entry in results:
            txn_id = str(entry.get("id"))
            score = float(entry.get("score", 0.0))
            label = labels.get(txn_id)
            if label is None:
                continue
            prediction = 1 if score >= threshold else 0
            if prediction == 1 and label == 1:
                tp += 1
            elif prediction == 1 and label == 0:
                fp += 1
            elif prediction == 0 and label == 1:
                fn += 1
        precision = tp / (tp + fp) if (tp + fp) else 0.0
        recall = tp / (tp + fn) if (tp + fn) else 0.0
        print(
            f"thr={threshold:.2f} TP={tp} FP={fp} FN={fn} "
            f"precision={precision:.3f} recall={recall:.3f}"
        )


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score a batch of transactions")
    parser.add_argument("api_base", help="Guardian API base URL, e.g. http://localhost:8000")
    parser.add_argument(
        "json_path",
        nargs="?",
        help="Path to JSON payload. When omitted, 1000 synthetic transactions are generated.",
    )
    parser.add_argument("--seed", type=int, default=99, help="Random seed for synthetic data")
    args = parser.parse_args(argv)

    if args.json_path:
        try:
            transactions, labels = _load_transactions(args.json_path)
        except Exception as exc:  # noqa: BLE001
            print(f"Failed to load transactions: {exc}", file=sys.stderr)
            return 1
    else:
        transactions = _generate_synthetic(1000, args.seed)
        labels = {txn["id"]: int(txn.get("label", 0)) for txn in transactions}

    payload = _prepare_payload(transactions)
    url = args.api_base.rstrip("/") + "/api/score"

    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})

    start = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        print(f"API request failed with status {exc.code}: {exc.read().decode('utf-8', 'ignore')}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"API request error: {exc}", file=sys.stderr)
        return 1
    end = time.perf_counter()

    try:
        results = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON response: {exc}", file=sys.stderr)
        return 1

    batch_size = len(payload) if payload else 1
    latency_ms = (end - start) * 1000.0
    per_item_ms = latency_ms / batch_size
    print(f"batch={batch_size} latency_ms={latency_ms:.2f} per_item_ms={per_item_ms:.4f}")

    if isinstance(results, list):
        _compute_metrics(results, labels, thresholds=[0.60, 0.70, 0.80])
    else:
        print("Unexpected response format (expected list)", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
