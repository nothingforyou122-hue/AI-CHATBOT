# server.py
import os, base64, uuid
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from ai_brain import ask_chat, build_image_prompt
from ai_image import generate_image_bytes
from auth import check_api_key

ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT, "..", "frontend")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# in-memory simple session store
CONVERSATIONS: dict[str, list[tuple[str,str]]] = {}

@app.post("/api/chat")
async def chat(req: Request, x_api_key: str | None = None):
    body = await req.json()
    prompt = body.get("prompt")
    session = body.get("session") or str(body.get("session_id") or "default")
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt required")

    history = CONVERSATIONS.get(session, [])
    reply = ask_chat(prompt, history=history)
    # store conversation
    CONVERSATIONS.setdefault(session, []).append((prompt, reply))
    # keep last 20
    CONVERSATIONS[session] = CONVERSATIONS[session][-20:]
    return JSONResponse({"reply": reply, "session": session})

@app.post("/api/generate")
async def generate(req: Request):
    body = await req.json()
    prompt = body.get("prompt")
    if not prompt:
        raise HTTPException(status_code=400, detail="prompt required")
    # Use LLM-based prompt expansion optionally
    sd_prompt = build_image_prompt(prompt)
    try:
        image_bytes = generate_image_bytes(sd_prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return JSONResponse({"image": b64, "prompt_used": sd_prompt})

@app.get("/api/health")
def health():
    return {"status": "ok"}
