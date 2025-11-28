from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"


def ask_chat(prompt, history=None):
    if history is None:
        history = []

    messages = []

    # System identity
    messages.append({
        "role": "system",
        "content": "You are AI-CHATBOT, a helpful, professional AI assistant."
    })

    # Conversation memory
    for user, bot in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": bot})

    # New message
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=600
    )

    return response.choices[0].message.content


def build_image_prompt(prompt: str):
    return f"Ultra-detailed, cinematic, high resolution: {prompt}"
