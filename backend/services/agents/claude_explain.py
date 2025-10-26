import os, requests

CLAUDE_URL = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL = "claude-3-sonnet-20240229"

def _fallback_text(reasons: list) -> str:
    if not reasons:
        return "Flagged due to unusual transaction pattern."
    feats = ", ".join(f"{r.get('feature')}={r.get('value')}" for r in reasons)
    return f"Flagged due to unusual values: {feats}."

def explain_with_claude(reasons: list) -> str:
    key = os.getenv("CLAUDE_API_KEY")
    if not key:
        return _fallback_text(reasons)

    prompt = "The following features indicate a risky transaction:\n"
    for r in reasons:
        prompt += f"- {r.get('feature')}: {r.get('value')}\n"
    prompt += "\nExplain in one crisp sentence why this looks fraudulent."

    headers = {"x-api-key": key, "anthropic-version": "2023-06-01"}
    body = {
        "model": CLAUDE_MODEL,
        "max_tokens": 80,
        "temperature": 0.2,
        "messages": [{"role": "user", "content": prompt}],
    }
    try:
        res = requests.post(CLAUDE_URL, json=body, headers=headers, timeout=20)
        res.raise_for_status()
        return res.json()["content"][0]["text"]
    except Exception:
        return _fallback_text(reasons)