# Self-Healing System Setup Guide

This guide shows you how to make CozmicLearning automatically fix itself without manual intervention.

---

## 🔄 **What "Self-Healing" Means**

Instead of crashing when errors occur, the app will:
- ✅ Automatically retry failed operations
- ✅ Fix corrupted session data
- ✅ Recover from database errors
- ✅ Handle API timeouts gracefully
- ✅ Log errors without crashing
- ✅ Monitor its own health

---

## 📦 **Already Implemented Self-Healing Features**

### **1. Safe Session Access** ✅
```python
# Won't crash if key is missing
xp = session.get("xp", 0)  # Returns 0 if not found
```

### **2. Database Auto-Migration** ✅
```python
# Automatically adds missing columns on startup
rebuild_database_if_needed()
```

### **3. Environment Variable Validation** ✅
```python
# Stops app if critical keys are missing (prevents silent failures)
# Auto-generates SECRET_KEY if not provided
```

---

## 🚀 **New Self-Healing Features to Add**

I've created `modules/self_healing.py` with powerful recovery tools. Here's how to integrate them:

### **Step 1: Update app.py Imports**

Add at the top of app.py (after existing imports):

```python
# Self-healing imports
from modules.self_healing import (
    auto_retry,
    safe_execute,
    ensure_session_defaults,
    fix_corrupted_session,
    safe_db_commit,
    resilient_api_call,
    health_monitor,
    log_unhandled_exception
)
```

### **Step 2: Enable Automatic Error Logging**

Add after `app = Flask(...)` in app.py:

```python
# Automatically log all unhandled exceptions
got_request_exception.connect(log_unhandled_exception, app)
```

### **Step 3: Replace Manual Commit with Self-Healing Commit**

Find all instances of:
```python
db.session.commit()
```

Replace with:
```python
safe_db_commit(db.session)
```

**Why?** Automatically retries on database lock, rolls back on error, prevents data corruption.

### **Step 4: Add Session Self-Healing to Routes**

For any route that uses session data, add at the beginning:

```python
@app.route('/dashboard')
def dashboard():
    # Auto-heal session if corrupted
    ensure_session_defaults(session)
    fix_corrupted_session(session)

    # Now safe to use session variables
    xp = session["xp"]  # Guaranteed to exist
    ...
```

### **Step 5: Make API Calls Resilient**

Replace direct OpenAI calls:

**Before:**
```python
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": question}]
)
```

**After:**
```python
response = resilient_api_call(
    openai.ChatCompletion.create,
    model="gpt-4",
    messages=[{"role": "user", "content": question}],
    max_retries=3
)
```

**Benefits:**
- Automatically retries on timeout
- Handles rate limits (waits and retries)
- Recovers from temporary network failures

### **Step 6: Add Health Monitoring Dashboard (Admin Only)**

Add a new route to monitor app health:

```python
@app.route("/admin/health")
def admin_health():
    if not is_admin():
        abort(403)

    health_status = health_monitor.get_error_summary()

    return render_template("admin/health.html",
                         status=health_status['status'],
                         total_errors=health_status['total_errors'],
                         errors_by_type=health_status['errors_by_type'],
                         time_window=health_status['time_window'])
```

---

## 🎯 **Quick Integration (Copy-Paste Ready)**

### **Add to app.py right after `app = Flask(...)`:**

```python
# ============================================================
# SELF-HEALING SETUP
# ============================================================

from modules.self_healing import (
    ensure_session_defaults,
    fix_corrupted_session,
    safe_db_commit,
    resilient_api_call,
    health_monitor,
    log_unhandled_exception
)

# Enable automatic error logging
got_request_exception.connect(log_unhandled_exception, app)

# Before every request, ensure session is healthy
@app.before_request
def heal_session():
    """Auto-heal session data before every request"""
    ensure_session_defaults(session)
    fix_corrupted_session(session)
```

That's it! Now every route automatically gets:
- ✅ Healed session data
- ✅ Logged errors
- ✅ Health monitoring

---

## 📊 **Usage Examples**

### **Example 1: Self-Healing Database Commits**

```python
@app.route("/save-progress", methods=["POST"])
def save_progress():
    student = Student.query.get(session["student_id"])
    student.xp += 10

    # Old way (crashes on error):
    # db.session.commit()

    # New way (auto-retries, rolls back on failure):
    if safe_db_commit(db.session):
        flash("Progress saved!", "success")
    else:
        flash("Failed to save progress. Please try again.", "error")

    return redirect("/dashboard")
```

### **Example 2: Self-Healing API Calls**

```python
@app.route("/ask-question", methods=["POST"])
def ask_question():
    question = request.form.get("question")

    try:
        # Automatically retries on timeout, rate limit, network error
        response = resilient_api_call(
            openai.ChatCompletion.create,
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            max_retries=3
        )

        answer = response.choices[0].message.content
        return jsonify({"answer": answer})

    except Exception as e:
        # Even if all retries fail, app doesn't crash
        logging.error(f"OpenAI call failed: {e}")
        return jsonify({"error": "AI is temporarily unavailable. Please try again."}), 503
```

### **Example 3: Decorator for Auto-Retry**

```python
from modules.self_healing import auto_retry

@auto_retry(max_attempts=3)
def send_email_notification(user_email, subject, body):
    """Automatically retries if email fails to send"""
    msg = EmailMessage(subject, body, to=[user_email])
    mail.send(msg)

# Usage:
try:
    send_email_notification(
        user_email="student@example.com",
        subject="Welcome!",
        body="Thanks for signing up!"
    )
except Exception as e:
    # Only fails if all 3 attempts fail
    logging.error(f"Failed to send email after retries: {e}")
```

---

## 🏥 **Health Monitoring**

### **Check App Health Anytime**

```python
status = health_monitor.get_error_summary()

print(status)
# Output:
# {
#     'status': 'healthy',  # or 'degraded' or 'critical'
#     'total_errors': 3,
#     'errors_by_type': {
#         'KeyError': 1,
#         'OperationalError': 2
#     },
#     'time_window': 'Last 15 minutes'
# }
```

### **Automatic Alerts**

The health monitor automatically logs CRITICAL alerts when:
- Same error occurs more than 10 times in 1 hour
- Indicates a systemic problem that needs attention

---

## 🔧 **Advanced: Custom Error Recovery**

Create your own self-healing functions:

```python
from modules.self_healing import safe_execute

@safe_execute(default_return=[], log_errors=True)
def get_user_courses(user_id):
    """
    Gets user courses. If query fails, returns empty list instead of crashing.
    """
    return Course.query.filter_by(user_id=user_id).all()

# Usage:
courses = get_user_courses(session["student_id"])
# Never crashes, always returns a list (empty if error)
```

---

## ✅ **Benefits of Self-Healing System**

| Problem | Without Self-Healing | With Self-Healing |
|---------|---------------------|-------------------|
| Database lock | App crashes | Auto-retries 3 times |
| API timeout | 500 error page | Retries, then shows friendly message |
| Missing session key | KeyError crash | Auto-creates with default value |
| Corrupted session | Weird behavior | Auto-detects and fixes |
| Network hiccup | Request fails | Retries with backoff |
| High error rate | Silent until you check logs | Auto-alerts when threshold exceeded |

---

## 🎯 **Recommended Implementation Order**

**Week 1: Critical Auto-Healing**
1. ✅ Add `@app.before_request` session healing
2. ✅ Replace all `db.session.commit()` with `safe_db_commit()`
3. ✅ Enable automatic error logging

**Week 2: API Resilience**
4. ✅ Wrap OpenAI calls with `resilient_api_call()`
5. ✅ Wrap Stripe calls with `resilient_api_call()`
6. ✅ Add email retry decorator

**Week 3: Monitoring**
7. ✅ Add admin health dashboard
8. ✅ Set up alerts for critical errors
9. ✅ Monitor for 1 week

---

## 📈 **Expected Results**

**Before Self-Healing:**
- 5-10 crashes per day
- Users see error pages
- Manual intervention required

**After Self-Healing:**
- 0-1 crashes per day
- 95% of errors auto-recover
- Users rarely see errors
- You sleep better! 😴

---

## 🚨 **What Self-Healing CANNOT Fix**

Self-healing is powerful but has limits:

❌ **Cannot fix:**
- Missing API keys (app won't start)
- Completely wrong code logic
- Permanent database corruption
- Running out of server memory
- Stripe account suspension

✅ **CAN fix:**
- Temporary database locks
- Network timeouts
- Rate limit errors
- Corrupted session data
- Missing session keys
- Temporary API outages

---

## 📝 **Maintenance**

**Monthly:**
- Review health monitor logs
- Check for recurring error patterns
- Optimize retry counts if needed

**Quarterly:**
- Review and update error handling
- Add new self-healing for new features

---

**Last Updated:** 2025-12-07
**Status:** Ready to implement
**Estimated Implementation Time:** 2-3 hours
