import os, time
# If you get a CREAO_API_KEY later, you can replace this stub with a real call.

def run_creao_flow(action: str, txn_id: str) -> dict:
    # Stubbed workflow trace (good for Creao prize narrative)
    return {
        "status": "ok",
        "chain": [
            {"step": "score_threshold_check", "result": "exceeded"},
            {"step": "selected_action", "result": action},
            {"step": "txn_id", "result": txn_id},
            {"step": "executed_at", "result": time.time()},
        ],
    }