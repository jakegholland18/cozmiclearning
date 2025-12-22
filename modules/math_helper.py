# modules/math_helper.py

from modules.shared_ai import study_buddy_ai, filter_gambling_content
from modules.personality_helper import apply_personality
from modules.answer_formatter import parse_into_sections, format_answer


# -----------------------------------------------------------
# Detect Christian-related math questions
# -----------------------------------------------------------
def is_christian_question(text: str) -> bool:
    keywords = [
        "christian", "christianity", "god", "jesus", "bible",
        "biblical", "faith", "christian perspective",
        "how does this relate to christianity",
        "how does this relate to god"
    ]
    txt = text.lower()
    return any(k in txt for k in keywords)


# -----------------------------------------------------------
# Detect probability/gambling-related questions
# -----------------------------------------------------------
def is_probability_question(text: str) -> bool:
    keywords = [
        "probability", "odds", "chance", "likelihood", "random",
        "dice", "coin", "card", "bet", "gamble", "casino",
        "roulette", "blackjack", "poker", "lottery", "expected value"
    ]
    txt = text.lower()
    return any(k in txt for k in keywords)


# -----------------------------------------------------------
# Build standard math prompt (NO bullets)
# -----------------------------------------------------------
def build_math_prompt(question: str, grade: str):
    # Add extra safety guidelines for probability questions
    probability_safety = ""
    if is_probability_question(question):
        probability_safety = """

IMPORTANT - PROBABILITY SAFETY GUIDELINES:
• Use ONLY age-appropriate examples: board games, game shows, carnival games, coin flips, weather, sports stats
• NEVER explain gambling strategies, betting systems, or how to improve casino odds
• If gambling is mentioned, frame it as a cautionary math lesson showing house edge
• Emphasize stewardship: God calls us to be wise with resources
• Redirect to educational probability concepts
"""

    return f"""
You are a gentle math tutor for a grade {grade} student.

The student asked:
\"{question}\"
{probability_safety}
Use the SIX-section CozmicLearning format.
NO bullet points. ONLY calm paragraphs.

SECTION 1 — OVERVIEW
Explain the math idea in 2–3 short sentences.

SECTION 2 — KEY FACTS
Describe the key steps, rules, or concepts in 3–5 simple sentences.
No lists or bullets.

SECTION 3 — CHRISTIAN VIEW
Explain softly how many Christians appreciate order, logic, and truth
in math. If it does not apply naturally, simply explain that Christians
still value clear thinking.

SECTION 4 — AGREEMENT
Explain in one short paragraph what all worldviews agree on about the math.

SECTION 5 — DIFFERENCE
Explain gently how motivation or worldview might differ, even if
the math steps stay the same.

SECTION 6 — PRACTICE
Give 2–3 tiny practice problems and provide short example answers.
Write them in simple, tiny paragraph sentences.
"""


# -----------------------------------------------------------
# Build Christian-directed math prompt (NO bullets)
# -----------------------------------------------------------
def build_christian_math_prompt(question: str, grade: str):
    # Add extra safety guidelines for probability questions
    probability_safety = ""
    if is_probability_question(question):
        probability_safety = """

IMPORTANT - PROBABILITY SAFETY GUIDELINES:
• Use ONLY age-appropriate examples: board games, game shows, carnival games, coin flips, weather, sports stats
• NEVER explain gambling strategies, betting systems, or how to improve casino odds
• If gambling is mentioned, frame it as a cautionary math lesson showing house edge
• Connect to Biblical stewardship: God calls us to be wise with resources (Luke 16:10-11)
• Redirect to educational probability concepts
"""

    return f"""
The student asked this math question from a Christian perspective:

\"{question}\"
{probability_safety}
Use the SIX-section CozmicLearning format.
NO bullet points.

SECTION 1 — OVERVIEW
Explain the idea slowly and simply.

SECTION 2 — KEY FACTS
Describe the rules, steps, or concepts needed to solve this.

SECTION 3 — CHRISTIAN VIEW
Explain softly how Christians may appreciate order, consistency, and design
in creation, including mathematics.

SECTION 4 — AGREEMENT
Explain what all worldviews agree on about the math.

SECTION 5 — DIFFERENCE
Explain kindly how motivations or values may differ while the math stays the same.

SECTION 6 — PRACTICE
Give a couple of tiny practice problems with short example answers.
"""


# -----------------------------------------------------------
# MAIN PUBLIC FUNCTION — math explanation
# -----------------------------------------------------------
def explain_math(question: str, grade_level="5", character="nova"):

    # Build proper base prompt
    if is_christian_question(question):
        base_prompt = build_christian_math_prompt(question, grade_level)
    else:
        base_prompt = build_math_prompt(question, grade_level)

    # Personality wrapper
    enriched_prompt = apply_personality(character, base_prompt)

    # AI output
    raw = study_buddy_ai(enriched_prompt, grade_level, character)

    # Apply gambling content filter for probability questions
    if is_probability_question(question):
        raw, was_flagged = filter_gambling_content(raw, topic="probability")
        if was_flagged:
            print(f"⚠️  Gambling content detected and filtered in math response")

    # Universal parsing
    sections = parse_into_sections(raw)

    # Return as structured dict for subject.html
    return format_answer(
        overview=sections.get("overview", ""),
        key_facts=sections.get("key_facts", []),
        christian_view=sections.get("christian_view", ""),
        agreement=sections.get("agreement", []),
        difference=sections.get("difference", []),
        practice=sections.get("practice", []),
        raw_text=raw
    )

