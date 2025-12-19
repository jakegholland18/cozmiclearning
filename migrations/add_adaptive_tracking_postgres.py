"""
Add adaptive assignment tracking columns to student_submissions table (PostgreSQL version)
Adds current_question_index and mc_phase_complete for hybrid adaptive assignments
"""

import os
import sys

def migrate():
    """Add adaptive tracking columns to PostgreSQL database"""

    # Import after adding parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

    from app import app, db
    from sqlalchemy import text

    print("Starting PostgreSQL migration: add adaptive assignment tracking columns")

    with app.app_context():
        try:
            print(f"Connected to database: {db.engine.url}")

            # Check if current_question_index column already exists
            result = db.session.execute(
                text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'student_submissions'
                AND column_name = 'current_question_index'
                """)
            )

            row = result.fetchone()
            result.close()  # Close the result set

            if row:
                print("✅ Column 'current_question_index' already exists in student_submissions")
            else:
                # Add the current_question_index column
                print("Adding current_question_index column...")
                db.session.execute(
                    text("""
                    ALTER TABLE student_submissions
                    ADD COLUMN current_question_index INTEGER DEFAULT 0
                    """)
                )
                db.session.commit()
                print("✅ Successfully added 'current_question_index' column")

            # Check if mc_phase_complete column already exists
            result = db.session.execute(
                text("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'student_submissions'
                AND column_name = 'mc_phase_complete'
                """)
            )

            row = result.fetchone()
            result.close()  # Close the result set

            if row:
                print("✅ Column 'mc_phase_complete' already exists in student_submissions")
            else:
                # Add the mc_phase_complete column
                print("Adding mc_phase_complete column...")
                db.session.execute(
                    text("""
                    ALTER TABLE student_submissions
                    ADD COLUMN mc_phase_complete BOOLEAN DEFAULT FALSE
                    """)
                )
                db.session.commit()
                print("✅ Successfully added 'mc_phase_complete' column")

            print("✅ Migration completed successfully - all columns verified")
            return True

        except Exception as e:
            print(f"❌ Migration failed with error: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("Running PostgreSQL migration: Add adaptive tracking columns...")
    success = migrate()
    if success:
        print("\n✅ Migration completed successfully!")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)
