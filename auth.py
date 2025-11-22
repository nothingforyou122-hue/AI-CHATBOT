# auth.py
from fastapi import Header, HTTPException

# Basic API key check for web calls from the frontend.
# For production you should use a more robust auth (user accounts, tokens).
FRONTEND_KEY = "REPLACE_WITH_STRONG_RANDOM"  # local default, override in env when deploying

def check_api_key(x_api_key: str | None = Header(None)):
    if x_api_key is None:
        raise HTTPException(status_code=401, detail="Missing API key")
    if x_api_key != FRONTEND_KEY and x_api_key != __import__("os").environ.get("FRONTEND_KEY"):
        raise HTTPException(status_code=403, detail="Invalid API key")
