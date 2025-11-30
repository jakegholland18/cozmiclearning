# modules/shared_ai.py

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------------------------------------------------------
# CHARACTER VOICES
# -------------------------------------------------------
def build_character_voice(character: str) -> str:
    voices = {
        "lio":    "Speak smooth, confident, mission-focused, like a calm space agent.",
        "jasmine": "Speak warm, bright, curious, like a kind space big sister.",
        "everly":  "Speak elegant, brave, compassionate, like a gentle warrior-princess.",
        "nova":    "Speak energetic, curious, nerdy-smart, excited about learning.",
        "theo":    "Speak thoughtful, patient, wise, like a soft academic mentor.",
    }
    return voices.get(character, "Speak in a friendly, warm tutoring voice.")


# -------------------------------------------------------
# GRADE LEVEL DEPTH RULES
# -------------------------------------------------------
def grade_depth_instruction(grade: str) -> str:
    g = int(grade)

    if g <= 3:
        return "Use extremely simple words and very short sentences. Explain slowly and gently."
    if g <= 5:
        return "Use simple language with clear examples. Keep ideas small and concrete."
    if g <= 8:
        return "Use moderate detail, logical explanation, and age-appropriate examples."
    if g <= 10:
        return "Use deeper reasoning, connections, and clearer examples."
    if g <= 12:
        return "Use high-school level depth, real-world examples, and strong conceptual clarity."

    return "Use college-level clarity and deep conceptual reasoning."


# -------------------------------------------------------
# SYSTEM PROMPT — SIX-SECTION FORMAT (DEFAULT)
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

STRICT FORMAT RULES:
• No bullet points.
• No dashes used as list items.
• No numbered lists.
• No asterisk lists.
• ONLY paragraphs of full sentences.
• Each section MUST contain 2–5 sentences.
• After each label, put one blank line, then the paragraph.
• Never modify section labels.
• Never merge or remove sections.
• Never add new sections.
"""


# -------------------------------------------------------
# DEFAULT STUDY BUDDY (6-SECTION FORMAT)
# Used by normal subject helpers (math, science, etc.)
# -------------------------------------------------------
def study_buddy_ai(prompt: str, grade: str, character: str) -> str:
    depth_rule = grade_depth_instruction(grade)
    voice = build_character_voice(character)

    system_prompt = f"""
{BASE_SYSTEM_PROMPT}

CHARACTER VOICE:
{voice}

GRADE LEVEL DEPTH RULE:
{depth_rule}

CLARITY RULE:
Your explanations must become deeper and more detailed for older grades,
especially grades 9–12.

OUTPUT REQUIREMENT:
For ALL SIX sections:
• Use EXACT labels.
• Write 2–5 full sentences.
• NO bullets. NO lists. NO line breaks inside the paragraph.
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
SYSTEM:
{system_prompt}

STUDENT QUESTION:
{prompt}
"""
    )

    return response.output_text


# -------------------------------------------------------
# RAW STUDY BUDDY (NO FORCED SECTIONS)
# Used by POWERGRID master guide + deep chat
# -------------------------------------------------------
def study_buddy_ai_raw(prompt: str, grade: str, character: str) -> str:
    """
    Freeform AI helper that obeys the caller's prompt formatting.
    No six-section template is enforced here.
    """

    depth_rule = grade_depth_instruction(grade)
    voice = build_character_voice(character)

    system_prompt = f"""
You are HOMEWORK BUDDY — a warm, gentle tutor.

RULES:
• Follow the USER'S instructions for structure and formatting.
• Do NOT force any fixed number of sections.
• Do NOT add the 6-section template.
• Do NOT add extra headings unless the user explicitly asks.
• Adapt depth and vocabulary to grade level.

CHARACTER VOICE:
{voice}

GRADE LEVEL DEPTH RULE:
{depth_rule}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=f"""
SYSTEM:
{system_prompt}

STUDENT PROMPT:
{prompt}
"""
    )

    return response.output_text
