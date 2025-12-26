from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ============================================================
# PARENT ACCOUNTS
# ============================================================

class Parent(db.Model):
    __tablename__ = "parents"
    __table_args__ = (
        db.Index('idx_parent_email', 'email'),
        db.Index('idx_parent_access_code', 'access_code'),
        db.Index('idx_parent_stripe_customer', 'stripe_customer_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))

    # Unique access code for student linking (e.g., "ABC123")
    access_code = db.Column(db.String(10), unique=True, nullable=True)

    # Subscription fields
    plan = db.Column(db.String(50))           # free/basic/premium
    billing = db.Column(db.String(20))        # monthly/yearly
    trial_start = db.Column(db.DateTime)
    trial_end = db.Column(db.DateTime)
    subscription_active = db.Column(db.Boolean, default=False)

    # Stripe integration
    stripe_customer_id = db.Column(db.String(255), nullable=True)
    stripe_subscription_id = db.Column(db.String(255), nullable=True)

    # Time limits (Phase 3)
    daily_limit_minutes = db.Column(db.Integer, nullable=True)  # null = no limit

    # Email preferences (Phase 4)
    email_reports_enabled = db.Column(db.Boolean, default=True)
    email_weekly_summary = db.Column(db.Boolean, default=True)  # Weekly summary emails
    last_report_sent = db.Column(db.DateTime, nullable=True)

    # Password reset tokens
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)

    # Account lockout fields
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One parent → many students
    students = db.relationship("Student", backref="parent_ref", lazy=True)


# ============================================================
# TEACHER ACCOUNTS
# ============================================================

class Teacher(db.Model):
    __tablename__ = "teachers"
    __table_args__ = (
        db.Index('idx_teacher_email', 'email'),
        db.Index('idx_teacher_stripe_customer', 'stripe_customer_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(255))

    # Subscription fields (optional for teacher accounts)
    plan = db.Column(db.String(50))
    billing = db.Column(db.String(20))
    trial_start = db.Column(db.DateTime)
    trial_end = db.Column(db.DateTime)
    subscription_active = db.Column(db.Boolean, default=False)

    # Stripe integration
    stripe_customer_id = db.Column(db.String(255), nullable=True)
    stripe_subscription_id = db.Column(db.String(255), nullable=True)

    # Password reset tokens
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)

    # Account lockout fields
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    classes = db.relationship("Class", backref="teacher", lazy=True)
    assigned_practices = db.relationship("AssignedPractice", backref="teacher_ref", lazy=True)


# ============================================================
# CLASSROOMS
# ============================================================

# Association table for many-to-many relationship between students and classes
student_classes = db.Table('student_classes',
    db.Column('student_id', db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('classes.id', ondelete='CASCADE'), primary_key=True),
    db.Column('joined_at', db.DateTime, default=datetime.utcnow, nullable=False)
)

class Class(db.Model):
    __tablename__ = "classes"
    __table_args__ = (
        db.Index('idx_class_teacher', 'teacher_id'),
        db.Index('idx_class_join_code', 'join_code'),
    )

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)

    class_name = db.Column(db.String(120))
    grade_level = db.Column(db.String(20))
    join_code = db.Column(db.String(8), unique=True)  # Unique code for students to join

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Many-to-many relationship with students
    students = db.relationship("Student", secondary=student_classes, back_populates="classes", lazy=True)
    assignments = db.relationship("AssignedPractice", backref="class_ref", lazy=True)


# ============================================================
# STUDENTS
# ============================================================

class Student(db.Model):
    __tablename__ = "students"
    __table_args__ = (
        db.Index('idx_student_email', 'student_email'),
        db.Index('idx_student_parent', 'parent_id'),
        db.Index('idx_student_stripe_customer', 'stripe_customer_id'),
    )

    id = db.Column(db.Integer, primary_key=True)

    # DEPRECATED: Keep for backward compatibility during migration, will be removed
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id", ondelete="SET NULL"), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("parents.id", ondelete="SET NULL"))

    student_name = db.Column(db.String(120))
    student_email = db.Column(db.String(120))
    password_hash = db.Column(db.String(255))  # For secure authentication
    date_of_birth = db.Column(db.Date)  # For age verification and COPPA compliance

    # Subscription fields
    plan = db.Column(db.String(50))           # free/basic/premium
    billing = db.Column(db.String(20))        # monthly/yearly
    trial_start = db.Column(db.DateTime)
    trial_end = db.Column(db.DateTime)
    subscription_active = db.Column(db.Boolean, default=False)

    # Stripe integration
    stripe_customer_id = db.Column(db.String(255), nullable=True)
    stripe_subscription_id = db.Column(db.String(255), nullable=True)

    # Differentiation engine ability tier
    ability_level = db.Column(db.String(20), default="on_level")  
    # below / on_level / advanced

    # Auto-updated from analytics
    average_score = db.Column(db.Float, default=0.0)

    # Time tracking (Phase 3)
    last_login = db.Column(db.DateTime, nullable=True)
    today_minutes = db.Column(db.Integer, default=0)  # resets daily

    # Password reset tokens
    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)

    # Account lockout fields
    failed_login_attempts = db.Column(db.Integer, default=0)
    account_locked_until = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Many-to-many relationship with classes
    classes = db.relationship("Class", secondary=student_classes, back_populates="students", lazy=True)

    # Keep old backref for backward compatibility
    class_ref = db.relationship("Class", foreign_keys=[class_id], backref="legacy_students", lazy=True)

    assessment_results = db.relationship("AssessmentResult", backref="student", lazy=True)


# ============================================================
# ANALYTICS — RESULTS & SCORES
# ============================================================

class AssessmentResult(db.Model):
    __tablename__ = "assessment_results"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))

    subject = db.Column(db.String(50))
    topic = db.Column(db.String(200))

    score_percent = db.Column(db.Float)
    num_correct = db.Column(db.Integer)
    num_questions = db.Column(db.Integer)

    difficulty_level = db.Column(db.String(20))  # easy / medium / hard
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============================================================
# TEACHER-ASSIGNED PRACTICE SETS
# ============================================================

class AssignedPractice(db.Model):
    __tablename__ = "assigned_practice"
    __table_args__ = (
        db.Index('idx_assignment_teacher', 'teacher_id'),
        db.Index('idx_assignment_class', 'class_id'),
        db.Index('idx_assignment_published', 'is_published'),
        db.Index('idx_assignment_dates', 'open_date', 'due_date'),
    )

    id = db.Column(db.Integer, primary_key=True)

    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)

    title = db.Column(db.String(200))
    subject = db.Column(db.String(50))
    topic = db.Column(db.String(200))
    instructions = db.Column(db.Text)
    open_date = db.Column(db.DateTime, nullable=True)  # When assignment becomes visible to students
    due_date = db.Column(db.DateTime, nullable=True)   # When assignment closes

    # Assignment type for gradebook categorization
    assignment_type = db.Column(db.String(50), default="practice")  # practice / quiz / test / homework

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Differentiation level
    differentiation_mode = db.Column(db.String(50), default="none")
    # none / adaptive / gap_fill / mastery / scaffold

    # 🔥 NEW — Full AI preview mission data (steps, hints, final message)
    preview_json = db.Column(db.Text, nullable=True)

    # 🔥 NEW — Teacher must approve before publishing to students
    is_published = db.Column(db.Boolean, default=False)

    # Manual questions (optional)
    questions = db.relationship("AssignedQuestion", backref="practice", lazy=True)
    
    # Student submissions for grading
    submissions = db.relationship("StudentSubmission", backref="assignment", lazy=True)


# ============================================================
# QUESTIONS INSIDE A PRACTICE SET
# ============================================================

class AssignedQuestion(db.Model):
    __tablename__ = "assigned_questions"
    __table_args__ = (
        db.Index('idx_question_practice', 'practice_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    practice_id = db.Column(db.Integer, db.ForeignKey("assigned_practice.id", ondelete="CASCADE"), nullable=False)

    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default="free")  # free / multiple_choice

    # MC options
    choice_a = db.Column(db.String(255))
    choice_b = db.Column(db.String(255))
    choice_c = db.Column(db.String(255))
    choice_d = db.Column(db.String(255))

    correct_answer = db.Column(db.String(255))
    explanation = db.Column(db.Text)
    difficulty_level = db.Column(db.String(20))  # easy / medium / hard

    # Visual aids for questions (ASCII diagrams, Mermaid charts, etc.)
    visual_type = db.Column(db.Text)  # ascii, mermaid, description, none
    visual_content = db.Column(db.Text)  # The actual visual content
    visual_caption = db.Column(db.Text)  # Caption for the visual

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ============================================================
# TEACHER LESSON PLANS
# ============================================================

class LessonPlan(db.Model):
    __tablename__ = "lesson_plans"

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(50))
    topic = db.Column(db.String(200))
    grade = db.Column(db.String(20))

    # Six-section structure stored as JSON
    sections_json = db.Column(db.Text)  # {overview, key_facts, christian_view, agreement, difference, practice}
    
    # Full raw text for export/display
    full_text = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    teacher = db.relationship("Teacher", backref="lesson_plans", lazy=True)


# ============================================================
# MESSAGING SYSTEM
# ============================================================

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    
    # Sender info
    sender_type = db.Column(db.String(20), nullable=False)  # 'teacher' or 'parent'
    sender_id = db.Column(db.Integer, nullable=False)  # ID of teacher or parent
    
    # Recipient info
    recipient_type = db.Column(db.String(20), nullable=False)  # 'teacher' or 'parent'
    recipient_id = db.Column(db.Integer, nullable=False)  # ID of teacher or parent
    
    # Student context (which student is this about)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=True)
    
    # Message content
    subject = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    
    # Progress report attachment (optional JSON data)
    progress_report_json = db.Column(db.Text, nullable=True)
    
    # Thread management
    thread_id = db.Column(db.Integer, nullable=True)  # For grouping replies
    
    # Status
    is_read = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship("Student", backref="messages", lazy=True)


# ============================================================
# STUDENT SUBMISSIONS & GRADES
# ============================================================

class StudentSubmission(db.Model):
    __tablename__ = "student_submissions"
    __table_args__ = (
        db.UniqueConstraint('student_id', 'assignment_id', name='unique_student_assignment'),
        db.Index('idx_submission_student', 'student_id'),
        db.Index('idx_submission_assignment', 'assignment_id'),
        db.Index('idx_submission_status', 'status'),
        db.Index('idx_submission_timestamps', 'started_at', 'submitted_at'),
    )

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assigned_practice.id", ondelete="CASCADE"), nullable=False)
    
    # Submission status
    status = db.Column(db.String(20), default="not_started")  # not_started / in_progress / submitted / graded
    
    # Grading
    score = db.Column(db.Float, nullable=True)  # Percentage score (0-100)
    points_earned = db.Column(db.Float, nullable=True)
    points_possible = db.Column(db.Float, nullable=True)
    grade_released = db.Column(db.Boolean, default=False)  # Teacher has released grade to student

    # Answers submitted (JSON of question_id: answer pairs)
    answers_json = db.Column(db.Text, nullable=True)

    # Teacher feedback
    feedback = db.Column(db.Text, nullable=True)

    # Adaptive assignment tracking (for hybrid adaptive mode)
    current_question_index = db.Column(db.Integer, default=0)  # Index of current question (0-based)
    mc_phase_complete = db.Column(db.Boolean, default=False)  # True when student finishes MC questions and moves to free response

    # Timestamps
    started_at = db.Column(db.DateTime, nullable=True)
    submitted_at = db.Column(db.DateTime, nullable=True)
    graded_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student_rel = db.relationship("Student", backref="submissions", lazy=True)


# ============================================================
# QUESTION LOGGING & MODERATION
# ============================================================

class QuestionLog(db.Model):
    """
    Logs all student questions and AI interactions for safety review.
    Tracks moderation flags, parent notifications, and admin reviews.
    """
    __tablename__ = "question_logs"

    id = db.Column(db.Integer, primary_key=True)
    
    # Student info
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    
    # Question details
    question_text = db.Column(db.Text, nullable=False)
    sanitized_text = db.Column(db.Text, nullable=True)  # After sanitization
    subject = db.Column(db.String(50), nullable=True)  # Which subject/planet
    context = db.Column(db.String(50), nullable=True)  # "question", "chat", "practice", "powergrid"
    grade_level = db.Column(db.String(10), nullable=True)
    
    # AI response
    ai_response = db.Column(db.Text, nullable=True)
    
    # Moderation results (input)
    flagged = db.Column(db.Boolean, default=False)
    allowed = db.Column(db.Boolean, default=True)  # Whether content was processed
    moderation_reason = db.Column(db.Text, nullable=True)  # Why flagged/blocked
    moderation_data_json = db.Column(db.Text, nullable=True)  # Full moderation details (JSON)
    severity = db.Column(db.String(20), nullable=True)  # "low", "medium", "high"

    # Output moderation results (AI response) - TEMPORARILY COMMENTED FOR MIGRATION
    # These will be uncommented after migration adds the columns
    # output_flagged = db.Column(db.Boolean, default=False)
    # output_moderation_reason = db.Column(db.Text, nullable=True)  # Why AI output was flagged

    # Admin review
    reviewed = db.Column(db.Boolean, default=False)
    reviewed_by = db.Column(db.String(100), nullable=True)  # Admin/teacher email
    reviewed_at = db.Column(db.DateTime, nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    
    # Parent notification
    parent_notified = db.Column(db.Boolean, default=False)
    parent_notified_at = db.Column(db.DateTime, nullable=True)
    
    # Student appeal system
    appeal_requested = db.Column(db.Boolean, default=False)
    appeal_reason = db.Column(db.Text, nullable=True)
    appeal_status = db.Column(db.String(20), nullable=True)  # "pending", "approved", "denied"
    appeal_reviewed_by = db.Column(db.String(100), nullable=True)
    appeal_reviewed_at = db.Column(db.DateTime, nullable=True)
    appeal_notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship("Student", backref="question_logs", lazy=True)


# ============================================================
# CHAPTER & LESSON PROGRESS TRACKING
# ============================================================

class ChapterProgress(db.Model):
    """
    Tracks student progress through structured lesson chapters.
    Stores completion status, quiz scores, and unlocking prerequisites.
    """
    __tablename__ = "chapter_progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

    # Chapter identification
    subject = db.Column(db.String(50), nullable=False)  # num_forge, atom_sphere, etc.
    grade = db.Column(db.String(10), nullable=False)    # K, 1, 2, 3, ... 12
    chapter_id = db.Column(db.String(100), nullable=False)  # counting_basics, mult_mastery, etc.

    # Progress tracking
    lessons_completed = db.Column(db.Integer, default=0)
    total_lessons = db.Column(db.Integer, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)

    # Quiz tracking (for chapter completion)
    quiz_score = db.Column(db.Float, nullable=True)  # Percentage (0-100)
    quiz_attempts = db.Column(db.Integer, default=0)
    quiz_passed = db.Column(db.Boolean, default=False)  # True if score >= 80%

    # Timestamps
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student = db.relationship("Student", backref="chapter_progress")

    # Composite unique constraint - one progress record per student/subject/grade/chapter
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject', 'grade', 'chapter_id',
                          name='uix_student_chapter'),
    )


class LessonProgress(db.Model):
    """
    Tracks individual lesson completion and time spent.
    Enables detailed analytics and progress visualization.
    """
    __tablename__ = "lesson_progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)

    # Lesson identification
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    chapter_id = db.Column(db.String(100), nullable=False)
    lesson_title = db.Column(db.String(200), nullable=False)

    # Completion tracking
    is_complete = db.Column(db.Boolean, default=False)
    time_spent_minutes = db.Column(db.Integer, default=0)  # Total time spent

    # Practice tracking
    practice_score = db.Column(db.Float, nullable=True)  # Last practice score (0-100)
    practice_attempts = db.Column(db.Integer, default=0)

    # Timestamps
    first_viewed = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student = db.relationship("Student", backref="lesson_progress")

    # Composite unique constraint
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject', 'grade', 'chapter_id', 'lesson_title',
                          name='uix_student_lesson'),
    )


class ChapterQuiz(db.Model):
    """
    Stores quiz questions for chapter completion assessments.
    Each chapter can have multiple quiz questions.
    """
    __tablename__ = "chapter_quizzes"

    id = db.Column(db.Integer, primary_key=True)

    # Quiz identification
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    chapter_id = db.Column(db.String(100), nullable=False)

    # Question data
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(20), default="multiple_choice")  # multiple_choice, true_false, free_response

    # Answer choices (for MC questions)
    choice_a = db.Column(db.String(255), nullable=True)
    choice_b = db.Column(db.String(255), nullable=True)
    choice_c = db.Column(db.String(255), nullable=True)
    choice_d = db.Column(db.String(255), nullable=True)

    correct_answer = db.Column(db.String(255), nullable=False)
    explanation = db.Column(db.Text, nullable=True)

    # Difficulty and ordering
    difficulty = db.Column(db.String(20), default="medium")  # easy, medium, hard
    question_order = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChapterBadge(db.Model):
    """
    Achievement badges awarded for completing chapters.
    Provides motivation and visual progress indicators.
    """
    __tablename__ = "chapter_badges"

    id = db.Column(db.Integer, primary_key=True)

    # Badge identification
    badge_key = db.Column(db.String(100), unique=True, nullable=False)  # e.g., "num_forge_1_counting_basics"
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    icon = db.Column(db.String(50))  # emoji or icon identifier

    # Chapter association
    subject = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(10), nullable=False)
    chapter_id = db.Column(db.String(100), nullable=False)

    # Badge tier/type
    tier = db.Column(db.String(20), default="bronze")  # bronze, silver, gold, platinum
    badge_type = db.Column(db.String(50), default="chapter_complete")  # chapter_complete, perfect_score, speed_master

    # Requirements
    requirement_type = db.Column(db.String(50), default="completion")  # completion, quiz_score, time_limit
    requirement_value = db.Column(db.Integer, nullable=True)  # e.g., 100 for perfect score

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentChapterBadge(db.Model):
    """
    Tracks which chapter badges students have earned.
    Links students to their chapter achievements.
    """
    __tablename__ = "student_chapter_badges"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey("chapter_badges.id"), nullable=False)

    # Context of earning
    quiz_score = db.Column(db.Float, nullable=True)  # Score when badge was earned
    completion_time_minutes = db.Column(db.Integer, nullable=True)  # How long it took

    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student = db.relationship("Student", backref="chapter_badges")
    badge = db.relationship("ChapterBadge")


# ============================================================
# ACHIEVEMENTS & BADGES
# ============================================================

class Achievement(db.Model):
    __tablename__ = "achievements"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(255))
    icon = db.Column(db.String(50))  # emoji or icon identifier
    category = db.Column(db.String(50))  # streak, level, mastery, exploration, milestone
    requirement_value = db.Column(db.Integer)  # e.g., 7 for "7-day streak"
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentAchievement(db.Model):
    __tablename__ = "student_achievements"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    achievement_id = db.Column(db.Integer, db.ForeignKey("achievements.id"))
    
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship("Student", backref="earned_achievements")
    achievement = db.relationship("Achievement")


# ============================================================
# ACTIVITY LOG
# ============================================================

class ActivityLog(db.Model):
    __tablename__ = "activity_log"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    
    activity_type = db.Column(db.String(50))  # question_answered, assignment_completed, achievement_earned, level_up
    subject = db.Column(db.String(50), nullable=True)
    description = db.Column(db.String(255))
    xp_earned = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship("Student", backref="activities")


# ============================================================
# ARCADE MODE - LEARNING GAMES
# ============================================================

class ArcadeGame(db.Model):
    """Catalog of available arcade games"""
    __tablename__ = "arcade_games"

    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.String(50), unique=True)  # speed_math, vocab_builder, etc.
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    subject = db.Column(db.String(50))  # math, science, reading, writing
    icon = db.Column(db.String(50))  # emoji
    difficulty_levels = db.Column(db.String(100))  # JSON array of grade ranges
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GameSession(db.Model):
    """Individual game play sessions with scores"""
    __tablename__ = "game_sessions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    game_key = db.Column(db.String(50))  # References ArcadeGame.game_key

    # Game metadata
    grade_level = db.Column(db.String(10))
    difficulty = db.Column(db.String(20))  # easy, medium, hard
    game_mode = db.Column(db.String(20), default="timed")  # timed, practice, challenge

    # Performance metrics
    score = db.Column(db.Integer)
    time_seconds = db.Column(db.Integer)
    accuracy = db.Column(db.Float)  # Percentage
    questions_answered = db.Column(db.Integer)
    questions_correct = db.Column(db.Integer)

    # Power-ups used (JSON array of powerup_keys)
    powerups_used = db.Column(db.Text, nullable=True)

    # Rewards
    xp_earned = db.Column(db.Integer, default=0)
    tokens_earned = db.Column(db.Integer, default=0)

    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    # Relationships
    student = db.relationship("Student", backref="game_sessions")


class GameLeaderboard(db.Model):
    """High scores and leaderboard tracking"""
    __tablename__ = "game_leaderboards"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    game_key = db.Column(db.String(50))
    grade_level = db.Column(db.String(10))
    difficulty = db.Column(db.String(20))  # easy, medium, hard

    # Best scores
    high_score = db.Column(db.Integer)
    best_time = db.Column(db.Integer)  # Fastest completion in seconds
    best_accuracy = db.Column(db.Float)
    total_plays = db.Column(db.Integer, default=0)

    # Last updated
    last_played = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student = db.relationship("Student", backref="leaderboard_entries")


class PracticeSession(db.Model):
    """Student self-created practice sessions from Learning Planets"""
    __tablename__ = "practice_sessions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)

    # Practice metadata
    subject = db.Column(db.String(50))  # e.g., "math_haven", "atom_sphere"
    topic = db.Column(db.String(200))  # What they practiced
    grade_level = db.Column(db.String(10))
    mode = db.Column(db.String(20))  # quick, full, timed, teach, related, interactive

    # Performance metrics
    total_questions = db.Column(db.Integer)
    questions_answered = db.Column(db.Integer, default=0)
    questions_correct = db.Column(db.Integer, default=0)
    score_percent = db.Column(db.Float)  # Overall percentage

    # Time tracking
    time_spent_seconds = db.Column(db.Integer)  # Total time spent

    # Completion status
    completed = db.Column(db.Boolean, default=False)

    # Practice data (JSON storage of questions and answers)
    practice_data_json = db.Column(db.Text, nullable=True)  # Full practice session data
    answers_json = db.Column(db.Text, nullable=True)  # Student answers

    # Timestamps
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    student = db.relationship("Student", backref="practice_sessions")


class HomeschoolLessonPlan(db.Model):
    """AI-generated and manual lesson plans for homeschool parents"""
    __tablename__ = "homeschool_lesson_plans"

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("parents.id"), nullable=False)

    # Basic Info
    title = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(50))  # math, science, history, etc.
    grade_level = db.Column(db.String(20))
    topic = db.Column(db.Text)
    duration = db.Column(db.Integer)  # Duration in minutes

    # Lesson Content (stored as JSON for flexibility)
    objectives = db.Column(db.JSON)  # List of learning objectives
    materials = db.Column(db.JSON)  # List of materials needed
    activities = db.Column(db.JSON)  # Structured lesson activities
    discussion_questions = db.Column(db.JSON)  # List of questions
    assessment = db.Column(db.Text)  # Assessment ideas
    homework = db.Column(db.Text)  # Homework/practice suggestions
    extensions = db.Column(db.Text)  # Extension activities

    # Teaching Notes
    notes = db.Column(db.Text)  # Teacher's private notes
    biblical_integration = db.Column(db.Text, nullable=True)  # Optional Bible verses/principles

    # Metadata
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed
    is_favorite = db.Column(db.Boolean, default=False)
    tags = db.Column(db.JSON)  # Custom tags
    source = db.Column(db.String(20), default='ai_generated')  # ai_generated, manual, imported

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    taught_date = db.Column(db.DateTime, nullable=True)

    # Relationships
    parent = db.relationship("Parent", backref="homeschool_lesson_plans")


# ============================================================
# ASSIGNMENT TEMPLATES (SHARED: TEACHERS & HOMESCHOOL)
# ============================================================

class AssignmentTemplate(db.Model):
    """
    Reusable assignment templates for teachers and homeschool parents.
    Allows saving successful assignments as templates for future use.
    Supports private templates and optional public library sharing.
    """
    __tablename__ = "assignment_templates"

    id = db.Column(db.Integer, primary_key=True)

    # Owner (either teacher OR parent, not both)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("parents.id"), nullable=True)

    # Template metadata
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(50))  # num_forge, atom_sphere, ink_haven, etc.
    grade_level = db.Column(db.String(20))  # K, 1, 2, 3, ... 12

    # Full assignment data stored as JSON
    # Includes: questions, difficulty, differentiation settings, instructions, etc.
    template_data = db.Column(db.Text, nullable=False)  # JSON string

    # Sharing & Discovery
    is_public = db.Column(db.Boolean, default=False)  # Public library templates
    use_count = db.Column(db.Integer, default=0)  # How many times duplicated

    # Categorization
    tags = db.Column(db.Text, nullable=True)  # JSON array: ["fractions", "word_problems"]

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    teacher = db.relationship("Teacher", backref="assignment_templates", lazy=True)
    parent = db.relationship("Parent", backref="assignment_templates", lazy=True)


# ============================================================
# ARCADE MODE ENHANCEMENTS - BADGES, POWERUPS, CHALLENGES
# ============================================================

class ArcadeBadge(db.Model):
    """Achievement badges specific to arcade games"""
    __tablename__ = "arcade_badges"

    id = db.Column(db.Integer, primary_key=True)
    badge_key = db.Column(db.String(50), unique=True)  # perfect_score, speed_demon, etc.
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    icon = db.Column(db.String(50))  # emoji
    category = db.Column(db.String(50))  # score, speed, accuracy, streak, mastery

    # Requirements
    requirement_type = db.Column(db.String(50))  # score, accuracy, time, streak, total_plays
    requirement_value = db.Column(db.Integer)
    game_key = db.Column(db.String(50), nullable=True)  # null = applies to all games

    # Badge tier
    tier = db.Column(db.String(20))  # bronze, silver, gold, platinum

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentBadge(db.Model):
    """Tracks which badges students have earned"""
    __tablename__ = "student_badges"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    badge_id = db.Column(db.Integer, db.ForeignKey("arcade_badges.id"))
    game_key = db.Column(db.String(50), nullable=True)  # Which game it was earned in

    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    student = db.relationship("Student", backref="arcade_badges")
    badge = db.relationship("ArcadeBadge")


class PowerUp(db.Model):
    """Available power-ups that can be purchased with tokens"""
    __tablename__ = "powerups"

    id = db.Column(db.Integer, primary_key=True)
    powerup_key = db.Column(db.String(50), unique=True)  # freeze_time, fifty_fifty, skip_question
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    icon = db.Column(db.String(50))  # emoji

    # Cost and effect
    token_cost = db.Column(db.Integer)  # How many tokens to purchase
    effect_duration = db.Column(db.Integer, nullable=True)  # Seconds (for time-based effects)
    uses_per_game = db.Column(db.Integer, default=1)  # How many times can be used per game

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentPowerUp(db.Model):
    """Tracks student's power-up inventory"""
    __tablename__ = "student_powerups"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    powerup_id = db.Column(db.Integer, db.ForeignKey("powerups.id"))

    quantity = db.Column(db.Integer, default=1)  # How many they own

    # Relationships
    student = db.relationship("Student", backref="powerups")
    powerup = db.relationship("PowerUp")


class DailyChallenge(db.Model):
    """Special daily challenges with bonus rewards"""
    __tablename__ = "daily_challenges"

    id = db.Column(db.Integer, primary_key=True)
    game_key = db.Column(db.String(50))
    challenge_date = db.Column(db.Date, unique=True)  # One challenge per day

    # Challenge requirements
    target_score = db.Column(db.Integer, nullable=True)
    target_accuracy = db.Column(db.Float, nullable=True)
    target_time = db.Column(db.Integer, nullable=True)
    grade_level = db.Column(db.String(10))
    difficulty = db.Column(db.String(20))  # easy, medium, hard

    # Rewards
    bonus_xp = db.Column(db.Integer, default=100)
    bonus_tokens = db.Column(db.Integer, default=50)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudentChallengeProgress(db.Model):
    """Tracks student progress on daily challenges"""
    __tablename__ = "student_challenge_progress"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    challenge_id = db.Column(db.Integer, db.ForeignKey("daily_challenges.id"))

    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Best attempt stats
    best_score = db.Column(db.Integer)
    best_accuracy = db.Column(db.Float)
    best_time = db.Column(db.Integer)

    # Relationships
    student = db.relationship("Student", backref="daily_challenges")
    challenge = db.relationship("DailyChallenge")


class GameStreak(db.Model):
    """Tracks consecutive days of gameplay"""
    __tablename__ = "game_streaks"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), unique=True)

    current_streak = db.Column(db.Integer, default=0)
    longest_streak = db.Column(db.Integer, default=0)
    last_played_date = db.Column(db.Date, nullable=True)

    # Relationships
    student = db.relationship("Student", backref="game_streak", uselist=False)


# ============================================================
# ASYNCHRONOUS MULTIPLAYER MODELS
# ============================================================

class AsyncChallenge(db.Model):
    """
    Asynchronous multiplayer challenges.
    Challenger plays first, friends attempt later with same questions.
    """
    __tablename__ = 'async_challenges'

    id = db.Column(db.Integer, primary_key=True)
    challenger_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    game_key = db.Column(db.String(100), nullable=False)  # Which game
    difficulty = db.Column(db.String(20), nullable=False)  # easy/medium/hard
    questions_json = db.Column(db.Text, nullable=False)  # Exact questions as JSON
    challenger_score = db.Column(db.Integer, nullable=False)
    challenger_time = db.Column(db.Float, nullable=False)  # Time in seconds
    expires_at = db.Column(db.DateTime, nullable=False)  # 24-48 hour expiry
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed, expired

    # Relationships
    challenger = db.relationship('Student', backref='challenges_created')
    participants = db.relationship('ChallengeParticipant', backref='challenge', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<AsyncChallenge {self.id} by student {self.challenger_id}>'


class ChallengeParticipant(db.Model):
    """
    Tracks who's been challenged and their results
    """
    __tablename__ = 'challenge_participants'

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('async_challenges.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    score = db.Column(db.Integer)  # NULL until they complete
    time_taken = db.Column(db.Float)  # Time in seconds
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)
    viewed = db.Column(db.Boolean, default=False)  # Have they seen the challenge?
    viewed_at = db.Column(db.DateTime)

    # Relationships
    student = db.relationship('Student', backref='challenges_received')

    def __repr__(self):
        return f'<ChallengeParticipant student={self.student_id} challenge={self.challenge_id}>'


class ArcadeTeam(db.Model):
    """
    Teams for team battles (2v2, 3v3, etc.)
    """
    __tablename__ = 'arcade_teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_code = db.Column(db.String(10), unique=True, nullable=False)  # Join code
    captain_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    team_type = db.Column(db.String(50), default='custom')  # family, coop, classroom, custom
    max_members = db.Column(db.Integer, default=4)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    active = db.Column(db.Boolean, default=True)

    # Relationships
    captain = db.relationship('Student', backref='teams_led')
    members = db.relationship('TeamMember', backref='team', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<ArcadeTeam {self.name}>'


class TeamMember(db.Model):
    """
    Members of arcade teams
    """
    __tablename__ = 'team_members'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('arcade_teams.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    role = db.Column(db.String(20), default='member')  # captain, member
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    student = db.relationship('Student', backref='team_memberships')

    def __repr__(self):
        return f'<TeamMember student={self.student_id} team={self.team_id}>'


class TeamMatch(db.Model):
    """
    Team vs Team battles
    """
    __tablename__ = 'team_matches'

    id = db.Column(db.Integer, primary_key=True)
    team_a_id = db.Column(db.Integer, db.ForeignKey('arcade_teams.id'), nullable=False)
    team_b_id = db.Column(db.Integer, db.ForeignKey('arcade_teams.id'), nullable=False)
    game_key = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    team_a_score = db.Column(db.Integer, default=0)
    team_b_score = db.Column(db.Integer, default=0)
    winner_team_id = db.Column(db.Integer, db.ForeignKey('arcade_teams.id'))
    match_status = db.Column(db.String(20), default='waiting')  # waiting, active, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime)

    # Relationships
    team_a = db.relationship('ArcadeTeam', foreign_keys=[team_a_id])
    team_b = db.relationship('ArcadeTeam', foreign_keys=[team_b_id])
    winner_team = db.relationship('ArcadeTeam', foreign_keys=[winner_team_id])

    def __repr__(self):
        return f'<TeamMatch {self.team_a_id} vs {self.team_b_id}>'


# ============================================================
# AUDIT LOG
# ============================================================

class AuditLog(db.Model):
    """
    Audit trail for critical actions (security, data changes, etc.)
    """
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)

    # Who performed the action
    user_id = db.Column(db.Integer, nullable=False)  # ID of user
    user_type = db.Column(db.String(20), nullable=False)  # 'teacher', 'student', 'parent', 'admin'
    user_email = db.Column(db.String(120), nullable=True)  # For quick reference

    # What action was performed
    action = db.Column(db.String(100), nullable=False)  # e.g., 'login', 'delete_class', 'grade_submission'
    resource_type = db.Column(db.String(50), nullable=True)  # e.g., 'class', 'assignment', 'student'
    resource_id = db.Column(db.Integer, nullable=True)  # ID of affected resource

    # Additional context
    details = db.Column(db.Text, nullable=True)  # JSON or text with additional context
    ip_address = db.Column(db.String(45), nullable=True)  # Support IPv6
    user_agent = db.Column(db.Text, nullable=True)

    # Status of action
    status = db.Column(db.String(20), nullable=False, default='success')  # 'success', 'failed', 'blocked'
    error_message = db.Column(db.Text, nullable=True)  # If action failed

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<AuditLog {self.user_type}:{self.user_id} {self.action} {self.status}>'


# ============================================================
# LEARNING LAB - Learning Preferences & Strategies
# ============================================================

class LearningProfile(db.Model):
    """
    Stores student's learning preferences and strategies that work for them.

    IMPORTANT: This does NOT diagnose learning disabilities or medical conditions.
    It tracks preferences, strengths, and helpful strategies discovered by the student.
    """
    __tablename__ = 'learning_profiles'
    __table_args__ = (
        db.Index('idx_learning_profile_student', 'student_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False)

    # Quiz completion
    quiz_completed = db.Column(db.Boolean, default=False)
    quiz_completed_at = db.Column(db.DateTime, nullable=True)

    # Learning Style Preferences (based on quiz responses, not diagnosis)
    primary_learning_style = db.Column(db.String(50), nullable=True)  # visual/auditory/kinesthetic/reading_writing
    secondary_learning_style = db.Column(db.String(50), nullable=True)

    # Study Preferences
    focus_preference = db.Column(db.String(50), nullable=True)  # short_bursts/long_sessions/varies
    best_study_time = db.Column(db.String(50), nullable=True)  # morning/afternoon/evening/night
    study_environment = db.Column(db.String(50), nullable=True)  # quiet/music/nature_sounds/noise
    break_frequency = db.Column(db.String(50), nullable=True)  # every_15_min/every_30_min/every_hour/rarely

    # Processing Preferences
    processing_speed = db.Column(db.String(50), nullable=True)  # fast/moderate/methodical
    prefers_step_by_step = db.Column(db.Boolean, default=False)
    prefers_big_picture = db.Column(db.Boolean, default=False)

    # Memory Preferences
    memory_style = db.Column(db.String(50), nullable=True)  # visual/verbal/hands_on/mixed
    uses_mnemonics = db.Column(db.Boolean, default=False)

    # Reading Preferences
    reading_preference = db.Column(db.String(50), nullable=True)  # text_only/audio_support/visual_aids/all
    prefers_large_text = db.Column(db.Boolean, default=False)
    prefers_colored_backgrounds = db.Column(db.Boolean, default=False)

    # Tool Usage (tracks what student actually uses)
    uses_text_to_speech = db.Column(db.Boolean, default=False)
    uses_focus_timer = db.Column(db.Boolean, default=False)
    uses_task_breakdown = db.Column(db.Boolean, default=False)
    uses_visual_organizers = db.Column(db.Boolean, default=False)
    uses_movement_breaks = db.Column(db.Boolean, default=False)

    # Effective Strategies (JSON array of strategy keys that work for this student)
    effective_strategies = db.Column(db.Text, nullable=True)  # JSON: ["pomodoro", "movement_breaks", "visual_notes"]

    # Profile strengths summary (generated after quiz)
    strengths_summary = db.Column(db.Text, nullable=True)  # Friendly text describing student's learning superpowers

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student = db.relationship("Student", backref=db.backref("learning_profile", uselist=False))

    def __repr__(self):
        return f'<LearningProfile student_id={self.student_id} style={self.primary_learning_style}>'


class StudentSubjectProgress(db.Model):
    """
    Tracks student progress and activity per subject for the subjects page.
    Calculates mastery, XP, and last visit time for each learning planet.
    """
    __tablename__ = 'student_subject_progress'
    __table_args__ = (
        db.Index('idx_subject_progress_student', 'student_id'),
        db.Index('idx_subject_progress_subject', 'subject_key'),
        db.Index('idx_subject_progress_student_subject', 'student_id', 'subject_key'),
        db.UniqueConstraint('student_id', 'subject_key', name='uq_student_subject'),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    subject_key = db.Column(db.String(50), nullable=False)  # num_forge, atom_sphere, etc.

    # Activity tracking
    questions_answered = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)
    total_time_minutes = db.Column(db.Integer, default=0)  # Total study time
    last_visited = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Progress metrics
    xp_earned = db.Column(db.Integer, default=0)
    mastery_percentage = db.Column(db.Integer, default=0)  # 0-100

    # Milestones
    lessons_completed = db.Column(db.Integer, default=0)
    chapters_completed = db.Column(db.Integer, default=0)

    # Timestamps
    first_visit = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student = db.relationship("Student", backref="subject_progress")

    def __repr__(self):
        return f'<StudentSubjectProgress student_id={self.student_id} subject={self.subject_key} mastery={self.mastery_percentage}%>'


class StrategyUsage(db.Model):
    """
    Tracks when students use different learning strategies and how helpful they find them.
    Helps identify which strategies work best for each student.
    """
    __tablename__ = 'strategy_usage'
    __table_args__ = (
        db.Index('idx_strategy_usage_student', 'student_id'),
        db.Index('idx_strategy_usage_key', 'strategy_key'),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)

    strategy_key = db.Column(db.String(100), nullable=False)  # e.g., "pomodoro_timer", "text_to_speech", "visual_notes"
    category = db.Column(db.String(50), nullable=True)  # focus/reading/memory/organization/etc

    # Usage tracking
    times_used = db.Column(db.Integer, default=1)
    first_used_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Effectiveness (student can rate how helpful it was)
    helpfulness_rating = db.Column(db.Integer, nullable=True)  # 1-5 stars, null if not rated
    student_notes = db.Column(db.Text, nullable=True)  # Student's own notes about the strategy

    # Relationships
    student = db.relationship("Student", backref="strategy_usage_logs")

    def __repr__(self):
        return f'<StrategyUsage student={self.student_id} strategy={self.strategy_key} used={self.times_used}x>'


class PomodoroSession(db.Model):
    """
    Tracks Pomodoro timer sessions for focus tracking and analytics.
    """
    __tablename__ = 'pomodoro_session'
    __table_args__ = (
        db.Index('idx_pomodoro_student_date', 'student_id', 'session_date'),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    session_date = db.Column(db.DateTime, default=datetime.utcnow)
    work_duration = db.Column(db.Integer)  # minutes completed
    break_duration = db.Column(db.Integer)  # minutes
    completed = db.Column(db.Boolean, default=False)
    interrupted = db.Column(db.Boolean, default=False)
    focus_rating = db.Column(db.Integer, nullable=True)  # 1-5, self-reported

    student = db.relationship('Student', backref='pomodoro_sessions')

    def __repr__(self):
        return f'<PomodoroSession student={self.student_id} duration={self.work_duration}min completed={self.completed}>'


class StudyBuddyConversation(db.Model):
    """
    Represents a conversation thread in AI Study Buddy.
    Students can have multiple conversations on different topics.
    """
    __tablename__ = 'study_buddy_conversation'
    __table_args__ = (
        db.Index('idx_conversation_student_created', 'student_id', 'created_at'),
        db.Index('idx_conversation_student_updated', 'student_id', 'last_message_at'),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(200), nullable=False)  # Auto-generated from first question
    subject = db.Column(db.String(50), nullable=True)  # Detected subject area
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    message_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)  # Current conversation
    archived = db.Column(db.Boolean, default=False)

    student = db.relationship('Student', backref='study_buddy_conversations')
    messages = db.relationship('StudyBuddyMessage', backref='conversation', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<StudyBuddyConversation id={self.id} student={self.student_id} title="{self.title}">'


class StudyBuddyMessage(db.Model):
    """
    Stores AI Study Buddy conversation history.
    """
    __tablename__ = 'study_buddy_message'
    __table_args__ = (
        db.Index('idx_study_buddy_student_time', 'student_id', 'timestamp'),
        db.Index('idx_study_buddy_conversation', 'conversation_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey("study_buddy_conversation.id", ondelete="CASCADE"), nullable=True)
    message = db.Column(db.Text, nullable=False)
    is_student = db.Column(db.Boolean, nullable=False)  # True = from student, False = from AI
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    topic = db.Column(db.String(100), nullable=True)  # What topic was discussed
    learning_style_used = db.Column(db.String(50), nullable=True)  # Which style AI adapted to
    helpful_rating = db.Column(db.Integer, nullable=True)  # Student feedback on AI response

    # SAFETY & MODERATION FIELDS
    flagged = db.Column(db.Boolean, default=False)  # Content moderation flag
    flagged_reason = db.Column(db.String(200), nullable=True)  # Why it was flagged
    moderation_scores = db.Column(db.JSON, nullable=True)  # OpenAI moderation API scores
    parent_notified = db.Column(db.Boolean, default=False)  # Parent notification sent
    reviewed = db.Column(db.Boolean, default=False)  # Admin reviewed
    reviewer_notes = db.Column(db.Text, nullable=True)  # Admin notes

    student = db.relationship('Student', backref='study_buddy_messages')

    def __repr__(self):
        return f'<StudyBuddyMessage student={self.student_id} from_student={self.is_student} flagged={self.flagged}>'


class TaskBreakdown(db.Model):
    """
    AI-generated task breakdowns for assignments.
    """
    __tablename__ = 'task_breakdown'
    __table_args__ = (
        db.Index('idx_task_breakdown_student', 'student_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    assignment_id = db.Column(db.Integer, nullable=True)  # Optional link to assignment
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    student = db.relationship('Student', backref='task_breakdowns')
    steps = db.relationship('TaskStep', backref='breakdown', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<TaskBreakdown id={self.id} title="{self.title}" completed={self.completed}>'


class TaskStep(db.Model):
    """
    Individual steps in a task breakdown.
    """
    __tablename__ = 'task_step'

    id = db.Column(db.Integer, primary_key=True)
    breakdown_id = db.Column(db.Integer, db.ForeignKey("task_breakdown.id", ondelete="CASCADE"), nullable=False)
    step_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    estimated_minutes = db.Column(db.Integer, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    actual_minutes = db.Column(db.Integer, nullable=True)  # How long it actually took

    def __repr__(self):
        return f'<TaskStep breakdown={self.breakdown_id} step={self.step_number} completed={self.completed}>'


class AIAssignment(db.Model):
    """
    AI-generated multi-modal assignments for teachers.
    """
    __tablename__ = 'ai_assignment'
    __table_args__ = (
        db.Index('idx_ai_assignment_teacher', 'teacher_id'),
    )

    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    topic = db.Column(db.String(200), nullable=False)
    grade_level = db.Column(db.String(20))
    subject = db.Column(db.String(100), nullable=True)
    objectives = db.Column(db.Text)
    generated_content = db.Column(db.JSON)  # All 4 learning style versions
    rubric = db.Column(db.JSON)  # Scoring rubric
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)  # Has teacher shared it with students

    teacher = db.relationship('Teacher', backref='ai_assignments')

    def __repr__(self):
        return f'<AIAssignment id={self.id} topic="{self.topic}" teacher={self.teacher_id}>'


# ============================================================
# ADMIN USERS
# ============================================================

class Admin(db.Model):
    """
    Admin users with full system access.
    Separate from teachers/parents/students for better security.
    """
    __tablename__ = "admins"
    __table_args__ = (
        db.Index('idx_admin_email', 'email'),
        db.Index('idx_admin_username', 'username'),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Admin metadata
    full_name = db.Column(db.String(120))
    is_active = db.Column(db.Boolean, default=True)
    is_super_admin = db.Column(db.Boolean, default=False)  # Super admin can manage other admins

    # Security tracking
    last_login = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(45))  # IPv6 compatible
    failed_login_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime)  # Account lockout after too many failed attempts

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('admins.id'))  # Which admin created this admin
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    creator = db.relationship('Admin', remote_side=[id], backref='created_admins')

    def __repr__(self):
        return f'<Admin id={self.id} username="{self.username}" email="{self.email}">'

    def is_locked(self):
        """Check if account is currently locked"""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False


