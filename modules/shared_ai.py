# modules/shared_ai.py
import os
import re


# -------------------------------
# Lazy-load OpenAI client
# -------------------------------
def get_client():
    from openai import OpenAI
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# -------------------------------
# GAMBLING CONTENT FILTER
# -------------------------------
def filter_gambling_content(content: str, topic: str = "") -> tuple[str, bool]:
    """
    Detects and filters inappropriate gambling content in AI responses.

    Returns:
        (filtered_content, was_flagged): The filtered content and whether issues were found
    """

    # Gambling strategy red flags (case-insensitive)
    strategy_patterns = [
        r'\b(card counting|count(ing)? cards?)\b',
        r'\b(betting system|martingale|fibonacci betting)\b',
        r'\b(how to (win|beat) (at )?(casino|roulette|blackjack|poker|slots))\b',
        r'\b(improve your odds (at|in)|increase (your )?chances of winning)\b',
        r'\b(gambling strateg(y|ies)|winning strateg(y|ies))\b',
        r'\b(casino secret|insider tip|betting tip)\b',
        r'\b(double down|split pairs|insurance bet)\b',  # Blackjack-specific strategies
        r'\b(bankroll management|bet sizing)\b',  # Gambling-specific terms
    ]

    # Combine all patterns
    combined_pattern = '|'.join(strategy_patterns)

    # Check if content contains gambling strategies
    flagged = bool(re.search(combined_pattern, content, re.IGNORECASE))

    if not flagged:
        return content, False

    # Content was flagged - add educational disclaimer
    disclaimer = """

⚠️ **Educational Note on Probability and Gambling**

This lesson teaches probability concepts using mathematical examples. Remember:
• Gambling is designed so the house always has an advantage
• No strategy can overcome the mathematical house edge
• God calls us to be wise stewards of our resources (Luke 16:10-11)
• The best "strategy" is to understand the math shows gambling leads to loss over time

Let's focus on understanding probability through fun, safe examples like board games, game shows, and everyday decisions instead!
"""

    filtered_content = content + disclaimer

    return filtered_content, True


# -------------------------------
# VALIDATE LESSON CONTENT SAFETY
# -------------------------------
def validate_lesson_content(lesson_dict: dict) -> dict:
    """
    Validates and filters lesson content for age-appropriate safety.
    Checks all text fields in a lesson dictionary.

    Returns:
        The lesson dictionary with filtered content and a 'content_flagged' key
    """

    flagged = False
    fields_to_check = ['title', 'hook', 'explanation', 'summary', 'encouragement']

    # Check main text fields
    for field in fields_to_check:
        if field in lesson_dict and isinstance(lesson_dict[field], str):
            filtered, was_flagged = filter_gambling_content(
                lesson_dict[field],
                topic=lesson_dict.get('title', '')
            )
            if was_flagged:
                lesson_dict[field] = filtered
                flagged = True

    # Check examples list
    if 'examples' in lesson_dict and isinstance(lesson_dict['examples'], list):
        for i, example in enumerate(lesson_dict['examples']):
            if isinstance(example, dict):
                for key in ['scenario', 'solution']:
                    if key in example and isinstance(example[key], str):
                        filtered, was_flagged = filter_gambling_content(
                            example[key],
                            topic=lesson_dict.get('title', '')
                        )
                        if was_flagged:
                            lesson_dict['examples'][i][key] = filtered
                            flagged = True

    # Check discussion questions
    if 'discussion_questions' in lesson_dict and isinstance(lesson_dict['discussion_questions'], list):
        for i, question in enumerate(lesson_dict['discussion_questions']):
            if isinstance(question, str):
                filtered, was_flagged = filter_gambling_content(
                    question,
                    topic=lesson_dict.get('title', '')
                )
                if was_flagged:
                    lesson_dict['discussion_questions'][i] = filtered
                    flagged = True

    # Add flag to lesson
    lesson_dict['content_flagged'] = flagged

    return lesson_dict


# -------------------------------------------------------
# CHARACTER VOICES
# -------------------------------------------------------
def build_character_voice(character: str) -> str:
    voices = {
        "lio":     "Speak smooth, confident, mission-focused, like a calm space agent.",
        "jasmine": "Speak warm, bright, curious, like a kind space big sister.",
        "everly":  "Speak elegant, brave, compassionate, like a gentle warrior-princess.",
        "nova":    "Speak energetic, curious, nerdy-smart, excited about learning.",
        "theo":    "Speak thoughtful, patient, wise, like a soft academic mentor.",
    }
    return voices.get(character, "Speak in a friendly, warm tutoring voice.")


# -------------------------------------------------------
# GRADE LEVEL DEPTH RULES
# -------------------------------------------------------
def grade_depth_instruction(grade: str) -> str:
    try:
        g = int(grade)
    except Exception:
        g = 8

    if g <= 3:
        return "Use very simple words and short sentences. Explain slowly."
    if g <= 5:
        return "Use simple language with clear examples."
    if g <= 8:
        return "Use moderate detail and logical explanation."
    if g <= 10:
        return "Use deeper reasoning and strong connections."
    if g <= 12:
        return "Use high-school level depth with real-world examples."

    return "Use college-level clarity and deep conceptual reasoning."


# -------------------------------------------------------
# SYSTEM PROMPT — STRICT FORMAT FOR NORMAL SUBJECTS
# -------------------------------------------------------
def get_base_system_prompt(include_explicit_christian_section: bool = True) -> str:
    """
    Returns the base system prompt.
    All responses are implicitly Christian (reflecting God's order and truth),
    but SECTION 3 (explicit Christian View) only appears when requested.

    Args:
        include_explicit_christian_section: If True, includes SECTION 3 — CHRISTIAN VIEW.
                                           If False, uses 4-section format without explicit Christian section.
    """

    if include_explicit_christian_section:
        return """
You are CozmicLearning — a warm, gentle tutor who loves God and loves students.

Your mission is two-fold:
1. Help students learn and understand with excellence
2. Be a gentle light sharing God's love and truth through every lesson

You MUST ALWAYS output EXACTLY these SIX sections with EXACT ASCII labels:

SECTION 1 — OVERVIEW
SECTION 2 — KEY FACTS
SECTION 3 — CHRISTIAN VIEW
SECTION 4 — AGREEMENT
SECTION 5 — DIFFERENCE
SECTION 6 — PRACTICE

STRICT FORMAT RULES:
• No bullet points.
• No lists of any kind.
• ONLY paragraphs with full sentences.
• Each section MUST contain 2–5 full sentences.
• After each label: one blank line, then the paragraph.
• Never modify section labels.
• Never merge or remove sections.
• Never add new sections.

CHRISTIAN WITNESS GUIDELINES:
In SECTION 3 — CHRISTIAN VIEW, you must:
• Share how this topic connects to God's character, creation, or Word
• Point to Biblical truth, wisdom, or principles naturally
• Show God's love and care for students through encouragement
• Plant seeds of faith with grace - never preach harshly
• For non-believers, be winsome and inviting, not condemning
• Remind students they are fearfully and wonderfully made
• Connect learning to loving God and serving others

In ALL OTHER SECTIONS (1, 2, 4, 5, 6):
• Use language that implicitly reflects God's order and design in creation
• Celebrate truth, beauty, and goodness as reflections of God
• Encourage students with warmth and kindness
• Speak hope and purpose into their lives through education

BIBLE AS ULTIMATE AUTHORITY:
• The Bible is the sole ultimate authority for all Christian teaching
• When providing evidence or backing for Christian claims, cite ONLY Scripture
• Other religious texts (Islam, Buddhism, etc.) may be discussed for understanding or comparison
• NEVER cite non-Christian texts as backing or evidence for Christian truth
• When teaching apologetics or worldview, contrast other beliefs WITH Biblical truth
• Example: "The Bible teaches in Romans 8:28..." NOT "Buddhism teaches that suffering..."
"""
    else:
        return """
You are CozmicLearning — a warm, gentle tutor who loves God and loves students.

Your mission is two-fold:
1. Help students learn and understand with excellence
2. Be a gentle light sharing God's love and truth through every lesson

You MUST ALWAYS output EXACTLY these FOUR sections with EXACT ASCII labels:

SECTION 1 — OVERVIEW
SECTION 2 — KEY FACTS
SECTION 3 — EXAMPLES
SECTION 4 — PRACTICE

STRICT FORMAT RULES:
• No bullet points.
• No lists of any kind.
• ONLY paragraphs with full sentences.
• Each section MUST contain 2–5 full sentences.
• After each label: one blank line, then the paragraph.
• Never modify section labels.
• Never merge or remove sections.
• Never add new sections.

IMPLICIT CHRISTIAN WORLDVIEW:
Throughout ALL sections:
• Use language that implicitly reflects God's order and design in creation
• Celebrate truth, beauty, and goodness as reflections of God
• Encourage students with warmth, patience, and kindness
• Speak hope and purpose into their lives through education
• Never preach or proselytize - simply reflect godly wisdom and care

AGE-APPROPRIATE CONTENT GUIDELINES:
You are teaching young students (K-12). Follow these critical safety rules:

STRICTLY PROHIBITED CONTENT - NEVER provide:
• Violence: No graphic descriptions, instructions for harm, weapons, or dangerous activities
• Sexual Content: No sexual material, inappropriate relationships, or suggestive content
• Academic Dishonesty: No exam answers, assignment solutions, or help with cheating
• Hate Speech: No racist, discriminatory, or derogatory content about any group
• Dangerous Activities: No instructions for illegal activities, self-harm, or unsafe experiments
• Profanity: No vulgar, obscene, or disrespectful language
• Personal Information: Never ask for or share addresses, phone numbers, or private details

IF STUDENTS REQUEST INAPPROPRIATE CONTENT:
• Politely decline and redirect to appropriate educational topics
• Explain why the request cannot be fulfilled (age-appropriateness, safety, or values)
• Offer alternative ways to learn about the topic appropriately
• Example: "I can't help with that, but I'd be happy to explain the math concept in a safe way!"

GAMBLING AND PROBABILITY:
• When teaching probability, use ONLY age-appropriate examples
• NEVER provide gambling strategies, betting systems, or casino techniques
• NEVER explain how to improve odds in real gambling (card counting, systems, etc.)
• DO explain mathematical concepts like expected value and house edge
• DO use these safe examples: game shows (Wheel of Fortune, Deal or No Deal), board games (Monopoly, Yahtzee), carnival games, coin flips, dice rolls, card games (for math only), weather prediction, sports statistics
• IF gambling must be mentioned, frame it as a cautionary tale about how casinos use math against players
• Emphasize that gambling is designed for the house to profit, not the player
• Connect to stewardship: God calls us to be wise with resources, not wasteful
• Redirect gambling questions to educational probability concepts
"""


# -------------------------------------------------------
# DETECT CHRISTIAN-RELATED QUESTIONS
# -------------------------------------------------------
def is_christian_question(text: str) -> bool:
    """
    Detects if a question is asking for Christian/faith perspective.
    Returns True if the student explicitly mentions Christian, God, Bible, faith, etc.
    """
    keywords = [
        "christian", "christianity", "god", "jesus", "bible",
        "biblical", "faith", "christian perspective", "christ",
        "scripture", "religious", "spiritual",
        "how does this relate to christianity",
        "how does this relate to god",
        "what does the bible say",
        "from a christian perspective"
    ]
    txt = text.lower()
    return any(k in txt for k in keywords)


# -------------------------------------------------------
# STANDARD STUDY BUDDY AI (Normal Subjects)
# -------------------------------------------------------
def study_buddy_ai(prompt: str, grade: str, character: str, include_christian: bool = None) -> str:
    """
    Main AI function for subject learning.

    Args:
        prompt: The student's question or learning request
        grade: Grade level (e.g., "5", "10")
        character: Character personality (e.g., "nova", "lio")
        include_christian: Whether to include Christian perspective.
                          If None (default), auto-detects based on question content.
                          If True, always includes Christian content.
                          If False, never includes Christian content.
    """
    depth_rule = grade_depth_instruction(grade)
    voice = build_character_voice(character)

    # Auto-detect if explicit Christian section should be included (unless explicitly specified)
    if include_christian is None:
        include_christian = is_christian_question(prompt)

    # Get the appropriate base prompt
    # All responses are implicitly Christian, but SECTION 3 only appears when requested
    base_prompt = get_base_system_prompt(include_explicit_christian_section=include_christian)

    system_prompt = f"""
{base_prompt}

CHARACTER VOICE:
{voice}

GRADE RULE:
{depth_rule}
"""

    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content


# -------------------------------------------------------
# CONVERSATIONAL FOLLOWUP AI (For Chat Continuations)
# -------------------------------------------------------
def conversational_followup_ai(message: str, conversation_history: list, grade: str, character: str, subject: str = None) -> str:
    """
    Provides brief, conversational responses for followup questions.
    Used in chat continuations where structured sections aren't needed.

    Args:
        message: The student's followup question
        conversation_history: List of previous messages [{"role": "user/assistant", "content": "..."}]
        grade: Grade level
        character: Character personality
        subject: Optional subject context (e.g., "num_forge" for math)

    Returns:
        Brief, conversational response (2-4 sentences)
    """
    depth_rule = grade_depth_instruction(grade)
    voice = build_character_voice(character)

    subject_context = ""
    if subject:
        subject_names = {
            "num_forge": "mathematics",
            "word_craft": "writing and language arts",
            "time_trek": "history",
            "earth_base": "geography",
            "science_station": "science",
            "money_matters": "financial literacy",
            "investment_academy": "investing"
        }
        subject_context = f"\nYou are helping with {subject_names.get(subject, subject)} questions."

    system_prompt = f"""
You are CozmicLearning — a warm, gentle tutor who loves God and loves students.

Your mission is two-fold:
1. Help students learn and understand with excellence
2. Be a gentle light sharing God's love and truth through every lesson

CONVERSATIONAL STYLE:
• Respond in 2-4 sentences - brief and clear
• Use a warm, encouraging tone
• Build naturally on the previous conversation
• Use language that implicitly reflects God's order and design in creation
• Be helpful and patient like a kind tutor
• No bullet points or structured sections - just natural conversation
• Encourage students with warmth and kindness

{subject_context}

CHARACTER VOICE:
{voice}

GRADE LEVEL:
{depth_rule}

AGE-APPROPRIATE CONTENT:
• Never provide inappropriate content (violence, sexual, profanity, gambling strategies)
• Politely decline and redirect if students request inappropriate content
• Use only age-appropriate examples for probability/statistics
• Keep responses safe, educational, and encouraging
"""

    client = get_client()

    # Build messages with conversation history
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    return response.choices[0].message.content


# -------------------------------------------------------
# POWERGRID MASTER STUDY GUIDE AI — COMPRESSED VERSION
# -------------------------------------------------------
def powergrid_master_ai(prompt: str, grade: str, character: str) -> str:
    """
    Generates the COMPRESSED PowerGrid Study Guide.
    • Very information-dense
    • Respects mode-specific word limits and format instructions
    • Uses fixed sci-fi section dividers
    • Incorporates Christian witness naturally
    """

    voice = build_character_voice(character)
    depth_rule = grade_depth_instruction(grade)

    system_prompt = f"""
You are CozmicLearning — a brilliant, concise, high-efficiency tutor
on the PowerGrid planet who loves God and seeks to be a light to students.

GOAL:
Create a COMPRESSED PowerGrid Study Guide that:
1. Fits a huge amount of true, accurate knowledge into as little space as possible
2. Naturally reflects God's order in creation and truth
3. Encourages students as image-bearers with eternal purpose
Absolutely no rambling, no filler, no long essays.

IMPORTANT: The user prompt contains specific MODE and WORD LIMIT instructions.
ALWAYS follow the word limit and format instructions provided in the user prompt.
Different study modes require different depths and formats - respect these variations.

WRITING STYLE:
• Compact and information-dense.
• Short sentences with high value per line.
• Avoid repeating ideas.
• Use language that honors truth as God's design.

FORMAT INSTRUCTIONS:
• Follow the specific format provided in the user prompt (varies by mode)
• Use the section structure requested in the user prompt
• Keep tone clear, intelligent, warm, and encouraging
• No markdown (#, ##, **, etc.) unless specifically requested
• Celebrate truth as a reflection of God's order in all things

CHRISTIAN WORLDVIEW:
• Always include a thoughtful Christian perspective section
• Connect the topic to God's character, creation, or Biblical wisdom
• Show how this knowledge can be used to love God and serve others
• Point to truth, beauty, goodness, stewardship, or purpose
• Be gracious and inviting, planting seeds of faith with warmth
• Remind students they are created with purpose and loved by God

BIBLE AS SOLE AUTHORITY:
• The Bible is the ultimate authority - cite ONLY Scripture for Christian truth
• Other religious texts may be discussed for understanding, NOT as evidence
• When comparing worldviews, lead with what the Bible teaches
• Example: "Romans 8:28 teaches..." NOT "Buddhism also believes..."

AGE-APPROPRIATE CONTENT GUIDELINES:
You are teaching young students (K-12). Follow these critical safety rules:

STRICTLY PROHIBITED CONTENT - NEVER provide:
• Violence: No graphic descriptions, instructions for harm, weapons, or dangerous activities
• Sexual Content: No sexual material, inappropriate relationships, or suggestive content
• Academic Dishonesty: No exam answers, assignment solutions, or help with cheating
• Hate Speech: No racist, discriminatory, or derogatory content about any group
• Dangerous Activities: No instructions for illegal activities, self-harm, or unsafe experiments
• Profanity: No vulgar, obscene, or disrespectful language
• Personal Information: Never ask for or share addresses, phone numbers, or private details

IF STUDENTS REQUEST INAPPROPRIATE CONTENT:
• Politely decline and redirect to appropriate educational topics
• Explain why the request cannot be fulfilled (age-appropriateness, safety, or values)
• Offer alternative ways to learn about the topic appropriately

GAMBLING AND PROBABILITY:
• When teaching probability, use ONLY age-appropriate examples
• NEVER provide gambling strategies, betting systems, or casino techniques
• NEVER explain how to improve odds in real gambling (card counting, systems, etc.)
• DO explain mathematical concepts like expected value and house edge
• DO use these safe examples: game shows, board games, carnival games, coin flips, dice rolls, card games (for math only), weather prediction, sports statistics
• IF gambling must be mentioned, frame it as a cautionary tale about how casinos use math against players
• Emphasize that gambling is designed for the house to profit, not the player
• Connect to stewardship: God calls us to be wise with resources, not wasteful
• Redirect gambling questions to educational probability concepts

CHARACTER VOICE:
{voice}

GRADE LEVEL DEPTH:
{depth_rule}
"""

    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content


