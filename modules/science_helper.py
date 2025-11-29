# modules/science_helper.py

from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality
from modules.answer_formatter import format_answer


# -------------------------------------------------------
# Detect Christian-oriented science questions
# -------------------------------------------------------
def is_christian_question(text: str) -> bool:
    keywords = [
        "christian", "christianity", "god", "jesus", "bible",
        "biblical", "creation", "faith", "christian perspective",
        "from a christian view", "how does this relate to christianity",
        "how does this relate to god"
    ]
    return any(k.lower() in text.lower() for k in keywords)


# -------------------------------------------------------
# Build 6-section prompt (standard science question)
# -------------------------------------------------------
def build_science_prompt(topic: str, grade_level: str):
    return f"""
You are a gentle science teacher for a grade {grade_level} student.

The student asked:
"{topic}"

Write the answer using SIX very kid-friendly sections.

SECTION 1 — OVERVIEW  
Explain the science idea in 3–4 smooth, simple sentences  
using everyday language. Keep it soft and calm.

SECTION 2 — KEY FACTS  
Explain the important science ideas using slow, warm sentences  
matter, energy, organisms, ecosystems, forces, space, weather, etc.  
No bullet points. No lists. Just small, clear sentences.

SECTION 3 — CHRISTIAN VIEW  
Explain gently how many Christians see science as studying  
the order, structure, and patterns in creation.  
Do not claim the Bible teaches modern science.  
Just explain the gentle worldview piece.

SECTION 4 — AGREEMENT  
Explain what all people agree on  
(observation, evidence, experiments, nature patterns).

SECTION 5 — DIFFERENCE  
Explain kindly how a Christian worldview may add meaning  
like purpose, stewardship, responsibility, or gratitude.

SECTION 6 — PRACTICE  
Ask 2–3 kid-friendly reflection questions  
and then give simple example answers that model how to think.

No lists. No headings. Just smooth conversation.
"""


# -------------------------------------------------------
# Build 6-section prompt (Christian-directed science question)
# -------------------------------------------------------
def build_christian_science_prompt(topic: str, grade_level: str):
    return f"""
The student asked this science question from a Christian perspective:

"{topic}"

Answer using SIX warm, simple, child-friendly sections.

SECTION 1 — OVERVIEW  
Explain what the question means in very gentle language.

SECTION 2 — KEY FACTS  
Explain the important science ideas  
(observation, evidence, nature, forces, life, space, earth).

SECTION 3 — CHRISTIAN VIEW  
Explain softly how many Christians understand science  
as exploring a world with order, patterns, and consistency.  
Keep Scripture references gentle and simple, only if relevant.

SECTION 4 — AGREEMENT  
Explain what Christians and non-Christians agree on in science  
(facts, experiments, natural laws, curiosity, learning).

SECTION 5 — DIFFERENCE  
Explain kindly how Christians may add meaning  
(purpose, creation care, moral responsibility, wonder).

SECTION 6 — PRACTICE  
Ask 2–3 reflection questions and give short example answers  
appropriate for a grade {grade_level} student.

Keep everything slow, calm, and conversational.
"""


# -------------------------------------------------------
# MAIN PUBLIC FUNCTION — integrates with new formatter
# -------------------------------------------------------
def explain_science(topic: str, grade_level="8", character="everly"):
    # Choose the correct prompt format
    if is_christian_question(topic):
        prompt = build_christian_science_prompt(topic, grade_level)
    else:
        prompt = build_science_prompt(topic, grade_level)

    # Add personality wrapper
    prompt = apply_personality(character, prompt)

    # Get raw AI output
    raw = study_buddy_ai(prompt, grade_level, character)

    # Helper to slice labeled sections
    def extract(label):
        return raw.split(label)[-1].strip() if label in raw else "No information provided."

    overview       = extract("SECTION 1")
    key_facts      = extract("SECTION 2")
    christian_view = extract("SECTION 3")
    agreement      = extract("SECTION 4")
    difference     = extract("SECTION 5")
    practice       = extract("SECTION 6")

    # Format everything into the clean kid-friendly HTML structure
    return format_answer(
        overview=overview,
        key_facts=key_facts,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )
