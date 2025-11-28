import os
from groq import Groq

MODEL = "llama-3.1-8b-instant"
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Your name is AI-CHATBOT.
You were created by the user.
Never mention OpenAI, Meta, Groq, or other companies.
"""


def ask_chat(prompt):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    return completion.choices[0].message.content
