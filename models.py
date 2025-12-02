from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Teacher(db.Model):
    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Class(db.Model):
    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))
    class_name = db.Column(db.String(120))
    grade_level = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    teacher = db.relationship("Teacher", backref="classes")


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"))
    student_name = db.Column(db.String(120))
    student_email = db.Column(db.String(120))

    # Ability engine
    ability_level = db.Column(db.String(20), default="on_level")
    average_score = db.Column(db.Float, default=0.0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    class_ref = db.relationship("Class", backref="students")


class AssessmentResult(db.Model):
    """
    Every practice question attempt is stored here.
    Supports full analytics, heatmaps, pivot tables, & ability scoring.
    """
    __tablename__ = "assessment_results"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))

    # Subject like "math", "science", etc.
    subject = db.Column(db.String(50))

    # Topic like "fractions", "photosynthesis"
    topic = db.Column(db.String(200))

    # NEW FIELDS (required for auto_logger)
    question_text = db.Column(db.String(255))   # store actual question asked
    question_type = db.Column(db.String(50))    # "multiple_choice" or "free"

    # Performance
    score_percent = db.Column(db.Float)         # 0–100
    num_correct = db.Column(db.Integer)
    num_questions = db.Column(db.Integer)

    # Difficulty Tier
    difficulty_level = db.Column(db.String(20))

    # Timestamp
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Backref
    student = db.relationship("Student", backref="assessment_results")

