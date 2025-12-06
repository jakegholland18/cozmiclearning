"""
Database initialization script for arcade enhancements.
Run this script once to populate the database with badges and power-ups.

Usage:
    python init_arcade_enhancements.py
"""

from app import app
from models import db
from modules.arcade_enhancements import initialize_badges, initialize_powerups


def main():
    """Initialize arcade enhancement database tables"""
    with app.app_context():
        print("🎮 Initializing Arcade Enhancements...")
        print("=" * 50)

        # Create all new tables
        print("\n📊 Creating database tables...")
        db.create_all()
        print("✅ Tables created successfully")

        # Initialize badges
        print("\n🏆 Initializing badges...")
        initialize_badges()

        # Initialize power-ups
        print("\n⚡ Initializing power-ups...")
        initialize_powerups()

        print("\n" + "=" * 50)
        print("✅ Arcade enhancements initialized successfully!")
        print("\nNew features available:")
        print("  • 12 achievement badges across 5 categories")
        print("  • 5 power-ups available for purchase")
        print("  • Daily challenges with bonus rewards")
        print("  • Streak tracking system")
        print("  • Practice mode (no timer)")
        print("  • Enhanced statistics and progress tracking")
        print("\nNew routes:")
        print("  • /arcade/badges - View and track badges")
        print("  • /arcade/powerups - Power-up shop")
        print("  • /arcade/challenges - Daily challenge")
        print("  • /arcade/stats - Detailed statistics")
        print("=" * 50)


if __name__ == "__main__":
    main()
