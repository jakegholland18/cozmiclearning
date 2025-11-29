from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality
from modules.answer_formatter import format_answer


# -----------------------------------------------------------
# Detect Christian-related question
# -----------------------------------------------------------
def is_christian_question(text: str) -> bool:
    keywords = [
        "Christian", "Christianity", "God", "Jesus", "Bible",
        "biblical", "faith", "Christian perspective",
        "how does this relate to Christianity",
        "how does this relate to God"
    ]
    return any(k.lower() in text.lower() for k in keywords)


# -----------------------------------------------------------
# Main structured math explanation generator
# -----------------------------------------------------------
def explain_math(question: str, grade_level="5", character="everly"):
    """
    Creates a simplified, section-based math explanation.
    Returns a dictionary using the new structured format.
    """

    # Christian worldview (optional section)
    christian_requested = is_christian_question(question)

    # Build the AI prompt
    prompt = f"""
You are a warm, friendly math tutor for a grade {grade_level} student.

The student asked:
"{question}"

Provide the answer in SIX SHORT SECTIONS, each written in simple kid-friendly language:

1. OVERVIEW — Explain the idea in 3–4 kid-friendly sentences.
2. KEY FACTS — 3–5 important truths or simple rules they should know.
3. CHRISTIAN VIEW — If Christianity is relevant, gently explain how Christians may see order and logic in math. If not relevant, say "This math topic doesn't have a direct Christian teaching, but some Christians appreciate how math shows order in creation."
4. AGREEMENT — Show how Christians + non-Christians would understand the *same math* the same way.
5. DIFFERENCE — A very small note if worldview affects how math is understood (usually it doesn’t).
6. PRACTICE — Give 2 practice questions + short answers.

Write everything in soft, simple language for children.
Avoid jargon unless you explain it.
Keep sections short and not overwhelming.
"""

    # Apply personality
    prompt = apply_personality(character, prompt)

    # Get AI response
    raw = study_buddy_ai(prompt, grade_level, character)

    # -------------------------------------------------------
    # Split AI response into the six final sections
    # -------------------------------------------------------
    def extract(label):
        start = raw.find(label)
        if start == -1:
            return "Not available."
        start += len(label)
        end = raw.find("\n", start)
        return raw[start:].strip()

    overview = extract("1. OVERVIEW")
    key_facts = extract("2. KEY FACTS")
    christian_view = extract("3. CHRISTIAN VIEW")
    agreement = extract("4. AGREEMENT")
    difference = extract("5. DIFFERENCE")
    practice = extract("6. PRACTICE")

    # PACKAGE THE STRUCTURED RESULT
    return format_answer(
        overview=overview,
        key_facts=key_facts,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )



