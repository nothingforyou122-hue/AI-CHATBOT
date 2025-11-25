import os
from groq import Groq

# Load API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# -------------------------------
# FIXED NAME — AI-CHATBOT
# -------------------------------
SYSTEM_PROMPT = (
    "You are AI-CHATBOT — a helpful futuristic assistant. "
    "Always refer to yourself as AI-CHATBOT. "
    "You can chat, write code, and produce detailed image prompts "
    "for the image generator."
)

def ask_chat(prompt: str, history=None) -> str:
    if history is None:
        history = []

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})

    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# -------------------------------
# Image prompt builder
# -------------------------------
def build_image_prompt(user_prompt: str) -> str:
    """Expand a short description into a detailed image prompt."""
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": (
                    "You are a prompt enhancer. Convert user descriptions into "
                    "high-quality, detailed image generation prompts."
                )},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception:
        return user_prompt
