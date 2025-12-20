#!/usr/bin/env python3
"""
Database migration script to create practice_sessions table
Run this to set up the self-practice tracking feature
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import PracticeSession

def run_migration():
    """Create practice_sessions table if it doesn't exist"""
    with app.app_context():
        try:
            # Check if table exists by trying to query it
            PracticeSession.query.first()
            print("✅ practice_sessions table already exists")
        except Exception:
            # Table doesn't exist, create it
            print("📊 Creating practice_sessions table...")
            db.create_all()
            print("✅ practice_sessions table created successfully!")
            print("\n📝 You can now track student self-practice in the gradebook")

if __name__ == "__main__":
    run_migration()
