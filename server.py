from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
import os

from ai_brain import ask_chat

app = FastAPI()

# Serve Frontend UI
@app.get("/", response_class=HTMLResponse)
async def home():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()


# Chat API
@app.post("/api/chat")
async def chat(prompt: str = Form(...)):
    try:
        reply = await ask_chat(prompt)
        return {"reply": reply}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# File Upload API
@app.post("/api/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    return {"filename": file.filename, "size": len(content)}
