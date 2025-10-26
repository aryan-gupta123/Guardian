import os
import requests
from typing import Optional


def speak_alert(text: str) -> Optional[str]:
    """
    Generate audio alert using Fish Audio API.
    Returns audio URL if successful, None otherwise.
    """
    key = os.getenv("FISH_AUDIO_API_KEY")
    if not key:
        return None
    try:
        r = requests.post(
            "https://api.fish.audio/tts",
            json={"text": text, "voice": "en-US-default"},
            headers={"Authorization": f"Bearer {key}"},
            timeout=20,
        )
        if r.ok:
            return r.json().get("audio_url")
    except Exception:
        pass
    return None
