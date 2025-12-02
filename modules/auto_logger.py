# modules/auto_logger.py
# ============================================================
# AUTO LOGGER for CozmicLearning
# Logs every practice question as an assessment entry.
# Supports heatmaps, pivot tables, trend tracking, and ability tiers.
# ============================================================

from datetime import datetime
from models import db, Student, AssessmentResult
from modules.ability_helper import recalc_student_ability


# ------------------------------------------------------------
# INTERNAL: Normalize subject code into readable subject
# (Because your subjects use "num_forge", "terra_nova", etc.)
# ------------------------------------------------------------

SUBJECT_MAP = {
    "num_forge": "math",
    "atom_sphere": "science",
    "chrono_core": "history",
    "story_verse": "reading",
    "ink_haven": "writing",
    "faith_realm": "bible",
    "coin_quest": "money",
    "stock_star": "investing",
    "terra_nova": "general",
    "truth_forge": "apologetics",
    "power_grid": "deep_study",
}


def normalize_subject(subject_code: str) -> str:
    if not subject_code:
        return "general"
    subject_code = subject_code.strip().lower()
    return SUBJECT_MAP.get(subject_code, subject_code)


# ------------------------------------------------------------
# LOG A SINGLE PRACTICE QUESTION EVENT
# ------------------------------------------------------------

def log_practice_event(
    student_id: int,
    subject: str,
    topic: str,
    question_text: str,
    is_correct: bool,
    difficulty_level: str = None,
    question_type: str = None,  # "multiple_choice" or "free"
):
    """
    Logs ONE question attempt:
    • Stores correctness
    • Stores question text
    • Stores question type
    • Stores difficulty tier
    • Updates the student's ability level
    """

    student = Student.query.get(student_id)
    if not student:
        return False

    normalized_subject = normalize_subject(subject)

    # Correctness -> 100 or 0
    num_correct = 1 if is_correct else 0
    score_percent = num_correct * 100

    result = AssessmentResult(
        student_id=student_id,
        subject=normalized_subject,
        topic=topic.strip() or "General",
        question_text=question_text[:255],  # prevent DB overflow
        question_type=question_type or "free",
        num_correct=num_correct,
        num_questions=1,
        score_percent=score_percent,
        difficulty_level=difficulty_level or student.ability_level,
        timestamp=datetime.utcnow(),
    )

    db.session.add(result)
    db.session.commit()

    # Recalculate ability tier
    recalc_student_ability(student)
    db.session.commit()

    return True


# ------------------------------------------------------------
# LOG A FULL COMPLETED PRACTICE SESSION
# ------------------------------------------------------------

def log_finished_practice_session(
    student_id: int,
    subject: str,
    topic: str,
    steps: list,
):
    """
    Logs ALL answered questions from a session.
    This feeds:
        • Pivot heatmap (topic_key = subject|topic)
        • Ability tier engine
        • Class analytics page
        • Parent dashboard progress
    """

    student = Student.query.get(student_id)
    if not student:
        return False

    normalized_subject = normalize_subject(subject)

    for step in steps:
        status = step.get("status", "")
        if status not in ["correct", "given_up"]:
            continue

        is_correct = (status == "correct")

        question_text = step.get("prompt", "")[:255]
        qtype = step.get("type", "free")

        num_correct = 1 if is_correct else 0
        score_percent = num_correct * 100

        result = AssessmentResult(
            student_id=student_id,
            subject=normalized_subject,
            topic=topic.strip() or "General",
            question_text=question_text,
            question_type=qtype,
            num_correct=num_correct,
            num_questions=1,
            score_percent=score_percent,
            difficulty_level=student.ability_level,
            timestamp=datetime.utcnow(),
        )

        db.session.add(result)

    db.session.commit()

    recalc_student_ability(student)
    db.session.commit()

    return True



