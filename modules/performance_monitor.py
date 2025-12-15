# modules/performance_monitor.py
"""
Performance Monitoring System for CozmicLearning

Tracks:
- User signups/logins
- AI question volume
- Response times
- Error rates
- Active users

Usage:
    from modules.performance_monitor import track_event, get_metrics_summary

    # Track events
    track_event('signup', user_type='student')
    track_event('ai_question', subject='num_forge', response_time=3.2)

    # Get summary
    summary = get_metrics_summary()
"""

import os
import json
from datetime import datetime, timedelta
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


# -------------------------------------------------------
# IN-MEMORY METRICS STORAGE
# (For production, use Redis or database)
# -------------------------------------------------------
_metrics = {
    'signups': defaultdict(int),      # {date: count}
    'logins': defaultdict(int),       # {date: count}
    'ai_questions': defaultdict(int), # {date: count}
    'errors': defaultdict(int),       # {date: count}
    'response_times': [],             # [time1, time2, ...]
    'active_users': set(),            # {user_id1, user_id2, ...}
}

_daily_metrics = {
    'last_reset': datetime.utcnow().date()
}


# -------------------------------------------------------
# TRACK EVENTS
# -------------------------------------------------------
def track_event(event_type: str, **kwargs):
    """
    Track a performance event.

    Args:
        event_type: 'signup', 'login', 'ai_question', 'error', 'page_view'
        **kwargs: Additional context (user_type, subject, response_time, etc.)

    Examples:
        track_event('signup', user_type='student')
        track_event('login', user_id=123)
        track_event('ai_question', subject='num_forge', response_time=3.2)
        track_event('error', error_type='timeout', route='/ask')
    """
    today = datetime.utcnow().date()

    # Reset daily metrics if new day
    if _daily_metrics['last_reset'] != today:
        reset_daily_metrics()

    try:
        if event_type == 'signup':
            _metrics['signups'][str(today)] += 1
            user_type = kwargs.get('user_type', 'unknown')
            logger.info(f"📊 METRIC: New {user_type} signup")

        elif event_type == 'login':
            _metrics['logins'][str(today)] += 1
            user_id = kwargs.get('user_id')
            if user_id:
                _metrics['active_users'].add(user_id)
            logger.info(f"📊 METRIC: User login (ID: {user_id})")

        elif event_type == 'ai_question':
            _metrics['ai_questions'][str(today)] += 1
            subject = kwargs.get('subject', 'unknown')
            response_time = kwargs.get('response_time', 0)
            if response_time:
                _metrics['response_times'].append(response_time)
            logger.info(f"📊 METRIC: AI question - {subject} ({response_time:.2f}s)")

        elif event_type == 'error':
            _metrics['errors'][str(today)] += 1
            error_type = kwargs.get('error_type', 'unknown')
            route = kwargs.get('route', 'unknown')
            logger.error(f"📊 METRIC: Error - {error_type} on {route}")

        elif event_type == 'page_view':
            # Track page views if needed
            page = kwargs.get('page', 'unknown')
            logger.debug(f"📊 METRIC: Page view - {page}")

        # Keep response_times list manageable (last 1000 only)
        if len(_metrics['response_times']) > 1000:
            _metrics['response_times'] = _metrics['response_times'][-1000:]

    except Exception as e:
        logger.error(f"Error tracking metric: {e}")


def reset_daily_metrics():
    """Reset metrics for new day."""
    _daily_metrics['last_reset'] = datetime.utcnow().date()
    _metrics['active_users'].clear()
    logger.info("📊 Daily metrics reset")


# -------------------------------------------------------
# GET METRICS SUMMARY
# -------------------------------------------------------
def get_metrics_summary(days: int = 7) -> dict:
    """
    Get summary of metrics for last N days.

    Args:
        days: Number of days to include (default 7)

    Returns:
        dict with metrics summary
    """
    today = datetime.utcnow().date()
    date_range = [(today - timedelta(days=i)).isoformat() for i in range(days)]

    # Calculate totals
    total_signups = sum(_metrics['signups'].get(d, 0) for d in date_range)
    total_logins = sum(_metrics['logins'].get(d, 0) for d in date_range)
    total_questions = sum(_metrics['ai_questions'].get(d, 0) for d in date_range)
    total_errors = sum(_metrics['errors'].get(d, 0) for d in date_range)

    # Calculate average response time
    response_times = _metrics['response_times']
    avg_response_time = sum(response_times) / len(response_times) if response_times else 0

    # Active users today
    active_users_count = len(_metrics['active_users'])

    summary = {
        'period': f'Last {days} days',
        'total_signups': total_signups,
        'total_logins': total_logins,
        'total_ai_questions': total_questions,
        'total_errors': total_errors,
        'active_users_today': active_users_count,
        'avg_response_time': round(avg_response_time, 2),
        'daily_breakdown': {
            'signups': {d: _metrics['signups'].get(d, 0) for d in date_range},
            'logins': {d: _metrics['logins'].get(d, 0) for d in date_range},
            'ai_questions': {d: _metrics['ai_questions'].get(d, 0) for d in date_range},
            'errors': {d: _metrics['errors'].get(d, 0) for d in date_range},
        }
    }

    return summary


def print_metrics_summary(days: int = 7):
    """Print formatted metrics summary to console."""
    summary = get_metrics_summary(days)

    print("\n" + "="*60)
    print(f"📊 COZMICLEARNING METRICS - {summary['period']}")
    print("="*60)
    print(f"\n📈 TOTALS:")
    print(f"   Signups:        {summary['total_signups']}")
    print(f"   Logins:         {summary['total_logins']}")
    print(f"   AI Questions:   {summary['total_ai_questions']}")
    print(f"   Errors:         {summary['total_errors']}")
    print(f"   Active Today:   {summary['active_users_today']}")
    print(f"   Avg Response:   {summary['avg_response_time']}s")
    print("="*60 + "\n")


# -------------------------------------------------------
# PERFORMANCE ALERTS
# -------------------------------------------------------
def check_performance_alerts() -> list:
    """
    Check for performance issues and return alerts.

    Returns:
        list of alert messages
    """
    alerts = []

    # Check response times
    response_times = _metrics['response_times']
    if response_times:
        avg_response = sum(response_times) / len(response_times)
        if avg_response > 5:
            alerts.append(f"⚠️ High average response time: {avg_response:.2f}s")

    # Check error rate
    today = datetime.utcnow().date().isoformat()
    errors_today = _metrics['errors'].get(today, 0)
    questions_today = _metrics['ai_questions'].get(today, 0)

    if questions_today > 0:
        error_rate = (errors_today / questions_today) * 100
        if error_rate > 5:
            alerts.append(f"⚠️ High error rate: {error_rate:.1f}%")

    # Check active users (approaching capacity)
    active_users = len(_metrics['active_users'])
    if active_users > 40:
        alerts.append(f"⚠️ High concurrent users: {active_users} (approaching capacity)")

    return alerts


# -------------------------------------------------------
# SAVE/LOAD METRICS (PERSISTENCE)
# -------------------------------------------------------
def save_metrics_to_file(filepath: str = 'metrics_backup.json'):
    """Save metrics to file for persistence."""
    try:
        metrics_serializable = {
            'signups': dict(_metrics['signups']),
            'logins': dict(_metrics['logins']),
            'ai_questions': dict(_metrics['ai_questions']),
            'errors': dict(_metrics['errors']),
            'response_times': _metrics['response_times'],
            'active_users': list(_metrics['active_users']),
            'last_updated': datetime.utcnow().isoformat()
        }

        with open(filepath, 'w') as f:
            json.dump(metrics_serializable, f, indent=2)

        logger.info(f"Metrics saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving metrics: {e}")


def load_metrics_from_file(filepath: str = 'metrics_backup.json'):
    """Load metrics from file."""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)

            _metrics['signups'] = defaultdict(int, data.get('signups', {}))
            _metrics['logins'] = defaultdict(int, data.get('logins', {}))
            _metrics['ai_questions'] = defaultdict(int, data.get('ai_questions', {}))
            _metrics['errors'] = defaultdict(int, data.get('errors', {}))
            _metrics['response_times'] = data.get('response_times', [])
            _metrics['active_users'] = set(data.get('active_users', []))

            logger.info(f"Metrics loaded from {filepath}")
    except Exception as e:
        logger.error(f"Error loading metrics: {e}")


# -------------------------------------------------------
# WEEKLY REPORT GENERATOR
# -------------------------------------------------------
def generate_weekly_report() -> str:
    """
    Generate formatted weekly performance report.

    Returns:
        str: Formatted report text
    """
    summary = get_metrics_summary(days=7)

    report = f"""
╔══════════════════════════════════════════════════════════╗
║       COZMICLEARNING WEEKLY PERFORMANCE REPORT          ║
╚══════════════════════════════════════════════════════════╝

📅 Period: {summary['period']}

📊 KEY METRICS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   New Signups:        {summary['total_signups']:>6}
   Total Logins:       {summary['total_logins']:>6}
   AI Questions:       {summary['total_ai_questions']:>6}
   Errors:             {summary['total_errors']:>6}
   Active Users Today: {summary['active_users_today']:>6}
   Avg Response Time:  {summary['avg_response_time']:>6.2f}s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 DAILY BREAKDOWN:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    # Add daily breakdown
    dates = sorted(summary['daily_breakdown']['signups'].keys(), reverse=True)
    for date in dates:
        signups = summary['daily_breakdown']['signups'].get(date, 0)
        logins = summary['daily_breakdown']['logins'].get(date, 0)
        questions = summary['daily_breakdown']['ai_questions'].get(date, 0)
        errors = summary['daily_breakdown']['errors'].get(date, 0)

        report += f"""
{date}:
   Signups: {signups:>3} | Logins: {logins:>4} | Questions: {questions:>4} | Errors: {errors:>3}
"""

    # Check for alerts
    alerts = check_performance_alerts()
    if alerts:
        report += "\n⚠️  ALERTS:\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        for alert in alerts:
            report += f"   {alert}\n"
    else:
        report += "\n✅ NO ALERTS - All systems normal\n"

    report += "\n" + "="*60 + "\n"

    return report


# -------------------------------------------------------
# INITIALIZE ON IMPORT
# -------------------------------------------------------
# Try to load existing metrics on startup
load_metrics_from_file()
