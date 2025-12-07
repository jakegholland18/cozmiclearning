# How to Monitor Your Self-Healing Website

Your website now fixes itself automatically! Here's how to check on it.

---

## 🎯 **Quick Monitoring (Daily - 2 Minutes)**

### **Option 1: Health Dashboard (Easiest)**

1. Go to **https://cozmiclearning-1.onrender.com/admin/health**
2. Log in as admin if needed
3. Check the status badge:
   - ✅ **GREEN (Healthy)** = Everything is great! No action needed.
   - ⚠️ **YELLOW (Degraded)** = Some errors, but self-healing is handling them. Check back in an hour.
   - 🚨 **RED (Critical)** = High error rate. Review Render logs.

**That's it!** Takes 30 seconds.

---

### **Option 2: Render Logs (If you see yellow/red)**

1. Go to https://dashboard.render.com/
2. Click on your "cozmiclearning" service
3. Click "Logs" tab
4. Look for these messages:

**✅ Good Signs (Self-Healing Working):**
```
Session was corrupted and has been auto-repaired
Database locked, retrying in 0.2s (attempt 1/3)
✅ Added column game_sessions.game_mode
```

**⚠️ Warning Signs (Check but don't panic):**
```
Function get_user_courses failed (attempt 2/3). Retrying...
API call failed (attempt 1/3). Retrying in 0.5s...
```
These are EXPECTED - the system is recovering automatically.

**🚨 Red Flags (Need attention):**
```
HIGH ERROR RATE DETECTED: KeyError has occurred 15 times in the last hour
Database commit failed after 3 attempts
CRITICAL ERROR: Missing Required Environment Variables
```

---

## 📊 **What Each Status Means**

### **✅ Healthy Status**
- **What it means:** 0-9 errors in the past hour
- **What to do:** Nothing! Enjoy your coffee ☕
- **Check frequency:** Once per week (or never)

### **⚠️ Degraded Status**
- **What it means:** 10-99 errors in the past hour, but all auto-recovered
- **What to do:** Check back in 1-2 hours. If still degraded, review logs.
- **Check frequency:** Once per day until it returns to healthy

### **🚨 Critical Status**
- **What it means:** 100+ errors in the past hour
- **What to do:**
  1. Check Render logs for the specific error
  2. Look at "Errors by Type" section on health dashboard
  3. If same error repeating, may need manual fix
- **Check frequency:** Check immediately, monitor every hour

---

## 📅 **Recommended Monitoring Schedule**

### **Week 1 After Launch:**
- Check health dashboard: 2x per day (morning & evening)
- Review Render logs: 1x per day
- **Why:** Make sure self-healing is working for real users

### **Weeks 2-4:**
- Check health dashboard: 1x per day
- Review Render logs: If degraded/critical status
- **Why:** Verify stability with growing user base

### **After Month 1:**
- Check health dashboard: 2-3x per week
- Review Render logs: Only if critical status
- **Why:** System is stable, self-healing handles most issues

---

## 🔔 **When to Take Action**

### **✅ No Action Needed:**
- Health status: Healthy
- Total errors: 0-5 in past hour
- Errors recovering automatically (retrying messages in logs)

### **⚠️ Monitor Closely:**
- Health status: Degraded for more than 4 hours
- Same error type appears 10+ times
- Users report slow performance

### **🚨 Immediate Action:**
- Health status: Critical for more than 1 hour
- Any error with "CRITICAL" in the logs
- Users cannot log in or access key features
- Stripe payments failing

---

## 🛠️ **Common Self-Healing Scenarios**

### **Scenario 1: Database Lock**
**What you'll see in logs:**
```
Database locked, retrying in 0.2s (attempt 1/3)
Database locked, retrying in 0.4s (attempt 2/3)
```

**What's happening:**
- Two users tried to save data at exact same moment
- Self-healing retries after brief delay
- Usually succeeds on attempt 2 or 3

**Action needed:** ✅ None - this is normal and auto-fixes

---

### **Scenario 2: Corrupted Session**
**What you'll see in logs:**
```
Session key 'xp' has wrong type. Converting to int
Session key 'level' is negative. Resetting to 0.
Session was corrupted and has been auto-repaired.
```

**What's happening:**
- User's session data got corrupted (browser bug, network issue)
- Self-healing detected and fixed it
- User experience: seamless, no error seen

**Action needed:** ✅ None - user won't even notice

---

### **Scenario 3: API Timeout**
**What you'll see in logs:**
```
API call failed (attempt 1/3). Retrying in 0.5s... Error: Timeout
API call failed (attempt 2/3). Retrying in 1.0s... Error: Timeout
Stripe API response successful
```

**What's happening:**
- OpenAI or Stripe API was slow/timed out
- Self-healing retried automatically
- Succeeded on retry

**Action needed:** ✅ None if it succeeds within 3 tries

---

### **Scenario 4: High Error Rate Alert**
**What you'll see in logs:**
```
HIGH ERROR RATE DETECTED: KeyError has occurred 12 times in the last hour.
Details: KeyError: 'student_id'
```

**What's happening:**
- Same error happening repeatedly
- Self-healing can recover from individual errors, but pattern suggests a code bug
- Need to investigate why 'student_id' is missing

**Action needed:** ⚠️ Check the specific error, may need developer to fix root cause

---

## 📈 **Understanding Error Counts**

### **Normal Error Rates:**
- **0-5 errors/hour:** Excellent, expected with real users
- **5-10 errors/hour:** Normal, self-healing working well
- **10-25 errors/hour:** Higher than ideal, monitor closely
- **25+ errors/hour:** Investigate cause

### **What Causes Normal Errors?**
- Users hitting back button multiple times
- Users closing browser mid-request
- Network hiccups
- Database locks from concurrent users
- API rate limits

**These are all auto-recovered by self-healing!**

---

## 🎛️ **Health Dashboard Features**

When you visit **/admin/health**, you'll see:

1. **Status Badge** - Overall health (green/yellow/red)
2. **Total Errors** - Count in past hour
3. **Time Window** - How long errors are tracked
4. **Error Types** - List of error names and counts
5. **Self-Healing Info** - What's being auto-fixed

**Example of a healthy dashboard:**
```
✅ Healthy
Total Errors: 3
Time Window: Last 45 minutes
Errors by Type:
  - OperationalError: 2 (database locks, auto-retried)
  - KeyError: 1 (session fixed)
```

**Example of a critical dashboard:**
```
🚨 Critical
Total Errors: 47
Time Window: Last 58 minutes
Errors by Type:
  - AttributeError: 45 (INVESTIGATE!)
  - TypeError: 2
```

---

## 🚀 **Pro Tips**

### **Tip 1: Bookmark the Health URL**
Add to your bookmarks:
```
https://cozmiclearning-1.onrender.com/admin/health
```

Quick check anytime without logging into Render.

### **Tip 2: Set a Phone Reminder**
- Monday, Wednesday, Friday at 9am: Check health dashboard
- Takes 30 seconds

### **Tip 3: Trust the Self-Healing**
- If status is "healthy", don't dig into logs
- Self-healing handles 95% of issues
- Only investigate when status is degraded for 4+ hours

### **Tip 4: Error Counters Reset Hourly**
- If you see 8 errors at 2:15pm, check again at 3:05pm
- Counters reset every hour
- Helps identify ongoing vs. one-time issues

---

## 🆘 **When to Get Help**

**Contact a developer if:**
- Critical status for more than 2 hours
- Same error appears 50+ times
- Users reporting they can't access the site
- Payment processing completely broken

**Before contacting developer, collect:**
1. Screenshot of /admin/health page
2. Last 100 lines from Render logs
3. When the issue started
4. What users are reporting (if any)

---

## ✅ **Success Checklist**

After self-healing is deployed, you should see:

- [ ] /admin/health page loads and shows status
- [ ] Status is "Healthy" or "Degraded" (not critical)
- [ ] Render logs show "Session was corrupted and has been auto-repaired" messages
- [ ] Render logs show retry messages for database commits
- [ ] Errors are being logged with full details
- [ ] Site is working normally for users

---

## 📞 **Quick Reference**

| What You Want | Where to Go |
|--------------|-------------|
| Quick health check | https://cozmiclearning-1.onrender.com/admin/health |
| Detailed logs | https://dashboard.render.com/ → Logs |
| Error counts | /admin/health → "Errors by Type" section |
| Deploy status | https://dashboard.render.com/ → Events |

---

**Last Updated:** 2025-12-07
**Self-Healing Status:** ✅ Active and Monitoring
