#!/usr/bin/env python3
"""
Simple standalone script to add grade_released column.
Run this manually if the automatic migration didn't work.

Usage:
    python add_grade_released_column.py
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    print("=" * 60)
    print("Adding grade_released column to student_submissions table")
    print("=" * 60)

    from app import app, db

    with app.app_context():
        try:
            # Check if column already exists
            print("\n1. Checking if column already exists...")
            result = db.session.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'student_submissions'
                AND column_name = 'grade_released'
                """
            )

            if result.fetchone():
                print("   ✅ Column 'grade_released' already exists!")
                print("   Nothing to do.")
                return True

            print("   ➡️  Column does not exist, will add it now.")

            # Add the column
            print("\n2. Adding grade_released column...")
            db.session.execute(
                """
                ALTER TABLE student_submissions
                ADD COLUMN grade_released BOOLEAN DEFAULT FALSE
                """
            )
            db.session.commit()
            print("   ✅ Successfully added column!")

            # Set existing graded submissions to released=True
            print("\n3. Setting grade_released=True for existing graded assignments...")
            result = db.session.execute(
                """
                UPDATE student_submissions
                SET grade_released = TRUE
                WHERE status = 'graded'
                """
            )
            rows_updated = result.rowcount
            db.session.commit()
            print(f"   ✅ Updated {rows_updated} existing graded submissions")

            print("\n" + "=" * 60)
            print("✅ MIGRATION COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            return True

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            print("\nFull error details:")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
