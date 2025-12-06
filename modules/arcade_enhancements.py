"""
Arcade Mode Enhancements
========================
This module provides enhanced features for the arcade mode including:
- Badge/achievement system
- Power-ups
- Daily challenges
- Streak tracking
- Practice mode support
"""

from datetime import datetime, date, timedelta
from models import (
    db, ArcadeBadge, StudentBadge, PowerUp, StudentPowerUp,
    DailyChallenge, StudentChallengeProgress, GameStreak, GameSession
)
import random


# ============================================================
# BADGE DEFINITIONS
# ============================================================

ARCADE_BADGES = [
    # Score-based badges
    {
        "badge_key": "perfect_score",
        "name": "Perfect Score",
        "description": "Get 100% accuracy in any game",
        "icon": "🎯",
        "category": "accuracy",
        "requirement_type": "accuracy",
        "requirement_value": 100,
        "tier": "gold"
    },
    {
        "badge_key": "high_scorer",
        "name": "High Scorer",
        "description": "Score 2000+ points in a single game",
        "icon": "⭐",
        "category": "score",
        "requirement_type": "score",
        "requirement_value": 2000,
        "tier": "silver"
    },
    {
        "badge_key": "mega_scorer",
        "name": "Mega Scorer",
        "description": "Score 5000+ points in a single game",
        "icon": "🌟",
        "category": "score",
        "requirement_type": "score",
        "requirement_value": 5000,
        "tier": "gold"
    },

    # Speed-based badges
    {
        "badge_key": "speed_demon",
        "name": "Speed Demon",
        "description": "Complete a game in under 30 seconds",
        "icon": "⚡",
        "category": "speed",
        "requirement_type": "time",
        "requirement_value": 30,
        "tier": "silver"
    },
    {
        "badge_key": "lightning_fast",
        "name": "Lightning Fast",
        "description": "Complete a game in under 20 seconds",
        "icon": "🔥",
        "category": "speed",
        "requirement_type": "time",
        "requirement_value": 20,
        "tier": "gold"
    },

    # Streak badges
    {
        "badge_key": "daily_player",
        "name": "Daily Player",
        "description": "Play arcade games 3 days in a row",
        "icon": "📅",
        "category": "streak",
        "requirement_type": "streak",
        "requirement_value": 3,
        "tier": "bronze"
    },
    {
        "badge_key": "weekly_warrior",
        "name": "Weekly Warrior",
        "description": "Play arcade games 7 days in a row",
        "icon": "🔥",
        "category": "streak",
        "requirement_type": "streak",
        "requirement_value": 7,
        "tier": "silver"
    },
    {
        "badge_key": "unstoppable",
        "name": "Unstoppable",
        "description": "Play arcade games 30 days in a row",
        "icon": "💪",
        "category": "streak",
        "requirement_type": "streak",
        "requirement_value": 30,
        "tier": "platinum"
    },

    # Mastery badges (per game)
    {
        "badge_key": "game_master",
        "name": "Game Master",
        "description": "Play the same game 50 times",
        "icon": "👑",
        "category": "mastery",
        "requirement_type": "total_plays",
        "requirement_value": 50,
        "tier": "gold"
    },
    {
        "badge_key": "dedicated_player",
        "name": "Dedicated Player",
        "description": "Play the same game 20 times",
        "icon": "🎮",
        "category": "mastery",
        "requirement_type": "total_plays",
        "requirement_value": 20,
        "tier": "silver"
    },

    # Accuracy badges
    {
        "badge_key": "sharpshooter",
        "name": "Sharpshooter",
        "description": "Get 95%+ accuracy in any game",
        "icon": "🎯",
        "category": "accuracy",
        "requirement_type": "accuracy",
        "requirement_value": 95,
        "tier": "silver"
    },
    {
        "badge_key": "ace_student",
        "name": "Ace Student",
        "description": "Get 90%+ accuracy in any game",
        "icon": "📚",
        "category": "accuracy",
        "requirement_type": "accuracy",
        "requirement_value": 90,
        "tier": "bronze"
    },
]


# ============================================================
# POWER-UP DEFINITIONS
# ============================================================

POWERUPS = [
    {
        "powerup_key": "freeze_time",
        "name": "Freeze Time",
        "description": "Pause the timer for 10 seconds",
        "icon": "❄️",
        "token_cost": 50,
        "effect_duration": 10,
        "uses_per_game": 1
    },
    {
        "powerup_key": "fifty_fifty",
        "name": "50/50",
        "description": "Remove 2 wrong answers from a multiple choice question",
        "icon": "🎲",
        "token_cost": 30,
        "effect_duration": None,
        "uses_per_game": 3
    },
    {
        "powerup_key": "skip_question",
        "name": "Skip Question",
        "description": "Skip to the next question without penalty",
        "icon": "⏭️",
        "token_cost": 40,
        "effect_duration": None,
        "uses_per_game": 2
    },
    {
        "powerup_key": "double_points",
        "name": "Double Points",
        "description": "Earn 2x points for the next 3 questions",
        "icon": "💎",
        "token_cost": 75,
        "effect_duration": None,
        "uses_per_game": 1
    },
    {
        "powerup_key": "hint",
        "name": "Hint",
        "description": "Get a helpful hint for the current question",
        "icon": "💡",
        "token_cost": 20,
        "effect_duration": None,
        "uses_per_game": 5
    },
]


# ============================================================
# INITIALIZATION FUNCTIONS
# ============================================================

def initialize_badges():
    """Create all badge definitions in the database"""
    for badge_data in ARCADE_BADGES:
        existing = ArcadeBadge.query.filter_by(badge_key=badge_data["badge_key"]).first()
        if not existing:
            badge = ArcadeBadge(**badge_data)
            db.session.add(badge)
    db.session.commit()
    print(f"✅ Initialized {len(ARCADE_BADGES)} arcade badges")


def initialize_powerups():
    """Create all power-up definitions in the database"""
    for powerup_data in POWERUPS:
        existing = PowerUp.query.filter_by(powerup_key=powerup_data["powerup_key"]).first()
        if not existing:
            powerup = PowerUp(**powerup_data)
            db.session.add(powerup)
    db.session.commit()
    print(f"✅ Initialized {len(POWERUPS)} power-ups")


# ============================================================
# BADGE CHECKING & AWARDING
# ============================================================

def check_and_award_badges(student_id, game_session):
    """
    Check if a game session qualifies for any badges and award them.
    Returns list of newly earned badges.
    """
    newly_earned = []

    # Get all badges
    all_badges = ArcadeBadge.query.all()

    # Get student's existing badges
    existing_badge_ids = {sb.badge_id for sb in StudentBadge.query.filter_by(student_id=student_id).all()}

    for badge in all_badges:
        # Skip if already earned
        if badge.id in existing_badge_ids:
            continue

        # Check if badge is game-specific and matches
        if badge.game_key and badge.game_key != game_session.game_key:
            continue

        earned = False

        # Check badge requirements
        if badge.requirement_type == "score":
            earned = game_session.score >= badge.requirement_value

        elif badge.requirement_type == "accuracy":
            earned = game_session.accuracy >= badge.requirement_value

        elif badge.requirement_type == "time":
            # Time badges are for UNDER the requirement (faster is better)
            earned = game_session.time_seconds <= badge.requirement_value

        elif badge.requirement_type == "streak":
            streak = GameStreak.query.filter_by(student_id=student_id).first()
            if streak:
                earned = streak.current_streak >= badge.requirement_value

        elif badge.requirement_type == "total_plays":
            # Count plays of this specific game
            total = GameSession.query.filter_by(
                student_id=student_id,
                game_key=game_session.game_key
            ).count()
            earned = total >= badge.requirement_value

        # Award the badge
        if earned:
            student_badge = StudentBadge(
                student_id=student_id,
                badge_id=badge.id,
                game_key=game_session.game_key
            )
            db.session.add(student_badge)
            newly_earned.append(badge)

    if newly_earned:
        db.session.commit()

    return newly_earned


# ============================================================
# STREAK TRACKING
# ============================================================

def update_game_streak(student_id):
    """
    Update student's game streak based on today's play.
    Returns the updated streak object.
    """
    streak = GameStreak.query.filter_by(student_id=student_id).first()

    if not streak:
        # Create new streak
        streak = GameStreak(
            student_id=student_id,
            current_streak=1,
            longest_streak=1,
            last_played_date=date.today()
        )
        db.session.add(streak)
    else:
        today = date.today()
        last_played = streak.last_played_date

        if last_played == today:
            # Already played today, no change
            pass
        elif last_played == today - timedelta(days=1):
            # Played yesterday, increment streak
            streak.current_streak += 1
            streak.last_played_date = today

            # Update longest streak if needed
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
        else:
            # Streak broken, reset to 1
            streak.current_streak = 1
            streak.last_played_date = today

    db.session.commit()
    return streak


# ============================================================
# DAILY CHALLENGES
# ============================================================

def generate_daily_challenge():
    """
    Generate today's daily challenge if one doesn't exist.
    Returns the DailyChallenge object.
    """
    today = date.today()
    existing = DailyChallenge.query.filter_by(challenge_date=today).first()

    if existing:
        return existing

    # Pick a random game
    games = [
        "speed_math", "number_detective", "fraction_frenzy", "equation_race",
        "element_match", "lab_quiz", "planet_explorer",
        "vocab_builder", "spelling_sprint", "grammar_quest",
        "timeline_challenge", "geography_dash"
    ]

    game_key = random.choice(games)
    grade_level = str(random.randint(1, 12))

    # Set challenging but achievable targets
    challenge = DailyChallenge(
        game_key=game_key,
        challenge_date=today,
        target_score=random.randint(1500, 3000),
        target_accuracy=random.randint(85, 95),
        target_time=random.randint(40, 55),
        grade_level=grade_level,
        bonus_xp=100,
        bonus_tokens=50
    )

    db.session.add(challenge)
    db.session.commit()

    return challenge


def get_todays_challenge():
    """Get today's daily challenge, generating if needed"""
    return generate_daily_challenge()


def check_daily_challenge_completion(student_id, game_session):
    """
    Check if a game session completed today's daily challenge.
    Returns True if challenge was completed (and rewards awarded).
    """
    today = date.today()
    challenge = DailyChallenge.query.filter_by(challenge_date=today).first()

    if not challenge:
        return False

    # Check if this session matches the challenge
    if game_session.game_key != challenge.game_key:
        return False

    if game_session.grade_level != challenge.grade_level:
        return False

    # Check if already completed
    progress = StudentChallengeProgress.query.filter_by(
        student_id=student_id,
        challenge_id=challenge.id
    ).first()

    if progress and progress.completed:
        return False  # Already completed

    # Check if session meets requirements
    requirements_met = (
        (not challenge.target_score or game_session.score >= challenge.target_score) and
        (not challenge.target_accuracy or game_session.accuracy >= challenge.target_accuracy) and
        (not challenge.target_time or game_session.time_seconds <= challenge.target_time)
    )

    if requirements_met:
        # Mark as completed or create progress
        if not progress:
            progress = StudentChallengeProgress(
                student_id=student_id,
                challenge_id=challenge.id,
                best_score=game_session.score,
                best_accuracy=game_session.accuracy,
                best_time=game_session.time_seconds
            )
            db.session.add(progress)

        progress.completed = True
        progress.completed_at = datetime.utcnow()

        # Award bonus rewards (add to session)
        game_session.xp_earned += challenge.bonus_xp
        game_session.tokens_earned += challenge.bonus_tokens

        db.session.commit()
        return True

    else:
        # Update progress with best attempt
        if not progress:
            progress = StudentChallengeProgress(
                student_id=student_id,
                challenge_id=challenge.id,
                best_score=game_session.score,
                best_accuracy=game_session.accuracy,
                best_time=game_session.time_seconds
            )
            db.session.add(progress)
        else:
            # Update if this attempt was better
            if game_session.score > (progress.best_score or 0):
                progress.best_score = game_session.score
            if game_session.accuracy > (progress.best_accuracy or 0):
                progress.best_accuracy = game_session.accuracy
            if not progress.best_time or game_session.time_seconds < progress.best_time:
                progress.best_time = game_session.time_seconds

        db.session.commit()
        return False


# ============================================================
# POWER-UP MANAGEMENT
# ============================================================

def purchase_powerup(student_id, powerup_key, student_tokens):
    """
    Purchase a power-up for a student.
    Returns (success:bool, message:str, remaining_tokens:int)
    """
    powerup = PowerUp.query.filter_by(powerup_key=powerup_key).first()

    if not powerup:
        return False, "Power-up not found", student_tokens

    if student_tokens < powerup.token_cost:
        return False, f"Not enough tokens. Need {powerup.token_cost}, have {student_tokens}", student_tokens

    # Check if student already owns this power-up
    student_powerup = StudentPowerUp.query.filter_by(
        student_id=student_id,
        powerup_id=powerup.id
    ).first()

    if student_powerup:
        # Increment quantity
        student_powerup.quantity += 1
    else:
        # Create new
        student_powerup = StudentPowerUp(
            student_id=student_id,
            powerup_id=powerup.id,
            quantity=1
        )
        db.session.add(student_powerup)

    # Deduct tokens
    remaining_tokens = student_tokens - powerup.token_cost

    db.session.commit()

    return True, f"Purchased {powerup.name}!", remaining_tokens


def get_student_powerups(student_id):
    """
    Get all power-ups owned by a student.
    Returns list of dicts with powerup details and quantities.
    """
    student_powerups = StudentPowerUp.query.filter_by(student_id=student_id).all()

    result = []
    for sp in student_powerups:
        if sp.quantity > 0:
            result.append({
                "id": sp.powerup.id,
                "key": sp.powerup.powerup_key,
                "name": sp.powerup.name,
                "description": sp.powerup.description,
                "icon": sp.powerup.icon,
                "quantity": sp.quantity,
                "uses_per_game": sp.powerup.uses_per_game
            })

    return result


def use_powerup(student_id, powerup_key):
    """
    Use/consume a power-up from student's inventory.
    Returns (success:bool, message:str)
    """
    powerup = PowerUp.query.filter_by(powerup_key=powerup_key).first()

    if not powerup:
        return False, "Power-up not found"

    student_powerup = StudentPowerUp.query.filter_by(
        student_id=student_id,
        powerup_id=powerup.id
    ).first()

    if not student_powerup or student_powerup.quantity <= 0:
        return False, "You don't have this power-up"

    # Decrement quantity
    student_powerup.quantity -= 1
    db.session.commit()

    return True, f"Used {powerup.name}!"


# ============================================================
# STATISTICS
# ============================================================

def get_student_arcade_stats(student_id):
    """
    Get comprehensive arcade statistics for a student.
    Returns dict with various stats.
    """
    # Total games played
    total_games = GameSession.query.filter_by(student_id=student_id).count()

    # Total XP and tokens earned
    sessions = GameSession.query.filter_by(student_id=student_id).all()
    total_xp = sum(s.xp_earned for s in sessions)
    total_tokens = sum(s.tokens_earned for s in sessions)

    # Average accuracy
    accuracies = [s.accuracy for s in sessions if s.accuracy is not None]
    avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else 0

    # Best score
    scores = [s.score for s in sessions if s.score is not None]
    best_score = max(scores) if scores else 0

    # Current streak
    streak = GameStreak.query.filter_by(student_id=student_id).first()
    current_streak = streak.current_streak if streak else 0
    longest_streak = streak.longest_streak if streak else 0

    # Badges earned
    badges_earned = StudentBadge.query.filter_by(student_id=student_id).count()

    # Challenges completed
    challenges_completed = StudentChallengeProgress.query.filter_by(
        student_id=student_id,
        completed=True
    ).count()

    return {
        "total_games": total_games,
        "total_xp": total_xp,
        "total_tokens": total_tokens,
        "avg_accuracy": round(avg_accuracy, 1),
        "best_score": best_score,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "badges_earned": badges_earned,
        "challenges_completed": challenges_completed
    }
