from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality
from modules.answer_formatter import format_answer


# -----------------------------------------------------------
# STRUCTURED APOLOGETICS RESPONSE
# -----------------------------------------------------------
def apologetics_answer(question: str, grade_level="8", character="everly"):
    """
    Creates a structured, gentle apologetics explanation using
    the same 6-section child-friendly format as all other helpers.
    """

    # Build the structured tutoring prompt
    prompt = f"""
You are a warm, gentle Christian apologetics tutor teaching a grade {grade_level} student.

The student asked:
"{question}"

Provide the answer in SIX SHORT SECTIONS.
Use simple, comforting language suitable for kids.

SECTION 1 — OVERVIEW  
Give a simple explanation in 3–4 sentences about what the question is *really about*.

SECTION 2 — KEY IDEAS  
Explain 3–5 important points Christians believe about this topic.  
Use very simple sentences.

SECTION 3 — CHRISTIAN VIEW  
Explain kindly what Christians believe and *why* they find these beliefs meaningful.  
You may mention Scripture gently.  
Keep it short.

SECTION 4 — AGREEMENT  
Explain what Christians and non-Christians would both agree on.

SECTION 5 — DIFFERENCE  
Explain how Christian and secular worldviews might see the topic differently,  
but keep the tone respectful, gentle, and kind.

SECTION 6 — PRACTICE  
Ask 2–3 simple reflection questions the child can think about  
(“Why do people ask this?” “What do you think…?” etc).  
Then give very short sample answers.

Avoid debate language.  
Stay kind, respectful, and simple.
"""

    # Apply personality voice
    prompt = apply_personality(character, prompt)

    # Get raw AI response
    raw = study_buddy_ai(prompt, grade_level, character)

    # -------------------------------------------------------
    # Extract sections from raw text
    # -------------------------------------------------------
    def extract(label):
        if label not in raw:
            return "Not available."
        start = raw.find(label) + len(label)
        return raw[start:].strip()

    overview = extract("SECTION 1")
    key_ideas = extract("SECTION 2")
    christian_view = extract("SECTION 3")
    agreement = extract("SECTION 4")
    difference = extract("SECTION 5")
    practice = extract("SECTION 6")

    # Package it for the answer page
    return format_answer(
        overview=overview,
        key_facts=key_ideas,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )
