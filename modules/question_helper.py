# modules/question_helper.py

from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality
from modules.answer_formatter import format_answer


# -------------------------------------------------------
# Detect if student wants Christian perspective
# -------------------------------------------------------
def is_christian_question(text: str) -> bool:
    keywords = [
        "christian", "christianity", "jesus", "god", "faith",
        "biblical", "bible", "how does this relate to god",
        "from a christian perspective", "christian worldview"
    ]
    return any(k.lower() in text.lower() for k in keywords)


# -------------------------------------------------------
# Build 6-section prompt (general question)
# -------------------------------------------------------
def build_general_prompt(question: str, grade_level: str):
    return f"""
You are a gentle teacher for a grade {grade_level} student.

The student asked:
"{question}"

Answer using SIX child-friendly sections.

SECTION 1 — OVERVIEW  
Explain the topic in 3–4 very simple sentences using everyday language.

SECTION 2 — KEY FACTS  
Share a few important ideas about how this works in real life  
(keep sentences short, soft, and warm).

SECTION 3 — CHRISTIAN VIEW  
If the topic has moral or worldview elements, gently explain  
how many Christians think about it  
(kindness, honesty, purpose, design, wisdom).  
If the topic isn’t naturally Christian, still explain how Christians  
look for meaning, responsibility, or gratitude in learning.

SECTION 4 — AGREEMENT  
Explain what people of ANY worldview agree on  
(common sense facts, science basics, kindness, cause & effect).

SECTION 5 — DIFFERENCE  
Explain gently where a Christian worldview might add  
a different motivation or meaning  
(hope, purpose, responsibility, compassion, stewardship).

SECTION 6 — PRACTICE  
Ask 2–3 child-friendly reflection questions  
and give short example answers in simple wording.

Do not use lists or bullet symbols.  
Keep everything calm, slow, and spoken-like.
"""


# -------------------------------------------------------
# Build 6-section prompt (Christian question)
# -------------------------------------------------------
def build_christian_prompt(question: str, grade_level: str):
    return f"""
The student asked from a Christian perspective:

"{question}"

Answer using SIX warm, simple sections.

SECTION 1 — OVERVIEW  
Explain what the question means in simple, everyday language.

SECTION 2 — KEY FACTS  
Share the important ideas Christians consider  
(meaning, purpose, morality, creation, choices, wisdom).

SECTION 3 — CHRISTIAN VIEW  
Explain gently how many Christians understand this topic  
using Scripture softly if relevant.  
Keep the tone calm, slow, and age-appropriate.

SECTION 4 — AGREEMENT  
Explain what Christians and non-Christians often agree on  
(kindness, truthfulness, learning from mistakes, curiosity).

SECTION 5 — DIFFERENCE  
Explain kindly how Christian beliefs may add a different  
motivation or meaning behind actions or ideas.

SECTION 6 — PRACTICE  
Ask 2–3 reflection questions  
and then give short example answers  
to help them think.

No lists, no bullets, no intense language.  
Just gentle conversation.
"""


# -------------------------------------------------------
# Main Public Function — uses formatter.py
# -------------------------------------------------------
def answer_question(question: str, grade_level="8", character="everly"):

    # Choose which 6-section format to use
    if is_christian_question(question):
        prompt = build_christian_prompt(question, grade_level)
    else:
        prompt = build_general_prompt(question, grade_level)

    # Apply personality
    prompt = apply_personality(character, prompt)

    # Get AI output
    raw = study_buddy_ai(prompt, grade_level, character)

    # Helper to extract each labeled section
    def extract(label):
        return raw.split(label)[-1].strip() if label in raw else "No information provided."

    overview       = extract("SECTION 1")
    key_facts      = extract("SECTION 2")
    christian_view = extract("SECTION 3")
    agreement      = extract("SECTION 4")
    difference     = extract("SECTION 5")
    practice       = extract("SECTION 6")

    # Format using your kid-friendly answer HTML generator
    return format_answer(
        overview=overview,
        key_facts=key_facts,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )
