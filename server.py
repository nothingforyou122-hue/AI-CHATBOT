import os, base64
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from ai_brain import ask_chat, build_image_prompt
from ai_image import generate_image_bytes

ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(ROOT, "frontend")   # ✅ FIXED PATH

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve frontend
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

# memory chat history
CONVERSATIONS = {}

# ✅ CHAT ROUTE
@app.post("/api/chat")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("prompt")
    session = data.get("session", "default")

    if not prompt:
        return JSONResponse({"reply": "Please enter a message."})

    history = CONVERSATIONS.get(session, [])

    # ✅ Force personality
    system_prompt = "You are AI-CHATBOT, a helpful, honest assistant."

    reply = ask_chat(prompt, history=history)

    CONVERSATIONS.setdefault(session, []).append((prompt, reply))
    CONVERSATIONS[session] = CONVERSATIONS[session][-20:]

    return JSONResponse({"reply": reply})


# ✅ IMAGE ROUTE
@app.post("/api/generate")
async def generate(req: Request):
    body = await req.json()
    prompt = body.get("prompt")

    if not prompt:
        return JSONResponse({"error": "Prompt required"})

    final_prompt = build_image_prompt(prompt)

    image_bytes = generate_image_bytes(final_prompt)
    b64 = base64.b64encode(image_bytes).decode("utf-8")

    return JSONResponse({"image": b64})


# ✅ FILE SCAN ROUTE
@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()

    try:
        text = content.decode("utf-8", errors="ignore")
    except:
        return {"info": "Could not read this file type."}

    analysis = ask_chat(f"Analyze this file and summarize:\n{text[:3000]}")

    return {"summary": analysis}


# ✅ HEALTH CHECK
@app.get("/api/health")
def health():
    return {"status": "AI-CHATBOT online"}
