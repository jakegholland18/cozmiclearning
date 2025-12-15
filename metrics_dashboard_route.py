# ADD THIS TO YOUR app.py

"""
PERFORMANCE METRICS DASHBOARD ROUTE

Add this code to your app.py file to create a /metrics endpoint
that shows real-time performance data.

Access at: https://cozmiclearning-1.onrender.com/metrics
(Requires admin/owner login for security)
"""

from modules.performance_monitor import (
    get_metrics_summary,
    generate_weekly_report,
    check_performance_alerts,
    print_metrics_summary
)


# -------------------------------------------------------
# METRICS DASHBOARD ROUTE
# -------------------------------------------------------
@app.route('/metrics')
@login_required
def metrics_dashboard():
    """
    Performance metrics dashboard.
    Only accessible to admins/owners.
    """
    # Security: Only allow owners/admins
    if not hasattr(current_user, 'role') or current_user.role not in ['owner', 'admin']:
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('index'))

    # Get metrics summary
    summary_7day = get_metrics_summary(days=7)
    summary_30day = get_metrics_summary(days=30)
    alerts = check_performance_alerts()

    return render_template('metrics_dashboard.html',
                         summary_7day=summary_7day,
                         summary_30day=summary_30day,
                         alerts=alerts)


# -------------------------------------------------------
# METRICS API ENDPOINT (JSON)
# -------------------------------------------------------
@app.route('/api/metrics')
@login_required
def metrics_api():
    """
    Get metrics as JSON.
    For programmatic access or external monitoring.
    """
    # Security check
    if not hasattr(current_user, 'role') or current_user.role not in ['owner', 'admin']:
        return jsonify({'error': 'Access denied'}), 403

    days = request.args.get('days', 7, type=int)
    summary = get_metrics_summary(days=days)
    alerts = check_performance_alerts()

    return jsonify({
        'success': True,
        'metrics': summary,
        'alerts': alerts,
        'timestamp': datetime.utcnow().isoformat()
    })


# -------------------------------------------------------
# TRACK EVENTS IN YOUR EXISTING ROUTES
# -------------------------------------------------------

# Example 1: Track signups
# In your signup routes, add:

@app.route('/student/signup', methods=['POST'])
def student_signup():
    # ... your existing signup code ...

    # After successful signup:
    from modules.performance_monitor import track_event
    track_event('signup', user_type='student', user_id=new_student.id)

    # ... rest of your code ...


# Example 2: Track logins
# In your login routes, add:

@app.route('/student/login', methods=['POST'])
def student_login():
    # ... your existing login code ...

    # After successful login:
    from modules.performance_monitor import track_event
    track_event('login', user_type='student', user_id=student.id)

    # ... rest of your code ...


# Example 3: Track AI questions
# In your /ask route, add:

@app.route('/ask', methods=['POST'])
def ask_question():
    import time
    start_time = time.time()

    # ... your existing AI question code ...

    # After generating response:
    from modules.performance_monitor import track_event
    response_time = time.time() - start_time
    track_event('ai_question',
                subject=request.form.get('subject'),
                response_time=response_time,
                user_id=current_user.id)

    # ... rest of your code ...


# Example 4: Track errors
# In error handlers or try/except blocks:

@app.errorhandler(500)
def internal_error(error):
    from modules.performance_monitor import track_event
    track_event('error', error_type='500', route=request.path)

    # ... your existing error handling ...


# -------------------------------------------------------
# DAILY METRICS REPORT (SCHEDULED TASK)
# -------------------------------------------------------

def send_daily_metrics_email():
    """
    Send daily metrics report via email.
    Call this from a scheduled task (cron job, Render cron, etc.)
    """
    from modules.performance_monitor import generate_weekly_report
    from flask_mail import Message

    report = generate_weekly_report()

    msg = Message(
        subject='CozmicLearning Daily Metrics Report',
        recipients=[os.getenv('OWNER_EMAIL', 'your-email@example.com')],
        body=report
    )

    try:
        mail.send(msg)
        logger.info('Daily metrics report sent')
    except Exception as e:
        logger.error(f'Failed to send metrics report: {e}')


# To run daily, add to Render cron job or use APScheduler:
# (Optional - only if you want automated daily reports)

"""
Add to requirements.txt:
APScheduler==3.10.4

Add to app.py:
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_metrics_email, 'cron', hour=9, minute=0)
scheduler.start()
"""
