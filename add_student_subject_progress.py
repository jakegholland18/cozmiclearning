#!/usr/bin/env python3
"""
Database migration to add student subject progress tracking.

This migration:
1. Creates student_subject_progress table
2. Tracks mastery, XP, and last visit per subject
3. Enables real-time progress display on subjects page

Run this to enable real progress tracking for learning planets.
"""

import os
os.environ['SKIP_STRIPE_CHECK'] = '1'

from app import app, db
from sqlalchemy import text
from datetime import datetime

def add_student_subject_progress():
    with app.app_context():
        print("🔧 Adding student subject progress tracking system...")

        try:
            with db.engine.connect() as conn:
                # Step 1: Create student_subject_progress table
                print("\n📋 Step 1: Creating student_subject_progress table...")

                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS student_subject_progress (
                        id SERIAL PRIMARY KEY,
                        student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                        subject_key VARCHAR(50) NOT NULL,

                        -- Activity tracking
                        questions_answered INTEGER DEFAULT 0,
                        correct_answers INTEGER DEFAULT 0,
                        total_time_minutes INTEGER DEFAULT 0,
                        last_visited TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

                        -- Progress metrics
                        xp_earned INTEGER DEFAULT 0,
                        mastery_percentage INTEGER DEFAULT 0,

                        -- Milestones
                        lessons_completed INTEGER DEFAULT 0,
                        chapters_completed INTEGER DEFAULT 0,

                        -- Timestamps
                        first_visit TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

                        -- Constraints
                        CONSTRAINT uq_student_subject UNIQUE(student_id, subject_key)
                    )
                """))
                print("  ✓ Created student_subject_progress table")

                # Create indexes
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_subject_progress_student
                    ON student_subject_progress(student_id)
                """))
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_subject_progress_subject
                    ON student_subject_progress(subject_key)
                """))
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_subject_progress_student_subject
                    ON student_subject_progress(student_id, subject_key)
                """))
                print("  ✓ Created indexes on student_subject_progress")

                conn.commit()

            print("\n✅ Student subject progress tracking installed successfully!")
            print("\n🎉 New features enabled:")
            print("  - Real-time mastery percentages per subject")
            print("  - Actual XP tracking")
            print("  - Last visited timestamps")
            print("  - Questions answered tracking")
            print("  - Study time tracking")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    add_student_subject_progress()
