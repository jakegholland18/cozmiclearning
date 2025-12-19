#!/usr/bin/env python3
"""
Add adaptive assignment tracking columns to student_submissions table (SQLite version)
Adds current_question_index and mc_phase_complete for hybrid adaptive assignments
"""

import os
import sys

def main():
    print("=" * 60)
    print("Adding adaptive tracking columns to student_submissions")
    print("=" * 60)

    sys.path.insert(0, os.path.dirname(__file__))

    from app import app, db
    from sqlalchemy import text

    with app.app_context():
        try:
            # Check if current_question_index column already exists
            print("\n1. Checking if current_question_index column exists...")
            result = db.session.execute(
                text("PRAGMA table_info(student_submissions)")
            )
            columns = [row[1] for row in result.fetchall()]

            if 'current_question_index' in columns:
                print("   ✅ Column 'current_question_index' already exists!")
            else:
                print("   ➡️  Adding current_question_index column...")
                db.session.execute(
                    text("""
                    ALTER TABLE student_submissions
                    ADD COLUMN current_question_index INTEGER DEFAULT 0
                    """)
                )
                db.session.commit()
                print("   ✅ Successfully added 'current_question_index' column")

            # Check if mc_phase_complete column already exists
            print("\n2. Checking if mc_phase_complete column exists...")
            result = db.session.execute(
                text("PRAGMA table_info(student_submissions)")
            )
            columns = [row[1] for row in result.fetchall()]

            if 'mc_phase_complete' in columns:
                print("   ✅ Column 'mc_phase_complete' already exists!")
            else:
                print("   ➡️  Adding mc_phase_complete column...")
                db.session.execute(
                    text("""
                    ALTER TABLE student_submissions
                    ADD COLUMN mc_phase_complete BOOLEAN DEFAULT 0
                    """)
                )
                db.session.commit()
                print("   ✅ Successfully added 'mc_phase_complete' column")

            print("\n" + "=" * 60)
            print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            return True

        except Exception as e:
            print(f"\n❌ Migration failed: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
