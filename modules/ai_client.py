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


def get_completion(user_prompt: str, system_prompt: str = "", model: str = "gpt-4o-mini") -> str:
    """
    Gets an AI completion with optional system prompt.
    Used for tutorial help and other assistant features.

    Args:
        user_prompt: The user's question or request
        system_prompt: Optional system instructions for the AI
        model: OpenAI model to use (default: gpt-4o-mini)

    Returns:
        AI response as string
    """
    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content

