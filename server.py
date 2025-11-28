# server.py
import os
import base64
from fastapi import FastAPI, Request, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from ai_brain import ask_chat, build_image_prompt
from ai_image import generate_image_bytes  # keep your existing ai_image.py

ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT, "frontend")

app = FastAPI(title="AI-CHATBOT")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files at /static and index at /
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/", response_class=FileResponse)
def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Index not found")
    return index_path

# In-memory conversation store
CONVERSATIONS: dict[str, list[tuple[str,str]]] = {}

@app.post("/api/chat")
async def chat(req: Request):
    try:
        body = await req.json()
        prompt = body.get("prompt")
        session = body.get("session") or "default"

        if not prompt:
            raise HTTPException(status_code=400, detail="prompt required")

        history = CONVERSATIONS.get(session, [])
        # ask_chat is responsible for system prompt & identity lock
        reply = ask_chat(prompt, history=history)

        CONVERSATIONS.setdefault(session, []).append((prompt, reply))
        CONVERSATIONS[session] = CONVERSATIONS[session][-30:]

        return JSONResponse({"reply": reply, "session": session})
    except HTTPException as he:
        raise he
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/generate")
async def generate(req: Request):
    try:
        body = await req.json()
        prompt = body.get("prompt")
        if not prompt:
            raise HTTPException(status_code=400, detail="prompt required")

        sd_prompt = build_image_prompt(prompt)
        image_bytes = generate_image_bytes(sd_prompt)
        b64 = base64.b64encode(image_bytes).decode("utf-8")
        return JSONResponse({"image": b64, "prompt_used": sd_prompt})
    except HTTPException as he:
        raise he
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Accepts file uploads (text-like files best). Returns a short summary using ask_chat.
    Requires python-multipart in requirements.txt.
    """
    try:
        raw = await file.read()
        # try decode as utf-8 text; fallback to bytes length message
        try:
            text = raw.decode("utf-8", errors="ignore")
        except Exception:
            text = ""
        if not text:
            return JSONResponse({"error": "File could not be read as text."})

        # limit length to avoid huge payloads
        snippet = text[:4000]
        summary = ask_chat(f"Summarize and extract key points from this file:\n\n{snippet}", history=[])
        return JSONResponse({"summary": summary})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/health")
def health():
    return {"status": "AI-CHATBOT online"}
