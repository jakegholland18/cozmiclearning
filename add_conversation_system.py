#!/usr/bin/env python3
"""
Database migration to add Study Buddy conversation management system.

This migration:
1. Creates study_buddy_conversation table
2. Adds conversation_id to study_buddy_message table
3. Creates a default conversation for existing messages

Run this to enable conversation library and management features.
"""

import os
os.environ['SKIP_STRIPE_CHECK'] = '1'

from app import app, db
from sqlalchemy import text
from datetime import datetime

def add_conversation_system():
    with app.app_context():
        print("🔧 Adding Study Buddy conversation management system...")

        try:
            with db.engine.connect() as conn:
                # Step 1: Create study_buddy_conversation table
                print("\n📋 Step 1: Creating study_buddy_conversation table...")

                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS study_buddy_conversation (
                        id SERIAL PRIMARY KEY,
                        student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                        title VARCHAR(200) NOT NULL,
                        subject VARCHAR(50),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        message_count INTEGER DEFAULT 0,
                        is_active BOOLEAN DEFAULT TRUE,
                        archived BOOLEAN DEFAULT FALSE
                    )
                """))
                print("  ✓ Created study_buddy_conversation table")

                # Create indexes
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_conversation_student_created
                    ON study_buddy_conversation(student_id, created_at)
                """))
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_conversation_student_updated
                    ON study_buddy_conversation(student_id, last_message_at)
                """))
                print("  ✓ Created indexes on study_buddy_conversation")

                # Step 2: Add conversation_id to study_buddy_message
                print("\n📋 Step 2: Adding conversation_id to study_buddy_message...")

                # Check if column already exists
                result = conn.execute(text("""
                    SELECT column_name
                    FROM information_schema.columns
                    WHERE table_name='study_buddy_message' AND column_name='conversation_id'
                """))
                column_exists = result.fetchone() is not None

                if not column_exists:
                    conn.execute(text("""
                        ALTER TABLE study_buddy_message
                        ADD COLUMN conversation_id INTEGER REFERENCES study_buddy_conversation(id) ON DELETE CASCADE
                    """))
                    print("  ✓ Added conversation_id column")

                    # Create index
                    conn.execute(text("""
                        CREATE INDEX IF NOT EXISTS idx_study_buddy_conversation
                        ON study_buddy_message(conversation_id)
                    """))
                    print("  ✓ Created index on conversation_id")
                else:
                    print("  ℹ️  conversation_id column already exists")

                # Step 3: Migrate existing messages to default conversations
                print("\n📋 Step 3: Migrating existing messages to conversations...")

                # Get list of students with messages but no conversations
                result = conn.execute(text("""
                    SELECT DISTINCT student_id
                    FROM study_buddy_message
                    WHERE conversation_id IS NULL
                """))
                students_with_messages = [row[0] for row in result]

                for student_id in students_with_messages:
                    # Get first message from this student
                    result = conn.execute(text("""
                        SELECT message, timestamp
                        FROM study_buddy_message
                        WHERE student_id = :student_id AND is_student = TRUE
                        ORDER BY timestamp ASC
                        LIMIT 1
                    """), {"student_id": student_id})

                    first_message_row = result.fetchone()

                    if first_message_row:
                        first_message = first_message_row[0]
                        first_timestamp = first_message_row[1]

                        # Generate title from first message (first 50 chars)
                        title = first_message[:50].strip()
                        if len(first_message) > 50:
                            title += "..."

                        # Create default conversation
                        result = conn.execute(text("""
                            INSERT INTO study_buddy_conversation
                            (student_id, title, created_at, last_message_at, is_active, archived)
                            VALUES (:student_id, :title, :created_at, :last_message_at, FALSE, TRUE)
                            RETURNING id
                        """), {
                            "student_id": student_id,
                            "title": title or "Conversation",
                            "created_at": first_timestamp,
                            "last_message_at": datetime.utcnow()
                        })

                        conversation_id = result.fetchone()[0]

                        # Link all messages from this student to this conversation
                        conn.execute(text("""
                            UPDATE study_buddy_message
                            SET conversation_id = :conversation_id
                            WHERE student_id = :student_id AND conversation_id IS NULL
                        """), {
                            "conversation_id": conversation_id,
                            "student_id": student_id
                        })

                        # Update message count
                        result = conn.execute(text("""
                            SELECT COUNT(*) FROM study_buddy_message
                            WHERE conversation_id = :conversation_id
                        """), {"conversation_id": conversation_id})

                        message_count = result.fetchone()[0]

                        conn.execute(text("""
                            UPDATE study_buddy_conversation
                            SET message_count = :message_count
                            WHERE id = :conversation_id
                        """), {
                            "message_count": message_count,
                            "conversation_id": conversation_id
                        })

                        print(f"  ✓ Created conversation for student {student_id} ({message_count} messages)")

                conn.commit()

            print("\n✅ Conversation management system installed successfully!")
            print("\n🎉 New features enabled:")
            print("  - Students can start new conversations")
            print("  - Students can delete conversations")
            print("  - Students can view conversation library")
            print("  - Students can resume past conversations")
            print("  - Conversations are organized by topic")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    add_conversation_system()
