# modules/study_helper.py

from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality


# -----------------------------------------------------------
# Build QUIZ prompt using the new 6-section structure
# -----------------------------------------------------------
def build_quiz_prompt(topic: str, grade_level: str):
    """
    Creates a quiz request using the new simplified 6-section answer model.
    The AI will still output 6 sections because of shared_ai.py.
    """

    return f"""
Create a gentle study quiz for the topic "{topic}".

Make the questions calm and short so a grade {grade_level} student can understand.
Ask simple questions the way a tutor would talk while sitting beside the student.

The 6-section structure should still be used, but the explanation in the OVERVIEW
and KEY FACTS sections should stay short and quiz-focused.

In the PRACTICE section, include a few quiz questions with short example answers.
"""


# -----------------------------------------------------------
# Build FLASHCARD prompt (6-section friendly)
# -----------------------------------------------------------
def build_flashcard_prompt(topic: str, grade_level: str):
    """
    Creates a flashcard-style study guide under the 6-section format.
    AI will still format final output using the 6 sections.
    """

    return f"""
Create simple flashcards for the topic "{topic}" 
for a grade {grade_level} student.

Each flashcard should be explained inside the 6-section structure.
Keep OVERVIEW and KEY FACTS gentle and simple.

In the PRACTICE section, show 3–5 flashcard-style Q&A pairs
spoken like a friendly tutor holding real cards.
"""


# -----------------------------------------------------------
# PUBLIC FUNCTIONS — NO MORE SOCRATIC LAYER
# (Because your new 6-section AI system handles structure)
# -----------------------------------------------------------
def generate_quiz(topic: str, grade_level="8", character=None):
    """
    Creates a gentle quiz using the new universal 6-section output.
    """

    if character is None:
        character = "theo"  # default calm teacher

    base_prompt = build_quiz_prompt(topic, grade_level)

    # Add character personality
    enriched_prompt = apply_personality(character, base_prompt)

    # Send through new 6-section study_buddy model
    return study_buddy_ai(enriched_prompt, grade_level, character)


def flashcards(topic: str, grade_level="8", character=None):
    """
    Creates flashcards using the new 6-section output.
    """

    if character is None:
        character = "theo"

    base_prompt = build_flashcard_prompt(topic, grade_level)

    enriched_prompt = apply_personality(character, base_prompt)

    return study_buddy_ai(enriched_prompt, grade_level, character)
