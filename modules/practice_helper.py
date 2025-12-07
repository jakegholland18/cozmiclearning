# modules/practice_helper.py

import json
from typing import Dict, Any, List
from modules.shared_ai import get_client, build_character_voice, grade_depth_instruction


# ------------------------------------------------------------
# Differentiation Analysis
# ------------------------------------------------------------

def analyze_differentiation(questions: List[Dict], differentiation_mode: str) -> Dict[str, Any]:
    """
    Analyze questions to verify differentiation is working.
    Returns metrics and validation for the selected differentiation mode.
    """
    if not questions:
        return {"valid": False, "metrics": {}, "warnings": ["No questions to analyze"]}

    metrics = {
        "total_questions": len(questions),
        "has_hints": 0,
        "has_explanations": 0,
        "multiple_choice": 0,
        "free_response": 0,
        "difficulty_levels": [],
        "avg_prompt_length": 0,
        "avg_hint_length": 0,
    }

    total_prompt_length = 0
    total_hint_length = 0

    for q in questions:
        prompt = q.get("prompt", "")
        hint = q.get("hint", "")
        explanation = q.get("explanation", "")
        q_type = q.get("type", "free")

        # Count features
        if hint and len(hint) > 10:
            metrics["has_hints"] += 1
            total_hint_length += len(hint)

        if explanation and len(explanation) > 10:
            metrics["has_explanations"] += 1

        if q_type == "multiple_choice":
            metrics["multiple_choice"] += 1
        else:
            metrics["free_response"] += 1

        total_prompt_length += len(prompt)

        # Estimate difficulty based on question characteristics
        difficulty = estimate_question_difficulty(q)
        metrics["difficulty_levels"].append(difficulty)

    # Calculate averages
    metrics["avg_prompt_length"] = total_prompt_length // len(questions)
    metrics["avg_hint_length"] = total_hint_length // metrics["has_hints"] if metrics["has_hints"] > 0 else 0

    # Validate based on differentiation mode
    validation = validate_differentiation_mode(metrics, differentiation_mode, len(questions))

    return {
        "valid": validation["valid"],
        "metrics": metrics,
        "warnings": validation["warnings"],
        "checks": validation["checks"],
        "difficulty_trend": analyze_difficulty_trend(metrics["difficulty_levels"])
    }


def estimate_question_difficulty(question: Dict) -> str:
    """
    Estimate difficulty of a single question based on characteristics.
    Returns: "easy", "medium", or "hard"
    """
    prompt = question.get("prompt", "")
    hint = question.get("hint", "")
    q_type = question.get("type", "free")

    difficulty_score = 0

    # Length indicators
    if len(prompt) > 200:
        difficulty_score += 2  # Long questions are often harder
    elif len(prompt) > 100:
        difficulty_score += 1

    # Type indicators
    if q_type == "free":
        difficulty_score += 1  # Free response is harder than multiple choice

    # Multi-step indicators (keywords)
    multi_step_keywords = ["calculate", "then", "next", "finally", "both", "compare", "analyze", "explain why"]
    if any(keyword in prompt.lower() for keyword in multi_step_keywords):
        difficulty_score += 2

    # Hint quality (good hints suggest harder questions)
    if len(hint) > 50:
        difficulty_score += 1

    # Vocabulary complexity (simple check for advanced words)
    advanced_words = ["synthesize", "evaluate", "derive", "integrate", "differentiate", "critique"]
    if any(word in prompt.lower() for word in advanced_words):
        difficulty_score += 2

    # Return difficulty rating
    if difficulty_score >= 5:
        return "hard"
    elif difficulty_score >= 3:
        return "medium"
    else:
        return "easy"


def analyze_difficulty_trend(difficulty_levels: List[str]) -> str:
    """
    Analyze if difficulty is progressive (easy → hard), flat, or random.
    """
    if len(difficulty_levels) < 3:
        return "insufficient_data"

    # Map to numeric scores
    score_map = {"easy": 1, "medium": 2, "hard": 3}
    scores = [score_map.get(d, 2) for d in difficulty_levels]

    # Check for progressive pattern (first half easier than second half)
    mid = len(scores) // 2
    first_half_avg = sum(scores[:mid]) / mid
    second_half_avg = sum(scores[mid:]) / (len(scores) - mid)

    if second_half_avg > first_half_avg + 0.3:
        return "progressive"  # Gets harder
    elif abs(second_half_avg - first_half_avg) < 0.3:
        return "balanced"  # Consistent difficulty
    else:
        return "mixed"  # Random difficulty


def validate_differentiation_mode(metrics: Dict, mode: str, total: int) -> Dict:
    """
    Validate that questions match the expected differentiation mode characteristics.
    """
    checks = []
    warnings = []
    valid = True

    if mode == "scaffold":
        # Scaffold should have hints on most/all questions
        hint_percentage = (metrics["has_hints"] / total) * 100
        checks.append({
            "label": "Questions with hints",
            "value": f"{metrics['has_hints']}/{total} ({hint_percentage:.0f}%)",
            "passed": hint_percentage >= 80
        })
        if hint_percentage < 80:
            warnings.append(f"Only {hint_percentage:.0f}% of questions have hints (expected 80%+ for scaffold mode)")
            valid = False

        # Should have good explanations
        expl_percentage = (metrics["has_explanations"] / total) * 100
        checks.append({
            "label": "Questions with explanations",
            "value": f"{metrics['has_explanations']}/{total} ({expl_percentage:.0f}%)",
            "passed": expl_percentage >= 80
        })
        if expl_percentage < 80:
            warnings.append(f"Only {expl_percentage:.0f}% have detailed explanations (expected 80%+)")

    elif mode == "mastery":
        # Mastery should have more hard questions
        hard_count = metrics["difficulty_levels"].count("hard")
        hard_percentage = (hard_count / total) * 100
        checks.append({
            "label": "Challenging questions",
            "value": f"{hard_count}/{total} ({hard_percentage:.0f}%)",
            "passed": hard_percentage >= 40
        })
        if hard_percentage < 40:
            warnings.append(f"Only {hard_percentage:.0f}% are challenging (expected 40%+ for mastery mode)")
            valid = False

        # Should favor free response
        free_percentage = (metrics["free_response"] / total) * 100
        checks.append({
            "label": "Free response questions",
            "value": f"{metrics['free_response']}/{total} ({free_percentage:.0f}%)",
            "passed": free_percentage >= 50
        })

    elif mode == "adaptive":
        # Adaptive should have mixed difficulty
        easy = metrics["difficulty_levels"].count("easy")
        medium = metrics["difficulty_levels"].count("medium")
        hard = metrics["difficulty_levels"].count("hard")

        checks.append({
            "label": "Difficulty distribution",
            "value": f"Easy: {easy}, Medium: {medium}, Hard: {hard}",
            "passed": easy > 0 and hard > 0  # Must have both ends
        })
        if not (easy > 0 and hard > 0):
            warnings.append("Adaptive mode should include easy and hard questions")
            valid = False

    elif mode == "gap_fill":
        # Gap fill should have explanations and hints
        hint_percentage = (metrics["has_hints"] / total) * 100
        expl_percentage = (metrics["has_explanations"] / total) * 100

        checks.append({
            "label": "Teaching support",
            "value": f"Hints: {hint_percentage:.0f}%, Explanations: {expl_percentage:.0f}%",
            "passed": hint_percentage >= 60 and expl_percentage >= 60
        })
        if hint_percentage < 60 or expl_percentage < 60:
            warnings.append("Gap fill mode needs strong teaching support (hints + explanations)")

    # General check for all modes
    checks.append({
        "label": "Question variety",
        "value": f"MC: {metrics['multiple_choice']}, Free: {metrics['free_response']}",
        "passed": metrics['multiple_choice'] > 0 and metrics['free_response'] > 0
    })

    return {
        "valid": valid,
        "checks": checks,
        "warnings": warnings
    }


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
- Start medium.
- Harder after correct answers.
- Easier after incorrect answers.
- Smooth difficulty curve.
"""

    if mode == "gap_fill":
        return base_prompt + """
DIFFERENTIATION MODE: GAP FILL
- Include prerequisite/foundation skills.
- Target common misconceptions.
- Step-by-step reasoning.
- Aim to fix misunderstandings.
"""

    if mode == "mastery":
        return base_prompt + """
DIFFERENTIATION MODE: MASTERY
- Push difficulty higher.
- Include multi-step reasoning.
- Real-world application.
- At least 3 synthesis/rigor problems.
"""

    if mode == "scaffold":
        return base_prompt + """
PRACTICE MODE: FULL PRACTICE - COMPREHENSIVE WITH SCAFFOLDING
CRITICAL: This mode provides thorough practice WITH helpful hints and step-by-step support!

REQUIREMENTS:
- Mix of multiple choice AND free response questions
- EVERY question MUST include a helpful hint
- Hints should guide thinking without giving away the answer
- Progressive difficulty - start easier, build to harder
- Break complex problems into smaller steps
- Include detailed explanations that teach the concept
- Build confidence through gradual progression

HINT EXAMPLES:
- "Think about what happens to the denominator when you multiply fractions"
- "Remember that photosynthesis requires sunlight, water, and CO2"
- "Start by identifying the subject and verb in the sentence"

FOCUS: Comprehensive learning with support and guidance
"""

    if mode == "multiple_choice_only":
        return base_prompt + """
PRACTICE MODE: QUICK QUIZ
CRITICAL: EVERY question MUST be multiple choice with exactly 4 options (A, B, C, D)!

REQUIREMENTS:
- 100% multiple choice format - NO free response questions allowed
- Each question has exactly 4 answer options labeled A, B, C, D
- Questions test core concepts and recall
- Fast-paced, straightforward assessment
- Focus on "what" and "which" rather than "why" or "how"
- Make distractors plausible but clearly wrong

EXAMPLE FORMAT:
"What is 3/4 + 1/2?"
A. 5/6
B. 4/6
C. 5/4
D. 1 1/4
Expected: ["d"]
"""

    if mode == "quick_assessment":
        return base_prompt + """
PRACTICE MODE: TIMED CHALLENGE
- Mix of multiple choice and short answer
- Questions should be answerable quickly (under 2 minutes each)
- Focus on core concepts and skills
- No lengthy word problems
- Test readiness and speed
- Clear, unambiguous questions
"""

    if mode == "deep_conceptual":
        return base_prompt + """
PRACTICE MODE: TEACH ME MORE - DEEP CONCEPTUAL UNDERSTANDING
CRITICAL: This mode MUST focus on deeper understanding, NOT basic practice!

REQUIRED QUESTION TYPES (use ALL of these):
1. "Explain WHY..." questions - require 2-3 sentence explanations
2. "How does this work..." - ask about underlying mechanisms
3. "What would happen if..." - hypothetical scenarios
4. "Compare and contrast..." - analytical thinking
5. "Apply this concept to..." - real-world applications

EXAMPLES OF GOOD QUESTIONS:
- "Explain WHY multiplying fractions gives a smaller result than the original fractions"
- "How does photosynthesis demonstrate the law of conservation of energy?"
- "What would happen if Earth's rotation suddenly stopped? Explain the physics."

AVOID: Simple recall, basic calculations, or yes/no questions
FOCUS: Deep thinking, connections, explanations, analysis
"""

    if mode == "cross_topic":
        return base_prompt + """
PRACTICE MODE: RELATED TOPICS - INTERDISCIPLINARY CONNECTIONS
CRITICAL: This mode MUST show how topics connect across subjects!

REQUIRED APPROACH (use ALL of these):
1. Explicitly connect to OTHER subjects (math↔science, history↔literature, etc.)
2. Ask "How does [this topic] relate to [other subject]?" questions
3. Show real-world applications that cross disciplines
4. Explore historical context or future implications
5. Make students see the BIG PICTURE beyond just one subject

EXAMPLES OF GOOD QUESTIONS:
- "How do fractions relate to musical rhythm and beats?"
- "How is the water cycle similar to the economic cycle of supply and demand?"
- "How did scientific discoveries during the Industrial Revolution change society?"

AVOID: Questions that stay within one subject only
FOCUS: Connections, relationships, interdisciplinary thinking, big picture
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
    num_questions: int = 10,
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

CRITICAL REQUIREMENT: Generate EXACTLY {num_questions} questions.

TOPIC FOCUS:
ALL questions must be SPECIFICALLY about: {topic}
- Do NOT ask generic questions like "What do you remember about..."
- Every question must test specific knowledge, skills, or concepts from this topic
- Questions should be detailed and require applying knowledge of {topic}

GOAL:
Generate {num_questions} clear, grade-appropriate practice questions:
- Mix of multiple-choice and free-response
- ALL focused specifically on: {topic}
- Subject area: {flavor}
- Difficulty: {difficulty}
- Grade level: {depth_rule}

STUDENT CONTEXT:
- Student ability level: {student_ability}
- Applied differentiation mode: {differentiation_mode}

FORMAT REQUIREMENTS:
- Direct, professional question prompts (no narrative framing)
- Clear, unambiguous wording
- Concise hints that guide without giving away the answer
- Brief, instructional explanations
- Standard academic tone

RETURN FORMAT - VALID JSON ONLY:
{{
  "steps": [
    {{
      "prompt": "What is 3/4 + 1/2?",
      "type": "multiple_choice",
      "choices": ["A. 5/6", "B. 4/6", "C. 5/4", "D. 1 1/4"],
      "expected": ["d"],
      "hint": "Find a common denominator first.",
      "explanation": "Convert both fractions to fourths: 3/4 + 2/4 = 5/4 = 1 1/4"
    }},
    {{
      "prompt": "Simplify: 8/12",
      "type": "free",
      "choices": [],
      "expected": ["2/3"],
      "hint": "Find the GCF of 8 and 12.",
      "explanation": "Both 8 and 12 are divisible by 4. 8÷4=2, 12÷4=3, so 8/12 = 2/3"
    }}
  ],
  "final_message": "Great work on {topic}!"
}}

Example for word problems:
{{
  "steps": [
    {{
      "prompt": "Sarah ate 1/4 of a pizza and John ate 3/8 of the same pizza. What fraction of the pizza did they eat together?",
      "type": "multiple_choice",
      "choices": ["A. 4/12", "B. 5/8", "C. 1/2", "D. 7/12"],
      "expected": ["b"],
      "hint": "Add the fractions using a common denominator of 8.",
      "explanation": "1/4 = 2/8. So 2/8 + 3/8 = 5/8"
    }}
  ],
  "final_message": "Excellent work!"
}}

CRITICAL RULES:
1. Generate EXACTLY {num_questions} questions in the "steps" array
2. Every question must be a SPECIFIC problem about {topic}
3. Return ONLY valid JSON - no other text before or after
4. For multiple choice, use format "A. answer", "B. answer", etc.
5. Expected answers for MC should be lowercase letters: ["a"], ["b"], etc.
"""
    else:
        # Gamified mission style for student practice
        base_prompt = f"""
You are COZMICLEARNING PRACTICE MODE, a galaxy-themed tutor
guiding students through "missions" of questions.

CRITICAL: Generate EXACTLY {num_questions} questions.

GOAL:
Generate a {num_questions}-question interactive practice mission:
- Some multiple-choice questions
- Some free-response questions
- Some word problems (if subject allows)
- ALL tightly focused on this specific skill/topic: {topic}
- Subject flavor: {flavor}
- Difficulty: {difficulty}
- Tone & style: use the tutor voice/personality: {voice}
- Grade level rule: {depth_rule}

STUDENT CONTEXT:
- Student ability level: {student_ability}
- Applied differentiation mode: {differentiation_mode}

THE EXPERIENCE:
- It should feel like a learning "mission" on a CozmicLearning planet.
- Questions should be clear, unambiguous, and age-appropriate.
- Hints should gently guide.
- Explanations should be supportive, like a real tutor.

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

REMEMBER: Generate EXACTLY {num_questions} questions in the steps array.
"""

    # ------------------------------------------------------------
    # 🔥 APPLY DIFFERENTIATION RULES
    # ------------------------------------------------------------
    system_prompt = apply_differentiation(base_prompt, differentiation_mode)

    user_prompt = f"""Generate {num_questions} specific practice questions about: {topic}

IMPORTANT:
- Create actual problems to solve (not "what do you remember" questions)
- For math topics: include calculations, word problems, and concept questions
- Use a mix of multiple-choice and free-response questions
- Return ONLY valid JSON, starting with a single opening brace and ending with a single closing brace
- No extra text before or after the JSON"""

    # ------------------------------------------------------------
    # OPENAI CALL
    # ------------------------------------------------------------
    client = get_client()

    # DEBUG: Print prompts for teacher context
    if context == "teacher":
        print(f"\n{'='*60}")
        print(f"🎯 TEACHER QUESTION GENERATION DEBUG")
        print(f"{'='*60}")
        print(f"Topic: {topic}")
        print(f"Subject: {subject}")
        print(f"Num Questions: {num_questions}")
        print(f"Grade: {grade_level}")
        print(f"\nSYSTEM PROMPT (first 300 chars):\n{system_prompt[:300]}...")
        print(f"\nUSER PROMPT:\n{user_prompt}")
        print(f"{'='*60}\n")

    response = client.responses.create(
        model="gpt-4.1-mini",
        max_output_tokens=4000,  # Increased from 1800 to accommodate more questions with full details
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    raw = response.output_text.strip()

    # DEBUG: Print AI response for teacher context
    if context == "teacher":
        print(f"\n{'='*60}")
        print(f"🤖 AI RESPONSE (first 800 chars):")
        print(f"{'='*60}")
        print(raw[:800])
        print(f"{'='*60}\n")

    # ------------------------------------------------------------
    # CLEAN AND PARSE JSON
    # ------------------------------------------------------------
    # Fix double braces if AI followed our old instruction literally
    if raw.startswith('{{') and raw.endswith('}}'):
        print(f"⚠️ AI returned double braces - fixing for {topic}")
        raw = raw[1:-1]  # Remove outer braces to get valid JSON

    # Try to extract JSON if AI added extra text
    json_str = raw
    if not raw.startswith('{'):
        # Look for JSON object in the response
        start = raw.find('{')
        end = raw.rfind('}') + 1
        if start != -1 and end > start:
            json_str = raw[start:end]
        else:
            print(f"⚠️ No JSON object found in response for {topic}")
            json_str = raw

    # Fix common JSON escape issues
    # Replace invalid escape sequences that aren't part of valid JSON escapes
    import re
    # Fix backslashes that aren't followed by valid escape characters
    json_str = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', json_str)

    try:
        data = json.loads(json_str)
    except Exception as e:
        # fallback: generate requested number of basic questions
        print(f"⚠️ JSON parsing failed for {topic}. Error: {str(e)}")
        print(f"Raw response (first 500 chars): {raw[:500]}")
        fallback_steps = []
        for i in range(num_questions):
            fallback_steps.append({
                "prompt": f"Question {i+1} about {topic}: Explain a key concept or solve a problem related to this topic.",
                "type": "free",
                "choices": [],
                "expected": [""],
                "hint": "Think about what you've learned.",
                "explanation": "Your answer should demonstrate understanding of the topic.",
                "status": "unanswered",
            })
        return {
            "steps": fallback_steps,
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
