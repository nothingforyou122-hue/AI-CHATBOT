import os, base64
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from ai_brain import ask_chat

ROOT = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(ROOT, "frontend")

app = FastAPI()

# ✅ Serve frontend correctly
app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")

@app.post("/api/chat")
async def chat(req: Request):
    data = await req.json()
    prompt = data.get("prompt", "")

    if not prompt:
        return {"reply": "Please type something."}

    reply = ask_chat(prompt)
    return {"reply": reply}

@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    size = len(content)

    return {"reply": f"File '{file.filename}' uploaded successfully ({size} bytes)."}
