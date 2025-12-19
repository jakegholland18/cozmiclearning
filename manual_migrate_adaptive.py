#!/usr/bin/env python3
"""
Manual migration script for adaptive tracking columns
Run this directly on Render if automatic migration fails
"""

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import app, db
from sqlalchemy import text

def run_manual_migration():
    """Manually add adaptive tracking columns to student_submissions"""

    print("=" * 70)
    print("MANUAL MIGRATION: Add Adaptive Tracking Columns")
    print("=" * 70)

    with app.app_context():
        try:
            # Show database info
            print(f"\nDatabase URL: {db.engine.url}")
            print(f"Database dialect: {db.engine.dialect.name}")

            # Test connection
            print("\nTesting database connection...")
            db.session.execute(text("SELECT 1"))
            print("✅ Database connection successful")

            # Check existing columns
            print("\nChecking existing columns in student_submissions table...")
            result = db.session.execute(
                text("""
                SELECT column_name, data_type, column_default
                FROM information_schema.columns
                WHERE table_name = 'student_submissions'
                ORDER BY ordinal_position
                """)
            )

            existing_columns = {}
            for row in result:
                existing_columns[row[0]] = {
                    'type': row[1],
                    'default': row[2]
                }
                print(f"  - {row[0]}: {row[1]} (default: {row[2]})")

            result.close()

            # Check and add current_question_index
            print("\n" + "-" * 70)
            if 'current_question_index' in existing_columns:
                print("✅ Column 'current_question_index' already exists")
                print(f"   Type: {existing_columns['current_question_index']['type']}")
                print(f"   Default: {existing_columns['current_question_index']['default']}")
            else:
                print("❌ Column 'current_question_index' is MISSING")
                print("   Adding column...")

                db.session.execute(
                    text("""
                    ALTER TABLE student_submissions
                    ADD COLUMN current_question_index INTEGER DEFAULT 0
                    """)
                )
                db.session.commit()
                print("✅ Successfully added 'current_question_index' column")

            # Check and add mc_phase_complete
            print("\n" + "-" * 70)
            if 'mc_phase_complete' in existing_columns:
                print("✅ Column 'mc_phase_complete' already exists")
                print(f"   Type: {existing_columns['mc_phase_complete']['type']}")
                print(f"   Default: {existing_columns['mc_phase_complete']['default']}")
            else:
                print("❌ Column 'mc_phase_complete' is MISSING")
                print("   Adding column...")

                db.session.execute(
                    text("""
                    ALTER TABLE student_submissions
                    ADD COLUMN mc_phase_complete BOOLEAN DEFAULT FALSE
                    """)
                )
                db.session.commit()
                print("✅ Successfully added 'mc_phase_complete' column")

            # Verify final state
            print("\n" + "=" * 70)
            print("VERIFICATION: Checking final table structure...")
            print("=" * 70)

            result = db.session.execute(
                text("""
                SELECT column_name, data_type, column_default
                FROM information_schema.columns
                WHERE table_name = 'student_submissions'
                AND column_name IN ('current_question_index', 'mc_phase_complete')
                ORDER BY column_name
                """)
            )

            final_columns = []
            for row in result:
                final_columns.append(row[0])
                print(f"✅ {row[0]}: {row[1]} (default: {row[2]})")

            result.close()

            if 'current_question_index' in final_columns and 'mc_phase_complete' in final_columns:
                print("\n" + "=" * 70)
                print("✅ MIGRATION SUCCESSFUL!")
                print("=" * 70)
                print("\nBoth columns are now present in the student_submissions table.")
                print("The application should work correctly now.")
                return True
            else:
                print("\n" + "=" * 70)
                print("❌ MIGRATION INCOMPLETE!")
                print("=" * 70)
                print(f"\nMissing columns: {set(['current_question_index', 'mc_phase_complete']) - set(final_columns)}")
                return False

        except Exception as e:
            print("\n" + "=" * 70)
            print("❌ MIGRATION FAILED!")
            print("=" * 70)
            print(f"\nError: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            return False

if __name__ == "__main__":
    print("\n🚀 Starting manual migration...\n")
    success = run_manual_migration()

    if success:
        print("\n✅ Migration completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Migration failed - check error messages above")
        sys.exit(1)
