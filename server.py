import os
import base64

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# ✅ LOAD ENV
load_dotenv()

from ai_brain import ask_chat, build_image_prompt
from ai_image import generate_image_bytes

# ✅ CREATE APP FIRST
app = FastAPI()

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ STATIC FILES
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# ✅ MEMORY
CONVERSATIONS = {}

# ✅ CHAT ENDPOINT
@app.post("/api/chat")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("prompt")

    if not prompt:
        return JSONResponse({"reply": "No message received."})

    history = CONVERSATIONS.get("default", [])
    reply = ask_chat(prompt, history)

    CONVERSATIONS.setdefault("default", []).append((prompt, reply))
    CONVERSATIONS["default"] = CONVERSATIONS["default"][-30:]

    # ✅ ALWAYS RETURN "reply"
    return JSONResponse({"reply": reply})

# ✅ IMAGE GENERATION
@app.post("/api/generate")
async def generate(req: Request):
    data = await req.json()
    prompt = data.get("prompt")

    if not prompt:
        return JSONResponse({"error": "No prompt provided"})

    prompt = build_image_prompt(prompt)
    image_bytes = generate_image_bytes(prompt)

    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return JSONResponse({"image": encoded})

# ✅ HEALTH CHECK
@app.get("/api/health")
def health():
    return {"status": "ok"}
