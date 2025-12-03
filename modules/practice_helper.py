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
# DIFFERENTIATION ENGINE (adds instructions to prompt)
# ------------------------------------------------------------

def apply_differentiation(base_prompt: str, mode: str) -> str:
    if mode == "none":
        return base_prompt

    if mode == "adaptive":
        return base_prompt + """
DIFFERENTIATION MODE: ADAPTIVE
• Start medium.
• Harder after correct answers.
• Easier after incorrect answers.
• Smooth difficulty curve.
"""

    if mode == "gap_fill":
        return base_prompt + """
DIFFERENTIATION MODE: GAP FILL
• Include prerequisite/foundation skills.
• Target common misconceptions.
• Step-by-step reasoning.
• Aim to fix misunderstandings.
"""

    if mode == "mastery":
        return base_prompt + """
DIFFERENTIATION MODE: MASTERY
• Push difficulty higher.
• Include multi-step reasoning.
• Real-world application.
• At least 3 synthesis/rigor problems.
"""

    if mode == "scaffold":
        return base_prompt + """
DIFFERENTIATION MODE: SCAFFOLDED SUPPORT
• Below grade-level entry.
• Break tasks into smaller steps.
• Simpler vocabulary & numbers.
• Confidence-building approach.
"""

    return base_prompt


# ------------------------------------------------------------
# MAIN PRACTICE GENERATOR (CozmicLearning mission)
# ------------------------------------------------------------

def generate_practice_session(
    topic: str,
    subject: str,
    grade_level: str = "8",
    character: str = "everly",
    differentiation_mode: str = "none",
    student_ability: str = "on_level",
    context: str = "student",  # "student" or "teacher"
) -> Dict[str, Any]:
    """
    Generate a 10-question practice 'mission' with differentiation support.
    Context: "student" = gamified mission style; "teacher" = clean professional format.
    """

    difficulty = _difficulty_for_grade(grade_level)
    flavor = _subject_flavor(subject)
    voice = build_character_voice(character) if context == "student" else ""
    depth_rule = grade_depth_instruction(grade_level)

    if not topic:
        topic = "the last skill the student reviewed"

    # ------------------------------------------------------------
    # 🌌 BASE SYSTEM PROMPT
    # ------------------------------------------------------------
    if context == "teacher":
        # Professional, clean format for teacher assignments
        base_prompt = f"""
You are an educational content generator creating practice questions for teacher assignments.

GOAL:
Generate 10 clear, grade-appropriate practice questions:
• Mix of multiple-choice and free-response
• Focused on: {topic}
• Subject area: {flavor}
• Difficulty: {difficulty}
• Grade level: {depth_rule}

STUDENT CONTEXT:
• Student ability level: {student_ability}
• Applied differentiation mode: {differentiation_mode}

FORMAT REQUIREMENTS:
• Direct, professional question prompts (no narrative framing)
• Clear, unambiguous wording
• Concise hints that guide without giving away the answer
• Brief, instructional explanations
• Standard academic tone"""
    else:
        # Gamified mission style for student practice
        base_prompt = f"""
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

STUDENT CONTEXT:
• Student ability level: {student_ability}
• Applied differentiation mode: {differentiation_mode}

THE EXPERIENCE:
• It should feel like a learning "mission" on a CozmicLearning planet.
• Questions should be clear, unambiguous, and age-appropriate.
• Hints should gently guide.
• Explanations should be supportive, like a real tutor.

RETURN ONLY VALID JSON:

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

    # ------------------------------------------------------------
    # 🔥 APPLY DIFFERENTIATION RULES
    # ------------------------------------------------------------
    system_prompt = apply_differentiation(base_prompt, differentiation_mode)

    user_prompt = "Generate all 10 questions now. Return ONLY valid JSON."

    # ------------------------------------------------------------
    # OPENAI CALL
    # ------------------------------------------------------------
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
    # TRY PARSING JSON
    # ------------------------------------------------------------
    try:
        data = json.loads(raw)
    except:
        # fallback safe question
        return {
            "steps": [
                {
                    "prompt": f"What is one thing you know about {topic}?",
                    "type": "free",
                    "choices": [],
                    "expected": [""],
                    "hint": "Anything related works!",
                    "explanation": "Just share what you remember.",
                    "status": "unanswered",
                }
            ],
            "final_message": "Great job completing your mission! 🚀",
            "topic": topic,
            "differentiation_mode": differentiation_mode,
            "student_ability": student_ability,
        }

    # ------------------------------------------------------------
    # CLEANUP/VALIDATION
    # ------------------------------------------------------------
    valid_steps = []

    for step in data.get("steps", []):
        prompt = str(step.get("prompt", "")).strip()
        qtype = step.get("type", "free")

        if qtype not in ["multiple_choice", "free"]:
            qtype = "free"

        # Choices for MC
        choices = step.get("choices", []) if qtype == "multiple_choice" else []
        if not isinstance(choices, list):
            choices = []

        # Expected answers
        expected_raw = step.get("expected", [])
        if not isinstance(expected_raw, list):
            expected_raw = [expected_raw]

        expected = [str(x).strip().lower() for x in expected_raw if x]

        # Fix multiple-choice answer letters
        if qtype == "multiple_choice":
            choice_letters = []
            for ch in choices:
                try:
                    letter = ch.split(".")[0].strip().lower()
                except:
                    letter = ""
                choice_letters.append(letter)

            corrected = []
            for exp in expected:
                if exp in choice_letters:
                    corrected.append(exp)
                else:
                    for idx, choice in enumerate(choices):
                        if exp and exp in choice.lower():
                            corrected.append(choice_letters[idx])

            if not corrected:
                corrected = ["a"]

            expected = corrected

        hint = str(step.get("hint", "Think carefully.")).strip()
        explanation = str(step.get("explanation", "Let's walk through it together.")).strip()

        valid_steps.append({
            "prompt": prompt,
            "type": qtype,
            "choices": choices,
            "expected": expected or [""],
            "hint": hint,
            "explanation": explanation,
            "status": "unanswered",
        })

    if not valid_steps:
        valid_steps = [
            {
                "prompt": f"What do you know about {topic}?",
                "type": "free",
                "choices": [],
                "expected": [""],
                "hint": "Anything is okay.",
                "explanation": "Let's begin with what you remember.",
                "status": "unanswered",
            }
        ]

    final_message = data.get(
        "final_message",
        "You completed the Cozmic mission! 🚀 Amazing work."
    )

    # ------------------------------------------------------------
    # FINAL RETURN — NOW INCLUDES DIFFERENTIATION + ABILITY
    # ------------------------------------------------------------
    return {
        "steps": valid_steps,
        "final_message": final_message,
        "topic": topic,
        "differentiation_mode": differentiation_mode,
        "student_ability": student_ability,
    }
