# modules/writing_helper.py

from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality


# -------------------------------------------------------
# Detect Christian-oriented writing questions
# -------------------------------------------------------
def is_christian_question(text: str) -> bool:
    keywords = [
        "christian", "christianity", "god", "jesus",
        "bible", "faith", "biblical",
        "from a christian perspective",
        "christian worldview",
        "how does this relate to christianity",
        "how does this relate to god"
    ]
    return any(k.lower() in text.lower() for k in keywords)


# -------------------------------------------------------
# Build prompt for writing skill using new 6-section format
# -------------------------------------------------------
def build_writing_skill_prompt(topic: str, grade_level: str):
    return f"""
Teach the writing skill "{topic}" using the 6-section Homework Buddy format.

Make OVERVIEW and KEY FACTS very simple.
Explain the writing idea clearly, with one calm example.
Keep everything friendly and easy for grade {grade_level}.
"""


# -------------------------------------------------------
# Build prompt for a writing task using the new format
# -------------------------------------------------------
def build_writing_task_prompt(task: str, grade_level: str):
    return f"""
Help the student complete this writing task:

{task}

Explain it using the 6-section Homework Buddy answer format.
Keep the ideas clear and the examples small and simple.
"""


# -------------------------------------------------------
# Build prompt for editing text using the new format
# -------------------------------------------------------
def build_editing_prompt(text: str, grade_level: str):
    return f"""
Improve this piece of student writing:

{text}

Use the 6-section Homework Buddy format.
Explain improvements gently with simple, encouraging wording.
"""


# -------------------------------------------------------
# Build prompt for creative writing using new format
# -------------------------------------------------------
def build_creative_prompt(prompt_text: str, grade_level: str):
    return f"""
Create a gentle creative story based on this prompt:

{prompt_text}

Use the 6-section Homework Buddy answer format.
Keep the tone warm, calm, and age-appropriate.
"""


# -------------------------------------------------------
# PUBLIC FUNCTIONS — NO MORE SOCRATIC LAYERS
# -------------------------------------------------------

def explain_writing(topic: str, grade_level="8", character=None):
    """
    Explains a writing skill using the Homework Buddy 6-section format.
    """

    if character is None:
        character = "theo"

    if is_christian_question(topic):
        base_prompt = f"""
Explain the writing topic "{topic}" and include a gentle Christian viewpoint.

Use the 6-section Homework Buddy answer format.
Keep the tone warm and simple for a grade {grade_level} student.
"""
    else:
        base_prompt = build_writing_skill_prompt(topic, grade_level)

    enriched = apply_personality(character, base_prompt)
    return study_buddy_ai(enriched, grade_level, character)



def help_write(task: str, grade_level="8", character=None):
    """
    Helps the student complete a writing assignment using the 6-section format.
    """

    if character is None:
        character = "theo"

    if is_christian_question(task):
        base_prompt = f"""
The student wants this writing task explained with a Christian-friendly view:

{task}

Use the 6-section Homework Buddy structure.
Be gentle and very clear.
"""
    else:
        base_prompt = build_writing_task_prompt(task, grade_level)

    enriched = apply_personality(character, base_prompt)
    return study_buddy_ai(enriched, grade_level, character)



def edit_writing(text: str, grade_level="8", character=None):
    """
    Improves the student's writing using the new 6-section structure.
    """

    if character is None:
        character = "theo"

    if is_christian_question(text):
        base_prompt = f"""
Edit this writing sample with a gentle Christian perspective:

{text}

Use the 6-section Homework Buddy format.
Make improvements clear, simple, and kind.
"""
    else:
        base_prompt = build_editing_prompt(text, grade_level)

    enriched = apply_personality(character, base_prompt)
    return study_buddy_ai(enriched, grade_level, character)



def creative_writing(prompt_text: str, grade_level="8", character=None):
    """
    Creates a gentle, age-friendly story using the 6-section format.
    """

    if character is None:
        character = "theo"

    if is_christian_question(prompt_text):
        base_prompt = f"""
Write a creative story based on this prompt with a gentle Christian viewpoint:

{prompt_text}

Use the 6-section Homework Buddy format.
Keep it calm, positive, and grade-friendly.
"""
    else:
        base_prompt = build_creative_prompt(prompt_text, grade_level)

    enriched = apply_personality(character, base_prompt)
    return study_buddy_ai(enriched, grade_level, character)


