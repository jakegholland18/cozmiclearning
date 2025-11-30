# modules/shared_ai.py
import os

# -------------------------------
# Lazy-load OpenAI client
# -------------------------------
def get_client():
    from openai import OpenAI
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------------------------------------------------------
# CHARACTER VOICES
# -------------------------------------------------------
def build_character_voice(character: str) -> str:
    voices = {
        "lio":    "Smooth, confident, mission-focused, calm space agent.",
        "jasmine": "Warm, bright, curious, like a kind space big sister.",
        "everly":  "Elegant, brave, compassionate, like a gentle warrior-princess.",
        "nova":    "Energetic, curious, nerdy-smart, excited about learning.",
        "theo":    "Thoughtful, patient, wise, like a soft academic mentor.",
    }
    return voices.get(character, "Friendly, warm tutoring voice.")


# -------------------------------------------------------
# GRADE LEVEL DEPTH RULES
# -------------------------------------------------------
def grade_depth_instruction(grade: str) -> str:
    g = int(grade)

    if g <= 3:
        return "Use very simple words and short sentences. Explain slowly."
    if g <= 5:
        return "Use simple language with clear examples."
    if g <= 8:
        return "Use moderate detail and logical explanation."
    if g <= 10:
        return "Use deeper reasoning and strong connections."
    if g <= 12:
        return "Use high-school depth with real-world examples."

    return "Use college-level clarity and deep conceptual reasoning."


# -------------------------------------------------------
# SYSTEM PROMPT FOR NORMAL SUBJECT RESPONSES
# -------------------------------------------------------
BASE_SYSTEM_PROMPT = """
You are HOMEWORK BUDDY — a warm, gentle tutor.

You MUST ALWAYS output EXACTLY these SIX sections with EXACT ASCII labels:

SECTION 1 — OVERVIEW
SECTION 2 — KEY FACTS
SECTION 3 — CHRISTIAN VIEW
SECTION 4 — AGREEMENT
SECTION 5 — DIFFERENCE
SECTION 6 — PRACTICE

STRICT RULES:
• No bullet points.
• No lists.
• ONLY paragraphs with full sentences.
• Each section MUST contain 2–5 sentences.
• After each label: one blank line, then the paragraph.
• Never alter section labels.
• Never add or remove sections.
"""


# -------------------------------------------------------
# NORMAL STUDY BUDDY AI (All subjects except PowerGrid)
# -------------------------------------------------------
def study_buddy_ai(prompt: str, grade: str, character: str) -> str:
    depth_rule = grade_depth_instruction(grade)
    voice = build_character_voice(character)

    system_prompt = f"""
{BASE_SYSTEM_PROMPT}

CHARACTER VOICE:
{voice}

GRADE RULE:
{depth_rule}
"""

    client = get_client()

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user",  "content": prompt},
        ]
    )

    return response.output_text


# -------------------------------------------------------
# POWERGRID — COMPRESSED STUDY GUIDE GENERATOR
# -------------------------------------------------------
def powergrid_master_ai(topic_text: str, grade: str, character: str) -> str:
    """
    NEW COMPRESSED POWERGRID ENGINE
    • Hyper-efficient
    • 1,200-word hard cap
    • Very dense information
    • No rambling
    • Render-safe
    """

    voice = build_character_voice(character)
    depth_rule = grade_depth_instruction(grade)

    # FINAL, OPTIMIZED, COMPRESSED SYSTEM PROMPT
    system_prompt = f"""
You are HOMEWORK BUDDY — a brilliant, concise, high-efficiency tutor.

GOAL:
Create a **compressed PowerGrid Study Guide** that fits LOTS of knowledge in
as little space as possible. No filler. No rambling. No long essays.

ABSOLUTE HARD LIMIT:
⛔ NEVER exceed **1,200 words**.

STYLE RULES:
• Extremely compact and information-dense.
• Short sentences. Maximum clarity.
• Crisp bullets allowed.
• Micro-paragraphs only.
• Prefer: definitions → insights → quick examples.
• Avoid repetition.
• Never waste space.

MANDATORY FORMAT:
1. MICRO-OVERVIEW (3–5 sentences)
2. CORE IDEAS (compressed bullets)
3. FAST DEEP DIVE (tight micro-paragraphs)
4. MINI DIAGRAM (≤ 5 ASCII lines if helpful)
5. EXAMPLES (1–2 sentences each)
6. COMMON MISTAKES (short bullets)
7. CHRISTIAN WORLDVIEW (1 short paragraph)

CHARACTER VOICE:
{voice}

GRADE LEVEL:
{depth_rule}
"""

    client = get_client()

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user",
             "content": f"Create a compressed PowerGrid Study Guide about:\n{topic_text}"},
        ]
    )

    return response.output_text

