# modules/study_helper.py

from modules.shared_ai import study_buddy_ai, powergrid_master_ai, get_client
from modules.personality_helper import apply_personality
import json


# ============================================================
# DEEP STUDY CHAT FOLLOW-UP (Conversation Mode)
# ============================================================
def deep_study_chat(question, grade_level="8", character="nova"):
    """
    PowerGrid Deep Study Chat:
    Generates conversational follow-up responses
    AFTER the compressed PowerGrid study guide.
    """

    # Normalize input (string or list of turns)
    if isinstance(question, str):
        conversation = [{"role": "user", "content": question.strip()}]
    elif isinstance(question, list):
        conversation = []
        for turn in question:
            if isinstance(turn, dict):
                conversation.append({
                    "role": turn.get("role", "user"),
                    "content": str(turn.get("content", "")).strip()
                })
            else:
                conversation.append({
                    "role": "user",
                    "content": str(turn).strip()
                })
    else:
        conversation = [{"role": "user", "content": str(question)}]

    # Build readable dialogue
    dialogue_text = ""
    for turn in conversation:
        speaker = "Student" if turn["role"] == "user" else "Tutor"
        dialogue_text += f"{speaker}: {turn['content']}\n"

    # Tutor response prompt
    prompt = f"""
You are a warm, patient, expert tutor.

GRADE LEVEL: {grade_level}

Conversation so far:
{dialogue_text}

NOW RESPOND AS THE TUTOR.

RULES:
• Keep responses natural, friendly, and conversational
• Answer ONLY the student's most recent message
• No long essays
• No structured sections
• No study guide formatting
• No repeating the master study guide
• If student wants more detail, go deeper conversationally
"""

    reply = study_buddy_ai(prompt, grade_level, character)

    if isinstance(reply, dict):
        return reply.get("raw_text") or reply.get("text") or str(reply)

    return reply



# ============================================================
# OLD MASTER GUIDE (Bullet-Only) — STILL AVAILABLE
# ============================================================
def generate_master_study_guide(text, grade_level="8", character="nova"):
    """
    OLD bullet-only master guide for legacy subjects.
    """

    prompt = f"""
Create the most complete MASTER STUDY GUIDE possible.

CONTENT SOURCE:
{text}

GOALS:
• Extremely in-depth
• Beginner → expert
• Bullet points only
• Sub-bullets for detail
• Diagrams when needed
• Examples, analogies, memory tips
• Common mistakes
• Formulas when relevant

STYLE:
• Clean bullets only
• No paragraphs
• Highly structured
• Friendly tutor tone
• Grade {grade_level}

FORMAT:
• Plain text
• Very long
"""

    response = study_buddy_ai(prompt, grade_level, character)

    if isinstance(response, dict):
        return response.get("raw_text") or response.get("text") or str(response)

    return response



# ============================================================
# NEW COMPRESSED POWERGRID STUDY GUIDE (WITH MODES)
# ============================================================
def generate_powergrid_master_guide(text, grade_level="8", character="nova", mode="standard", learning_style="balanced"):
    """
    ENHANCED POWERGRID MASTER GUIDE with multiple modes and learning styles
    
    MODES:
    - quick: Brief bullet-point summary
    - standard: Balanced depth (default)
    - deep: Maximum detail and depth
    - socratic: Question-based learning
    
    LEARNING STYLES:
    - visual: Diagrams, charts, visual examples
    - auditory: Verbal explanations, rhythm, patterns
    - kinesthetic: Hands-on examples, physical analogies
    - balanced: Mix of all styles (default)
    """

    # Mode-specific adjustments
    if mode == "quick":
        word_limit = 400
        format_instructions = """
QUICK SUMMARY FORMAT:
1. KEY CONCEPT (1 sentence)
2. MAIN POINTS (5-7 bullets max)
3. ESSENTIAL FACTS (3-5 bullets)
4. QUICK EXAMPLE (1-2 sentences)
5. REMEMBER THIS (1 key takeaway)
"""
    elif mode == "deep":
        word_limit = 1800
        format_instructions = """
DEEP DIVE FORMAT:
1. COMPREHENSIVE OVERVIEW (full paragraph)
2. CORE CONCEPTS (detailed bullets with sub-points)
3. IN-DEPTH ANALYSIS (multiple paragraphs)
4. STUDY TECHNIQUES (How to master this topic effectively)
   - Memory techniques and mnemonics specific to this content
   - Recommended study schedule and review strategies
   - Active learning approaches (practice methods, self-testing)
   - Tips for long-term retention
5. REAL-WORLD CONNECTIONS (How this applies to everyday life)
   - Practical applications students encounter daily
   - Current events or modern examples
   - Career and professional connections
   - Why this matters beyond the classroom
6. EXTENSIVE EXAMPLES (3-5 detailed examples)
7. EDGE CASES & NUANCES (advanced understanding)
8. COMMON MISTAKES (detailed explanations)
9. PRACTICE PROBLEMS (with solutions)
10. CHRISTIAN WORLDVIEW (expanded perspective)

⚠️ DO NOT include ASCII art, diagrams, or visual elements - use descriptive text only!
"""
    elif mode == "socratic":
        word_limit = 1000
        format_instructions = """
SOCRATIC LEARNING FORMAT:
1. OPENING QUESTION (What do you already know about this?)
2. GUIDED QUESTIONS (5-7 questions that build understanding)
   - Each question followed by the answer
   - Questions lead student to discover concepts
3. REFLECTION QUESTIONS (How does this connect to what you know?)
4. CHALLENGE QUESTIONS (Can you apply this to...?)
5. CHRISTIAN PERSPECTIVE QUESTION (How does this relate to God's design?)
"""
    else:  # standard
        word_limit = 1000
        format_instructions = """
STANDARD FORMAT:
1. OVERVIEW (3–5 sentences)
2. CORE IDEAS (structured bullets)
3. KEY CONCEPTS (micro-paragraphs)
4. STUDY TECHNIQUES (How to master this topic)
   - Best memory techniques for this content
   - Study and review strategies
   - Active practice methods
5. REAL-WORLD CONNECTIONS (Why this matters)
   - Everyday applications
   - Real-world examples
   - Career connections
6. EXAMPLES (2-3 practical examples)
7. COMMON MISTAKES (compact bullets)
8. CHRISTIAN WORLDVIEW (1 paragraph)

⚠️ DO NOT include ASCII art, diagrams, or "VISUAL DIAGRAM" sections!
"""

    # Learning style adjustments
    style_instructions = ""
    if learning_style == "visual":
        style_instructions = """
VISUAL LEARNER EMPHASIS:
- Use spatial organization and formatting (indentation, grouping)
- Provide visual metaphors and imagery in explanations
- Use "Picture this..." prompts with concrete visual descriptions
- Describe concepts with vivid, descriptive language
- Use clear text-based organization (numbered lists, bullet points)
- ⚠️ NO ASCII diagrams or visual elements - describe visually with words!
"""
    elif learning_style == "auditory":
        style_instructions = """
AUDITORY LEARNER EMPHASIS:
- Use verbal explanations and spoken-word patterns
- Include mnemonic devices and rhythmic patterns
- "Say it aloud:" prompts
- Explain as if teaching verbally
"""
    elif learning_style == "kinesthetic":
        style_instructions = """
KINESTHETIC LEARNER EMPHASIS:
- Hands-on examples and physical analogies
- "Try this:" action-oriented prompts
- Step-by-step procedures
- Real-world applications students can do
"""
    else:  # balanced
        style_instructions = """
BALANCED APPROACH:
- Mix of visual, auditory, and kinesthetic elements
- Varied presentation styles
- Appeal to multiple learning preferences
"""

    prompt = f"""
Create a POWERGRID STUDY GUIDE.

MODE: {mode.upper()}
LEARNING STYLE: {learning_style.upper()}

CONTENT:
{text}

WORD LIMIT: {word_limit} words maximum

{format_instructions}

{style_instructions}

STYLE:
• Information-dense and efficient
• Clear, warm, intelligent tone
• Grade {grade_level}-appropriate language
• Avoid repetition
• Prioritize understanding over memorization

TONE: Warm, encouraging tutor who loves learning
"""

    response = powergrid_master_ai(prompt, grade_level, character)

    if isinstance(response, dict):
        return response.get("raw_text") or response.get("text") or str(response)

    return response

