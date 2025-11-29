import os
import requests

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL = "llama-3.1-8b-instant"

async def ask_chat(prompt: str):
    if not GROQ_API_KEY:
        return "Error: No API key set."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are AI-CHATBOT."},
            {"role": "user", "content": prompt}
        ]
    }

    res = requests.post(url, headers=headers, json=data)

    r = res.json()

    if "choices" not in r:
        return "API Error. Check logs."

    return r["choices"][0]["message"]["content"]
