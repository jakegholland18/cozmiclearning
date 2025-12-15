# 📊 Complete Monitoring System - With Sentry Integration

**You Already Have**: ✅ Sentry error tracking (configured in app.py)

**I Just Added**:
- Custom metrics tracking (signups, logins, AI usage)
- Visual dashboard at /metrics
- Render alert setup guide

**This Guide**: How to use ALL your monitoring tools together

---

## 🎯 YOUR 3-LAYER MONITORING STACK

### **Layer 1: Sentry** (Already Set Up ✅)
**What It Does**: Catches Python errors automatically
- Database errors
- API failures
- Code crashes
- Performance issues

**Where to Check**: sentry.io dashboard

**Status**: ✅ Already configured in your app.py (lines 77-100)

---

### **Layer 2: Render Metrics** (Setup in 5 min)
**What It Does**: Server health monitoring
- CPU usage
- Memory usage
- Response times
- Network bandwidth

**Where to Check**: dashboard.render.com → Your Service → Metrics

**Status**: ⚠️ Need to add alerts (see below)

---

### **Layer 3: Custom Metrics** (Setup in 15 min)
**What It Does**: Business/user activity tracking
- User signups
- Login activity
- AI questions asked
- Feature usage

**Where to Check**: your-site.com/metrics (dashboard I built)

**Status**: ⚠️ Need to add code to app.py (see below)

---

## 🚀 QUICK SETUP (20 MINUTES)

### **STEP 1: Verify Sentry is Working** (2 min)

**Check Current Status**:

1. Go to **sentry.io**
2. Log in
3. Click your **CozmicLearning** project
4. Look for recent errors

**If you see errors**: ✅ Sentry is working!
**If no errors**: That's good! It means no crashes.

**Test Sentry** (optional):
Add this temporary route to app.py to trigger a test error:
```python
@app.route('/test-sentry')
def test_sentry():
    # This will send a test error to Sentry
    raise Exception("Test error from CozmicLearning - Sentry is working!")
```

Visit `/test-sentry` → Check Sentry → Should see the error appear within seconds.

---

### **STEP 2: Set Up Render Alerts** (5 min)

1. Go to **dashboard.render.com**
2. Click your **CozmicLearning** service
3. Click **"Settings"** tab
4. Scroll to **"Notifications"** or create alerts

**Create 4 Alerts**:

```
Alert 1: High CPU
- Metric: CPU
- Condition: > 80%
- Duration: 5 minutes
- Action: Email [your email]

Alert 2: High Memory
- Metric: Memory
- Condition: > 400 MB
- Duration: 5 minutes
- Action: Email [your email]

Alert 3: Slow Response
- Metric: HTTP Response Time
- Condition: > 5000 ms (5 seconds)
- Duration: 10 minutes
- Action: Email [your email]

Alert 4: High Error Rate
- Metric: HTTP 5xx Errors
- Condition: > 5% of requests
- Duration: 5 minutes
- Action: Email [your email]
```

Click **"Save"** on each.

✅ **Done! You'll now get emails for infrastructure issues.**

---

### **STEP 3: Add Custom Metrics to app.py** (15 min)

The monitoring code I created tracks user activity. Here's how to add it:

**A) Add Import** (at top of app.py, around line 10-20):
```python
# Add with your other imports
from modules.performance_monitor import track_event, get_metrics_summary, check_performance_alerts
```

**B) Add /metrics Route** (add after your other routes, around line 9000+):
```python
# -------------------------------------------------------
# PERFORMANCE METRICS DASHBOARD
# -------------------------------------------------------
@app.route('/metrics')
@login_required
def metrics_dashboard():
    """Performance metrics dashboard (Admin only)"""
    # Security: Only allow owners/admins
    if not hasattr(current_user, 'role') or current_user.role not in ['owner', 'admin']:
        flash('Access denied. Admin only.', 'error')
        return redirect(url_for('index'))

    # Get metrics
    summary_7day = get_metrics_summary(days=7)
    summary_30day = get_metrics_summary(days=30)
    alerts = check_performance_alerts()

    return render_template('metrics_dashboard.html',
                         summary_7day=summary_7day,
                         summary_30day=summary_30day,
                         alerts=alerts)
```

**C) Track Events in Your Routes**:

Find these routes in app.py and add tracking:

**Student Signup** (search for `@app.route('/student/signup')`):
```python
# After new student is created and saved to database:
track_event('signup', user_type='student', user_id=new_student.id)
```

**Teacher Signup** (search for `@app.route('/teacher/signup')`):
```python
# After new teacher is created:
track_event('signup', user_type='teacher', user_id=new_teacher.id)
```

**Student Login** (search for `@app.route('/student/login')`):
```python
# After successful login:
track_event('login', user_type='student', user_id=student.id)
```

**AI Question Route** (search for `@app.route('/ask')`):
```python
import time

# At START of route:
start_time = time.time()

# ... your existing code ...

# AFTER AI response generated:
response_time = time.time() - start_time
track_event('ai_question',
            subject=request.form.get('subject', 'unknown'),
            response_time=response_time,
            user_id=current_user.id)
```

**D) Deploy**:
```bash
git add app.py modules/performance_monitor.py website/templates/metrics_dashboard.html
git commit -m "Add custom metrics tracking"
git push origin main
```

Wait 2-3 minutes, then visit: **your-site.com/metrics**

---

## 📊 COMPREHENSIVE MONITORING WORKFLOW

### **Your Daily Routine** (2 minutes total):

**Morning Check** (9 AM daily):

**Step 1**: Check Sentry (30 seconds)
- Go to sentry.io
- Look for new errors (red notifications)
- If none: ✅ Good!
- If errors: Click to see details, fix urgent ones

**Step 2**: Check /metrics Dashboard (30 seconds)
- Go to your-site.com/metrics
- Quick glance:
  - Any alerts? (red warnings)
  - Active users count (note the number)
  - Response time (should be < 3 seconds)
  - Signups trending up or down?

**Step 3**: Check Render Metrics (30 seconds)
- dashboard.render.com → Your Service → Metrics
- CPU graph: Should be wavy, mostly < 50%
- Memory graph: Should be stable around 200-300 MB
- Response time: Should be mostly under 2 seconds

**Step 4**: Check Email (30 seconds)
- Any alerts from Render?
- Any Sentry error notifications?
- If yes → investigate
- If no → you're good!

**Total Time**: 2 minutes
**Frequency**: Daily (same time each day)

---

## 🚨 WHEN THINGS GO WRONG

### **Error Detection Flow**:

```
User experiences problem
    ↓
Error happens in code
    ↓
Sentry captures error automatically
    ↓
You get email: "New error in CozmicLearning"
    ↓
You click email → Go to Sentry
    ↓
See stack trace, user info, context
    ↓
Fix the bug
    ↓
Deploy fix
    ↓
Monitor to confirm it's fixed
```

### **Performance Issue Detection**:

```
Site getting slow
    ↓
Render detects: Response time > 5 seconds
    ↓
You get email: "High response time alert"
    ↓
You check /metrics dashboard
    ↓
See: 60 concurrent users (approaching capacity)
    ↓
Decision: Upgrade to Standard plan ($25/mo)
    ↓
Render → Settings → Change plan
    ↓
Performance improves instantly
```

---

## 📧 EMAIL ALERTS YOU'LL RECEIVE

### **From Sentry** (Errors):
```
Subject: [CozmicLearning] New Issue: AttributeError

Body:
- Error type and message
- Stack trace (what code failed)
- User context (which user experienced it)
- URL where it happened
- Link to full details in Sentry

Action: Click link, review error, fix code
```

### **From Render** (Infrastructure):
```
Subject: [Render] High CPU Alert - CozmicLearning

Body:
- CPU usage: 85% (threshold: 80%)
- Duration: 7 minutes
- Link to metrics

Action: Check if temporary spike or sustained issue
```

### **No Email** (Good!):
```
= Everything working normally
= Keep doing what you're doing
= Check /metrics once a day for trends
```

---

## 🎯 MONITORING INTEGRATION MATRIX

| **What to Monitor** | **Tool** | **Where to Check** | **Alert Method** |
|---------------------|----------|-------------------|------------------|
| Python errors | Sentry | sentry.io | Email |
| Database crashes | Sentry | sentry.io | Email |
| API failures | Sentry | sentry.io | Email |
| CPU usage | Render | dashboard.render.com | Email |
| Memory usage | Render | dashboard.render.com | Email |
| Response time | Render | dashboard.render.com | Email |
| User signups | Custom | your-site.com/metrics | Manual check |
| Login activity | Custom | your-site.com/metrics | Manual check |
| AI usage | Custom | your-site.com/metrics | Manual check |
| Capacity status | Custom | your-site.com/metrics | Visual warning |

---

## 🔍 INTERPRETING SENTRY ERRORS

### **Common Sentry Errors & What They Mean**:

**1. Database Errors**:
```
Error: OperationalError: database is locked
Cause: SQLite concurrent access issue
Fix: Upgrade to PostgreSQL (already on your roadmap)
Urgency: Medium (if happens frequently)
```

**2. OpenAI API Errors**:
```
Error: APIError: Rate limit exceeded
Cause: Too many AI requests too fast
Fix: Add rate limiting or caching
Urgency: High (users can't get help)
```

**3. Stripe Errors**:
```
Error: InvalidRequestError: No such customer
Cause: Trying to charge deleted customer
Fix: Add customer existence check
Urgency: High (payment failing)
```

**4. AttributeError / KeyError**:
```
Error: AttributeError: 'NoneType' object has no attribute 'name'
Cause: Code assumes data exists when it doesn't
Fix: Add null checks
Urgency: Medium
```

**5. Template Errors**:
```
Error: TemplateNotFound: student_dashboard.html
Cause: Template file missing or wrong path
Fix: Check template path, create missing file
Urgency: High (page won't load)
```

---

## 📊 SENTRY + CUSTOM METRICS INTEGRATION

### **How They Work Together**:

**Sentry tells you WHAT broke**:
- "Database connection failed at 2:15 PM"
- "User ID 123 got an error"
- Shows you the code line that failed

**Custom Metrics tell you WHY it matters**:
- "50 users were active when it broke"
- "This was during peak usage time"
- "10 signups failed because of this error"

**Example Integration**:

**Scenario**: Students can't submit AI questions

**Sentry shows**:
```
Error: OpenAI API timeout
Route: /ask
Time: 2:37 PM
Affected users: 15
```

**Custom Metrics shows**:
```
Active users at 2:37 PM: 45 (high)
AI questions attempted: 23
AI questions failed: 15
Response time: 12 seconds (very slow)
```

**Conclusion**: Too many concurrent AI requests → need to:
- Add request queuing
- OR upgrade server
- OR add caching
- OR increase OpenAI rate limits

---

## 🎯 WEEKLY REVIEW PROCESS (10 minutes)

**Every Monday Morning**:

**1. Review Sentry Dashboard** (3 min):
- Go to sentry.io → Issues
- Sort by "Last Seen"
- Check for:
  - Recurring errors (fix these!)
  - New errors (investigate)
  - High-volume errors (priority fix)
- Mark resolved errors as resolved

**2. Review Custom Metrics** (3 min):
- Go to /metrics
- Look at 7-day trends:
  - Are signups growing? ✅
  - Are logins increasing? ✅
  - Is engagement steady? ✅
  - Any unusual spikes? ⚠️

**3. Review Render Performance** (2 min):
- dashboard.render.com → Metrics
- Look at 7-day graphs:
  - CPU trending up? (may need upgrade)
  - Memory stable or growing? (watch for leaks)
  - Response times consistent? (good!)

**4. Plan Actions** (2 min):
- Any errors to fix this week?
- Approaching capacity? (plan upgrade)
- Any optimizations needed?
- Set goals for next week

---

## ✅ MONITORING SETUP CHECKLIST

**Sentry** (Already Done ✅):
- [x] Sentry SDK installed
- [x] DSN configured in environment
- [x] Flask integration enabled
- [x] Performance monitoring enabled (10% sampling)
- [x] PII filtering enabled
- [ ] Verify receiving error emails (test with /test-sentry route)

**Render Alerts** (5 min):
- [ ] High CPU alert created (> 80%)
- [ ] High Memory alert created (> 400 MB)
- [ ] Slow Response alert created (> 5 sec)
- [ ] High Error Rate alert created (> 5%)
- [ ] Test email received

**Custom Metrics** (15 min):
- [ ] performance_monitor.py imported in app.py
- [ ] /metrics route added
- [ ] Signup tracking added (teacher, student, parent)
- [ ] Login tracking added
- [ ] AI question tracking added
- [ ] Code deployed to Render
- [ ] Can access /metrics dashboard
- [ ] Seeing real data populate

---

## 🚀 OPTIMIZATION PRIORITIES

Based on your monitoring data, fix in this order:

**Priority 1: Errors** (Sentry)
- Any error affecting > 10 users
- Any error causing payment failures
- Any error preventing signup/login
- **Action**: Fix immediately

**Priority 2: Performance** (Render + Custom)
- Response times > 5 seconds
- CPU consistently > 80%
- Approaching capacity (40+ concurrent users)
- **Action**: Optimize or upgrade within 1 week

**Priority 3: User Experience** (Custom Metrics)
- Declining signup trends
- Low engagement
- Feature not being used
- **Action**: Investigate and improve

**Priority 4: Optimization** (All sources)
- Recurring but non-critical errors
- Slow but not broken features
- Memory usage growing slowly
- **Action**: Plan for future sprint

---

## 💰 COST BREAKDOWN

**Your Monitoring Stack Costs**:

| Tool | Cost | Value |
|------|------|-------|
| **Sentry** | $0-26/mo | ✅ Auto-catches all errors |
| **Render Metrics** | FREE (included) | ✅ Server health monitoring |
| **Custom Metrics** | FREE (code you own) | ✅ Business insights |
| **Your Time** | 2 min/day | ✅ Stay informed |
| **Total** | $0-26/mo | ✅ Complete visibility |

**Sentry Pricing**:
- **Developer (FREE)**: 5,000 errors/month
- **Team ($26/mo)**: 50,000 errors/month + extras
- **Start with FREE** → upgrade if you exceed limits

---

## 🎯 SUCCESS METRICS

**Your monitoring is working when**:

✅ You find out about errors BEFORE users complain
✅ You can predict when to upgrade (before site slows down)
✅ You know which features are popular (data-driven decisions)
✅ You catch and fix bugs in < 1 day
✅ You spend < 5 min/day on monitoring
✅ Uptime stays above 99.5%
✅ User complaints about performance drop to near-zero

---

## 📞 QUICK REFERENCE

**Daily Check** (2 min):
1. Sentry.io → Any new errors?
2. /metrics → Active users trending?
3. Render dashboard → CPU/Memory okay?
4. Email → Any alerts?

**Weekly Review** (10 min):
1. Sentry issues → Fix recurring errors
2. /metrics 7-day view → Growth trends
3. Render 7-day graphs → Performance trends
4. Plan optimizations

**When Alert Received**:
1. Check severity (critical? or minor?)
2. View details in relevant tool
3. Assess impact (how many users affected?)
4. Fix immediately or schedule
5. Monitor to confirm resolution

---

## ✅ YOU'RE ALL SET!

Your monitoring is now:
- ✅ **Comprehensive** - Covers errors, performance, and business metrics
- ✅ **Automated** - Alerts come to you, no constant checking
- ✅ **Actionable** - Clear data to drive decisions
- ✅ **Efficient** - Only 2 min/day required

**Next Steps**:
1. Set up Render alerts (5 min)
2. Add custom metrics code (15 min)
3. Deploy and test
4. Start your daily 2-min routine
5. Focus on growing your user base! 🚀

**The monitoring will tell you when to scale.** You can confidently launch knowing you'll see issues before they become problems!

Want help with:
1. Adding the metrics code to app.py right now?
2. Setting up Sentry performance monitoring better?
3. Creating automated weekly reports?
4. Building custom Sentry alerts for specific errors?

Just ask! 📊
