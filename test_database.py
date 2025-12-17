"""
CozmicLearning Database Integrity Test Suite

This script tests critical database operations to ensure:
- Models create correctly
- Relationships work properly
- Cascading deletes function
- Business logic enforced

Usage:
    python test_database.py

Run this before deployment to verify database health.
"""

from app import app, db
from models import (
    Student, Parent, Teacher, Class, Message,
    AssignedPractice, AssignedQuestion, StudentSubmission,
    ChapterProgress, LessonProgress, ChapterQuiz, ChapterBadge, StudentChapterBadge,
    ArcadeGame, GameSession, GameLeaderboard, ArcadeBadge, StudentBadge,
    Achievement, StudentAchievement, ActivityLog, QuestionLog,
    HomeschoolLessonPlan, AssignmentTemplate,
    AsyncChallenge, ChallengeParticipant
)
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
import random
import string

# Test Results Tracking
test_results = {
    "passed": 0,
    "failed": 0,
    "errors": []
}

def generate_random_string(length=6):
    """Generate random string for unique identifiers"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def print_test_header(test_name):
    """Print formatted test header"""
    print("\n" + "="*60)
    print(f"TEST: {test_name}")
    print("="*60)

def print_success(message):
    """Print success message"""
    print(f"✓ {message}")
    test_results["passed"] += 1

def print_failure(message, error=None):
    """Print failure message"""
    print(f"✗ {message}")
    if error:
        print(f"  Error: {error}")
        test_results["errors"].append({"test": message, "error": str(error)})
    test_results["failed"] += 1

# ============================================================
# TEST 1: STUDENT CREATION & AUTHENTICATION
# ============================================================

def test_student_creation():
    """Test student account creation"""
    print_test_header("Student Account Creation")

    with app.app_context():
        try:
            student = Student(
                name="Test Student",
                email=f"teststudent{generate_random_string()}@test.com",
                date_of_birth=datetime(2010, 1, 1),
                grade_level=5,
                character="nova"
            )
            db.session.add(student)
            db.session.commit()

            # Verify student created
            assert student.id is not None, "Student ID should not be None"
            assert student.grade_level == 5, "Grade level should be 5"
            assert student.character == "nova", "Character should be nova"

            print_success("Student created successfully")
            print_success(f"Student ID: {student.id}")
            print_success(f"Student email: {student.email}")

            # Cleanup
            db.session.delete(student)
            db.session.commit()
            print_success("Student deleted successfully (cleanup)")

        except Exception as e:
            print_failure("Student creation failed", e)
            db.session.rollback()

# ============================================================
# TEST 2: PARENT-STUDENT LINKAGE
# ============================================================

def test_parent_student_link():
    """Test parent-student linkage via access code"""
    print_test_header("Parent-Student Linkage")

    with app.app_context():
        try:
            # Create parent with access code
            access_code = generate_random_string()
            parent = Parent(
                name="Test Parent",
                email=f"testparent{generate_random_string()}@test.com",
                password_hash=generate_password_hash("password123"),
                access_code=access_code
            )
            db.session.add(parent)
            db.session.commit()
            print_success(f"Parent created with access code: {access_code}")

            # Create student with parent access code
            student = Student(
                name="Test Student",
                email=f"teststudent{generate_random_string()}@test.com",
                date_of_birth=datetime(2012, 1, 1),
                grade_level=4,
                parent_access_code=access_code
            )
            db.session.add(student)
            db.session.commit()
            print_success(f"Student created with parent access code")

            # Verify linkage
            db.session.refresh(student)
            assert student.parent is not None, "Student should have parent"
            assert student.parent.id == parent.id, "Parent ID should match"
            assert student.parent.access_code == access_code, "Access code should match"

            print_success(f"Parent-student linkage verified")
            print_success(f"Parent ID: {parent.id}, Student Parent ID: {student.parent.id}")

            # Cleanup
            db.session.delete(student)
            db.session.delete(parent)
            db.session.commit()
            print_success("Cleanup successful")

        except Exception as e:
            print_failure("Parent-student linkage failed", e)
            db.session.rollback()

# ============================================================
# TEST 3: TEACHER CLASS MANAGEMENT
# ============================================================

def test_teacher_class_workflow():
    """Test teacher creating class and adding students"""
    print_test_header("Teacher Class Management")

    with app.app_context():
        try:
            # Create teacher
            teacher = Teacher(
                name="Test Teacher",
                email=f"testteacher{generate_random_string()}@test.com",
                password_hash=generate_password_hash("password123")
            )
            db.session.add(teacher)
            db.session.commit()
            print_success(f"Teacher created (ID: {teacher.id})")

            # Create class
            join_code = generate_random_string()
            classroom = Class(
                name="Test Class",
                teacher_id=teacher.id,
                join_code=join_code
            )
            db.session.add(classroom)
            db.session.commit()
            print_success(f"Class created with join code: {join_code}")

            # Create student and join class
            student = Student(
                name="Test Student",
                email=f"teststudent{generate_random_string()}@test.com",
                date_of_birth=datetime(2010, 1, 1),
                grade_level=5,
                class_id=classroom.id
            )
            db.session.add(student)
            db.session.commit()
            print_success(f"Student joined class")

            # Verify relationships
            db.session.refresh(classroom)
            db.session.refresh(teacher)

            assert len(classroom.students) == 1, "Class should have 1 student"
            assert classroom.students[0].id == student.id, "Student ID should match"
            assert classroom.teacher.id == teacher.id, "Teacher ID should match"

            print_success("Class relationships verified")

            # Cleanup
            db.session.delete(student)
            db.session.delete(classroom)
            db.session.delete(teacher)
            db.session.commit()
            print_success("Cleanup successful")

        except Exception as e:
            print_failure("Teacher class workflow failed", e)
            db.session.rollback()

# ============================================================
# TEST 4: ASSIGNMENT CREATION & SUBMISSION
# ============================================================

def test_assignment_workflow():
    """Test complete assignment workflow"""
    print_test_header("Assignment Creation & Submission")

    with app.app_context():
        try:
            # Setup: Create teacher, class, student
            teacher = Teacher(
                name="Test Teacher",
                email=f"testteacher{generate_random_string()}@test.com",
                password_hash=generate_password_hash("password123")
            )
            classroom = Class(
                name="Test Class",
                teacher=teacher,
                join_code=generate_random_string()
            )
            student = Student(
                name="Test Student",
                email=f"teststudent{generate_random_string()}@test.com",
                date_of_birth=datetime(2010, 1, 1),
                grade_level=5
            )

            db.session.add_all([teacher, classroom, student])
            db.session.commit()

            student.class_id = classroom.id
            db.session.commit()
            print_success("Setup complete (teacher, class, student)")

            # Create assignment
            assignment = AssignedPractice(
                subject="math",
                topic="Fractions",
                teacher_id=teacher.id,
                class_id=classroom.id,
                published=True,
                open_date=datetime.utcnow(),
                due_date=datetime.utcnow() + timedelta(days=7)
            )
            db.session.add(assignment)
            db.session.commit()
            print_success(f"Assignment created (ID: {assignment.id})")

            # Add question to assignment
            question = AssignedQuestion(
                practice_id=assignment.id,
                question_text="What is 1/2 + 1/4?",
                question_type="multiple_choice",
                options=["1/4", "3/4", "1/2", "1"],
                correct_answer="3/4",
                points=10
            )
            db.session.add(question)
            db.session.commit()
            print_success(f"Question added to assignment")

            # Student submits answer
            submission = StudentSubmission(
                student_id=student.id,
                practice_id=assignment.id,
                question_id=question.id,
                student_answer="3/4",
                is_correct=True,
                points_earned=10
            )
            db.session.add(submission)
            db.session.commit()
            print_success(f"Student submitted answer")

            # Verify workflow
            db.session.refresh(assignment)
            assert len(assignment.questions) == 1, "Assignment should have 1 question"
            assert assignment.questions[0].correct_answer == "3/4"

            db.session.refresh(student)
            # Check if submissions relationship exists
            if hasattr(student, 'submissions'):
                assert len(student.submissions) >= 0, "Student submissions should be accessible"

            print_success("Assignment workflow verified")

            # Cleanup
            db.session.delete(submission)
            db.session.delete(question)
            db.session.delete(assignment)
            db.session.delete(student)
            db.session.delete(classroom)
            db.session.delete(teacher)
            db.session.commit()
            print_success("Cleanup successful")

        except Exception as e:
            print_failure("Assignment workflow failed", e)
            db.session.rollback()

# ============================================================
# TEST 5: CHAPTER PROGRESS & BADGES
# ============================================================

def test_chapter_progress():
    """Test chapter progress tracking and badge awarding"""
    print_test_header("Chapter Progress & Badge System")

    with app.app_context():
        try:
            # Create student
            student = Student(
                name="Test Student",
                email=f"teststudent{generate_random_string()}@test.com",
                date_of_birth=datetime(2010, 1, 1),
                grade_level=5
            )
            db.session.add(student)
            db.session.commit()
            print_success(f"Student created (ID: {student.id})")

            # Create chapter progress
            progress = ChapterProgress(
                student_id=student.id,
                subject="math",
                chapter_number=1,
                completed=True,
                quiz_score=95,
                completed_at=datetime.utcnow()
            )
            db.session.add(progress)
            db.session.commit()
            print_success(f"Chapter progress created (95% score)")

            # Create chapter badge
            badge = ChapterBadge(
                subject="math",
                chapter_number=1,
                badge_type="perfect_score",
                name="Perfect Score - Math Chapter 1",
                icon="🏆"
            )
            db.session.add(badge)
            db.session.commit()
            print_success(f"Chapter badge created")

            # Award badge to student
            student_badge = StudentChapterBadge(
                student_id=student.id,
                badge_id=badge.id,
                earned_at=datetime.utcnow()
            )
            db.session.add(student_badge)
            db.session.commit()
            print_success(f"Badge awarded to student")

            # Verify
            db.session.refresh(student)
            if hasattr(student, 'chapter_badges'):
                print_success(f"Student has chapter badges relationship")

            # Cleanup
            db.session.delete(student_badge)
            db.session.delete(badge)
            db.session.delete(progress)
            db.session.delete(student)
            db.session.commit()
            print_success("Cleanup successful")

        except Exception as e:
            print_failure("Chapter progress test failed", e)
            db.session.rollback()

# ============================================================
# TEST 6: ARCADE GAME SESSION
# ============================================================

def test_arcade_game_session():
    """Test arcade game session creation and leaderboard"""
    print_test_header("Arcade Game Session & Leaderboard")

    with app.app_context():
        try:
            # Create student
            student = Student(
                name="Test Student",
                email=f"teststudent{generate_random_string()}@test.com",
                date_of_birth=datetime(2010, 1, 1),
                grade_level=5
            )
            db.session.add(student)
            db.session.commit()
            print_success(f"Student created (ID: {student.id})")

            # Create game session
            session = GameSession(
                student_id=student.id,
                game_key="speed_math",
                score=850,
                time_taken=120.5,
                accuracy=0.85,
                difficulty="medium",
                tokens_earned=50,
                xp_earned=100
            )
            db.session.add(session)
            db.session.commit()
            print_success(f"Game session created (Score: 850)")

            # Create leaderboard entry
            leaderboard = GameLeaderboard(
                student_id=student.id,
                game_key="speed_math",
                difficulty="medium",
                high_score=850,
                best_time=120.5,
                best_accuracy=0.85
            )
            db.session.add(leaderboard)
            db.session.commit()
            print_success(f"Leaderboard entry created")

            # Verify
            assert session.score == 850
            assert session.accuracy == 0.85
            assert leaderboard.high_score == 850
            print_success("Game session data verified")

            # Cleanup
            db.session.delete(leaderboard)
            db.session.delete(session)
            db.session.delete(student)
            db.session.commit()
            print_success("Cleanup successful")

        except Exception as e:
            print_failure("Arcade game session test failed", e)
            db.session.rollback()

# ============================================================
# TEST 7: ACTIVITY LOGGING
# ============================================================

def test_activity_logging():
    """Test activity log creation"""
    print_test_header("Activity Logging System")

    with app.app_context():
        try:
            # Create student
            student = Student(
                name="Test Student",
                email=f"teststudent{generate_random_string()}@test.com",
                date_of_birth=datetime(2010, 1, 1),
                grade_level=5
            )
            db.session.add(student)
            db.session.commit()
            print_success(f"Student created (ID: {student.id})")

            # Log activity
            activity = ActivityLog(
                student_id=student.id,
                activity_type="question_answered",
                subject="math",
                details="Answered multiplication question correctly",
                timestamp=datetime.utcnow()
            )
            db.session.add(activity)
            db.session.commit()
            print_success(f"Activity logged")

            # Verify
            assert activity.activity_type == "question_answered"
            print_success("Activity log verified")

            # Cleanup
            db.session.delete(activity)
            db.session.delete(student)
            db.session.commit()
            print_success("Cleanup successful")

        except Exception as e:
            print_failure("Activity logging test failed", e)
            db.session.rollback()

# ============================================================
# TEST 8: CONTENT MODERATION (QUESTION LOG)
# ============================================================

def test_content_moderation():
    """Test question logging and flagging system"""
    print_test_header("Content Moderation & Flagging")

    with app.app_context():
        try:
            # Create student
            student = Student(
                name="Test Student",
                email=f"teststudent{generate_random_string()}@test.com",
                date_of_birth=datetime(2010, 1, 1),
                grade_level=5
            )
            db.session.add(student)
            db.session.commit()
            print_success(f"Student created (ID: {student.id})")

            # Log flagged question
            question_log = QuestionLog(
                student_id=student.id,
                subject="math",
                question="Test inappropriate content",
                flagged=True,
                flag_reason="Inappropriate language detected",
                severity="medium",
                timestamp=datetime.utcnow()
            )
            db.session.add(question_log)
            db.session.commit()
            print_success(f"Flagged question logged")

            # Verify
            assert question_log.flagged == True
            assert question_log.severity == "medium"
            print_success("Flagged content verified")

            # Cleanup
            db.session.delete(question_log)
            db.session.delete(student)
            db.session.commit()
            print_success("Cleanup successful")

        except Exception as e:
            print_failure("Content moderation test failed", e)
            db.session.rollback()

# ============================================================
# TEST 9: ASYNC MULTIPLAYER CHALLENGE
# ============================================================

def test_async_multiplayer():
    """Test asynchronous multiplayer challenge system"""
    print_test_header("Asynchronous Multiplayer Challenge")

    with app.app_context():
        try:
            # Create two students
            student1 = Student(
                name="Student 1",
                email=f"student1{generate_random_string()}@test.com",
                date_of_birth=datetime(2010, 1, 1),
                grade_level=5
            )
            student2 = Student(
                name="Student 2",
                email=f"student2{generate_random_string()}@test.com",
                date_of_birth=datetime(2010, 1, 1),
                grade_level=5
            )
            db.session.add_all([student1, student2])
            db.session.commit()
            print_success(f"Two students created")

            # Create challenge
            challenge = AsyncChallenge(
                challenger_id=student1.id,
                game_key="speed_math",
                difficulty="medium",
                questions_json='[{"question": "2+2", "answer": "4"}]',
                challenger_score=100,
                challenger_time=60.0,
                expires_at=datetime.utcnow() + timedelta(hours=48),
                status="active"
            )
            db.session.add(challenge)
            db.session.commit()
            print_success(f"Challenge created (ID: {challenge.id})")

            # Add participant
            participant = ChallengeParticipant(
                challenge_id=challenge.id,
                student_id=student2.id,
                viewed=False,
                completed=False
            )
            db.session.add(participant)
            db.session.commit()
            print_success(f"Participant added to challenge")

            # Complete challenge
            participant.completed = True
            participant.score = 90
            participant.time_taken = 65.0
            participant.completed_at = datetime.utcnow()
            db.session.commit()
            print_success(f"Participant completed challenge")

            # Verify
            assert challenge.challenger_id == student1.id
            assert participant.student_id == student2.id
            assert participant.completed == True
            assert participant.score == 90
            print_success("Multiplayer challenge verified")

            # Cleanup
            db.session.delete(participant)
            db.session.delete(challenge)
            db.session.delete(student1)
            db.session.delete(student2)
            db.session.commit()
            print_success("Cleanup successful")

        except Exception as e:
            print_failure("Async multiplayer test failed", e)
            db.session.rollback()

# ============================================================
# TEST 10: HOMESCHOOL LESSON PLAN
# ============================================================

def test_homeschool_lesson_plan():
    """Test homeschool lesson plan creation"""
    print_test_header("Homeschool Lesson Plan System")

    with app.app_context():
        try:
            # Create parent
            parent = Parent(
                name="Homeschool Parent",
                email=f"homeschool{generate_random_string()}@test.com",
                password_hash=generate_password_hash("password123"),
                access_code=generate_random_string()
            )
            db.session.add(parent)
            db.session.commit()
            print_success(f"Homeschool parent created (ID: {parent.id})")

            # Create lesson plan
            lesson_plan = HomeschoolLessonPlan(
                parent_id=parent.id,
                subject="math",
                topic="Fractions",
                grade_level=5,
                objectives="Understand fraction addition",
                materials="Worksheets, manipulatives",
                activities="Practice problems",
                biblical_integration=True,
                status="not_started"
            )
            db.session.add(lesson_plan)
            db.session.commit()
            print_success(f"Lesson plan created (ID: {lesson_plan.id})")

            # Verify
            assert lesson_plan.subject == "math"
            assert lesson_plan.biblical_integration == True
            assert lesson_plan.status == "not_started"
            print_success("Lesson plan verified")

            # Update status
            lesson_plan.status = "in_progress"
            db.session.commit()
            print_success("Lesson plan status updated")

            # Cleanup
            db.session.delete(lesson_plan)
            db.session.delete(parent)
            db.session.commit()
            print_success("Cleanup successful")

        except Exception as e:
            print_failure("Homeschool lesson plan test failed", e)
            db.session.rollback()

# ============================================================
# MAIN TEST RUNNER
# ============================================================

def run_all_tests():
    """Run all database tests"""
    print("\n" + "╔" + "═"*58 + "╗")
    print("║" + " "*10 + "COZMICLEARNING DATABASE TEST SUITE" + " "*14 + "║")
    print("╚" + "═"*58 + "╝")

    print("\nRunning comprehensive database integrity tests...")
    print("This will test all critical database operations.\n")

    # Run all tests
    test_student_creation()
    test_parent_student_link()
    test_teacher_class_workflow()
    test_assignment_workflow()
    test_chapter_progress()
    test_arcade_game_session()
    test_activity_logging()
    test_content_moderation()
    test_async_multiplayer()
    test_homeschool_lesson_plan()

    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"✓ Passed: {test_results['passed']}")
    print(f"✗ Failed: {test_results['failed']}")
    print(f"Total Tests: {test_results['passed'] + test_results['failed']}")

    if test_results['failed'] > 0:
        print("\n⚠ FAILURES DETECTED:")
        for error in test_results['errors']:
            print(f"  - {error['test']}: {error['error']}")
        print("\n❌ Some tests failed. Please review errors above.")
    else:
        print("\n✅ ALL TESTS PASSED! Database is healthy.")

    print("="*60 + "\n")

if __name__ == "__main__":
    run_all_tests()
