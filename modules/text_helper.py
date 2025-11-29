# modules/text_helper.py

from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality


# -------------------------------------------------------
# Detect Christian-oriented questions
# -------------------------------------------------------
def is_christian_question(text: str) -> bool:
    keywords = [
        "christian", "christianity", "bible", "god", "jesus",
        "faith", "biblical", "christian perspective"
    ]
    return any(k.lower() in text.lower() for k in keywords)


# -------------------------------------------------------
# Build summary prompt using the new 6-section format
# -------------------------------------------------------
def build_summary_prompt(text: str, grade_level: str):
    return f"""
Summarize and explain this reading passage in the new 6-section Homework Buddy format:

{text}

Make OVERVIEW and KEY FACTS very simple.
In the CHRISTIAN VIEW and AGREEMENT/DISAGREEMENT sections, keep the ideas gentle.
In the PRACTICE section, include 2–3 small questions the student could answer.
"""


# -------------------------------------------------------
# Build reading comprehension prompt
# -------------------------------------------------------
def build_comprehension_prompt(question: str, passage: str, grade_level: str):
    return f"""
The student needs help with a reading comprehension question.

Passage:
{passage}

Question:
{question}

Explain the answer using the 6-section Homework Buddy structure.
Keep everything extremely simple and kid-friendly.
In PRACTICE, include one small comprehension question they can try.
"""


# -------------------------------------------------------
# Build main idea prompt
# -------------------------------------------------------
def build_main_idea_prompt(passage: str, grade_level: str):
    return f"""
Help the student find the main idea of this passage:

{passage}

Use the 6-section structure.
Make the OVERVIEW and KEY FACTS very short and simple.
Explain clearly what the main idea is.
Add 1–2 tiny PRACTICE questions the student can answer.
"""


# -------------------------------------------------------
# Build general reading task prompt
# -------------------------------------------------------
def build_task_prompt(task: str, grade_level: str):
    return f"""
Help the student with this reading task:

{task}

Explain it using the 6-section Homework Buddy structure.
Keep everything gentle, simple, and easy for a grade {grade_level} student.
Add a short PRACTICE section at the end.
"""


# -------------------------------------------------------
# PUBLIC FUNCTIONS — NO MORE SOCRATIC LAYERS
# (the 6-section system handles structure)
# -------------------------------------------------------

def summarize_text(text: str, grade_level="8", character=None):

    if character is None:
        character = "theo"

    # Christian worldview option
    if is_christian_question(text):
        base_prompt = f"""
The student wants to understand this passage with a Christian perspective included:

{text}

Use the 6-section Homework Buddy answer structure.
Keep all sections gentle, short, and clear.
"""
    else:
        base_prompt = build_summary_prompt(text, grade_level)

    enriched = apply_personality(character, base_prompt)
    return study_buddy_ai(enriched, grade_level, character)



def reading_help(question: str, passage: str, grade_level="8", character=None):

    if character is None:
        character = "theo"

    if is_christian_question(question + " " + passage):
        base_prompt = f"""
The student wants reading help with a Christian perspective included.

Passage:
{passage}

Question:
{question}

Use the 6-section model. Keep everything warm, simple, and grade-appropriate.
"""
    else:
        base_prompt = build_comprehension_prompt(question, passage, grade_level)

    enriched = apply_personality(character, base_prompt)
    return study_buddy_ai(enriched, grade_level, character)



def find_main_idea(passage: str, grade_level="8", character=None):

    if character is None:
        character = "theo"

    if is_christian_question(passage):
        base_prompt = f"""
The student wants to find the main idea and also include a gentle Christian perspective.

Passage:
{passage}

Use the 6-section Homework Buddy structure.
Explain main idea simply and kindly.
"""
    else:
        base_prompt = build_main_idea_prompt(passage, grade_level)

    enriched = apply_personality(character, base_prompt)
    return study_buddy_ai(enriched, grade_level, character)



def help_with_reading_task(task: str, grade_level="8", character=None):

    if character is None:
        character = "theo"

    if is_christian_question(task):
        base_prompt = f"""
The student wants a Christian-friendly explanation of this reading task:

{task}

Use the 6-section Homework Buddy teaching format.
Keep everything gentle and very clear.
"""
    else:
        base_prompt = build_task_prompt(task, grade_level)

    enriched = apply_personality(character, base_prompt)
    return study_buddy_ai(enriched, grade_level, character)


