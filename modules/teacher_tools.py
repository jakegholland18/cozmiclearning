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
from modules.visual_generator import add_visual_to_question
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
    """Generate a comprehensive teacher lesson plan with 9 practical sections."""
    prompt = f"""Create a complete teacher lesson plan for teaching {subject.replace('_', ' ')} on the topic: '{topic}' for grade {grade}.

Use this EXACT structure with 9 sections:

SECTION 1 - LEARNING OBJECTIVES
[Clear, measurable learning goals - what students will know/be able to do by the end]

SECTION 2 - MATERIALS NEEDED
[List all resources, supplies, and materials required for the lesson]

SECTION 3 - INTRODUCTION/HOOK
[Engaging activity or question to capture student attention and introduce the topic - 5-10 minutes]

SECTION 4 - MAIN TEACHING POINTS
[Core content and concepts to teach - step-by-step instructional content]

SECTION 5 - ACTIVITIES/PRACTICE
[Hands-on activities, exercises, or practice problems for students to apply learning]

SECTION 6 - ASSESSMENT
[How to check for understanding - questions to ask, exit tickets, quick checks]

SECTION 7 - DIFFERENTIATION TIPS
[Strategies for struggling students, on-level students, and advanced students]

SECTION 8 - CHRISTIAN INTEGRATION
[Biblical connections, Scripture references, and faith integration points]

SECTION 9 - CLOSURE/SUMMARY
[How to wrap up the lesson and reinforce key takeaways - 5 minutes]

Make it practical, actionable, and ready to use in a classroom. {grade_depth_instruction(grade)}"""

    result = study_buddy_ai(prompt, grade, character)
    if isinstance(result, dict) and result.get("raw_text"):
        raw = result["raw_text"]
    else:
        raw = str(result)
    
    # Parse the 9-section format
    sections = _parse_teacher_lesson_plan(raw)
    return {"raw": raw, "sections": sections}


def _parse_teacher_lesson_plan(text: str) -> Dict:
    """Parse teacher lesson plan with 9 sections."""
    import re
    
    sections = {
        "learning_objectives": "",
        "materials_needed": "",
        "introduction_hook": "",
        "main_teaching_points": "",
        "activities_practice": "",
        "assessment": "",
        "differentiation_tips": "",
        "christian_integration": "",
        "closure_summary": "",
    }
    
    if not text:
        return sections
    
    pattern = re.compile(r"(SECTION\s+[1-9][^\n]*)", re.IGNORECASE)
    parts = pattern.split(text)
    
    if len(parts) == 1:
        sections["learning_objectives"] = parts[0].strip()
        return sections
    
    it = iter(parts)
    _ = next(it, "")
    
    for label_line, content in zip(it, it):
        label = label_line.lower()
        content = content.strip()
        
        if "section 1" in label:
            sections["learning_objectives"] = content
        elif "section 2" in label:
            sections["materials_needed"] = content
        elif "section 3" in label:
            sections["introduction_hook"] = content
        elif "section 4" in label:
            sections["main_teaching_points"] = content
        elif "section 5" in label:
            sections["activities_practice"] = content
        elif "section 6" in label:
            sections["assessment"] = content
        elif "section 7" in label:
            sections["differentiation_tips"] = content
        elif "section 8" in label:
            sections["christian_integration"] = content
        elif "section 9" in label:
            sections["closure_summary"] = content
    
    return sections


def assign_questions(
    subject: str,
    topic: str,
    grade: str = "8",
    character: str = "everly",
    differentiation_mode: str = "none",
    student_ability: str = "on_level",
    num_questions: int = 10,
) -> Dict:
    """
    Generate a set of questions suitable for assignment.

    Returns a dict with `questions` (list of question dicts) and metadata.
    Question dict shape is aligned to the app's assignment model expectations:
      {
        "prompt": str,
        "type": "multiple_choice" | "free",
        "choices": [str],
        "expected": [str],
        "hint": str,
        "explanation": str
      }
    """

    session = generate_practice_session(
        topic=topic,
        subject=subject,
        grade_level=grade,
        character=character,
        differentiation_mode=differentiation_mode,
        student_ability=student_ability,
        context="teacher",  # Clean, professional format for assignments
        num_questions=num_questions,  # Pass the requested number to generation
    )

    steps = session.get("steps", [])
    # Note: For dynamic modes (adaptive/scaffold/gap_fill/mastery), num_questions may be
    # larger than what students see (e.g., 30 questions for 10-student adaptive assignment)
    # Don't trim - we need the full pool for routing!

    questions: List[Dict] = []
    for s in steps:
        # Get expected answer, filtering out empty strings
        expected_raw = s.get("expected", [])
        if isinstance(expected_raw, list):
            expected = [e for e in expected_raw if e and str(e).strip()]
        elif expected_raw and str(expected_raw).strip():
            expected = [expected_raw]
        else:
            expected = []

        question_data = {
            "prompt": s.get("prompt", ""),
            "type": s.get("type", "free"),
            "choices": s.get("choices", []) if s.get("type") == "multiple_choice" else [],
            "expected": expected,
            "hint": s.get("hint", "Think carefully."),
            "explanation": s.get("explanation", "Let's walk through it together."),
        }

        # Preserve difficulty field for adaptive mode (used in hybrid adaptive assignments)
        if "difficulty" in s:
            question_data["difficulty"] = s["difficulty"]

        # Add visual aid if appropriate for this question
        visual_data = add_visual_to_question(
            question_text=question_data["prompt"],
            topic=topic,
            subject=subject,
            grade=grade
        )
        question_data["visual_type"] = visual_data["visual_type"]
        question_data["visual_content"] = visual_data["visual_content"]
        question_data["visual_caption"] = visual_data["visual_caption"]

        questions.append(question_data)

    payload = {
        "created_at": datetime.utcnow().isoformat(),
        "subject": subject,
        "topic": topic,
        "grade": grade,
        "character": character,
        "differentiation_mode": differentiation_mode,
        "student_ability": student_ability,
        "final_message": session.get("final_message", ""),
        "questions": questions,
    }

    return payload


def message_parents(class_id: int, teacher_id: int, message: str) -> Dict:
    """Stub: persist a message to parents of a class. Returns summary."""
    # In a future pass, add a Messages table. For now, return payload.
    return {"class_id": class_id, "teacher_id": teacher_id, "message": message, "sent_at": datetime.utcnow().isoformat()}


def get_class_analytics(class_id: int) -> Dict:
    """Compute class analytics from AssessmentResult: averages, ability tiers, per-subject breakdown, and trend deltas."""
    students = Student.query.filter_by(class_id=class_id).all()
    summary: Dict = {"class_id": class_id, "students": [], "subjects": {}, "flags": []}

    # Per-student analytics
    for s in students:
        results = (
            AssessmentResult.query.filter_by(student_id=s.id)
            .order_by(AssessmentResult.created_at.desc())
            .limit(20)
            .all()
        )
        last10 = results[:10]
        prev10 = results[10:20]
        scores_last = [r.score for r in last10 if r.score is not None]
        scores_prev = [r.score for r in prev10 if r.score is not None]
        avg_last = sum(scores_last) / len(scores_last) if scores_last else 0
        avg_prev = sum(scores_prev) / len(scores_prev) if scores_prev else 0
        delta = round(avg_last - avg_prev, 2)

        # Ability tier based on last10
        if avg_last < 60:
            tier = "struggling"
        elif avg_last < 85:
            tier = "on_level"
        else:
            tier = "advanced"

        # Per-subject breakdown (last10)
        subject_avgs: Dict[str, float] = {}
        subject_groups: Dict[str, List[float]] = {}
        for r in last10:
            subj = getattr(r, "subject", "unknown") or "unknown"
            if r.score is None:
                continue
            subject_groups.setdefault(subj, []).append(r.score)
        for subj, arr in subject_groups.items():
            subject_avgs[subj] = round(sum(arr) / len(arr), 2)

        # Flag low subjects for intervention
        weak_subjects = [subj for subj, a in subject_avgs.items() if a < 70]
        suggested_mode = "adaptive" if tier == "on_level" else ("scaffold" if tier == "struggling" else "mastery")

        summary["students"].append({
            "student_id": s.id,
            "name": getattr(s, "name", "Student"),
            "avg": round(avg_last, 2),
            "prev_avg": round(avg_prev, 2),
            "delta": delta,
            "ability": tier,
            "subjects": subject_avgs,
            "weak_subjects": weak_subjects,
            "suggested_mode": suggested_mode,
        })

        # Aggregate class-level subjects
        for subj, a in subject_avgs.items():
            agg = summary["subjects"].setdefault(subj, {"scores": []})
            agg["scores"].append(a)

        # Class flags: student with steep negative trend or multiple weak subjects
        if delta < -10 or len(weak_subjects) >= 2:
            summary["flags"].append({
                "student_id": s.id,
                "name": getattr(s, "name", "Student"),
                "delta": delta,
                "weak_subjects": weak_subjects,
            })

    # Compute class-level subject averages
    for subj, agg in summary["subjects"].items():
        arr = agg.get("scores", [])
        summary["subjects"][subj] = {"avg": round(sum(arr) / len(arr), 2) if arr else 0, "n": len(arr)}

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


def get_early_warnings(teacher_id: int) -> Dict:
    """
    Get comprehensive early warning alerts for all students across teacher's classes.
    Returns at-risk students categorized by warning type.
    """
    from models import Student, Class, AssessmentResult, ActivityLog
    from datetime import datetime, timedelta

    classes = Class.query.filter_by(teacher_id=teacher_id).all()
    warnings = {
        "declining_performance": [],  # Delta < -10
        "low_performance": [],  # 2+ subjects < 60%
        "inactive": [],  # No login in 7+ days
        "no_recent_activity": [],  # No activity in 7+ days
        "critical": []  # Multiple warning types
    }

    now = datetime.utcnow()
    week_ago = now - timedelta(days=7)

    for cls in classes:
        students = Student.query.filter_by(class_id=cls.id).all()

        for student in students:
            student_warnings = []

            # Check 1: Declining performance (delta < -10)
            results = (
                AssessmentResult.query.filter_by(student_id=student.id)
                .order_by(AssessmentResult.created_at.desc())
                .limit(20)
                .all()
            )

            if len(results) >= 10:
                last10 = results[:10]
                prev10 = results[10:20]
                scores_last = [r.score_percent for r in last10 if r.score_percent is not None]
                scores_prev = [r.score_percent for r in prev10 if r.score_percent is not None]

                if scores_last and scores_prev:
                    avg_last = sum(scores_last) / len(scores_last)
                    avg_prev = sum(scores_prev) / len(scores_prev)
                    delta = avg_last - avg_prev

                    if delta < -10:
                        student_warnings.append("declining")
                        warnings["declining_performance"].append({
                            "student_id": student.id,
                            "student_name": student.student_name,
                            "class_name": cls.class_name,
                            "class_id": cls.id,
                            "delta": round(delta, 1),
                            "current_avg": round(avg_last, 1),
                            "previous_avg": round(avg_prev, 1)
                        })

            # Check 2: Low performance in multiple subjects
            if len(results) >= 5:
                subject_groups = {}
                for r in results[:10]:
                    if r.subject and r.score_percent is not None:
                        subject_groups.setdefault(r.subject, []).append(r.score_percent)

                weak_subjects = []
                for subj, scores in subject_groups.items():
                    avg = sum(scores) / len(scores)
                    if avg < 60:
                        weak_subjects.append({"subject": subj, "avg": round(avg, 1)})

                if len(weak_subjects) >= 2:
                    student_warnings.append("low_performance")
                    warnings["low_performance"].append({
                        "student_id": student.id,
                        "student_name": student.student_name,
                        "class_name": cls.class_name,
                        "class_id": cls.id,
                        "weak_subjects": weak_subjects,
                        "count": len(weak_subjects)
                    })

            # Check 3: Haven't logged in recently
            if student.last_login:
                days_since_login = (now - student.last_login).days
                if days_since_login >= 7:
                    student_warnings.append("inactive")
                    warnings["inactive"].append({
                        "student_id": student.id,
                        "student_name": student.student_name,
                        "class_name": cls.class_name,
                        "class_id": cls.id,
                        "days_since_login": days_since_login,
                        "last_login": student.last_login.strftime("%Y-%m-%d") if student.last_login else "Never"
                    })

            # Check 4: No recent activity
            recent_activity = ActivityLog.query.filter(
                ActivityLog.student_id == student.id,
                ActivityLog.created_at >= week_ago
            ).count()

            if recent_activity == 0 and len(results) > 0:  # Has history but no recent activity
                student_warnings.append("no_activity")
                warnings["no_recent_activity"].append({
                    "student_id": student.id,
                    "student_name": student.student_name,
                    "class_name": cls.class_name,
                    "class_id": cls.id,
                    "days_inactive": 7
                })

            # Critical: Multiple warning types
            if len(student_warnings) >= 2:
                warnings["critical"].append({
                    "student_id": student.id,
                    "student_name": student.student_name,
                    "class_name": cls.class_name,
                    "class_id": cls.id,
                    "warning_types": student_warnings,
                    "warning_count": len(student_warnings)
                })

    # Calculate totals
    warnings["total_at_risk"] = len(set(
        [w["student_id"] for category in ["declining_performance", "low_performance", "inactive", "no_recent_activity"]
         for w in warnings[category]]
    ))

    return warnings