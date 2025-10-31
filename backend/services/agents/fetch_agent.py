import os, textwrap
from django.conf import settings
ARTIFACT_DIR = os.path.join(settings.MEDIA_ROOT, "artifacts")

def _ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def _local_text_artifact(action: str, txn_id: str) -> str:
    _ensure_dir(ARTIFACT_DIR)
    body = textwrap.dedent(f"""
    Transaction: {txn_id}
    Action: {action.replace('_', ' ').title()}
    Reason: Suspicious pattern detected by Guardian (anomaly exceeded threshold).
    """).strip()
    file_name = f"{txn_id}_{action}.txt"
    file_path = os.path.join(ARTIFACT_DIR, file_name)
    with open(file_path, "w") as f:
        f.write(body)
    # Served by Django static on /static/
    return f"/static/artifacts/{file_name}"

def run_fetch_action(action: str, txn_id: str) -> dict:
       key = os.getenv("FETCH_API_KEY")
       if key:
           r = requests.post(
               "https://agentverse.fetch.ai/v1/agents/execute",
               json={
                   "action": action,
                   "transaction_id": txn_id,
                   "context": {...}  # Send transaction details
               },
               headers={"Authorization": f"Bearer {key}"}
           )
           return r.json()
       # Fallback to local artifact
       return {"artifact_url": _local_text_artifact(action, txn_id)}