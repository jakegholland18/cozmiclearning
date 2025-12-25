#!/usr/bin/env python3
"""
Database migration to add moderation fields to StudyBuddyMessage table.

Run this to add safety and moderation tracking fields.
"""

import os
os.environ['SKIP_STRIPE_CHECK'] = '1'

from app import app, db
from sqlalchemy import text

def add_moderation_fields():
    with app.app_context():
        print("Adding moderation fields to study_buddy_message table...")

        try:
            # Add new columns
            with db.engine.connect() as conn:
                # Check if columns exist first
                result = conn.execute(text("PRAGMA table_info(study_buddy_message)"))
                columns = [row[1] for row in result]

                if 'flagged' not in columns:
                    conn.execute(text("ALTER TABLE study_buddy_message ADD COLUMN flagged BOOLEAN DEFAULT 0"))
                    print("  ✓ Added 'flagged' column")

                if 'flagged_reason' not in columns:
                    conn.execute(text("ALTER TABLE study_buddy_message ADD COLUMN flagged_reason VARCHAR(200)"))
                    print("  ✓ Added 'flagged_reason' column")

                if 'moderation_scores' not in columns:
                    conn.execute(text("ALTER TABLE study_buddy_message ADD COLUMN moderation_scores JSON"))
                    print("  ✓ Added 'moderation_scores' column")

                if 'parent_notified' not in columns:
                    conn.execute(text("ALTER TABLE study_buddy_message ADD COLUMN parent_notified BOOLEAN DEFAULT 0"))
                    print("  ✓ Added 'parent_notified' column")

                if 'reviewed' not in columns:
                    conn.execute(text("ALTER TABLE study_buddy_message ADD COLUMN reviewed BOOLEAN DEFAULT 0"))
                    print("  ✓ Added 'reviewed' column")

                if 'reviewer_notes' not in columns:
                    conn.execute(text("ALTER TABLE study_buddy_message ADD COLUMN reviewer_notes TEXT"))
                    print("  ✓ Added 'reviewer_notes' column")

                conn.commit()

            print("\n✅ Moderation fields added successfully!")
            print("\n🔒 Content safety features enabled:")
            print("  - OpenAI Moderation API integration")
            print("  - Academic dishonesty detection")
            print("  - Parent notification system")
            print("  - Admin review workflow")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    add_moderation_fields()
