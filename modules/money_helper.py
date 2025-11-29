# modules/money_helper.py

from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality
from modules.answer_formatter import format_answer


# ------------------------------------------------------------
# Detect Christian-oriented money questions
# ------------------------------------------------------------
def is_christian_question(text: str) -> bool:
    keywords = [
        "christian", "christianity", "bible", "jesus", "god",
        "biblical", "stewardship", "christian perspective",
        "what does the bible say", "christian worldview",
        "how does this relate to god"
    ]
    return any(k.lower() in text.lower() for k in keywords)


# ------------------------------------------------------------
# Money Teacher — 6 Simple Sections (Budgeting, Saving, Credit)
# ------------------------------------------------------------
def explain_money(topic: str, grade_level="8", character="everly"):

    christian = is_christian_question(topic)

    prompt = f"""
You are a gentle money teacher for a grade {grade_level} student.

The student asked about:
"{topic}"

Answer using SIX kid-friendly sections.

SECTION 1 — OVERVIEW
Describe the money idea in 3–4 very simple sentences.

SECTION 2 — KEY FACTS
Explain 3–5 simple facts about how this topic works in everyday life
(budgeting, saving, income, needs versus wants, interest, spending choices).

SECTION 3 — CHRISTIAN VIEW
Explain softly how many Christians see money:
stewardship, responsibility, avoiding greed, generosity, and wise planning.
If the question wasn’t Christian, still explain how faith can guide good habits.

SECTION 4 — AGREEMENT
Explain what people of any worldview agree on
(spending wisely, saving, planning, avoiding debt problems).

SECTION 5 — DIFFERENCE
Explain gently how Christian stewardship may differ
from a secular “money is the goal” view.

SECTION 6 — PRACTICE
Ask 2–3 short reflection questions
and provide brief example answers for each.

Tone must be soft, slow, gentle, and child-friendly.
No lists or bullet symbols. Just short, clear paragraphs.
"""

    # Apply personality
    prompt = apply_personality(character, prompt)

    # Get the AI response
    raw = study_buddy_ai(prompt, grade_level, character)

    # Helper to extract sections
    def extract(label):
        return raw.split(label)[-1].strip() if label in raw else "Not available."

    overview = extract("SECTION 1")
    key_facts = extract("SECTION 2")
    christian_view = extract("SECTION 3")
    agreement = extract("SECTION 4")
    difference = extract("SECTION 5")
    practice = extract("SECTION 6")

    # Format for HTML
    return format_answer(
        overview=overview,
        key_facts=key_facts,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )


# ------------------------------------------------------------
# Solve Accounting Problem — Now Uses Same 6-Section Format
# ------------------------------------------------------------
def solve_accounting_problem(problem: str, grade_level="8", character="everly"):

    prompt = f"""
You are a gentle accounting tutor for a grade {grade_level} student.

The student asked:
"{problem}"

Answer using SIX short sections.

SECTION 1 — OVERVIEW
Rephrase the accounting question in simple kid-friendly words.

SECTION 2 — KEY FACTS
Explain 3–5 simple ideas related to the problem:
assets, liabilities, expenses, revenues, debits, credits,
or whatever is appropriate.

SECTION 3 — CHRISTIAN VIEW
Softly explain how Christians view honesty, stewardship,
and responsibility in managing money.

SECTION 4 — AGREEMENT
Explain what everyone agrees on about basic accounting
(keeping track of money, being responsible, avoiding mistakes).

SECTION 5 — DIFFERENCE
Explain gently how Christian values of honesty and stewardship
can add a different motivation for financial responsibility.

SECTION 6 — PRACTICE
Walk through the steps of the accounting solution slowly,
then give 2 mini practice problems with answers.

Tone must be soft, calm, slow, and natural. No bullet points.
"""

    # Apply personality
    prompt = apply_personality(character, prompt)

    # AI Output
    raw = study_buddy_ai(prompt, grade_level, character)

    # Section extractor
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
# Money Quiz — Also in 6 Sections
# ------------------------------------------------------------
def accounting_quiz(topic: str, grade_level="8", character="everly"):

    prompt = f"""
Create a calm, gentle money quiz for grade {grade_level}.

Topic: "{topic}"

Use SIX SECTIONS:

SECTION 1 — OVERVIEW
Short explanation of the topic.

SECTION 2 — KEY FACTS
Simple facts the student should remember.

SECTION 3 — CHRISTIAN VIEW
Soft, encouraging explanation of stewardship and responsibility.

SECTION 4 — AGREEMENT
Explain what most people agree about regarding money.

SECTION 5 — DIFFERENCE
Kind comparison of Christian vs secular motivations.

SECTION 6 — PRACTICE
Write a few quiz questions and then the answer key,
both in very natural kid-friendly wording.

Tone must remain gentle, slow, and conversational.
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




