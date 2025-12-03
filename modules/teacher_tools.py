# modules/teacher_tools.py
"""
Teacher tooling: assignments, quizzes, lesson plans, messaging, analytics, and reports.

Depends on:
- practice_helper.generate_practice_session and apply_differentiation
- shared_ai.study_buddy_ai for lesson plan generation
- models for AssessmentResult and relationships
"""
from datetime import datetime
from typing import Dict, List, Optional

from modules.practice_helper import generate_practice_session, apply_differentiation
from modules.shared_ai import study_buddy_ai, build_character_voice, grade_depth_instruction
from modules.answer_formatter import format_answer
from models import db, Student, Teacher, Class, AssessmentResult


def assign_practice(subject: str, grade: str, differentiation_mode: str, student_ids: List[int], character: str) -> Dict:
    """Create a practice session payload for a set of students using differentiation."""
    prompt = {
        "subject": subject,
        "grade": grade,
        "mode": differentiation_mode,
    }
    session = generate_practice_session(subject, grade, mode=differentiation_mode)
    payload = {"created_at": datetime.utcnow().isoformat(), "session": session, "student_ids": student_ids}
    return payload


def generate_quiz(subject: str, grade: str, differentiation_mode: str, num_questions: int = 6) -> Dict:
    """Generate a short quiz using the practice engine with mode impacting difficulty."""
    session = generate_practice_session(subject, grade, mode=differentiation_mode, steps=num_questions)
    return {"created_at": datetime.utcnow().isoformat(), "quiz": session}


def generate_lesson_plan(subject: str, topic: str, grade: str, character: str) -> Dict:
    """Generate a six-section lesson plan using shared_ai pattern."""
    prompt = (
        f"Create a teacher-friendly lesson plan for {subject} on '{topic}'. "
        f"Use the six-section format. {grade_depth_instruction(grade)}"
    )
    result = study_buddy_ai(prompt, grade, character)
    if isinstance(result, dict) and result.get("raw_text"):
        raw = result["raw_text"]
    else:
        raw = str(result)
    # Format into sections to render on subject page or teacher view
    sections = format_answer(raw_text=raw)
    return {"raw": raw, "sections": sections}


def message_parents(class_id: int, teacher_id: int, message: str) -> Dict:
    """Stub: persist a message to parents of a class. Returns summary."""
    # In a future pass, add a Messages table. For now, return payload.
    return {"class_id": class_id, "teacher_id": teacher_id, "message": message, "sent_at": datetime.utcnow().isoformat()}


def get_class_analytics(class_id: int) -> Dict:
    """Compute class analytics from AssessmentResult: averages and ability tiers per student."""
    # Gather students
    students = Student.query.filter_by(class_id=class_id).all()
    summary = {"class_id": class_id, "students": []}
    for s in students:
        results = (
            AssessmentResult.query.filter_by(student_id=s.id)
            .order_by(AssessmentResult.created_at.desc())
            .limit(10)
            .all()
        )
        scores = [r.score for r in results if r.score is not None]
        avg = sum(scores) / len(scores) if scores else 0
        if avg < 60:
            tier = "struggling"
        elif avg < 85:
            tier = "on_level"
        else:
            tier = "advanced"
        summary["students"].append({"student_id": s.id, "name": getattr(s, "name", "Student"), "avg": avg, "ability": tier})
    return summary


def build_progress_report(student_id: int) -> Dict:
    """Return a simple progress report for a student based on last 10 results."""
    results = (
        AssessmentResult.query.filter_by(student_id=student_id)
        .order_by(AssessmentResult.created_at.desc())
        .limit(10)
        .all()
    )
    scores = [r.score for r in results if r.score is not None]
    avg = sum(scores) / len(scores) if scores else 0
    return {"student_id": student_id, "avg": avg, "results": [{"score": r.score, "subject": r.subject, "created_at": r.created_at.isoformat()} for r in results]}
