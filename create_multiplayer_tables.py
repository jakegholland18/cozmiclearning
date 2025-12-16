"""
Database Migration: Create Asynchronous Multiplayer Tables

Run this script to create the new tables for async multiplayer:
- async_challenges
- challenge_participants
- arcade_teams
- team_members
- team_matches

Usage:
    python create_multiplayer_tables.py
"""

from app import app, db
from models import AsyncChallenge, ChallengeParticipant, ArcadeTeam, TeamMember, TeamMatch

def create_multiplayer_tables():
    """Create all multiplayer-related tables"""
    with app.app_context():
        print("Creating asynchronous multiplayer tables...")

        try:
            # Create tables
            db.create_all()

            print("✅ Successfully created tables:")
            print("   - async_challenges")
            print("   - challenge_participants")
            print("   - arcade_teams")
            print("   - team_members")
            print("   - team_matches")
            print("\n✨ Async multiplayer database setup complete!")

        except Exception as e:
            print(f"❌ Error creating tables: {e}")
            raise

if __name__ == '__main__':
    create_multiplayer_tables()
