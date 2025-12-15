# modules/history_helper.py

from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality
from modules.answer_formatter import parse_into_sections, format_answer


# ------------------------------------------------------------
# Detect Christian-worldview history questions
# ------------------------------------------------------------
def is_christian_question(text: str) -> bool:
    keywords = [
        "christian", "christianity", "god", "jesus", "bible", "biblical",
        "faith", "christian worldview", "from a christian perspective",
        "how does this relate to christianity", "how does this relate to god"
    ]
    txt = text.lower()
    return any(k in txt for k in keywords)


# ------------------------------------------------------------
# Build prompt for non-Christian history teaching
# (NO bullets — ONLY paragraphs)
# ------------------------------------------------------------
def build_history_prompt(topic: str, grade: str):
    return f"""
You are a gentle history tutor for a grade {grade} student.

The student asked about:
\"{topic}\"

Use the SIX-section CozmicLearning structure.
NO bullet points allowed. Only short paragraphs.
IMPORTANT GUARDRAILS:
- Teach full, age-appropriate historical facts and established scholarship.
- Root framing in Christian virtues: truth, humility, justice, compassion, stewardship.
- Distinguish primary sources and observable facts from worldview-based interpretations.
- Present mainstream secular interpretations for awareness; do not endorse materialism.
- Keep tone respectful and focused on character, choices, and moral lessons.

SECTION 1 — OVERVIEW
Explain the topic in 2–3 short, calm sentences.

SECTION 2 — KEY FACTS
Describe when it happened, who was involved, and why it matters using a small paragraph.
Note where historians begin interpreting meaning beyond the facts.

SECTION 3 — CHRISTIAN VIEW
Explain softly how many Christians look at history by focusing on
choices, character, cause and effect, and moral lessons.
If Christianity is not part of the event, say Christians still
try to learn wisdom and character from history.

SECTION 4 — AGREEMENT
Explain in a short paragraph what nearly all worldviews agree on such as what happened,
causes, and basic lessons about human behavior and justice.

SECTION 5 — DIFFERENCE
Explain gently how a Christian worldview may interpret meaning or
purpose differently from a secular view, using simple, respectful language.

SECTION 6 — PRACTICE
Ask 2–3 tiny reflection questions and include short example answers.
Write them as tiny sentences, not bullet points.
"""


# ------------------------------------------------------------
# Build prompt for Christian-directed questions
# ------------------------------------------------------------
def build_christian_history_prompt(topic: str, grade: str):
    return f"""
The student asked this history question from a Christian perspective:

\"{topic}\"

Use the SIX-section CozmicLearning structure.
NO bullet points.
IMPORTANT GUARDRAILS:
- Teach full, age-appropriate historical facts without omitting established discoveries.
- Frame learning in Christian virtues and Biblical wisdom (Proverbs, Sermon on the Mount themes).
- Distinguish primary-source evidence from later interpretation.
- Present secular interpretations for awareness; remain rooted in a Biblical worldview.

SECTION 1 — OVERVIEW
Explain the topic slowly and clearly in 2–3 gentle sentences.

SECTION 2 — KEY FACTS
Describe the basic historical details in a short paragraph.

SECTION 3 — CHRISTIAN VIEW
Explain softly how Christians understand the event, focusing on
character, choices, consequences, providence, and wisdom.
Include one short Scripture reference or theme when appropriate.

SECTION 4 — AGREEMENT
Explain what people from any worldview usually agree on about the event.

SECTION 5 — DIFFERENCE
Explain kindly how interpretations of the event’s meaning or
purpose may differ between Christian and secular perspectives.

SECTION 6 — PRACTICE
Ask 2–3 reflection questions with tiny example answers using short sentences.
"""


# ------------------------------------------------------------
# MAIN HISTORY EXPLAINER — STANDARDIZED FOR ALL SUBJECTS
# ------------------------------------------------------------
def explain_history(topic: str, grade_level="8", character="nova"):

    if is_christian_question(topic):
        base_prompt = build_christian_history_prompt(topic, grade_level)
    else:
        base_prompt = build_history_prompt(topic, grade_level)

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
# SIMPLE HISTORY QUESTION
# ------------------------------------------------------------
def answer_history_question(question: str, grade_level="8", character="nova"):

    base_prompt = build_history_prompt(question, grade_level)
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
# HISTORY QUIZ — STILL 6 SECTIONS, NO BULLETS
# ------------------------------------------------------------
def generate_history_quiz(topic: str, grade_level="8", character="nova"):

    prompt = f"""
Create a gentle history quiz for a grade {grade_level} student.

Topic: \"{topic}\"

Use the SIX-section CozmicLearning format.
NO bullet points.

SECTION 1 — OVERVIEW
Give a soft introduction in a small paragraph.

SECTION 2 — KEY FACTS
Explain the main ideas students should remember
in a short, simple paragraph.

SECTION 3 — CHRISTIAN VIEW
Explain softly how Christians might think about the moral lessons
in this historical topic.

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
