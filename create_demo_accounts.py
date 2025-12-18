"""
Create Demo/Test Accounts for Admin Preview Mode

This script creates dedicated demo accounts that admin uses to preview
different user roles WITHOUT accessing real student/teacher/parent accounts.

Run this script once to set up the demo accounts.
"""

from app import app, db
from models import Student, Teacher, Parent, Class
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_demo_accounts():
    """Create demo accounts for admin preview mode"""

    with app.app_context():
        print("🎭 Creating Demo Accounts for Admin Preview Mode...")
        print("=" * 60)

        # ============================================================
        # 1. DEMO TEACHER ACCOUNT
        # ============================================================

        demo_teacher = Teacher.query.filter_by(email="demo.teacher@cozmiclearning.admin").first()

        if not demo_teacher:
            demo_teacher = Teacher(
                name="Demo Teacher (Admin Preview)",
                email="demo.teacher@cozmiclearning.admin",
                password_hash=generate_password_hash("DemoPreview123!"),
                created_at=datetime.utcnow(),
                subscription_active=True,
                plan="premium",
                trial_end=None  # No trial limit for demo
            )
            db.session.add(demo_teacher)
            db.session.flush()  # Get the ID
            print(f"✅ Created Demo Teacher (ID: {demo_teacher.id})")
        else:
            print(f"ℹ️  Demo Teacher already exists (ID: {demo_teacher.id})")

        # ============================================================
        # 2. DEMO CLASS
        # ============================================================

        demo_class = Class.query.filter_by(
            teacher_id=demo_teacher.id,
            class_name="Demo Class (Admin Preview)"
        ).first()

        if not demo_class:
            demo_class = Class(
                teacher_id=demo_teacher.id,
                class_name="Demo Class (Admin Preview)",
                grade_level="5",
                created_at=datetime.utcnow()
            )
            db.session.add(demo_class)
            db.session.flush()
            print(f"✅ Created Demo Class (ID: {demo_class.id})")
        else:
            print(f"ℹ️  Demo Class already exists (ID: {demo_class.id})")

        # ============================================================
        # 3. DEMO PARENT ACCOUNT
        # ============================================================

        demo_parent = Parent.query.filter_by(email="demo.parent@cozmiclearning.admin").first()

        if not demo_parent:
            demo_parent = Parent(
                name="Demo Parent (Admin Preview)",
                email="demo.parent@cozmiclearning.admin",
                password_hash=generate_password_hash("DemoPreview123!"),
                created_at=datetime.utcnow(),
                subscription_active=True,
                plan="premium",
                trial_end=None
            )
            db.session.add(demo_parent)
            db.session.flush()
            print(f"✅ Created Demo Parent (ID: {demo_parent.id})")
        else:
            print(f"ℹ️  Demo Parent already exists (ID: {demo_parent.id})")

        # ============================================================
        # 4. DEMO HOMESCHOOL PARENT ACCOUNT
        # Note: Homeschool parents use same Parent model, just without class
        # ============================================================

        demo_homeschool = Parent.query.filter_by(email="demo.homeschool@cozmiclearning.admin").first()

        if not demo_homeschool:
            demo_homeschool = Parent(
                name="Demo Homeschool Parent (Admin Preview)",
                email="demo.homeschool@cozmiclearning.admin",
                password_hash=generate_password_hash("DemoPreview123!"),
                created_at=datetime.utcnow(),
                subscription_active=True,
                plan="premium",
                trial_end=None
            )
            db.session.add(demo_homeschool)
            db.session.flush()
            print(f"✅ Created Demo Homeschool Parent (ID: {demo_homeschool.id})")
        else:
            print(f"ℹ️  Demo Homeschool Parent already exists (ID: {demo_homeschool.id})")

        # ============================================================
        # 5. DEMO STUDENT ACCOUNT (Linked to Demo Parent)
        # ============================================================

        demo_student = Student.query.filter_by(student_email="demo.student@cozmiclearning.admin").first()

        if not demo_student:
            demo_student = Student(
                student_name="Demo Student (Admin Preview)",
                student_email="demo.student@cozmiclearning.admin",
                password_hash=generate_password_hash("DemoPreview123!"),
                parent_id=demo_parent.id,
                class_id=demo_class.id,
                created_at=datetime.utcnow(),
                subscription_active=True,
                plan="premium",
                trial_end=None
            )
            db.session.add(demo_student)
            db.session.flush()
            print(f"✅ Created Demo Student (ID: {demo_student.id})")
        else:
            print(f"ℹ️  Demo Student already exists (ID: {demo_student.id})")

        # ============================================================
        # 6. DEMO HOMESCHOOL STUDENT (Linked to Demo Homeschool Parent)
        # ============================================================

        demo_homeschool_student = Student.query.filter_by(student_email="demo.homeschool.student@cozmiclearning.admin").first()

        if not demo_homeschool_student:
            demo_homeschool_student = Student(
                student_name="Demo Homeschool Student (Admin Preview)",
                student_email="demo.homeschool.student@cozmiclearning.admin",
                password_hash=generate_password_hash("DemoPreview123!"),
                parent_id=demo_homeschool.id,
                class_id=None,  # Homeschool students don't have classes
                created_at=datetime.utcnow(),
                subscription_active=True,
                plan="premium",
                trial_end=None
            )
            db.session.add(demo_homeschool_student)
            db.session.flush()
            print(f"✅ Created Demo Homeschool Student (ID: {demo_homeschool_student.id})")
        else:
            print(f"ℹ️  Demo Homeschool Student already exists (ID: {demo_homeschool_student.id})")

        # ============================================================
        # COMMIT ALL CHANGES
        # ============================================================

        db.session.commit()

        print("=" * 60)
        print("✅ Demo Accounts Setup Complete!")
        print()
        print("📋 DEMO ACCOUNT SUMMARY:")
        print(f"   Teacher:           {demo_teacher.name} (ID: {demo_teacher.id})")
        print(f"   Parent:            {demo_parent.name} (ID: {demo_parent.id})")
        print(f"   Homeschool Parent: {demo_homeschool.name} (ID: {demo_homeschool.id})")
        print(f"   Student:           {demo_student.student_name} (ID: {demo_student.id})")
        print(f"   Homeschool Student:{demo_homeschool_student.student_name} (ID: {demo_homeschool_student.id})")
        print()
        print("🔒 These accounts are for ADMIN PREVIEW ONLY")
        print("   Real student/teacher/parent accounts will never be accessed by admin")
        print()
        print("✅ Next step: Run the app and use admin dashboard to switch to these demo accounts")


if __name__ == "__main__":
    create_demo_accounts()
