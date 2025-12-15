# 📊 Performance Monitoring Setup for CozmicLearning

**Goal**: Set up monitoring so you know exactly how your site is performing and when to scale

**What You'll Monitor**:
1. Server health (CPU, memory, response times)
2. User activity (signups, logins, active users)
3. Error rates (crashes, timeouts, failures)
4. AI usage (OpenAI API calls, costs)
5. Database performance (query times, connections)

**Time to Set Up**: 30 minutes
**Cost**: FREE (using free tiers)

---

## 🎯 MONITORING STACK

### **Layer 1: Render Built-in Metrics** (FREE, Built-in)
- Server CPU, memory, network
- Response times
- HTTP status codes
- **Takes**: 5 minutes to set up alerts

### **Layer 2: Application Logging** (FREE, Built-in)
- User signups/logins
- AI question tracking
- Error logging
- **Takes**: Already logging, 10 minutes to improve

### **Layer 3: Google Analytics** (FREE, Optional)
- User behavior
- Page views
- Conversion tracking
- **Takes**: 15 minutes to add

### **Layer 4: Sentry Error Tracking** (FREE tier, Optional)
- Automatic error reporting
- Stack traces
- User context
- **Takes**: 20 minutes to add

---

## 🚀 PART 1: RENDER METRICS & ALERTS (5 MINUTES)

### **Step 1: Access Render Metrics**

**Navigate**:
1. Go to: dashboard.render.com
2. Click on **"CozmicLearning"** service (from list)
3. Click **"Metrics"** tab (top navigation)

**You'll See**:
- **CPU Usage** graph (should be 5-20% normally)
- **Memory Usage** graph (should be 100-300 MB normally)
- **Response Time** graph (should be < 2 seconds)
- **Bandwidth** graph
- **HTTP Status Codes** (200s = good, 500s = errors)

---

### **Step 2: Set Up Alerts**

**Navigate**:
1. Same page → Click **"Notifications"** (or Settings → Notifications)
2. Click **"Add Notification"** or **"Create Alert"**

**Alert 1: High CPU Usage**
```
Alert Name: High CPU Usage
Condition: CPU usage > 80%
Duration: 5 minutes
Action: Send email to [your email]
```

**Alert 2: High Memory Usage**
```
Alert Name: High Memory Usage
Condition: Memory usage > 400 MB
Duration: 5 minutes
Action: Send email to [your email]
```

**Alert 3: Slow Response Times**
```
Alert Name: Slow Response Times
Condition: Average response time > 5 seconds
Duration: 10 minutes
Action: Send email to [your email]
```

**Alert 4: Error Rate**
```
Alert Name: High Error Rate
Condition: 5xx errors > 5% of requests
Duration: 5 minutes
Action: Send email to [your email]
```

Click **"Save"** for each alert.

---

### **Step 3: Check Daily** (1 minute/day)

**Daily Routine**:
1. Go to dashboard.render.com → CozmicLearning → Metrics
2. Quick glance at graphs:
   - ✅ CPU under 50%?
   - ✅ Memory under 400 MB?
   - ✅ Response time under 3 seconds?
   - ✅ No spike in errors?
3. If all green → you're good!
4. If any red → investigate

**Set a daily reminder**: Check at same time each day (e.g., 9 AM)

---

## 📝 PART 2: APPLICATION LOGGING IMPROVEMENTS (10 MINUTES)

You're already logging to Render, let's make it more useful.

### **Step 1: Add User Activity Logging**

**Create**: `/Users/tamara/Desktop/cozmiclearning/modules/monitoring.py`

**Purpose**: Track important user events

I'll create this file for you in the next step.

---

### **Step 2: View Logs in Real-Time**

**Access Logs**:
1. dashboard.render.com → CozmicLearning → **"Logs"** tab
2. See real-time log stream

**What to Look For**:

✅ **Good Logs**:
```
INFO:root:New student signup: student@email.com
INFO:root:AI question asked: "What is photosynthesis?"
INFO:root:Response generated in 3.2 seconds
```

❌ **Bad Logs**:
```
ERROR:root:Database connection failed
ERROR:root:OpenAI API timeout after 30s
CRITICAL:root:Out of memory error
```

**Set up daily log review**: Scroll through last 100 lines each morning

---

### **Step 3: Add Custom Metrics Dashboard**

I'll create a simple metrics tracker that logs to a file you can review.

---

## 📈 PART 3: GOOGLE ANALYTICS (15 MINUTES - OPTIONAL)

### **Why Add Google Analytics**:
- See how many people visit your site
- Track which pages are popular
- See where users come from (ads, social media, etc.)
- Free and powerful

### **Step 1: Create Google Analytics Account**

1. Go to: analytics.google.com
2. Click **"Start measuring"**
3. Enter:
   - Account name: "CozmicLearning"
   - Property name: "CozmicLearning Website"
   - Time zone: Your timezone
   - Currency: USD
4. Click **"Next"** → **"Create"**
5. Accept terms

---

### **Step 2: Get Tracking Code**

1. Choose **"Web"** platform
2. Enter website URL: `https://cozmiclearning-1.onrender.com` (or your custom domain)
3. Enter stream name: "CozmicLearning Main"
4. Click **"Create stream"**

**Copy the Measurement ID**: It looks like `G-XXXXXXXXXX`

---

### **Step 3: Add Google Analytics to Your Site**

I'll show you exactly where to add the tracking code in your templates.

**File to Edit**: You need to add it to your base template so it's on every page.

---

### **Step 4: Verify It's Working**

1. Google Analytics → Reports → Realtime
2. Open your website in browser
3. You should see **"1 active user"** in Google Analytics (you!)
4. If you see yourself → ✅ Working!

**Note**: Takes 24-48 hours for full data to appear

---

## 🚨 PART 4: SENTRY ERROR TRACKING (20 MINUTES - OPTIONAL)

### **Why Add Sentry**:
- Automatically catches Python errors
- Emails you when crashes happen
- Shows stack traces and user context
- Free for up to 5,000 errors/month

### **Step 1: Create Sentry Account**

1. Go to: sentry.io
2. Click **"Get Started"**
3. Sign up (free account)
4. Choose plan: **"Developer"** (FREE)

---

### **Step 2: Create Project**

1. Click **"Create Project"**
2. Choose platform: **"Flask"**
3. Enter project name: "CozmicLearning"
4. Click **"Create Project"**

**Copy the DSN**: Looks like `https://xxxxx@xxxxx.ingest.sentry.io/xxxxx`

---

### **Step 3: Install Sentry**

I'll help you add this to your application.

---

## 📊 PART 5: CUSTOM METRICS TRACKER

Let me create a simple metrics system for you that tracks key numbers.

---

