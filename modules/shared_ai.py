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
        return "Use very simple words and short sentences. Explain slowly."
    if g <= 5:
        return "Use simple language with clear examples."
    if g <= 8:
        return "Use moderate detail and logical explanation."
    if g <= 10:
        return "Use deeper reasoning and strong connections."
    if g <= 12:
        return "Use high-school level depth with real-world examples."

    return "Use college-level clarity and deep conceptual reasoning."


# -------------------------------------------------------
# SYSTEM PROMPT — STRICT FORMAT FOR SUBJECT ANSWERS
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
• No lists of any kind.
• ONLY paragraphs with full sentences.
• Each section MUST contain 2–5 full sentences.
• After each label: one blank line, then the paragraph.
• Never modify section labels.
• Never merge or remove sections.
• Never add new sections.
"""


# -------------------------------------------------------
# STANDARD STUDY BUDDY AI (Normal Subjects)
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
            {"role": "user", "content": prompt},
        ]
    )

    return response.output_text


# -------------------------------------------------------
# POWERGRID MASTER STUDY GUIDE AI — SAFE VERSION
# -------------------------------------------------------
def powergrid_master_ai(prompt: str, grade: str, character: str) -> str:
    """
    Generates the ULTRA-DETAILED PowerGrid Guide.
    Length-capped + Render-safe.
    """

    voice = build_character_voice(character)
    depth_rule = grade_depth_instruction(grade)

    system_prompt = f"""
You are HOMEWORK BUDDY — a highly intelligent but warm tutor.

Your task is to create a POWERGRID MASTER STUDY GUIDE
that is extremely detailed but SAFE for server limits.

LENGTH RULES:
• Maximum length ~3,000–5,000 words.
• Do NOT exceed limit.
• Stop once concepts are fully explained.
• No infinite rambling.

MIXED FORMAT:
• Paragraphs + bullet points
• Sub-bullets allowed
• ASCII diagrams allowed
• Examples, analogies, comparisons
• Common mistakes
• Memory strategies
• Beginner → expert progression

FINAL SECTION:
CHRISTIAN WORLDVIEW PERSPECTIVE
(1–3 paragraphs connecting topic to compassion, truth, purpose, wisdom, etc.)

VOICE:
{voice}

GRADE LEVEL:
{depth_rule}
"""

    client = get_client()

    response = client.responses.create(
        model="gpt-4.1",
        max_output_tokens=3500,   # Render-safe
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    return response.output_text
