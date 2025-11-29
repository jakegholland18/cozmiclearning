# modules/history_helper.py

from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality
from modules.answer_formatter import format_answer


# ------------------------------------------------------------
# Detect Christian-worldview history questions
# ------------------------------------------------------------
def is_christian_question(text: str) -> bool:
    keywords = [
        "christian", "christianity", "god", "jesus", "bible", "biblical",
        "faith", "christian worldview", "from a christian perspective",
        "how does this relate to christianity", "how does this relate to god"
    ]
    return any(k.lower() in text.lower() for k in keywords)


# ------------------------------------------------------------
# GRADE-LEVEL TOPIC GUIDE
# ------------------------------------------------------------
HISTORY_TOPICS = {
    "1": ["families", "communities", "holidays", "basic timelines"],
    "2": ["local history", "famous americans", "geography basics"],
    "3": ["early american history", "native cultures", "maps", "civics"],
    "4": ["state history", "colonial times", "revolutions"],
    "5": ["us history overview", "exploration", "founding documents"],
    "6": ["ancient civilizations", "world religions overview", "government basics"],
    "7": ["middle ages", "renaissance", "exploration"],
    "8": ["constitution", "american gov.", "civil war", "industrial era"],
    "9": ["world history", "ancient to medieval", "global empires"],
    "10": ["modern world", "world wars", "global conflicts"],
    "11": ["us history", "government systems", "civil rights"],
    "12": ["economics", "modern issues", "civics advanced"]
}


# ------------------------------------------------------------
# MAIN HISTORY EXPLAINER — 6 SECTIONS
# ------------------------------------------------------------
def explain_history(topic: str, grade_level="8", character="everly"):
    """
    Explains any history topic using 6 small sections:
    overview, key facts, Christian view, agreement, difference, practice.
    """

    christian = is_christian_question(topic)

    prompt = f"""
You are a gentle history tutor for a grade {grade_level} student.

The student asked about:
"{topic}"

Answer using SIX very simple sections.

SECTION 1 — OVERVIEW  
Explain the topic in 3–4 short sentences without overwhelming them.

SECTION 2 — KEY FACTS  
Give 3–5 simple, kid-friendly facts about this topic.
Keep sentences short.

SECTION 3 — CHRISTIAN VIEW  
If the student wants a Christian perspective, explain gently how many Christians
see this historical event in terms of human choices, right/wrong, and God's
long-term plan. Keep it calm and non-forceful.
If not, simply say how Christians might understand the moral lessons involved.

SECTION 4 — AGREEMENT  
Explain what people of any worldview might agree on
(e.g., what happened, cause/effect, lessons about human behavior).

SECTION 5 — DIFFERENCE  
Explain softly how Christian and secular worldviews may interpret the event differently,
but stay very respectful and simple.

SECTION 6 — PRACTICE  
Ask 2–3 reflection questions and provide short example answers.

Tone must be:
calm, friendly, gentle, non-dramatic, and perfect for kids.

Grade-level guidance:
{", ".join(HISTORY_TOPICS.get(str(grade_level), []))}
"""

    # Apply character personality
    prompt = apply_personality(character, prompt)

    # Get raw AI output
    raw = study_buddy_ai(prompt, grade_level, character)

    # Helper to extract sections safely
    def extract(label):
        if label not in raw:
            return "Not available."
        return raw.split(label)[-1].strip()

    overview = extract("SECTION 1")
    key_facts = extract("SECTION 2")
    christian_view = extract("SECTION 3")
    agreement = extract("SECTION 4")
    difference = extract("SECTION 5")
    practice = extract("SECTION 6")

    # Final formatting for answer.html
    return format_answer(
        overview=overview,
        key_facts=key_facts,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )


# ------------------------------------------------------------
# GENERAL HISTORY QUESTION — SAME FORMAT
# ------------------------------------------------------------
def answer_history_question(question: str, grade_level="8", character="everly"):

    prompt = f"""
You are a kind and gentle history tutor for a grade {grade_level} student.

The student asked:
"{question}"

Answer using SIX very small sections:

SECTION 1 — OVERVIEW  
Restate the question's topic in simple terms.

SECTION 2 — KEY FACTS  
Explain 3–5 easy facts that help answer the question.

SECTION 3 — CHRISTIAN VIEW  
Explain softly how Christians might see moral lessons, human behavior,
or God's larger plan in history.

SECTION 4 — AGREEMENT  
Explain what people of any worldview typically agree on.

SECTION 5 — DIFFERENCE  
Explain respectfully how Christian and secular interpretations differ.

SECTION 6 — PRACTICE  
Ask 2–3 kid-friendly reflection questions with sample answers.

Tone: calm, friendly, simple.
"""

    prompt = apply_personality(character, prompt)
    raw = study_buddy_ai(prompt, grade_level, character)

    def extract(label):
        if label not in raw:
            return "Not available."
        return raw.split(label)[-1].strip()

    overview = extract("SECTION 1")
    key_facts = extract("SECTION 2")
    christian_view = extract("SECTION 3")
    agreement = extract("SECTION 4")
    difference = extract("SECTION 5")
    practice = extract("SECTION 6")

    return format_answer(
        overview=overview,
        key_facts=key_facts,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )


# ------------------------------------------------------------
# HISTORY QUIZ — works with new format
# ------------------------------------------------------------
def generate_history_quiz(topic: str, grade_level="8", character="everly"):

    prompt = f"""
Create a gentle, kid-friendly history quiz for a grade {grade_level} student.

Topic: "{topic}"

Use SIX SECTIONS:

SECTION 1 — OVERVIEW  
Short explanation of the topic.

SECTION 2 — KEY FACTS  
3–5 simple facts to help them remember.

SECTION 3 — CHRISTIAN VIEW  
Soft explanation of how Christians see lessons about choices, morality, or character.

SECTION 4 — AGREEMENT  
Common ground people agree on.

SECTION 5 — DIFFERENCE  
Respectful explanation of different interpretations.

SECTION 6 — PRACTICE  
Write 5 quiz questions and then the answer key.

Keep the tone warm, calm, and not dramatic.
"""

    prompt = apply_personality(character, prompt)
    raw = study_buddy_ai(prompt, grade_level, character)

    def extract(label):
        if label not in raw:
            return "Not available."
        return raw.split(label)[-1].strip()

    overview = extract("SECTION 1")
    key_facts = extract("SECTION 2")
    christian_view = extract("SECTION 3")
    agreement = extract("SECTION 4")
    difference = extract("SECTION 5")
    practice = extract("SECTION 6")

    return format_answer(
        overview=overview,
        key_facts=key_facts,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )


