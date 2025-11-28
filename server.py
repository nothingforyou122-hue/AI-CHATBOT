@app.post("/api/chat")
async def chat(req: Request):
    body = await req.json()
    prompt = body.get("prompt")

    if not prompt:
        return JSONResponse({"reply": "Empty prompt received."})

    history = CONVERSATIONS.get("default", [])
    reply = ask_chat(prompt, history=history)

    CONVERSATIONS.setdefault("default", []).append((prompt, reply))
    CONVERSATIONS["default"] = CONVERSATIONS["default"][-20:]

    # ✅ RETURN FORMAT FIX
    return JSONResponse({"reply": reply})
