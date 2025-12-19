"""
Add grade_released column to student_submissions table (PostgreSQL version)
Allows teachers to control when students can see their grades
"""

import os
import sys

def migrate():
    """Add grade_released column to PostgreSQL database"""

    # Import after adding parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

    from app import app, db
    from models import StudentSubmission

    print("Starting PostgreSQL migration: add grade_released column")

    with app.app_context():
        try:
            # Check if column already exists
            result = db.session.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'student_submissions'
                AND column_name = 'grade_released'
                """
            )

            if result.fetchone():
                print("✅ Column 'grade_released' already exists in student_submissions")
                return True

            # Add the column
            print("Adding grade_released column...")
            db.session.execute(
                """
                ALTER TABLE student_submissions
                ADD COLUMN grade_released BOOLEAN DEFAULT FALSE
                """
            )

            db.session.commit()
            print("✅ Successfully added 'grade_released' column to student_submissions")

            # Set existing graded submissions to released=True for backward compatibility
            print("Setting grade_released=True for existing graded submissions...")
            result = db.session.execute(
                """
                UPDATE student_submissions
                SET grade_released = TRUE
                WHERE status = 'graded'
                """
            )

            rows_updated = result.rowcount
            db.session.commit()
            print(f"✅ Set grade_released=True for {rows_updated} existing graded submissions")

            return True

        except Exception as e:
            print(f"❌ Migration failed: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("Running PostgreSQL migration: Add grade_released column...")
    success = migrate()
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)
