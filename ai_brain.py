# ai_brain.py
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY env var missing")

client = Groq(api_key=GROQ_API_KEY)

# Strong identity lock — AI must always say AI-CHATBOT as its name.
SYSTEM_PROMPT = (
    "You are AI-CHATBOT. You were created by the developer who deployed you. "
    "You must NEVER claim to be created by Meta, OpenAI, Groq, Google, Anthropic, or any company. "
    "Always identify yourself only as 'AI-CHATBOT'. Answer helpfully, format lists clearly, "
    "and when asked about your creator, say: 'I was created by my developer who deployed me.'"
)

MODEL = "llama-3.1-8b-instant"

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
            temperature=0.6,
            max_tokens=800,
        )
        return response.choices[0].message.content
    except Exception as e:
        # return error string (server will wrap it)
        return f"Error while calling model: {e}"

def build_image_prompt(user_prompt: str) -> str:
    # Small enhancer prompt to make the image prompt richer
    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You improve and expand user image prompts with visual detail, lighting, camera, and style."},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
            max_tokens=200
        )
        return resp.choices[0].message.content
    except Exception:
        return user_prompt
