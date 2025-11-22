# ai_image.py
import os
import requests
import base64
from typing import Optional

STABILITY_KEY = os.getenv("STABILITY_API_KEY")
STABILITY_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

if not STABILITY_KEY:
    raise RuntimeError("Missing STABILITY_API_KEY in environment")

def generate_image_bytes(prompt: str, output_format: str = "png", timeout: int = 120) -> bytes:
    headers = {
        "authorization": f"Bearer {STABILITY_KEY}",
        "accept": "application/json",
    }
    files = {
        "prompt": (None, prompt),
        "output_format": (None, output_format)
    }
    r = requests.post(STABILITY_URL, headers=headers, files=files, timeout=timeout)
    if r.status_code != 200:
        raise RuntimeError(f"Stability API error ({r.status_code}): {r.text}")
    data = r.json()
    b64 = data.get("image")
    if not b64:
        raise RuntimeError(f"No image returned: {data}")
    return base64.b64decode(b64)
