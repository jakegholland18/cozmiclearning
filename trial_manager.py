"""
Trial Management System for CozmicLearning
==========================================

Handles 7-day free trial lifecycle:
- Trial signup and activation
- Status checking
- Access control
- Expiration handling
- Upgrade prompts

All new users get 7 days of full access.
After trial: 2-day grace period, then hard block.
"""

from datetime import datetime, timedelta
from functools import wraps
from flask import redirect, flash, session

# ============================================================
# CONFIGURATION
# ============================================================

TRIAL_DAYS = 7  # 7-day free trial
GRACE_PERIOD_DAYS = 2  # 2 days grace period after trial
TRIAL_WARNING_DAYS = [3, 1]  # Show warnings at 3 days and 1 day remaining


# ============================================================
# CORE TRIAL FUNCTIONS
# ============================================================

def start_trial(user):
    """
    Start a 7-day trial for a new user.

    Args:
        user: Student, Parent, or Teacher model instance

    Sets:
        - trial_start = now
        - trial_end = now + 7 days
        - plan = "trial"
        - subscription_active = False
    """
    from models import db

    now = datetime.utcnow()

    user.trial_start = now
    user.trial_end = now + timedelta(days=TRIAL_DAYS)
    user.plan = "trial"
    user.subscription_active = False

    db.session.add(user)
    db.session.commit()

    print(f"✅ Trial started for {user.email}: {TRIAL_DAYS} days ending {user.trial_end.strftime('%Y-%m-%d')}")

    return {
        "trial_start": user.trial_start,
        "trial_end": user.trial_end,
        "days": TRIAL_DAYS
    }


def get_trial_status(user):
    """
    Get comprehensive trial status for a user.

    Args:
        user: Student, Parent, or Teacher model instance

    Returns:
        dict: {
            "status": str,  # "paid" | "active" | "ending_soon" | "grace" | "expired"
            "days_remaining": int,
            "trial_end_date": datetime,
            "can_access": bool,
            "should_show_warning": bool,
            "message": str,
            "upgrade_urgency": str  # "none" | "low" | "medium" | "high" | "critical"
        }
    """
    now = datetime.utcnow()

    # User has active paid subscription
    if user.subscription_active:
        return {
            "status": "paid",
            "days_remaining": None,
            "trial_end_date": None,
            "can_access": True,
            "should_show_warning": False,
            "message": f"Active {user.plan} subscription",
            "upgrade_urgency": "none"
        }

    # No trial configured (old users or error)
    if not user.trial_start or not user.trial_end:
        return {
            "status": "no_trial",
            "days_remaining": 0,
            "trial_end_date": None,
            "can_access": False,
            "should_show_warning": True,
            "message": "Please contact support to activate your account",
            "upgrade_urgency": "critical"
        }

    # Calculate days remaining
    time_remaining = user.trial_end - now
    days_remaining = max(0, time_remaining.days)
    grace_period_end = user.trial_end + timedelta(days=GRACE_PERIOD_DAYS)

    # Trial is active
    if now < user.trial_end:
        # Ending very soon (last day)
        if days_remaining == 0:
            return {
                "status": "ending_soon",
                "days_remaining": 0,
                "trial_end_date": user.trial_end,
                "can_access": True,
                "should_show_warning": True,
                "message": "⏰ Last day of your free trial! Upgrade now to keep access.",
                "upgrade_urgency": "critical"
            }
        # Show warning in final days
        elif days_remaining <= 3:
            return {
                "status": "ending_soon",
                "days_remaining": days_remaining,
                "trial_end_date": user.trial_end,
                "can_access": True,
                "should_show_warning": True,
                "message": f"⏰ Only {days_remaining} day{'s' if days_remaining > 1 else ''} left in your trial!",
                "upgrade_urgency": "high"
            }
        # Normal active trial
        else:
            return {
                "status": "active",
                "days_remaining": days_remaining,
                "trial_end_date": user.trial_end,
                "can_access": True,
                "should_show_warning": False,
                "message": f"{days_remaining} days remaining in your free trial",
                "upgrade_urgency": "low"
            }

    # Grace period (after trial but before hard block)
    elif now < grace_period_end:
        days_until_block = (grace_period_end - now).days
        return {
            "status": "grace",
            "days_remaining": 0,
            "trial_end_date": user.trial_end,
            "can_access": True,  # Limited/read-only access
            "should_show_warning": True,
            "message": f"⚠️ Your trial expired. You have {days_until_block} day{'s' if days_until_block != 1 else ''} to upgrade before losing access.",
            "upgrade_urgency": "critical"
        }

    # Trial expired (hard block)
    else:
        return {
            "status": "expired",
            "days_remaining": 0,
            "trial_end_date": user.trial_end,
            "can_access": False,
            "should_show_warning": True,
            "message": "❌ Your trial has ended. Upgrade to restore access to your account.",
            "upgrade_urgency": "critical"
        }


def can_access_feature(user, feature_name=None):
    """
    Check if user can access a feature based on trial/subscription status.

    Args:
        user: Student, Parent, or Teacher model instance
        feature_name: Optional specific feature to check

    Returns:
        tuple: (can_access: bool, reason: str)
    """
    status = get_trial_status(user)

    # Paid users get everything
    if status["status"] == "paid":
        return (True, "Active subscription")

    # Active trial gets everything
    if status["status"] in ["active", "ending_soon"]:
        return (True, "Trial active")

    # Grace period gets limited access
    if status["status"] == "grace":
        # Allow viewing but not creating
        readonly_features = ["dashboard", "view_progress", "view_assignments"]
        if feature_name in readonly_features:
            return (True, "Grace period - view only")
        else:
            return (False, "Trial expired - upgrade to create new content")

    # Hard blocked users get nothing
    if status["status"] == "expired":
        return (False, "Trial expired - please upgrade")

    # No trial configured
    return (False, "Account not activated")


# ============================================================
# DECORATORS FOR ACCESS CONTROL
# ============================================================

def trial_required(f):
    """
    Decorator: Require active trial or paid subscription.
    Redirects to upgrade page if trial expired (hard block).
    Shows warning if in grace period but allows access.

    Usage:
        @app.route("/practice")
        @trial_required
        def practice():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get current user (adjust based on your session management)
        user = get_current_user_from_session()

        if not user:
            flash("Please log in to continue", "warning")
            return redirect("/login")

        status = get_trial_status(user)

        # Hard block - force upgrade
        if status["status"] == "expired":
            flash(status["message"], "error")
            return redirect("/upgrade")

        # Grace period - show warning but allow access
        if status["status"] == "grace":
            flash(status["message"], "warning")

        # Allow access
        return f(*args, **kwargs)

    return decorated_function


def trial_required_create(f):
    """
    Decorator: Require active trial or paid subscription for CREATE actions.
    Blocks during grace period (read-only mode).

    Usage:
        @app.route("/create-assignment", methods=["POST"])
        @trial_required_create
        def create_assignment():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user_from_session()

        if not user:
            flash("Please log in to continue", "warning")
            return redirect("/login")

        can_access, reason = can_access_feature(user, "create")

        if not can_access:
            flash(f"Upgrade required: {reason}", "error")
            return redirect("/upgrade")

        return f(*args, **kwargs)

    return decorated_function


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_current_user_from_session():
    """
    Get current user from session.
    This should be replaced with your actual user retrieval logic.
    """
    from models import Student, Parent, Teacher

    user_id = session.get("user_id")
    user_type = session.get("user_type")

    if not user_id or not user_type:
        return None

    if user_type == "student":
        return Student.query.get(user_id)
    elif user_type == "parent":
        return Parent.query.get(user_id)
    elif user_type == "teacher":
        return Teacher.query.get(user_id)

    return None


def get_trial_progress_percent(user):
    """
    Get trial progress as percentage (0-100).
    Useful for progress bars.

    Returns:
        int: 0-100 representing days used
    """
    if user.subscription_active:
        return 100  # Paid = 100% complete

    if not user.trial_start or not user.trial_end:
        return 0

    total_days = (user.trial_end - user.trial_start).days
    elapsed_days = (datetime.utcnow() - user.trial_start).days

    if elapsed_days < 0:
        return 0
    if elapsed_days > total_days:
        return 100

    return int((elapsed_days / total_days) * 100)


def should_send_trial_reminder(user):
    """
    Check if user should receive trial reminder email.

    Returns:
        tuple: (should_send: bool, reminder_type: str)
            reminder_type: "3_days" | "1_day" | "expired" | "grace_ending"
    """
    status = get_trial_status(user)

    # Don't send to paid users
    if status["status"] == "paid":
        return (False, None)

    # 3 days remaining
    if status["days_remaining"] == 3:
        return (True, "3_days")

    # 1 day remaining
    if status["days_remaining"] == 1:
        return (True, "1_day")

    # Just expired (day 0 of grace)
    if status["status"] == "grace":
        grace_days = (datetime.utcnow() - user.trial_end).days
        if grace_days == 0:
            return (True, "expired")
        # Last day of grace
        elif grace_days == GRACE_PERIOD_DAYS - 1:
            return (True, "grace_ending")

    return (False, None)


# ============================================================
# ADMIN FUNCTIONS
# ============================================================

def extend_trial(user, extra_days):
    """
    Extend trial by X days (admin only).

    Args:
        user: User to extend trial for
        extra_days: Number of days to add

    Returns:
        dict: New trial end date
    """
    from models import db

    if not user.trial_end:
        return {"error": "User has no active trial"}

    old_end = user.trial_end
    user.trial_end = user.trial_end + timedelta(days=extra_days)
    db.session.add(user)
    db.session.commit()

    print(f"✅ Extended trial for {user.email} by {extra_days} days: {old_end} → {user.trial_end}")

    return {
        "old_end": old_end,
        "new_end": user.trial_end,
        "extra_days": extra_days
    }


def convert_to_paid(user, plan="premium"):
    """
    Convert trial user to paid subscriber.
    Called after successful Stripe payment.

    Args:
        user: User to convert
        plan: Plan name (premium, basic, pro, etc.)

    Returns:
        dict: Conversion confirmation
    """
    from models import db

    user.subscription_active = True
    user.plan = plan
    # Keep trial dates for analytics
    db.session.add(user)
    db.session.commit()

    print(f"✅ Converted {user.email} from trial to paid ({plan})")

    return {
        "success": True,
        "user_id": user.id,
        "plan": plan,
        "trial_start": user.trial_start,
        "trial_end": user.trial_end,
        "converted_at": datetime.utcnow()
    }


# ============================================================
# TEMPLATE CONTEXT PROCESSOR
# ============================================================

def trial_context_processor():
    """
    Add trial status to all templates.

    Usage in app.py:
        from trial_manager import trial_context_processor
        app.context_processor(trial_context_processor)

    Then in templates:
        {{ trial_status.days_remaining }}
        {{ trial_status.message }}
    """
    user = get_current_user_from_session()

    if not user:
        return dict(trial_status=None)

    return dict(
        trial_status=get_trial_status(user),
        trial_progress=get_trial_progress_percent(user)
    )
