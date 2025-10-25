# Guardian Model Features

The Guardian anomaly scorer relies on the following transaction-level features. All
numerical values are expected as floats unless specified otherwise. Missing values
are substituted with the documented defaults before scoring.

## Feature Reference

| Feature | Type | Expected Range | Default | Rationale |
| --- | --- | --- | --- | --- |
| `amount` | float (USD) | `[0, +inf)` (typically ≤ 1,000) | `0.0` | Larger purchases often deviate from a user’s usual spending and warrant attention. |
| `hour` | integer | `[0, 23]` hour of day (UTC) | `0` | Encodes time-of-day patterns; very late activity may signal compromised credentials. |
| `is_foreign` | binary (0/1) | `{0, 1}` | `0` | Marks cross-border use, a strong indicator of account takeover or card theft. |
| `merchant_risk` | float | `[0.0, 1.0]` | `0.0` | Captures historical fraud rates for the merchant to prioritise known hotspots. |
| `user_txn_rate` | float | `[0, +inf)` (transactions/hour) | `0.0` | Highlights sudden bursts of activity relative to the customer’s baseline. |

## Canonical Payload

```json
[
  {
    "id": "txn_123",
    "features": {
      "amount": 189.02,
      "hour": 2,
      "is_foreign": 1,
      "merchant_risk": 0.86,
      "user_txn_rate": 4.2
    }
  }
]
```

The scoring response mirrors this identifier and augments it with a normalised
risk score and a list of up to three human-readable reasons ordered by impact.
