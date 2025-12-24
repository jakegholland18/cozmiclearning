#!/usr/bin/env python3
"""
Add Learning Lab Tables - LearningProfile and StrategyUsage

This migration adds tables for the Learning Lab feature which helps
students discover their learning preferences and track helpful strategies.

IMPORTANT: This feature does NOT diagnose learning disabilities.
It tracks preferences and strategies that work for individual students.
"""

from app import app, db
from models import LearningProfile, StrategyUsage

if __name__ == '__main__':
    with app.app_context():
        print("🧠 Creating Learning Lab tables...")
        print("=" * 60)

        # Create tables
        db.create_all()

        print("✅ Created tables:")
        print("   - learning_profiles")
        print("   - strategy_usage")
        print("=" * 60)
        print("✨ Migration complete!")
        print("\nLearning Lab is ready to help students discover how they learn best!")
