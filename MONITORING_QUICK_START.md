# 🚀 Performance Monitoring - Quick Start Guide

## ✅ WHAT I BUILT FOR YOU

I've created a complete performance monitoring system! Here's what you have:

### **Files Created**:

1. **`modules/performance_monitor.py`** - Core monitoring system
   - Tracks signups, logins, AI questions, errors
   - Calculates averages, generates reports
   - Auto-saves metrics

2. **`website/templates/metrics_dashboard.html`** - Visual dashboard
   - Charts and graphs
   - Real-time metrics
   - Alerts and warnings

3. **`metrics_dashboard_route.py`** - Code to add to app.py
   - Routes for `/metrics` page
   - API endpoint for JSON data
   - Examples of how to track events

---

## 🚀 STEP 1: RENDER ALERTS (DO THIS NOW - 5 MIN)

**Set up email alerts** so you know if something breaks:

1. Go to **dashboard.render.com**
2. Click your CozmicLearning service
3. Settings → Notifications
4. Create 4 alerts:
   - CPU > 80% for 5 min
   - Memory > 400 MB for 5 min
   - Response time > 5 sec for 10 min
   - Error rate > 5% for 5 min
5. Save

**Done!** Now you get emails if site has problems.

---

## 🚀 STEP 2: ADD MONITORING TO APP.PY (15 MIN)

### **Quick Integration** (Copy/Paste 3 Code Blocks)

Open your **`app.py`** file and add these:

### **A) Add Import at Top** (Line ~10-20)
```python
# Add this with your other imports
from modules.performance_monitor import track_event, get_metrics_summary, check_performance_alerts
```

### **B) Add Metrics Dashboard Route** (Add anywhere after your other routes)
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

### **C) Track Events in Existing Routes** (Add to your existing routes)

**In Student Signup** (find your `/student/signup` route, add after successful signup):
```python
# After new student is created and saved:
track_event('signup', user_type='student', user_id=new_student.id)
```

**In Teacher Signup** (find your `/teacher/signup` route):
```python
# After new teacher is created:
track_event('signup', user_type='teacher', user_id=new_teacher.id)
```

**In Student Login** (find your `/student/login` route):
```python
# After successful login:
track_event('login', user_type='student', user_id=student.id)
```

**In AI Question Route** (find your `/ask` route):
```python
import time

# At the START of the route:
start_time = time.time()

# ... your existing code that generates AI response ...

# AFTER AI response is generated:
response_time = time.time() - start_time
track_event('ai_question',
            subject=request.form.get('subject', 'unknown'),
            response_time=response_time,
            user_id=current_user.id)
```

**That's it!** Save `app.py`.

---

## 🚀 STEP 3: DEPLOY & TEST (5 MIN)

### **Commit and Deploy**:

```bash
cd /Users/tamara/Desktop/cozmiclearning

# Add new files
git add modules/performance_monitor.py
git add website/templates/metrics_dashboard.html
git add app.py

# Commit
git commit -m "Add performance monitoring system"

# Push to GitHub (triggers Render deploy)
git push origin main
```

### **Test It Works**:

1. Wait 2-3 minutes for Render to deploy

2. Go to your site and log in as admin/owner

3. Visit: **https://cozmiclearning-1.onrender.com/metrics**

4. You should see the metrics dashboard!

---

## 📊 HOW TO USE IT

### **Daily Check** (1 minute):

Every morning:
1. Go to: **your-site.com/metrics**
2. Quick glance:
   - ✅ Any alerts? (If yes → investigate)
   - ✅ Response time < 3 seconds? (Good!)
   - ✅ Active users count (Track growth!)
   - ✅ Any error spike? (If yes → check logs)

### **Weekly Review** (5 minutes):

Once a week:
1. Review 7-day trends
2. Note user growth
3. Check if approaching capacity (30+ concurrent users)
4. Plan upgrades if needed

### **Check Render Metrics** (2 minutes):

Once a week:
1. dashboard.render.com → Your Service → Metrics
2. Look at CPU graph (should be < 50%)
3. Look at Memory graph (should be < 400 MB)
4. If consistently high → time to upgrade

---

## 📈 WHAT YOU'LL SEE

### **Metrics Dashboard Shows**:

**Top Cards**:
- New Signups (last 7 days)
- Total Logins (last 7 days)
- AI Questions Asked (last 7 days)
- Active Users Today (concurrent)

**Performance**:
- Average Response Time (target: < 3 seconds)
- Error Count (target: < 10/week)
- Capacity Status (current load vs. max)

**Daily Breakdown Table**:
- Day-by-day numbers
- Spot trends (growing? declining?)
- Identify busy days

**Alerts**:
- ⚠️ High response times
- ⚠️ High error rate
- ⚠️ Approaching capacity
- ✅ All systems normal

---

## 🚨 INTERPRETING METRICS

### **Good Signs** ✅:
- Response time: 1-3 seconds
- Active users: 10-30
- Signups trending up
- Low error count (< 5/day)

### **Warning Signs** ⚠️:
- Response time: 3-5 seconds
- Active users: 30-50
- Errors: 10-20/day
- CPU consistently > 60%

**Action**: Monitor closely, optimize code

### **Critical Signs** 🚨:
- Response time: > 5 seconds
- Active users: > 50
- Errors: > 20/day
- CPU consistently > 80%

**Action**: Upgrade Render plan NOW

---

## 📧 EMAIL ALERTS

You'll receive email when:
- ⚠️ CPU > 80% for 5 minutes
- ⚠️ Memory > 400 MB
- ⚠️ Response time > 5 seconds
- ⚠️ Error rate > 5%

**When you get an alert**:
1. Check /metrics dashboard
2. Check Render logs
3. Identify issue
4. Fix or upgrade

---

## 💡 QUICK WINS

### **Optimization Tips**:

**If response times are slow**:
1. Check OpenAI API status (status.openai.com)
2. Consider caching common questions
3. Optimize database queries
4. Upgrade Render plan

**If errors are increasing**:
1. Check Render logs for specifics
2. Look for patterns (same error repeatedly?)
3. Fix code bugs
4. Add better error handling

**If approaching capacity**:
1. Check if it's temporary spike or trend
2. Consider upgrading plan
3. Add caching to reduce load
4. Optimize heavy routes

---

## 🎯 SUCCESS CHECKLIST

**Setup Complete When**:
- [ ] Render alerts configured (CPU, Memory, Response, Errors)
- [ ] `performance_monitor.py` in modules/ folder
- [ ] Monitoring code added to app.py (imports, route, track_event calls)
- [ ] `metrics_dashboard.html` in templates/ folder
- [ ] Code committed and pushed to GitHub
- [ ] Render deployed successfully
- [ ] Can access /metrics page as admin
- [ ] See metrics updating in real-time

**All checked?** ✅ **You're monitoring like a pro!**

---

## 🔄 DAILY ROUTINE

**Morning** (1 minute):
- Open /metrics
- Quick scan for alerts
- Note user count

**Issues?**
- Check Render logs
- Fix or scale

**No issues?**
- Carry on! 🚀

---

## 📞 NEED HELP?

**Common Questions**:

**Q: "Metrics showing 0 for everything?"**
A: No events tracked yet. Use the site (signup, login, ask questions) and check again.

**Q: "Can't access /metrics page?"**
A: Make sure you're logged in as owner/admin. Check user.role in database.

**Q: "/metrics page shows error?"**
A: Check Render logs. Make sure all code was added correctly.

**Q: "How often should I check?"**
A: Daily quick check (1 min). Weekly deep dive (5 min).

---

## ✅ YOU'RE ALL SET!

Your monitoring is now:
- ✅ Tracking user activity
- ✅ Monitoring performance
- ✅ Alerting on issues
- ✅ Showing visual dashboard
- ✅ Helping you scale smartly

**Focus on growing your user base** - the monitoring will tell you when to upgrade! 📈

---

## 🎯 NEXT STEPS

**Today**:
1. Set up Render alerts (5 min)
2. Add monitoring code to app.py (15 min)
3. Deploy and test /metrics page (5 min)

**This Week**:
1. Check /metrics daily
2. Get familiar with the dashboard
3. Track your first users!

**Going Forward**:
- Monitor trends
- Plan upgrades proactively
- Optimize based on data
- Scale with confidence!

**You're ready to launch and scale! 🚀**
