# modules/ai_client.py

import os
from openai import OpenAI

# Load OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Sends a simple prompt to OpenAI and returns plain text output.
    Uses the Chat Completions API.
    """
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

