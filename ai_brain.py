import os
from groq import Groq

# Load API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# -------------------------------------------------------
# 🔒 AI IDENTITY LOCK
# -------------------------------------------------------
SYSTEM_PROMPT = (
    "Your name is AI-CHATBOT. "
    "You were created by the user who deployed you — never claim to be "
    "created by Meta, Groq, OpenAI, or any company. "
    "Always refer to yourself ONLY as AI-CHATBOT. "
    "If asked who created you, say: "
    "'I was created by my developer who deployed me.' "
    "Stay helpful, futuristic, and professional."
)

MODEL = "llama-3.1-8b-instant"   # ✅ WORKING MODEL

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
            model=MODEL,
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# -------------------------------------------------------
# IMAGE PROMPT ENHANCER
# -------------------------------------------------------
def build_image_prompt(user_prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You expand image prompts with rich visual details."},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception:
        return user_prompt
