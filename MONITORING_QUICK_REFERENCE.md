# 📋 Self-Healing Monitoring - Quick Reference Card

**Print this or save as phone wallpaper!**

---

## ✅ **Daily Check (30 seconds)**

1. Visit: **https://cozmiclearning-1.onrender.com/admin/health**
2. Look at status badge:
   - **GREEN** = ✅ All good, go enjoy your day!
   - **YELLOW** = ⚠️ Check back in 2 hours
   - **RED** = 🚨 Check Render logs now

**That's it!**

---

## 🎯 **When to Check**

| Frequency | Status | What to Do |
|-----------|--------|-----------|
| **Weekly** | Healthy | Quick glance at dashboard |
| **Daily** | Degraded | Check dashboard, review if still degraded next day |
| **Hourly** | Critical | Check logs, may need action |

---

## 🚦 **Status Meanings**

### ✅ GREEN (Healthy)
- **Errors:** 0-9 per hour
- **Action:** None needed
- **Normal?** Yes!

### ⚠️ YELLOW (Degraded)
- **Errors:** 10-99 per hour (all auto-recovered)
- **Action:** Monitor, check back in 2-4 hours
- **Normal?** Occasional spikes are OK

### 🚨 RED (Critical)
- **Errors:** 100+ per hour
- **Action:** Check Render logs, investigate
- **Normal?** No - needs attention

---

## 🔗 **Important Links**

| What | URL |
|------|-----|
| **Health Dashboard** | https://cozmiclearning-1.onrender.com/admin/health |
| **Render Logs** | https://dashboard.render.com/ → Your Service → Logs |
| **Render Dashboard** | https://dashboard.render.com/ |

---

## 📱 **Set Phone Reminder**

**Weekly Check:**
- Monday 9:00 AM: "Check CozmicLearning health dashboard"
- Duration: 1 minute

---

## ✨ **What Self-Healing Fixes Automatically**

- ✅ Corrupted session data
- ✅ Database locks
- ✅ API timeouts
- ✅ Missing session keys
- ✅ Negative/invalid values
- ✅ Network hiccups

**You don't need to do anything - it auto-fixes!**

---

## 🆘 **When to Get Developer Help**

- ❌ Critical status for 2+ hours
- ❌ Same error 50+ times
- ❌ Users can't log in
- ❌ Payments broken

---

## 💡 **Pro Tip**

**Trust the system!** If status is GREEN, don't worry about individual errors in logs. The self-healing system recovers from 95% of issues automatically.

---

**Last Updated:** 2025-12-07
