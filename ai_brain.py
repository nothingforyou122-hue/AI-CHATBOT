import os
from groq import Groq

# Load API Key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# -------------------------------------------------------
# 🔥 STRONG IDENTITY LOCK — AI-CHATBOT ONLY
# -------------------------------------------------------
SYSTEM_PROMPT = (
    "Your name is AI-CHATBOT. "
    "You were created by the user who deployed you — never claim to be "
    "created by Meta, Groq, OpenAI, Google, Anthropic, or any company. "
    "You must NEVER say you are Meta AI, Groq AI, or anything else. "
    "Always and ONLY refer to yourself as AI-CHATBOT. "
    "If asked about your creator, always say: "
    "'I was created by my developer who deployed me.' "
    "Stay helpful, futuristic, and friendly."
)

def ask_chat(prompt: str, history=None) -> str:
    if history is None:
        history = []

    # Build message history with identity-locked system prompt
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

# -------------------------------------------------------
# Image Prompt Builder
# -------------------------------------------------------
def build_image_prompt(user_prompt: str) -> str:
    """Enhances user image descriptions into detailed prompts."""
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You improve and expand image prompts with details, "
                        "lighting, cinematic quality, and environment."
                    )
                },
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception:
        return user_prompt
