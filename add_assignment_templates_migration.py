#!/usr/bin/env python3
"""
Wrapper for add_assignment_templates migration
Used by run_startup_migrations.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def add_assignment_templates():
    """Run the assignment templates migration"""
    try:
        from migrations.add_assignment_templates import run_migration
        from app import app

        with app.app_context():
            return run_migration()
    except Exception as e:
        print(f"❌ Error running assignment templates migration: {e}")
        return False

if __name__ == "__main__":
    success = add_assignment_templates()
    sys.exit(0 if success else 1)
