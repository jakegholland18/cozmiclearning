"""
Achievement & Badge System
Manages unlocking, tracking, and displaying student achievements
"""

from models import db, Achievement, StudentAchievement, ActivityLog, Student
from datetime import datetime


# ============================================================
# ACHIEVEMENT DEFINITIONS
# ============================================================

ACHIEVEMENT_CATALOG = [
    # Milestone Achievements
    {"name": "First Steps", "description": "Asked your first question", "icon": "👶", "category": "milestone", "requirement_value": 1},
    {"name": "Knowledge Seeker", "description": "Asked 10 questions", "icon": "🔍", "category": "milestone", "requirement_value": 10},
    {"name": "Curious Mind", "description": "Asked 50 questions", "icon": "🧠", "category": "milestone", "requirement_value": 50},
    {"name": "Question Master", "description": "Asked 100 questions", "icon": "🎓", "category": "milestone", "requirement_value": 100},
    
    # Streak Achievements
    {"name": "Getting Started", "description": "3-day learning streak", "icon": "🔥", "category": "streak", "requirement_value": 3},
    {"name": "Week Warrior", "description": "7-day learning streak", "icon": "⚡", "category": "streak", "requirement_value": 7},
    {"name": "Unstoppable", "description": "14-day learning streak", "icon": "💪", "category": "streak", "requirement_value": 14},
    {"name": "Dedication Legend", "description": "30-day learning streak", "icon": "👑", "category": "streak", "requirement_value": 30},
    
    # Level Achievements
    {"name": "Novice Explorer", "description": "Reached Level 5", "icon": "🌱", "category": "level", "requirement_value": 5},
    {"name": "Skilled Learner", "description": "Reached Level 10", "icon": "🌟", "category": "level", "requirement_value": 10},
    {"name": "Master Scholar", "description": "Reached Level 20", "icon": "💎", "category": "level", "requirement_value": 20},
    {"name": "Cosmic Genius", "description": "Reached Level 50", "icon": "🌌", "category": "level", "requirement_value": 50},
    
    # XP Achievements
    {"name": "Point Collector", "description": "Earned 1,000 XP", "icon": "⭐", "category": "xp", "requirement_value": 1000},
    {"name": "XP Champion", "description": "Earned 5,000 XP", "icon": "🏆", "category": "xp", "requirement_value": 5000},
    {"name": "Experience Master", "description": "Earned 10,000 XP", "icon": "💫", "category": "xp", "requirement_value": 10000},
    
    # Subject Exploration
    {"name": "Planet Explorer", "description": "Visited 3 different subjects", "icon": "🚀", "category": "exploration", "requirement_value": 3},
    {"name": "Galaxy Traveler", "description": "Visited all 11 subjects", "icon": "🌍", "category": "exploration", "requirement_value": 11},
    
    # Practice Achievements
    {"name": "Practice Makes Perfect", "description": "Completed 5 practice missions", "icon": "📝", "category": "practice", "requirement_value": 5},
    {"name": "Assignment Ace", "description": "Completed 10 assignments with 90%+ average", "icon": "🎯", "category": "mastery", "requirement_value": 10},
]


# ============================================================
# INITIALIZATION
# ============================================================

def initialize_achievements():
    """Create achievement records in database if they don't exist"""
    for ach_data in ACHIEVEMENT_CATALOG:
        existing = Achievement.query.filter_by(name=ach_data["name"]).first()
        if not existing:
            achievement = Achievement(
                name=ach_data["name"],
                description=ach_data["description"],
                icon=ach_data["icon"],
                category=ach_data["category"],
                requirement_value=ach_data["requirement_value"]
            )
            db.session.add(achievement)
    
    db.session.commit()


# ============================================================
# UNLOCK & CHECK LOGIC
# ============================================================

def check_and_award_achievements(student_id, session_data):
    """
    Check if student has unlocked new achievements based on current stats
    Returns list of newly unlocked achievements
    """
    student = Student.query.get(student_id)
    if not student:
        return []
    
    newly_unlocked = []
    
    # Get current student achievements
    earned_ids = {sa.achievement_id for sa in StudentAchievement.query.filter_by(student_id=student_id).all()}
    
    # Get all achievements
    all_achievements = Achievement.query.all()
    
    for achievement in all_achievements:
        # Skip if already earned
        if achievement.id in earned_ids:
            continue
        
        # Check if requirements are met
        earned = False
        
        if achievement.category == "streak":
            if session_data.get("streak", 0) >= achievement.requirement_value:
                earned = True
        
        elif achievement.category == "level":
            if session_data.get("level", 1) >= achievement.requirement_value:
                earned = True
        
        elif achievement.category == "xp":
            if session_data.get("xp", 0) >= achievement.requirement_value:
                earned = True
        
        elif achievement.category == "milestone":
            # Count questions from activity log
            question_count = ActivityLog.query.filter_by(
                student_id=student_id,
                activity_type="question_answered"
            ).count()
            if question_count >= achievement.requirement_value:
                earned = True
        
        elif achievement.category == "exploration":
            # Count unique subjects visited
            unique_subjects = db.session.query(ActivityLog.subject).filter(
                ActivityLog.student_id == student_id,
                ActivityLog.subject.isnot(None)
            ).distinct().count()
            if unique_subjects >= achievement.requirement_value:
                earned = True
        
        elif achievement.category == "practice":
            # Count completed assignments
            practice_count = ActivityLog.query.filter_by(
                student_id=student_id,
                activity_type="assignment_completed"
            ).count()
            if practice_count >= achievement.requirement_value:
                earned = True
        
        # Award achievement if earned
        if earned:
            student_achievement = StudentAchievement(
                student_id=student_id,
                achievement_id=achievement.id,
                earned_at=datetime.utcnow()
            )
            db.session.add(student_achievement)
            
            # Log achievement in activity feed
            activity = ActivityLog(
                student_id=student_id,
                activity_type="achievement_earned",
                description=f"Unlocked: {achievement.name}",
                xp_earned=50  # Bonus XP for achievements
            )
            db.session.add(activity)
            
            newly_unlocked.append(achievement)
    
    db.session.commit()
    return newly_unlocked


def get_student_achievements(student_id):
    """Get all achievements earned by student"""
    earned = db.session.query(Achievement, StudentAchievement).join(
        StudentAchievement, Achievement.id == StudentAchievement.achievement_id
    ).filter(StudentAchievement.student_id == student_id).order_by(
        StudentAchievement.earned_at.desc()
    ).all()
    
    return [{"achievement": ach, "earned_at": sa.earned_at} for ach, sa in earned]


def get_achievement_progress(student_id, session_data):
    """
    Get progress towards all achievements (for display)
    Returns dict with achievement info and progress percentage
    """
    student = Student.query.get(student_id)
    earned_ids = {sa.achievement_id for sa in StudentAchievement.query.filter_by(student_id=student_id).all()}
    all_achievements = Achievement.query.all()
    
    progress = []
    
    for achievement in all_achievements:
        current_value = 0
        
        if achievement.category == "streak":
            current_value = session_data.get("streak", 0)
        elif achievement.category == "level":
            current_value = session_data.get("level", 1)
        elif achievement.category == "xp":
            current_value = session_data.get("xp", 0)
        elif achievement.category == "milestone":
            current_value = ActivityLog.query.filter_by(
                student_id=student_id,
                activity_type="question_answered"
            ).count()
        elif achievement.category == "exploration":
            current_value = db.session.query(ActivityLog.subject).filter(
                ActivityLog.student_id == student_id,
                ActivityLog.subject.isnot(None)
            ).distinct().count()
        elif achievement.category == "practice":
            current_value = ActivityLog.query.filter_by(
                student_id=student_id,
                activity_type="assignment_completed"
            ).count()
        
        percent = min(100, int((current_value / achievement.requirement_value) * 100)) if achievement.requirement_value > 0 else 0
        
        progress.append({
            "achievement": achievement,
            "current": current_value,
            "required": achievement.requirement_value,
            "percent": percent,
            "earned": achievement.id in earned_ids
        })
    
    return progress


# ============================================================
# ACTIVITY LOGGING
# ============================================================

def log_activity(student_id, activity_type, subject=None, description="", xp_earned=0):
    """Log student activity for tracking and achievements"""
    activity = ActivityLog(
        student_id=student_id,
        activity_type=activity_type,
        subject=subject,
        description=description,
        xp_earned=xp_earned
    )
    db.session.add(activity)
    db.session.commit()


def get_recent_activities(student_id, limit=10):
    """Get recent student activities for activity feed"""
    activities = ActivityLog.query.filter_by(
        student_id=student_id
    ).order_by(ActivityLog.created_at.desc()).limit(limit).all()
    
    return activities
