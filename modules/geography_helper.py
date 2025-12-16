# modules/geography_helper.py

from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality
from modules.answer_formatter import parse_into_sections, format_answer


# ------------------------------------------------------------
# Detect Christian-worldview geography questions
# ------------------------------------------------------------
def is_christian_question(text: str) -> bool:
    keywords = [
        "christian", "christianity", "god", "jesus", "bible", "biblical",
        "faith", "christian worldview", "from a christian perspective",
        "how does this relate to christianity", "how does this relate to god",
        "stewardship", "creation care"
    ]
    txt = text.lower()
    return any(k in txt for k in keywords)


# ------------------------------------------------------------
# Build prompt for non-Christian geography teaching
# (NO bullets — ONLY paragraphs)
# ------------------------------------------------------------
def build_geography_prompt(topic: str, grade: str):
    return f"""
You are a gentle geography tutor for a grade {grade} student.

The student asked about:
\"{topic}\"

Use the SIX-section CozmicLearning structure.
NO bullet points allowed. Only short paragraphs.
IMPORTANT GUARDRAILS:
- Teach full, age-appropriate geographic facts and established knowledge.
- Root framing in Christian virtues: stewardship, compassion, cultural respect, creation care.
- Present factual geographic information (locations, cultures, physical features, systems).
- Encourage appreciation for God's creation and diverse cultures.
- Keep tone respectful and focused on understanding our world.

SECTION 1 — OVERVIEW
Explain the geographic topic in 2–3 short, calm sentences.

SECTION 2 — KEY FACTS
Describe the important geographic details: where it is, what makes it unique,
key features, climate, or cultural aspects using a small paragraph.

SECTION 3 — CHRISTIAN VIEW
Explain softly how Christians see geography through the lens of
creation care, cultural appreciation, and stewardship of the earth.
Connect to biblical themes of caring for God's creation when appropriate.

SECTION 4 — AGREEMENT
Explain in a short paragraph what nearly all people agree on about
this geographic topic such as physical facts, locations, and basic cultural information.

SECTION 5 — DIFFERENCE
Explain gently how a Christian worldview may interpret the purpose or
meaning of geography differently from a purely secular view, using simple, respectful language.

SECTION 6 — PRACTICE
Ask 2–3 tiny reflection questions and include short example answers.
Write them as tiny sentences, not bullet points.
"""


# ------------------------------------------------------------
# Build prompt for Christian-directed questions
# ------------------------------------------------------------
def build_christian_geography_prompt(topic: str, grade: str):
    return f"""
The student asked this geography question from a Christian perspective:

\"{topic}\"

Use the SIX-section CozmicLearning structure.
NO bullet points.
IMPORTANT GUARDRAILS:
- Teach full, age-appropriate geographic facts without omitting established knowledge.
- Frame learning in Christian virtues: stewardship, cultural respect, creation care, compassion.
- Present factual geographic information rooted in a Biblical worldview.
- Encourage appreciation for God's diverse creation and people.

SECTION 1 — OVERVIEW
Explain the topic slowly and clearly in 2–3 gentle sentences.

SECTION 2 — KEY FACTS
Describe the basic geographic details in a short paragraph.

SECTION 3 — CHRISTIAN VIEW
Explain softly how Christians understand geography through the lens of
creation care, cultural appreciation, and stewardship.
Include one short Scripture reference or theme when appropriate (Psalm 24:1, Genesis 1-2).

SECTION 4 — AGREEMENT
Explain what people from any worldview usually agree on about the geographic topic.

SECTION 5 — DIFFERENCE
Explain kindly how interpretations of geography's meaning or
purpose may differ between Christian and secular perspectives.

SECTION 6 — PRACTICE
Ask 2–3 reflection questions with tiny example answers using short sentences.
"""


# ------------------------------------------------------------
# MAIN GEOGRAPHY EXPLAINER — STANDARDIZED FOR ALL SUBJECTS
# ------------------------------------------------------------
def explain_geography(topic: str, grade_level="8", character="nova"):

    if is_christian_question(topic):
        base_prompt = build_christian_geography_prompt(topic, grade_level)
    else:
        base_prompt = build_geography_prompt(topic, grade_level)

    enriched = apply_personality(character, base_prompt)
    raw = study_buddy_ai(enriched, grade_level, character)

    sections = parse_into_sections(raw)

    return format_answer(
        overview=sections.get("overview", ""),
        key_facts=sections.get("key_facts", []),
        christian_view=sections.get("christian_view", ""),
        agreement=sections.get("agreement", []),
        difference=sections.get("difference", []),
        practice=sections.get("practice", []),
        raw_text=raw
    )


# ------------------------------------------------------------
# SIMPLE GEOGRAPHY QUESTION
# ------------------------------------------------------------
def answer_geography_question(question: str, grade_level="8", character="nova"):

    base_prompt = build_geography_prompt(question, grade_level)
    enriched = apply_personality(character, base_prompt)
    raw = study_buddy_ai(enriched, grade_level, character)

    sections = parse_into_sections(raw)

    return format_answer(
        overview=sections.get("overview", ""),
        key_facts=sections.get("key_facts", []),
        christian_view=sections.get("christian_view", ""),
        agreement=sections.get("agreement", []),
        difference=sections.get("difference", []),
        practice=sections.get("practice", []),
        raw_text=raw
    )


# ------------------------------------------------------------
# GEOGRAPHY QUIZ — STILL 6 SECTIONS, NO BULLETS
# ------------------------------------------------------------
def generate_geography_quiz(topic: str, grade_level="8", character="nova"):

    prompt = f"""
Create a gentle geography quiz for a grade {grade_level} student.

Topic: \"{topic}\"

Use the SIX-section CozmicLearning format.
NO bullet points.

SECTION 1 — OVERVIEW
Give a soft introduction in a small paragraph.

SECTION 2 — KEY FACTS
Explain the main geographic concepts students should remember
in a short, simple paragraph.

SECTION 3 — CHRISTIAN VIEW
Explain softly how Christians might think about creation care and
cultural appreciation related to this geographic topic.

SECTION 4 — AGREEMENT
Describe in a short paragraph what nearly everyone agrees on.

SECTION 5 — DIFFERENCE
Explain kindly how interpretations may differ.

SECTION 6 — PRACTICE
Write a few tiny quiz questions with short example answers.
No bullets, only paragraph sentences.
"""

    enriched = apply_personality(character, prompt)
    raw = study_buddy_ai(enriched, grade_level, character)
    sections = parse_into_sections(raw)

    return format_answer(
        overview=sections.get("overview", ""),
        key_facts=sections.get("key_facts", []),
        christian_view=sections.get("christian_view", ""),
        agreement=sections.get("agreement", []),
        difference=sections.get("difference", []),
        practice=sections.get("practice", []),
        raw_text=raw
    )
