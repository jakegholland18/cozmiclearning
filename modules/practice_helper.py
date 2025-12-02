# modules/practice_helper.py

import json
from typing import Dict, Any
from modules.shared_ai import get_client, build_character_voice, grade_depth_instruction


# ------------------------------------------------------------
# Difficulty text
# ------------------------------------------------------------

def _difficulty_for_grade(grade_level: str) -> str:
    try:
        g = int(grade_level)
    except:
        return "medium difficulty"

    if g <= 3:
        return "very easy early-elementary difficulty"
    if g <= 6:
        return "easy to medium upper-elementary difficulty"
    if g <= 8:
        return "middle-school difficulty"
    if g <= 10:
        return "medium-hard early high-school difficulty"
    return "advanced high-school difficulty"


# ------------------------------------------------------------
# Subject flavor shaping (CozmicLearning planets)
# ------------------------------------------------------------

def _subject_flavor(subject: str) -> str:
    mapping = {
        "num_forge": "math skills, word problems, equations, percentages, and reasoning.",
        "atom_sphere": "science concepts, experiments, cause-and-effect, and reasoning steps.",
        "faith_realm": "Bible knowledge, stories, verses, and application questions.",
        "chrono_core": "history timelines, events, causes, effects, and comparisons.",
        "ink_haven": "grammar, writing clarity, sentence improvement, and editing.",
        "truth_forge": "apologetics, reasoning, evidence, worldview logic.",
        "stock_star": "investing scenarios, percentages, returns, and decision-making.",
        "coin_quest": "money concepts: saving, spending, budgeting, interest, and value.",
        "terra_nova": "general knowledge, logic puzzles, problem solving.",
        "story_verse": "reading comprehension, inference, theme, characters.",
        "power_grid": "deep multi-step reasoning based on the topic.",
    }
    return mapping.get(subject, "general educational reasoning questions.")


# ------------------------------------------------------------
# MAIN PRACTICE GENERATOR (CozmicLearning mission)
# ------------------------------------------------------------

def generate_practice_session(
    topic: str,
    subject: str,
    grade_level: str = "8",
    character: str = "everly",
) -> Dict[str, Any]:
    """
    Generate a 10-question practice 'mission' for CozmicLearning.
    """

    difficulty = _difficulty_for_grade(grade_level)
    flavor = _subject_flavor(subject)
    voice = build_character_voice(character)
    depth_rule = grade_depth_instruction(grade_level)

    if not topic:
        topic = "the last skill the student reviewed"

    # ------------------------------------------------------------
    # 🌌 COZMICLEARNING SYSTEM PROMPT
    # ------------------------------------------------------------
    system_prompt = f"""
You are COZMICLEARNING PRACTICE MODE, a galaxy-themed tutor
guiding students through "missions" of questions.

GOAL:
Generate a 10-question interactive practice mission:
• Some multiple-choice questions
• Some free-response questions
• Some word problems (if subject allows)
• ALL tightly focused on this skill/topic: {topic}
• Subject flavor: {flavor}
• Difficulty: {difficulty}
• Tone & style: use the tutor voice/personality: {voice}
• Grade level rule: {depth_rule}

THE EXPERIENCE:
• It should feel like a learning "mission" on a CozmicLearning planet.
• Questions should be clear, unambiguous, and age-appropriate.
• Hints should gently guide, not generic.
• Explanations should feel like a teacher walking them through it.

RETURN ONLY VALID JSON in this format:

{{
  "steps": [
    {{
      "prompt": "...",
      "type": "multiple_choice" OR "free",
      "choices": ["A. ...", "B. ..."], 
      "expected": ["a"],
      "hint": "...",
      "explanation": "..."
    }}
  ],
  "final_message": "..."
}}
"""

    user_prompt = """
Generate the full 10-question JSON practice session now.
ONLY return the JSON object. No commentary.
"""

    client = get_client()
    response = client.responses.create(
        model="gpt-4.1-mini",
        max_output_tokens=1800,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    raw = response.output_text.strip()

    # ------------------------------------------------------------
    # Attempt JSON parse
    # ------------------------------------------------------------
    try:
        data = json.loads(raw)
    except Exception:
        return {
            "steps": [
                {
                    "prompt": f"Let's practice {topic}. What is one fact you remember?",
                    "type": "free",
                    "choices": [],
                    "expected": [""],
                    "hint": "Anything related works.",
                    "explanation": "Just share any detail you remember.",
                }
            ],
            "final_message": "Great work finishing this warm-up Cozmic mission! 🚀",
            "topic": topic,
        }

    # ------------------------------------------------------------
    # Validation / Cleanup + MC Auto-Fix
    # ------------------------------------------------------------

    valid_steps = []

    for step in data.get("steps", []):
        prompt = str(step.get("prompt", "")).strip()

        qtype = step.get("type", "free")
        if qtype not in ["multiple_choice", "free"]:
            qtype = "free"

        choices = step.get("choices", []) if qtype == "multiple_choice" else []
        if not isinstance(choices, list):
            choices = []

        expected_raw = step.get("expected", [])
        if not isinstance(expected_raw, list):
            expected_raw = [str(expected_raw)]

        expected = [str(x).lower().strip() for x in expected_raw if str(x).strip()]

        # ------------------------------------------------------------
        # 🛠 FIX MULTIPLE-CHOICE EXPECTED ANSWERS
        # ------------------------------------------------------------
        if qtype == "multiple_choice":
            corrected = []
            choice_letters = []

            for ch in choices:
                try:
                    letter = ch.split(".")[0].strip().lower()
                except Exception:
                    letter = ""
                choice_letters.append(letter)

            for exp in expected:
                if len(exp) == 1 and exp in choice_letters:
                    corrected.append(exp)
                    continue
                for idx, choice in enumerate(choices):
                    if exp and exp in choice.lower():
                        corrected.append(choice_letters[idx])

            if not corrected:
                corrected = ["a"]

            expected = corrected

        hint = str(step.get("hint", "Try focusing on what the question is asking.")).strip()
        explanation = str(step.get("explanation", "Let's walk through this together.")).strip()

        # ------------------------------------------------------------
        # 🔥 Add placeholder for "status" so auto_logger can read it later
        # ------------------------------------------------------------
        valid_steps.append({
            "prompt": prompt,
            "type": qtype,
            "choices": choices,
            "expected": expected or [""],
            "hint": hint,
            "explanation": explanation,
            "status": "unanswered",   # <-- NEW FIELD (needed for analytics logging)
        })

    if not valid_steps:
        valid_steps = [
            {
                "prompt": f"Tell me one thing you know about {topic}.",
                "type": "free",
                "choices": [],
                "expected": [""],
                "hint": "Anything related works!",
                "explanation": "Just share what you remember.",
                "status": "unanswered",
            }
        ]

    final_message = data.get(
        "final_message",
        "You completed this CozmicLearning practice mission! 🚀 Great work.",
    )

    return {
        "steps": valid_steps,
        "final_message": final_message,
        "topic": topic,
    }
