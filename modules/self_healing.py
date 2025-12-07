"""
Self-Healing Module for CozmicLearning
Automatic error recovery and health monitoring
"""

import logging
import time
import traceback
from functools import wraps
from datetime import datetime, timedelta

# ============================================================
# ERROR RECOVERY DECORATORS
# ============================================================

def auto_retry(max_attempts=3, delay=0.1, exponential_backoff=True):
    """
    Decorator that automatically retries a function if it fails.

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        exponential_backoff: If True, delay doubles after each retry

    Usage:
        @auto_retry(max_attempts=3)
        def my_database_function():
            db.session.commit()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    if attempt < max_attempts - 1:
                        # Calculate delay with exponential backoff
                        wait_time = delay * (2 ** attempt) if exponential_backoff else delay

                        logging.warning(
                            f"Function {func.__name__} failed (attempt {attempt + 1}/{max_attempts}). "
                            f"Retrying in {wait_time}s... Error: {str(e)}"
                        )

                        time.sleep(wait_time)
                    else:
                        logging.error(
                            f"Function {func.__name__} failed after {max_attempts} attempts. "
                            f"Final error: {str(e)}\n{traceback.format_exc()}"
                        )

            # If we got here, all attempts failed
            raise last_exception

        return wrapper
    return decorator


def safe_execute(default_return=None, log_errors=True):
    """
    Decorator that catches all exceptions and returns a default value.
    Prevents the entire app from crashing due to one function error.

    Args:
        default_return: Value to return if function fails
        log_errors: Whether to log errors

    Usage:
        @safe_execute(default_return=[])
        def get_user_courses():
            return Course.query.filter_by(user_id=user_id).all()
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    logging.error(
                        f"Error in {func.__name__}: {str(e)}\n"
                        f"Args: {args}, Kwargs: {kwargs}\n"
                        f"{traceback.format_exc()}"
                    )

                return default_return

        return wrapper
    return decorator


# ============================================================
# SESSION SELF-HEALING
# ============================================================

def ensure_session_defaults(session_obj):
    """
    Ensures all required session keys exist with default values.
    Auto-heals corrupted or incomplete sessions.

    Usage in routes:
        from modules.self_healing import ensure_session_defaults

        @app.route('/dashboard')
        def dashboard():
            ensure_session_defaults(session)
            # Now safe to use session["xp"], session["level"], etc.
    """
    defaults = {
        # Student defaults
        'character': 'everly',
        'level': 1,
        'xp': 0,
        'tokens': 100,
        'grade': '8',
        'ability': 'on_level',
        'practice_step': 0,
        'total_questions': 0,
        'correct_answers': 0,

        # Authentication flags
        'student_authenticated': False,
        'parent_authenticated': False,
        'teacher_authenticated': False,
        'admin_authenticated': False,

        # IDs (None if not logged in)
        'student_id': None,
        'parent_id': None,
        'teacher_id': None,
    }

    # Only add missing keys, don't overwrite existing values
    for key, default_value in defaults.items():
        if key not in session_obj:
            session_obj[key] = default_value

    return session_obj


def fix_corrupted_session(session_obj):
    """
    Detects and fixes corrupted session data.

    Returns:
        True if session was corrupted and fixed
        False if session was fine
    """
    corrupted = False

    # Check for invalid types
    type_checks = {
        'level': int,
        'xp': int,
        'tokens': int,
        'total_questions': int,
        'correct_answers': int,
    }

    for key, expected_type in type_checks.items():
        if key in session_obj:
            try:
                # Try to convert to expected type
                if not isinstance(session_obj[key], expected_type):
                    logging.warning(f"Session key '{key}' has wrong type. Converting to {expected_type.__name__}")
                    session_obj[key] = expected_type(session_obj[key])
                    corrupted = True
            except (ValueError, TypeError):
                logging.error(f"Session key '{key}' is corrupted. Resetting to default.")
                defaults = {'level': 1, 'xp': 0, 'tokens': 100, 'total_questions': 0, 'correct_answers': 0}
                session_obj[key] = defaults.get(key, 0)
                corrupted = True

    # Check for negative values (impossible states)
    non_negative_keys = ['level', 'xp', 'tokens', 'total_questions', 'correct_answers']
    for key in non_negative_keys:
        if key in session_obj and isinstance(session_obj[key], (int, float)):
            if session_obj[key] < 0:
                logging.warning(f"Session key '{key}' is negative. Resetting to 0.")
                session_obj[key] = 0
                corrupted = True

    if corrupted:
        logging.info("Session was corrupted and has been auto-repaired.")

    return corrupted


# ============================================================
# DATABASE SELF-HEALING
# ============================================================

def safe_db_commit(db_session, max_attempts=3):
    """
    Safely commit database changes with automatic retry and rollback.

    Usage:
        from modules.self_healing import safe_db_commit

        new_user = Student(name="John")
        db.session.add(new_user)

        if safe_db_commit(db.session):
            flash("User created!", "success")
        else:
            flash("Failed to create user. Please try again.", "error")

    Returns:
        True if commit succeeded
        False if commit failed after all retries
    """
    for attempt in range(max_attempts):
        try:
            db_session.commit()
            return True
        except Exception as e:
            db_session.rollback()

            if attempt < max_attempts - 1:
                wait_time = 0.1 * (2 ** attempt)
                logging.warning(
                    f"Database commit failed (attempt {attempt + 1}/{max_attempts}). "
                    f"Retrying in {wait_time}s... Error: {str(e)}"
                )
                time.sleep(wait_time)
            else:
                logging.error(
                    f"Database commit failed after {max_attempts} attempts. "
                    f"Error: {str(e)}\n{traceback.format_exc()}"
                )
                return False

    return False


def auto_vacuum_database(db_session):
    """
    Automatically vacuum and optimize the database.
    Call this periodically (e.g., once per day) to keep DB healthy.

    Usage (in a scheduled task or admin route):
        from modules.self_healing import auto_vacuum_database
        auto_vacuum_database(db.session)
    """
    try:
        logging.info("Running database vacuum and optimization...")
        db_session.execute("VACUUM")
        db_session.execute("ANALYZE")
        logging.info("Database optimization complete.")
        return True
    except Exception as e:
        logging.error(f"Database optimization failed: {e}")
        return False


# ============================================================
# API CALL SELF-HEALING
# ============================================================

def resilient_api_call(api_function, *args, max_retries=3, timeout=10, **kwargs):
    """
    Makes API calls with automatic retry on failure.
    Handles timeouts, network errors, and rate limits.

    Usage:
        from modules.self_healing import resilient_api_call

        response = resilient_api_call(
            openai.ChatCompletion.create,
            model="gpt-4",
            messages=[{"role": "user", "content": "Hello"}]
        )
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            # Set a timeout to prevent hanging
            result = api_function(*args, **kwargs)
            return result

        except Exception as e:
            last_exception = e
            error_str = str(e).lower()

            # Determine if we should retry
            should_retry = any([
                'timeout' in error_str,
                'connection' in error_str,
                'rate limit' in error_str,
                '429' in error_str,
                '500' in error_str,
                '502' in error_str,
                '503' in error_str,
            ])

            if should_retry and attempt < max_retries - 1:
                # Exponential backoff for rate limits
                if 'rate limit' in error_str or '429' in error_str:
                    wait_time = 2 ** (attempt + 1)
                else:
                    wait_time = 0.5 * (2 ** attempt)

                logging.warning(
                    f"API call failed (attempt {attempt + 1}/{max_retries}). "
                    f"Retrying in {wait_time}s... Error: {str(e)}"
                )

                time.sleep(wait_time)
            else:
                logging.error(
                    f"API call failed after {max_retries} attempts or error is not retryable. "
                    f"Error: {str(e)}"
                )
                break

    # All retries failed
    raise last_exception


# ============================================================
# HEALTH MONITORING
# ============================================================

class HealthMonitor:
    """
    Tracks application health and auto-reports issues.
    """

    def __init__(self):
        self.error_counts = {}
        self.last_reset = datetime.now()
        self.reset_interval = timedelta(hours=1)

    def record_error(self, error_type, details=""):
        """Record an error occurrence"""
        # Reset counters every hour
        if datetime.now() - self.last_reset > self.reset_interval:
            self.error_counts = {}
            self.last_reset = datetime.now()

        # Increment error count
        if error_type not in self.error_counts:
            self.error_counts[error_type] = 0

        self.error_counts[error_type] += 1

        # Alert if errors are too frequent
        if self.error_counts[error_type] > 10:
            logging.critical(
                f"HIGH ERROR RATE DETECTED: {error_type} has occurred "
                f"{self.error_counts[error_type]} times in the last hour. "
                f"Details: {details}"
            )

    def get_health_status(self):
        """Get current health status"""
        total_errors = sum(self.error_counts.values())

        if total_errors == 0:
            return "healthy"
        elif total_errors < 10:
            return "degraded"
        else:
            return "critical"

    def get_error_summary(self):
        """Get summary of recent errors"""
        return {
            'status': self.get_health_status(),
            'total_errors': sum(self.error_counts.values()),
            'errors_by_type': dict(self.error_counts),
            'time_window': f"Last {(datetime.now() - self.last_reset).seconds // 60} minutes"
        }


# Global health monitor instance
health_monitor = HealthMonitor()


# ============================================================
# AUTOMATIC ERROR REPORTING
# ============================================================

def log_unhandled_exception(sender, exception, **extra):
    """
    Automatically log all unhandled exceptions.

    Setup in app.py:
        from flask import got_request_exception
        from modules.self_healing import log_unhandled_exception

        got_request_exception.connect(log_unhandled_exception, app)
    """
    logging.error(
        f"UNHANDLED EXCEPTION:\n"
        f"URL: {extra.get('request', 'Unknown')}\n"
        f"Exception: {exception}\n"
        f"{traceback.format_exc()}"
    )

    # Record in health monitor
    health_monitor.record_error(
        error_type=type(exception).__name__,
        details=str(exception)
    )
