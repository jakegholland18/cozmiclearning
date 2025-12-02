# modules/ability_helper.py

from models import db, Student, AssessmentResult


def recalc_student_ability(student: Student):
    """
    Recalculates a student's ability tier based on their last 10 assessments.
    Ability Tiers:
        - struggling < 60%
        - on_level 60–84%
        - advanced 85%+
    """

    if not student:
        return None

    results = (
        AssessmentResult.query
        .filter_by(student_id=student.id)
        .order_by(AssessmentResult.timestamp.desc())
        .limit(10)
        .all()
    )

    if not results:
        student.ability_level = "on_level"
        db.session.commit()
        return "on_level"

    avg = sum(r.score_percent or 0 for r in results) / len(results)

    if avg >= 85:
        tier = "advanced"
    elif avg < 60:
        tier = "struggling"
    else:
        tier = "on_level"

    student.ability_level = tier
    db.session.commit()
    return tier
