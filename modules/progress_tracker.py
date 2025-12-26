"""
Progress Tracker Module

Tracks student progress across subjects for real-time display on subjects page.
Updates mastery, XP, and activity metrics when students answer questions.
"""

from models import db, StudentSubjectProgress
from datetime import datetime
from sqlalchemy import text


def track_question_activity(student_id, subject_key, is_correct=False, time_spent_seconds=0):
    """
    Track when a student answers a question in a subject.

    Args:
        student_id: Student ID
        subject_key: Subject identifier (num_forge, atom_sphere, etc.)
        is_correct: Whether the answer was correct
        time_spent_seconds: Time spent on the question
    """
    # Get or create progress record
    progress = StudentSubjectProgress.query.filter_by(
        student_id=student_id,
        subject_key=subject_key
    ).first()

    if not progress:
        progress = StudentSubjectProgress(
            student_id=student_id,
            subject_key=subject_key
        )
        db.session.add(progress)

    # Update activity metrics
    progress.questions_answered += 1
    if is_correct:
        progress.correct_answers += 1

    # Update time
    progress.total_time_minutes += max(1, time_spent_seconds // 60)
    progress.last_visited = datetime.utcnow()

    # Calculate XP (10 XP per question, +5 bonus if correct)
    xp_gain = 10
    if is_correct:
        xp_gain += 5
    progress.xp_earned += xp_gain

    # Calculate mastery percentage
    progress.mastery_percentage = calculate_mastery(progress)

    db.session.commit()

    return progress


def track_lesson_completion(student_id, subject_key):
    """
    Track when a student completes a lesson.

    Args:
        student_id: Student ID
        subject_key: Subject identifier
    """
    progress = StudentSubjectProgress.query.filter_by(
        student_id=student_id,
        subject_key=subject_key
    ).first()

    if not progress:
        progress = StudentSubjectProgress(
            student_id=student_id,
            subject_key=subject_key
        )
        db.session.add(progress)

    progress.lessons_completed += 1
    progress.xp_earned += 50  # Bonus XP for completing lesson
    progress.last_visited = datetime.utcnow()
    progress.mastery_percentage = calculate_mastery(progress)

    db.session.commit()

    return progress


def track_subject_visit(student_id, subject_key):
    """
    Track when a student visits a subject (updates last_visited).

    Args:
        student_id: Student ID
        subject_key: Subject identifier
    """
    progress = StudentSubjectProgress.query.filter_by(
        student_id=student_id,
        subject_key=subject_key
    ).first()

    if not progress:
        progress = StudentSubjectProgress(
            student_id=student_id,
            subject_key=subject_key
        )
        db.session.add(progress)

    progress.last_visited = datetime.utcnow()
    db.session.commit()

    return progress


def calculate_mastery(progress):
    """
    Calculate mastery percentage based on activity.

    Formula:
    - Questions answered: 50% weight
    - Accuracy: 30% weight
    - Lessons completed: 20% weight

    Args:
        progress: StudentSubjectProgress object

    Returns:
        int: Mastery percentage (0-100)
    """
    # Questions component (up to 50 points, maxes at 50 questions)
    questions_score = min(50, (progress.questions_answered / 50) * 50)

    # Accuracy component (up to 30 points)
    if progress.questions_answered > 0:
        accuracy = progress.correct_answers / progress.questions_answered
        accuracy_score = accuracy * 30
    else:
        accuracy_score = 0

    # Lessons component (up to 20 points, maxes at 10 lessons)
    lessons_score = min(20, (progress.lessons_completed / 10) * 20)

    total = int(questions_score + accuracy_score + lessons_score)

    return min(100, total)  # Cap at 100%


def get_student_progress_all_subjects(student_id):
    """
    Get progress for all subjects for a student.
    Returns dict mapping subject_key to progress data.

    Args:
        student_id: Student ID

    Returns:
        dict: {subject_key: {mastery, xp, last_visited, questions_answered, etc.}}
    """
    progress_records = StudentSubjectProgress.query.filter_by(
        student_id=student_id
    ).all()

    progress_dict = {}
    for record in progress_records:
        progress_dict[record.subject_key] = {
            'mastery_percentage': record.mastery_percentage,
            'xp_earned': record.xp_earned,
            'last_visited': record.last_visited,
            'questions_answered': record.questions_answered,
            'correct_answers': record.correct_answers,
            'lessons_completed': record.lessons_completed,
            'total_time_minutes': record.total_time_minutes,
            'first_visit': record.first_visit
        }

    return progress_dict


def get_recently_visited_subjects(student_id, limit=3):
    """
    Get most recently visited subjects for "Continue Your Journey" section.

    Args:
        student_id: Student ID
        limit: Number of subjects to return

    Returns:
        list: List of progress records, most recent first
    """
    return StudentSubjectProgress.query.filter_by(
        student_id=student_id
    ).filter(
        StudentSubjectProgress.mastery_percentage > 0
    ).order_by(
        StudentSubjectProgress.last_visited.desc()
    ).limit(limit).all()
