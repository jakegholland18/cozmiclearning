from modules.shared_ai import study_buddy_ai
from modules.personality_helper import apply_personality
from modules.answer_formatter import format_answer


# ------------------------------------------------------------
# Detect whether the question is Christian / Bible-related
# ------------------------------------------------------------
def is_christian_request(text: str) -> bool:
    keywords = [
        "bible", "jesus", "god", "christian", "faith", "scripture",
        "christianity", "biblical", "verse",
        "how does this relate to god", "what does this mean biblically"
    ]
    return any(k.lower() in text.lower() for k in keywords)


# ------------------------------------------------------------
# MAIN BIBLE LESSON — structured into 6 kid-friendly sections
# ------------------------------------------------------------
def bible_lesson(topic: str, grade_level="8", character="everly"):
    """
    Explains any Bible topic using the 6-section, child-friendly format:
    overview, key ideas, Christian view, agreement, difference, practice.
    """

    # Build structured tutoring prompt
    prompt = f"""
You are a gentle Christian Bible tutor teaching a grade {grade_level} student.

The student asked a Bible-related question:
"{topic}"

Answer using SIX small, easy-to-read sections.

SECTION 1 — OVERVIEW  
Explain in 3–4 short sentences what this topic or question is really about.

SECTION 2 — KEY IDEAS  
Explain 3–5 simple ideas Christians usually believe about this topic.  
Use very simple sentences.

SECTION 3 — CHRISTIAN VIEW  
Explain gently what Christians believe, why they believe it,
and how they see this truth connecting to everyday life or God's character.
You may mention Scripture softly and naturally.

SECTION 4 — AGREEMENT  
Share what Christians and non-Christians might both agree on
(or what anyone could notice about the topic).

SECTION 5 — DIFFERENCE  
Share kindly how Christian and secular worldviews might see the topic differently,
without arguing or sounding harsh.
Keep it extremely respectful and warm.

SECTION 6 — PRACTICE  
Ask 2–3 simple reflection questions  
and give very short example answers.

Tone must be:
calm, friendly, encouraging,
simple enough for a grade {grade_level} student,
and never preachy or forceful.
"""

    # Apply character personality
    prompt = apply_personality(character, prompt)

    # Get raw AI response
    raw = study_buddy_ai(prompt, grade_level, character)

    # Helper to safely extract sections
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

    # Convert into HTML sections
    return format_answer(
        overview=overview,
        key_facts=key_ideas,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )


# ------------------------------------------------------------
# EXPLAIN A VERSE — same 6-section structure
# ------------------------------------------------------------
def explain_verse(reference: str, text: str, grade_level="8", character="everly"):

    verse_question = f"What does {reference} mean? The verse says: {text}"

    prompt = f"""
You are a gentle Bible tutor helping a grade {grade_level} student.

The student asked:
"{verse_question}"

Answer using SIX small, easy-to-read sections.

SECTION 1 — OVERVIEW  
Explain simply what this verse is about.

SECTION 2 — KEY IDEAS  
Explain 3–5 simple points Christians often take from this verse.

SECTION 3 — CHRISTIAN VIEW  
Gently explain what Christians believe the verse teaches
and how it encourages them.

SECTION 4 — AGREEMENT  
Explain what people of any worldview might agree on.

SECTION 5 — DIFFERENCE  
Explain kindly how Christian and secular views may differ,
but keep it peaceful and respectful.

SECTION 6 — PRACTICE  
Ask 2–3 reflection questions  
and give short example answers.

Keep tone warm, calm, simple.
"""

    prompt = apply_personality(character, prompt)
    raw = study_buddy_ai(prompt, grade_level, character)

    def extract(label):
        if label not in raw:
            return "Not available."
        return raw.split(label)[-1].strip()

    overview = extract("SECTION 1")
    key_ideas = extract("SECTION 2")
    christian_view = extract("SECTION 3")
    agreement = extract("SECTION 4")
    difference = extract("SECTION 5")
    practice = extract("SECTION 6")

    return format_answer(
        overview=overview,
        key_facts=key_ideas,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )


# ------------------------------------------------------------
# BIBLE STORY — same structured format
# ------------------------------------------------------------
def explain_bible_story(story: str, grade_level="8", character="everly"):

    prompt = f"""
You are a gentle Bible tutor teaching a grade {grade_level} student.

Tell the student the story of:
"{story}"

Then explain it using SIX small sections.

SECTION 1 — OVERVIEW  
Retell the story in simple language.

SECTION 2 — KEY IDEAS  
Explain 3–5 simple truths Christians learn from this story.

SECTION 3 — CHRISTIAN VIEW  
Explain why Christians believe the story matters
and what they think God is teaching.

SECTION 4 — AGREEMENT  
Explain what anyone could notice about the story.

SECTION 5 — DIFFERENCE  
Explain how Christian and secular interpretations might differ,
kindly and gently.

SECTION 6 — PRACTICE  
Ask 2–3 short reflection questions  
with simple example answers.

Tone: warm, kid-friendly, calm.
"""

    prompt = apply_personality(character, prompt)
    raw = study_buddy_ai(prompt, grade_level, character)

    def extract(label):
        if label not in raw:
            return "Not available."
        return raw.split(label)[-1].strip()

    overview = extract("SECTION 1")
    key_ideas = extract("SECTION 2")
    christian_view = extract("SECTION 3")
    agreement = extract("SECTION 4")
    difference = extract("SECTION 5")
    practice = extract("SECTION 6")

    return format_answer(
        overview=overview,
        key_facts=key_ideas,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )


# ------------------------------------------------------------
# CHRISTIAN WORLDVIEW — general questions
# ------------------------------------------------------------
def christian_worldview(question: str, grade_level="8", character="everly"):

    prompt = f"""
You are a gentle Christian worldview tutor teaching a grade {grade_level} student.

The student asked:
"{question}"

Answer using SIX friendly sections
(overview, key ideas, Christian view, agreement, difference, practice).

Use very soft, child-friendly language.
Avoid debate style.
Keep everything comforting, respectful, and simple.
"""

    prompt = apply_personality(character, prompt)
    raw = study_buddy_ai(prompt, grade_level, character)

    def extract(label):
        if label not in raw:
            return "Not available."
        return raw.split(label)[-1].strip()

    overview = extract("SECTION 1")
    key_ideas = extract("SECTION 2")
    christian_view = extract("SECTION 3")
    agreement = extract("SECTION 4")
    difference = extract("SECTION 5")
    practice = extract("SECTION 6")

    return format_answer(
        overview=overview,
        key_facts=key_ideas,
        christian_view=christian_view,
        agreement=agreement,
        difference=difference,
        practice=practice
    )
