# modules/investment_helper.py

from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality
from modules.answer_formatter import format_answer


# ------------------------------------------------------------
# Detect Christian worldview financial questions
# ------------------------------------------------------------
def is_christian_question(text: str) -> bool:
    keywords = [
        "christian", "biblical", "god", "jesus", "bible", "faith",
        "christian perspective", "what does the bible say",
        "christian view", "how does this relate to god"
    ]
    return any(k.lower() in text.lower() for k in keywords)


# ------------------------------------------------------------
# MAIN INVESTING TEACHER — 6 SIMPLE SECTIONS
# ------------------------------------------------------------
def explain_investing(topic: str, grade_level="8", character="everly"):

    christian = is_christian_question(topic)

    prompt = f"""
You are a gentle investing tutor for a grade {grade_level} student.

The student asked about:
"{topic}"

Answer using SIX kid-friendly sections.

SECTION 1 — OVERVIEW  
Explain the money/investing idea in 3–4 very simple sentences.

SECTION 2 — KEY FACTS  
Give 3–5 easy facts about how this topic works in real life.
Short sentences. No hard math.

SECTION 3 — CHRISTIAN VIEW  
Explain softly how many Christians think about money:
stewardship, responsibility, avoiding greed, helping others,
and honoring God with wise choices.
If the question wasn’t Christian, briefly say how faith can guide wise habits.

SECTION 4 — AGREEMENT  
Explain what people from any worldview agree on about money
(saving, spending wisely, long-term planning, risk, etc.).

SECTION 5 — DIFFERENCE  
Explain gently how Christian ideas about stewardship may differ
slightly from a secular “money first” view, in a respectful way.

SECTION 6 — PRACTICE  
Ask 2–3 simple reflection questions and give short example answers.

Tone must be:
warm, calm, friendly, non-technical, and perfect for kids.

Do NOT use lists or formatting keywords like asterisks.
Just use short paragraphs separated by spacing.
"""

    # Apply personality
    prompt = apply_personality(character, prompt)

    # Get AI output
    raw = study_buddy_ai(prompt, grade_level, character)

    # Extract helper
    def extract(label):
        return raw.split(label)[-1].strip() if label in raw else "Not available."

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
# GENERAL INVESTING QUESTION — SAME SYSTEM
# ------------------------------------------------------------
def investment_question(question: str, grade_level="8", character="everly"):

    prompt = f"""
You are a gentle investing tutor for a grade {grade_level} student.

The student asked:
"{question}"

Answer using SIX short, calm sections:

SECTION 1 — OVERVIEW  
Explain what the student is really asking in child-friendly terms.

SECTION 2 — KEY FACTS  
Give 3–5 simple facts that help explain the answer.

SECTION 3 — CHRISTIAN VIEW  
Explain softly how Christian stewardship applies to the topic.

SECTION 4 — AGREEMENT  
Explain what people of any worldview agree on about the idea.

SECTION 5 — DIFFERENCE  
Explain gently how Christian and secular perspectives may differ.

SECTION 6 — PRACTICE  
Ask 2–3 small practice questions with short answers.

Tone:
friendly, slow, not overwhelming.
"""

    prompt = apply_personality(character, prompt)
    raw = study_buddy_ai(prompt, grade_level, character)

    def extract(label):
        return raw.split(label)[-1].strip() if label in raw else "Not available."

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
# INVESTING QUIZ — STILL 6 SECTIONS FOR CONSISTENCY
# ------------------------------------------------------------
def investment_quiz(topic: str, grade_level="8", character="everly"):

    prompt = f"""
Create a warm, calm investing quiz for a grade {grade_level} student.

Topic: "{topic}"

Use SIX SECTIONS:

SECTION 1 — OVERVIEW  
Short explanation of the topic.

SECTION 2 — KEY FACTS  
3–5 easy facts they should remember.

SECTION 3 — CHRISTIAN VIEW  
Soft explanation of Christian stewardship ideas.

SECTION 4 — AGREEMENT  
Common ideas everyone agrees on.

SECTION 5 — DIFFERENCE  
Respectful comparison of viewpoints.

SECTION 6 — PRACTICE  
Write 5 quiz questions and the answer key.

Tone must stay slow, peaceful, and not technical.
"""

    prompt = apply_personality(character, prompt)
    raw = study_buddy_ai(prompt, grade_level, character)

    def extract(label):
        return raw.split(label)[-1].strip() if label in raw else "Not available."

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
