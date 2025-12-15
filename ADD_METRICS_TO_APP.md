# 📊 Add Custom Metrics to app.py - Simple Guide

Since Sentry is working, just add these 3 code snippets to your app.py.

---

## STEP 1: Add Import at Top (1 minute)

**Find this section** in app.py (around lines 1-20):
```python
import os
import sys
import logging
...
```

**Add this line** with the other imports:
```python
from modules.performance_monitor import track_event, get_metrics_summary, check_performance_alerts
```

---

## STEP 2: Add /metrics Route (2 minutes)

**Find the end of your routes** in app.py (around line 9000+ near the bottom, before `if __name__ == '__main__'`).

**Add this entire block**:
```python
# -------------------------------------------------------
# PERFORMANCE METRICS DASHBOARD
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


@app.route('/api/metrics')
@login_required
def metrics_api():
    """Get metrics as JSON for API access"""
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
```

---

## STEP 3: Add Event Tracking (12 minutes)

Now add tracking to your existing routes. **Search for these routes in app.py and add the tracking lines:**

### **A) Student Signup Tracking**

**Search for**: `@app.route('/student/signup'` (probably around line 3000-4000)

**Find the part** where you create the new student and save to database. It looks something like:
```python
new_student = Student(...)
db.session.add(new_student)
db.session.commit()
```

**Add this line** AFTER the commit:
```python
track_event('signup', user_type='student', user_id=new_student.id)
```

---

### **B) Teacher Signup Tracking**

**Search for**: `@app.route('/teacher/signup'`

**Find where** teacher is created and saved:
```python
new_teacher = Teacher(...)
db.session.add(new_teacher)
db.session.commit()
```

**Add this line** AFTER the commit:
```python
track_event('signup', user_type='teacher', user_id=new_teacher.id)
```

---

### **C) Parent Signup Tracking**

**Search for**: `@app.route('/parent/signup'`

**Find where** parent is created:
```python
new_parent = Parent(...)
db.session.add(new_parent)
db.session.commit()
```

**Add this line** AFTER the commit:
```python
track_event('signup', user_type='parent', user_id=new_parent.id)
```

---

### **D) Student Login Tracking**

**Search for**: `@app.route('/student/login'`

**Find where** student successfully logs in (probably after password check):
```python
if check_password_hash(student.password_hash, password):
    login_user(student)
    # ... success redirect ...
```

**Add this line** AFTER `login_user(student)`:
```python
track_event('login', user_type='student', user_id=student.id)
```

---

### **E) Teacher Login Tracking**

**Search for**: `@app.route('/teacher/login'`

**After** successful login:
```python
login_user(teacher)
track_event('login', user_type='teacher', user_id=teacher.id)
```

---

### **F) Parent Login Tracking**

**Search for**: `@app.route('/parent/login'`

**After** successful login:
```python
login_user(parent)
track_event('login', user_type='parent', user_id=parent.id)
```

---

### **G) AI Question Tracking**

**Search for**: `@app.route('/ask'` or wherever you handle AI questions

**At the VERY START** of the route function, add:
```python
import time
start_time = time.time()
```

**AFTER the AI generates a response** (before returning the response to user), add:
```python
response_time = time.time() - start_time
track_event('ai_question',
            subject=request.form.get('subject', 'unknown'),
            response_time=response_time,
            user_id=current_user.id if current_user.is_authenticated else None)
```

---

## STEP 4: Test Locally (Optional but Recommended)

**Before deploying**, test that it works:

```bash
cd /Users/tamara/Desktop/cozmiclearning
python3 main.py
```

Open browser to `http://localhost:5000`

Try:
1. Sign up as student
2. Log in
3. Ask an AI question

Check terminal output - you should see:
```
📊 METRIC: New student signup
📊 METRIC: User login (ID: 1)
📊 METRIC: AI question - num_forge (3.2s)
```

If you see these → **Working! ✅**

Press Ctrl+C to stop local server.

---

## STEP 5: Deploy to Render

```bash
cd /Users/tamara/Desktop/cozmiclearning

# Check what changed
git status

# Add all changes
git add app.py modules/performance_monitor.py website/templates/metrics_dashboard.html

# Commit
git commit -m "Add performance metrics dashboard and tracking"

# Push (triggers Render deployment)
git push origin main
```

Wait 2-3 minutes for Render to deploy.

---

## STEP 6: Test on Production

1. Go to your site: `https://cozmiclearning-1.onrender.com`

2. Log in as **owner/admin**

3. Visit: `https://cozmiclearning-1.onrender.com/metrics`

4. You should see the **metrics dashboard**! 🎉

**At first**, all numbers will be 0 or very low (no data yet).

**As users sign up and use the site**, you'll see:
- Signups count increase
- Logins tracked
- AI questions counted
- Response times calculated

---

## ✅ VERIFICATION CHECKLIST

After deploying, verify:

- [ ] Can access /metrics page (as owner/admin)
- [ ] Dashboard loads without errors
- [ ] Sign up a test student → Check /metrics → Signups count increases
- [ ] Log in as that student → Check /metrics → Logins count increases
- [ ] Ask an AI question → Check /metrics → AI questions count increases
- [ ] Check Render logs → See "📊 METRIC:" messages

**All checked?** ✅ **Monitoring is LIVE!**

---

## 🎯 WHAT YOU'LL SEE

### **First Day** (Just Deployed):
- All metrics at 0 or very low
- Dashboard shows "No data yet"
- **This is normal!**

### **After 1 Week of Users**:
```
📊 7-Day Summary:
- Signups: 15
- Logins: 45
- AI Questions: 120
- Active Users Today: 8
- Avg Response Time: 3.2s
```

### **After 1 Month**:
```
📊 30-Day Summary:
- Signups: 75
- Logins: 250
- AI Questions: 800
- Active Users Today: 25
- Trends showing growth! 📈
```

---

## 📧 EMAIL ALERTS YOU'LL GET

**From Sentry** (Already working ✅):
```
Subject: [CozmicLearning] New Error

Python error occurred
Click to see details
```

**From Render** (After Step 1 ⚠️):
```
Subject: [Render] High CPU Alert

CPU at 85% for 7 minutes
Check dashboard
```

**From /metrics** (Manual check):
- No emails (you check dashboard daily)
- Visual alerts on /metrics page if issues

---

## 🔄 YOUR NEW DAILY ROUTINE (2 minutes)

**Every morning at 9 AM**:

**1. Check Email** (30 sec):
- Any Sentry errors? → Fix today
- Any Render alerts? → Investigate

**2. Check /metrics Dashboard** (60 sec):
- Go to: your-site.com/metrics
- Quick scan:
  - Signups: Trending up? ✅
  - Active users: Under 30? ✅
  - Response time: Under 3 sec? ✅
  - Any red alerts? ⚠️

**3. Check Sentry Dashboard** (30 sec):
- Go to: sentry.io
- Any new issues? → Add to fix list

**Total**: 2 minutes
**Result**: Complete visibility into your platform!

---

## 🚨 TROUBLESHOOTING

**Problem**: "Can't access /metrics page - 404 error"
**Solution**:
- Make sure you added the route to app.py
- Make sure you deployed (git push)
- Check Render logs for errors

**Problem**: "/metrics shows but all zeros"
**Solution**:
- This is normal at first (no data yet)
- Use the site (signup, login, ask questions)
- Refresh /metrics → should see numbers update

**Problem**: "ImportError: cannot import track_event"
**Solution**:
- Make sure performance_monitor.py is in modules/ folder
- Make sure you added the import at top of app.py
- Check Render logs for specific error

**Problem**: "Access Denied when accessing /metrics"
**Solution**:
- You must be logged in as owner/admin
- Check your user role in database
- Regular students/teachers can't access (security feature)

---

## 💡 QUICK TIPS

**Tip 1**: Bookmark these 3 URLs:
- sentry.io (error tracking)
- dashboard.render.com (infrastructure)
- your-site.com/metrics (custom metrics)

**Tip 2**: Check /metrics daily at same time (builds habit)

**Tip 3**: Take screenshot of /metrics on launch day (track growth!)

**Tip 4**: When you get Render alert, check /metrics too (context!)

**Tip 5**: Export metrics weekly (use /api/metrics endpoint)

---

## ✅ YOU'RE DONE WHEN...

- [x] Import added to app.py
- [x] /metrics route added to app.py
- [x] Tracking added to signup routes (3x: student, teacher, parent)
- [x] Tracking added to login routes (3x: student, teacher, parent)
- [x] Tracking added to AI question route
- [x] Code committed and pushed to GitHub
- [x] Render deployed successfully (check logs)
- [x] Can access /metrics page as admin
- [x] Test signup/login shows in metrics
- [x] Render alerts configured (from Step 1)

**All done?** 🎉 **You have professional monitoring!**

---

## 🎯 NEXT: FOCUS ON GROWTH

Your monitoring is complete. Now:

✅ Stop worrying about infrastructure
✅ Monitoring tells you when to scale
✅ Focus 100% on getting users
✅ Check metrics 2 min/day
✅ Let the system handle the rest

**Launch with confidence!** 🚀

Need help adding the code? Just ask and I'll walk you through it step by step!
