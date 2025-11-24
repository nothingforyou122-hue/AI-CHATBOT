# ai_brain.py
import os
from groq import Groq

GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    raise RuntimeError("Missing GROQ_API_KEY in environment")

client = Groq(api_key=GROQ_KEY)

SYSTEM_PROMPT = (
    "You are AlbinGPT — a helpful assistant that can chat, write code, and produce "
    "detailed image prompts for the image generator when the user asks. When user asks for images, "
    "return a short caption and an image prompt suitable for stable-diffusion."
)

def ask_chat(user_message: str, history: list[tuple[str,str]] | None = None):
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if history:
        for u, a in history:
            messages.append({"role": "user", "content": u})
            messages.append({"role": "assistant", "content": a})
    messages.append({"role": "user", "content": user_message})

    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        max_tokens=512,
    )
    return resp.choices[0].message.content

def build_image_prompt(user_text: str) -> str:
    """
    If you later want to always expand image prompts via LLM, call ask_chat with a special instruction.
    For now return a concise SD-ready prompt based on user_text.
    """
    # Lightweight deterministic enhancer:
    return (
        f"{user_text}, ultra-detailed, photorealistic, 8k, cinematic lighting, "
        "high detail, sharp focus, realistic materials, award-winning composition"
    )
