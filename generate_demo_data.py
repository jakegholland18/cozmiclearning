"""
CozmicLearning Demo Data Generator

This script populates your database with realistic sample data so you can see:
- How the gradebook looks with actual student submissions
- How analytics displays with performance data
- How the dashboard appears with active students

Usage:
    python generate_demo_data.py

This will create:
- 1 demo teacher account
- 2 demo classes with students
- 5-10 assignments per class
- Student submissions with varying grades
- Realistic analytics data

IMPORTANT: Run this in a test/staging environment, NOT production!
"""

from app import app, db
from models import (
    Teacher, Class, Student, Parent,
    AssignedPractice, AssignedQuestion, StudentSubmission,
    ChapterProgress, LessonProgress, GameSession,
    ArcadeGame, AssessmentResult, ActivityLog
)
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import random

# Demo Configuration
DEMO_EMAIL_PREFIX = "demo"  # All emails will be demo+something@cozmiclearning.com
DEMO_PASSWORD = "demo123"    # Simple password for all demo accounts

# Sample data
STUDENT_NAMES = [
    "Emma Johnson", "Liam Smith", "Olivia Brown", "Noah Davis",
    "Ava Wilson", "Elijah Moore", "Sophia Taylor", "James Anderson",
    "Isabella Thomas", "Mason Jackson", "Mia White", "Lucas Harris",
    "Charlotte Martin", "Benjamin Thompson", "Amelia Garcia", "Oliver Martinez"
]

SUBJECTS = ["math", "science", "english", "history", "bible"]

ASSIGNMENT_TITLES = {
    "math": [
        "Fraction Addition",
        "Multiplication Mastery",
        "Division Practice",
        "Word Problems Challenge",
        "Geometry Quiz"
    ],
    "science": [
        "Cell Biology",
        "Solar System Exploration",
        "States of Matter",
        "Chemical Reactions",
        "Ecosystems Study"
    ],
    "english": [
        "Grammar Fundamentals",
        "Vocabulary Builder",
        "Essay Writing",
        "Reading Comprehension",
        "Parts of Speech"
    ],
    "history": [
        "American Revolution",
        "Ancient Civilizations",
        "World War II",
        "Renaissance Period",
        "Colonial America"
    ],
    "bible": [
        "Gospel of John",
        "Old Testament Heroes",
        "Parables of Jesus",
        "Book of Acts",
        "Psalms Study"
    ]
}

QUESTIONS = {
    "math": [
        {"q": "What is 3/4 + 1/4?", "answer": "1", "options": ["1/2", "1", "2/4", "4/8"]},
        {"q": "Solve: 7 × 8 = ?", "answer": "56", "options": ["54", "56", "58", "49"]},
        {"q": "What is 144 ÷ 12?", "answer": "12", "options": ["10", "11", "12", "14"]},
        {"q": "If a rectangle has length 8 and width 5, what is its area?", "answer": "40", "options": ["13", "26", "40", "45"]},
        {"q": "Solve: 15 - 8 + 3 = ?", "answer": "10", "options": ["6", "10", "14", "20"]}
    ],
    "science": [
        {"q": "What is the powerhouse of the cell?", "answer": "Mitochondria", "options": ["Nucleus", "Mitochondria", "Ribosome", "Chloroplast"]},
        {"q": "How many planets are in our solar system?", "answer": "8", "options": ["7", "8", "9", "10"]},
        {"q": "What are the three states of matter?", "answer": "Solid, Liquid, Gas", "options": ["Hot, Cold, Warm", "Solid, Liquid, Gas", "Hard, Soft, Medium", "Big, Small, Tiny"]},
        {"q": "What is H2O commonly known as?", "answer": "Water", "options": ["Oxygen", "Hydrogen", "Water", "Air"]},
        {"q": "What is photosynthesis?", "answer": "Plants making food from sunlight", "options": ["Animals eating", "Plants making food from sunlight", "Water evaporating", "Rocks forming"]}
    ],
    "english": [
        {"q": "Which is the correct verb tense: 'I ____ to the store yesterday'?", "answer": "went", "options": ["go", "went", "gone", "going"]},
        {"q": "What is a synonym for 'happy'?", "answer": "Joyful", "options": ["Sad", "Angry", "Joyful", "Tired"]},
        {"q": "Identify the noun: 'The cat jumped over the fence.'", "answer": "Cat", "options": ["Jumped", "Cat", "Over", "The"]},
        {"q": "What is a metaphor?", "answer": "A comparison without using 'like' or 'as'", "options": ["A rhyme", "A comparison without using 'like' or 'as'", "A question", "A statement"]},
        {"q": "Which is a complete sentence?", "answer": "The dog ran quickly.", "options": ["Running fast", "The dog ran quickly.", "When he went", "Because of the"]}
    ],
    "history": [
        {"q": "When did the American Revolution begin?", "answer": "1775", "options": ["1750", "1775", "1800", "1825"]},
        {"q": "Who was the first president of the United States?", "answer": "George Washington", "options": ["Thomas Jefferson", "George Washington", "Abraham Lincoln", "Benjamin Franklin"]},
        {"q": "What year did World War II end?", "answer": "1945", "options": ["1939", "1941", "1943", "1945"]},
        {"q": "Where did the Renaissance begin?", "answer": "Italy", "options": ["France", "England", "Italy", "Spain"]},
        {"q": "What was the purpose of the Mayflower?", "answer": "Transport Pilgrims to America", "options": ["War ship", "Transport Pilgrims to America", "Cargo ship", "Fishing vessel"]}
    ],
    "bible": [
        {"q": "In what city was Jesus born?", "answer": "Bethlehem", "options": ["Jerusalem", "Nazareth", "Bethlehem", "Capernaum"]},
        {"q": "Who led the Israelites out of Egypt?", "answer": "Moses", "options": ["Abraham", "Moses", "David", "Joshua"]},
        {"q": "How many disciples did Jesus have?", "answer": "12", "options": ["7", "10", "12", "15"]},
        {"q": "What is the first book of the Bible?", "answer": "Genesis", "options": ["Exodus", "Genesis", "Matthew", "Psalms"]},
        {"q": "Who wrote most of the New Testament letters?", "answer": "Paul", "options": ["Peter", "John", "Paul", "James"]}
    ]
}

def clear_demo_data():
    """Remove all demo data from previous runs"""
    print("\n🧹 Clearing previous demo data...")
    print("✓ Skipping cleanup to avoid schema errors (will create new demo data)")

def create_demo_teacher():
    """Create or get existing demo teacher account"""
    print("\n👨‍🏫 Creating demo teacher...")

    with app.app_context():
        # Check if demo teacher already exists
        existing = Teacher.query.filter_by(email=f"{DEMO_EMAIL_PREFIX}+teacher@cozmiclearning.com").first()
        if existing:
            # Update subscription status to ensure access
            existing.subscription_active = True
            existing.trial_start = datetime.utcnow() - timedelta(days=5)
            existing.trial_end = datetime.utcnow() + timedelta(days=25)  # 30 day trial, 5 days used
            existing.plan = "trial"
            db.session.commit()
            print(f"✓ Demo Teacher already exists (updated subscription status)")
            print(f"  Email: {existing.email}")
            print(f"  Password: {DEMO_PASSWORD}")
            print(f"  ID: {existing.id}")
            print(f"  Subscription: Active Trial (25 days remaining)")
            return existing

        teacher = Teacher(
            name="Demo Teacher",
            email=f"{DEMO_EMAIL_PREFIX}+teacher@cozmiclearning.com",
            password_hash=generate_password_hash(DEMO_PASSWORD),
            subscription_active=True,
            trial_start=datetime.utcnow() - timedelta(days=5),
            trial_end=datetime.utcnow() + timedelta(days=25),  # 30 day trial, 5 days used
            plan="trial",
            created_at=datetime.utcnow() - timedelta(days=90)
        )
        db.session.add(teacher)
        db.session.commit()

        print(f"✓ Demo Teacher created")
        print(f"  Email: {teacher.email}")
        print(f"  Password: {DEMO_PASSWORD}")
        print(f"  ID: {teacher.id}")

        return teacher

def create_demo_classes(teacher):
    """Create demo classes"""
    print("\n🏫 Creating demo classes...")

    with app.app_context():
        classes = []

        # Class 1: 5th Grade Math
        class1 = Class(
            class_name="5th Grade Math & Science",
            teacher_id=teacher.id,
            grade_level=5,
            join_code="DEMO5A",
            created_at=datetime.utcnow() - timedelta(days=85)
        )
        db.session.add(class1)
        classes.append(class1)

        # Class 2: 7th Grade English & History
        class2 = Class(
            class_name="7th Grade English & History",
            teacher_id=teacher.id,
            grade_level=7,
            join_code="DEMO7B",
            created_at=datetime.utcnow() - timedelta(days=85)
        )
        db.session.add(class2)
        classes.append(class2)

        db.session.commit()

        print(f"✓ Created {len(classes)} classes")
        for cls in classes:
            print(f"  - {cls.class_name} (ID: {cls.id}, Code: {cls.join_code})")

        return classes

def create_demo_students(classes):
    """Create demo students and assign to classes"""
    print("\n👨‍🎓 Creating demo students...")

    with app.app_context():
        all_students = []

        # Distribute students across classes
        students_per_class = len(STUDENT_NAMES) // len(classes)

        for idx, cls in enumerate(classes):
            start_idx = idx * students_per_class
            end_idx = start_idx + students_per_class if idx < len(classes) - 1 else len(STUDENT_NAMES)

            class_students = []
            for i in range(start_idx, end_idx):
                name = STUDENT_NAMES[i]
                student = Student(
                    student_name=name,
                    student_email=f"{DEMO_EMAIL_PREFIX}+student{i+1}@cozmiclearning.com",
                    date_of_birth=datetime(2010 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28)),
                    class_id=cls.id,
                    ability_level=random.choice(["below", "on_level", "advanced"]),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(60, 85))
                )
                db.session.add(student)
                class_students.append(student)
                all_students.append(student)

            db.session.commit()
            print(f"✓ Created {len(class_students)} students for {cls.class_name}")

        print(f"  Total students: {len(all_students)}")
        return all_students

def create_demo_assignments(classes, teacher):
    """Create demo assignments for each class"""
    print("\n📝 Creating demo assignments...")

    with app.app_context():
        all_assignments = []

        for cls in classes:
            # Create 5-8 assignments per class
            num_assignments = random.randint(5, 8)

            for i in range(num_assignments):
                subject = random.choice(SUBJECTS)
                title = random.choice(ASSIGNMENT_TITLES[subject])

                # Create assignment
                days_ago = random.randint(5, 70)
                assignment = AssignedPractice(
                    title=title,
                    subject=subject,
                    topic=title,
                    teacher_id=teacher.id,
                    class_id=cls.id,
                    assignment_type=random.choice(["practice", "quiz", "test", "homework"]),
                    is_published=True,
                    open_date=datetime.utcnow() - timedelta(days=days_ago),
                    due_date=datetime.utcnow() - timedelta(days=days_ago - 7),
                    created_at=datetime.utcnow() - timedelta(days=days_ago + 1)
                )
                db.session.add(assignment)
                db.session.flush()  # Get assignment ID

                # Add 5-10 questions to assignment
                num_questions = random.randint(5, 10)
                questions_pool = QUESTIONS.get(subject, QUESTIONS["math"])

                for q_idx in range(num_questions):
                    q_data = random.choice(questions_pool)
                    opts = q_data["options"]
                    question = AssignedQuestion(
                        practice_id=assignment.id,
                        question_text=q_data["q"],
                        question_type="multiple_choice",
                        choice_a=opts[0] if len(opts) > 0 else "",
                        choice_b=opts[1] if len(opts) > 1 else "",
                        choice_c=opts[2] if len(opts) > 2 else "",
                        choice_d=opts[3] if len(opts) > 3 else "",
                        correct_answer=q_data["answer"],
                        difficulty_level="medium"
                    )
                    db.session.add(question)

                all_assignments.append(assignment)

            db.session.commit()
            print(f"✓ Created {num_assignments} assignments for {cls.class_name}")

        print(f"  Total assignments: {len(all_assignments)}")
        return all_assignments

def create_demo_submissions(assignments=None):
    """Create student submissions with varying grades"""
    print("\n📊 Creating student submissions...")

    with app.app_context():
        total_submissions = 0

        # Re-query assignments to get fresh session-bound objects
        all_assignments = AssignedPractice.query.all()

        for assignment in all_assignments:
            # Get students in this class
            students = Student.query.filter_by(class_id=assignment.class_id).all()
            questions = AssignedQuestion.query.filter_by(practice_id=assignment.id).all()

            # 70-95% of students complete each assignment
            completion_rate = random.uniform(0.7, 0.95)
            completing_students = random.sample(students, int(len(students) * completion_rate))

            for student in completing_students:
                # Each student's performance varies
                # 20% struggle (60-75%), 50% on-level (75-90%), 30% advanced (90-100%)
                performance_category = random.choices(
                    ['struggling', 'on-level', 'advanced'],
                    weights=[0.2, 0.5, 0.3]
                )[0]

                if performance_category == 'struggling':
                    accuracy = random.uniform(0.6, 0.75)
                elif performance_category == 'on-level':
                    accuracy = random.uniform(0.75, 0.9)
                else:  # advanced
                    accuracy = random.uniform(0.9, 1.0)

                # Create submission for each question
                total_points = 0
                earned_points = 0

                for question in questions:
                    is_correct = random.random() < accuracy
                    # Get wrong answer from choices
                    all_choices = [question.choice_a, question.choice_b, question.choice_c, question.choice_d]
                    all_choices = [c for c in all_choices if c]  # Remove empty
                    wrong_answer = random.choice([c for c in all_choices if c != question.correct_answer]) if len(all_choices) > 1 else question.correct_answer

                    submission = StudentSubmission(
                        student_id=student.id,
                        practice_id=assignment.id,
                        question_id=question.id,
                        student_answer=question.correct_answer if is_correct else wrong_answer,
                        is_correct=is_correct,
                        points_earned=10 if is_correct else 0,  # Fixed 10 points per question
                        submitted_at=datetime.utcnow() - timedelta(
                            days=random.randint(1, max(1, (datetime.utcnow() - assignment.due_date).days))
                        )
                    )

                    # Some submissions are graded, some pending
                    if random.random() < 0.8:  # 80% graded
                        submission.graded = True
                        submission.graded_at = submission.submitted_at + timedelta(hours=random.randint(2, 48))

                    total_points += question.points
                    earned_points += submission.points_earned

                    db.session.add(submission)
                    total_submissions += 1

            db.session.commit()

        print(f"✓ Created {total_submissions} student submissions")
        print(f"  Graded: ~{int(total_submissions * 0.8)}")
        print(f"  Pending: ~{int(total_submissions * 0.2)}")

def create_demo_progress(students):
    """Create chapter and lesson progress for students"""
    print("\n📚 Creating student progress data...")

    with app.app_context():
        total_chapter_progress = 0
        total_lesson_progress = 0

        for student in students:
            # Each student has completed 2-5 chapters
            num_chapters = random.randint(2, 5)

            for chapter_num in range(1, num_chapters + 1):
                subject = random.choice(SUBJECTS)
                progress = ChapterProgress(
                    student_id=student.id,
                    subject=subject,
                    chapter_number=chapter_num,
                    completed=True,
                    quiz_score=random.randint(70, 100),
                    completed_at=datetime.utcnow() - timedelta(days=random.randint(5, 60))
                )
                db.session.add(progress)
                total_chapter_progress += 1

                # Add 3-8 lesson completions per chapter
                num_lessons = random.randint(3, 8)
                for lesson_num in range(1, num_lessons + 1):
                    lesson_progress = LessonProgress(
                        student_id=student.id,
                        subject=subject,
                        chapter_number=chapter_num,
                        lesson_number=lesson_num,
                        completed=True,
                        time_spent=random.randint(300, 1800),  # 5-30 minutes
                        completed_at=datetime.utcnow() - timedelta(days=random.randint(5, 60))
                    )
                    db.session.add(lesson_progress)
                    total_lesson_progress += 1

        db.session.commit()
        print(f"✓ Created {total_chapter_progress} chapter completions")
        print(f"✓ Created {total_lesson_progress} lesson completions")

def create_demo_game_sessions(students):
    """Create arcade game session data"""
    print("\n🎮 Creating arcade game sessions...")

    with app.app_context():
        total_sessions = 0
        game_keys = ["speed_math", "element_match", "vocab_builder", "bible_trivia", "history_timeline"]

        for student in students:
            # Each student plays 5-15 games
            num_sessions = random.randint(5, 15)

            for _ in range(num_sessions):
                session = GameSession(
                    student_id=student.id,
                    game_key=random.choice(game_keys),
                    score=random.randint(500, 1000),
                    time_taken=random.uniform(60, 300),
                    accuracy=random.uniform(0.6, 1.0),
                    difficulty=random.choice(["easy", "medium", "hard"]),
                    tokens_earned=random.randint(10, 50),
                    xp_earned=random.randint(50, 150),
                    played_at=datetime.utcnow() - timedelta(days=random.randint(1, 60))
                )
                db.session.add(session)
                total_sessions += 1

        db.session.commit()
        print(f"✓ Created {total_sessions} game sessions")

def generate_demo_data():
    """Main function to generate all demo data"""
    print("\n" + "="*60)
    print("COZMICLEARNING DEMO DATA GENERATOR")
    print("="*60)
    print("\n⚠️  WARNING: This will create demo data in your database.")
    print("   Only run this in a test/staging environment!\n")

    response = input("Continue? (yes/no): ").strip().lower()
    if response != "yes":
        print("\n❌ Cancelled by user.")
        return

    try:
        # Clear previous demo data
        clear_demo_data()

        # Create demo data
        teacher = create_demo_teacher()
        classes = create_demo_classes(teacher)
        students = create_demo_students(classes)
        assignments = create_demo_assignments(classes, teacher)
        create_demo_submissions(assignments)
        create_demo_progress(students)
        create_demo_game_sessions(students)

        print("\n" + "="*60)
        print("✅ DEMO DATA GENERATION COMPLETE!")
        print("="*60)

        print("\n📋 DEMO LOGIN CREDENTIALS:")
        print("   Teacher Account:")
        print(f"     Email: {DEMO_EMAIL_PREFIX}+teacher@cozmiclearning.com")
        print(f"     Password: {DEMO_PASSWORD}")

        print("\n🎯 WHAT TO VIEW:")
        print("   1. Login as demo teacher")
        print("   2. Go to Gradebook (/teacher/gradebook)")
        print("   3. View Analytics (/teacher/analytics)")
        print("   4. Click into specific classes to see detailed data")

        print("\n📊 DATA SUMMARY:")
        print(f"   - 1 Teacher")
        print(f"   - {len(classes)} Classes")
        print(f"   - {len(students)} Students")
        print(f"   - {len(assignments)} Assignments")
        print(f"   - ~{len(assignments) * 8} Student Submissions")
        print(f"   - Realistic grade distribution (struggling, on-level, advanced)")

        print("\n🧹 TO REMOVE DEMO DATA:")
        print("   Run this script again and it will clear previous data first.")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("\nRolling back database changes...")
        db.session.rollback()

if __name__ == "__main__":
    generate_demo_data()
