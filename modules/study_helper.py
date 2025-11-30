# modules/study_helper.py

from modules.shared_ai import study_buddy_ai


def deep_study_chat(question, grade_level="8", character="everly"):
    """
    Conversational deep study tutor.
    This is NOT the study guide generator.
    This ONLY produces short, guided follow-up responses.
    """

    # ============================================================
    # NORMALIZE INPUT → ALWAYS produce a list of {"role", "content"}
    # ============================================================

    if isinstance(question, str):
        conversation = [{"role": "user", "content": question.strip()}]

    elif isinstance(question, list):
        conversation = []
        for turn in question:
            if isinstance(turn, dict) and "content" in turn:
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

    # ============================================================
    # BUILD READABLE DIALOGUE
    # ============================================================

    dialogue_text = ""
    for turn in conversation:
        speaker = "Student" if turn.get("role") == "user" else "Tutor"
        dialogue_text += f"{speaker}: {turn.get('content','')}\n"

    # ============================================================
    # AI PROMPT — SHORT FOLLOW-UP RESPONSE
    # ============================================================

    prompt = f"""
You are a warm, patient DEEP STUDY TUTOR.

Tone:
• Encouraging, calm, wise
• Never overwhelming
• Speak simply but intelligently

GRADE LEVEL: {grade_level}

Conversation so far:
{dialogue_text}

NOW RESPOND AS THE TUTOR.

FOLLOW-UP RULES:
• Give a short 1–3 paragraph explanation
• Help the student get to the bottom of their question
• Be very attentive to detail
• If they ask for more depth, give more depth
• If they ask for clarity, simplify
• Do NOT repeat any 6-section study guide
• Do NOT generate a long essay
• Stay focused ONLY on the student's most recent message
"""

    # ============================================================
    # CALL MODEL
    # ============================================================

    response = study_buddy_ai(prompt, grade_level, character)

    # Normalize
    if isinstance(response, dict):
        return response.get("raw_text") or response.get("text") or str(response)

    return response







