from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.environ.get("GROQ_API_KEY")
MODEL = "llama-3.1-8b-instant"

@app.post("/api/chat")
async def chat(req: Request):
    body = await req.json()
    prompt = body.get("prompt")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                      headers=headers, json=data)

    res = r.json()

    try:
        reply = res["choices"][0]["message"]["content"]
    except:
        reply = "AI backend error."

    return {"reply": reply}
