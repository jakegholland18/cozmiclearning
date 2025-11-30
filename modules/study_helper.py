# modules/study_helper.py

from modules.shared_ai import study_buddy_ai


def deep_study_chat(question, grade_level="8", character="everly"):
    """
    A robust conversational tutor for the PowerGrid planet.

    Accepts:
    • A single string (normal question)
    • A list of dict messages (full chat history)

    Returns:
    • A short conversational tutor reply (NOT a 6-section study guide)
    """

    # ============================================================
    # NORMALIZE INPUT → ALWAYS produce a list of {"role", "content"}
    # ============================================================

    if isinstance(question, str):
        # Single question: convert to a conversation
        conversation = [{"role": "user", "content": question.strip()}]

    elif isinstance(question, list):
        # Format chat history
        conversation = []
        for turn in question:
            if isinstance(turn, dict) and "content" in turn:
                conversation.append({
                    "role": turn.get("role", "user"),
                    "content": str(turn.get("content", "")).strip()
                })
            else:
                # raw string fallback
                conversation.append({
                    "role": "user",
                    "content": str(turn).strip()
                })

    else:
        conversation = [{"role": "user", "content": str(question)}]

    # ============================================================
    # BUILD NATURAL LANGUAGE DIALOGUE CONTEXT
    # ============================================================

    dialogue_text = ""
    for turn in conversation:
        role = turn.get("role", "user")
        speaker = "Student" if role == "user" else "Tutor"
        dialogue_text += f"{speaker}: {turn.get('content','')}\n"

    # ============================================================
    # AI PROMPT — SHORT FOLLOW-UP RESPONSE (NOT 6 SECTIONS)
    # ============================================================

    prompt = f"""
You are the DEEP STUDY TUTOR of PowerGrid.

Tone requirements:
• Warm, calm, clear
• Reflect gentle Christian virtues (wisdom, patience, integrity)
• NEVER mention Christianity or religion explicitly
• Speak like a thoughtful, friendly guide
• Help the student understand without overwhelming them

GRADE LEVEL: {grade_level}

Conversation so far:
{dialogue_text}

NOW RESPOND AS THE TUTOR.

FOLLOW-UP RULES:
• Reply with intent to help student get to bottom of their question
• Be able to get more detailed if student asks for more detail
• Do NOT repeat the original 6-section study guide
• Do NOT generate another full study guide
• Answer naturally and conversationally
• Stay focused on the student's last question
"""

    response = study_buddy_ai(prompt, grade_level, character)

    # Ensure we return just clean text
    if isinstance(response, dict):
        return response.get("raw_text") or response.get("text") or str(response)

    return response






