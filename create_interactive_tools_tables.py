#!/usr/bin/env python3
"""
Database migration script to create tables for interactive learning tools.

Run this to add:
- PomodoroSession
- StudyBuddyMessage
- TaskBreakdown
- TaskStep
- AIAssignment

Usage:
    python3 create_interactive_tools_tables.py
"""

import os
os.environ['SKIP_STRIPE_CHECK'] = '1'  # Skip Stripe validation for migrations

from app import app, db
from models import (
    PomodoroSession,
    StudyBuddyMessage,
    TaskBreakdown,
    TaskStep,
    AIAssignment
)

def create_tables():
    """Create new database tables for interactive learning tools"""
    with app.app_context():
        print("Creating interactive learning tools tables...")

        # Create all tables defined in models
        db.create_all()

        print("✅ Tables created successfully!")
        print("\nNew tables:")
        print("  - pomodoro_session (Pomodoro timer tracking)")
        print("  - study_buddy_message (AI Study Buddy conversations)")
        print("  - task_breakdown (AI task breakdowns)")
        print("  - task_step (Individual task steps)")
        print("  - ai_assignment (Teacher AI-generated assignments)")

        print("\n🚀 Interactive Learning Tools database is ready!")

if __name__ == "__main__":
    create_tables()
