# CozmicLearning: Staging & Production Environment Guide

## Overview
This guide shows how to safely test changes before deploying to your live website.

**Two Environments:**
- **Staging** (test.cozmiclearning.com) - Test everything here first
- **Production** (cozmiclearning.com) - Your live site that users see

---

## Quick Answer: The Best Setup

### 1. Use Git Branches
```
main branch ────────► cozmiclearning.com (LIVE)
                      
staging branch ─────► test.cozmiclearning.com (TESTING)
```

### 2. Daily Workflow
```bash
# Make changes on staging
git checkout staging
git add -A
git commit -m "Add new feature"
git push origin staging
# → Auto-deploys to test.cozmiclearning.com
# → Test it thoroughly

# When ready to go live
git checkout main
git merge staging
git push origin main
# → Auto-deploys to cozmiclearning.com
```

---

## Detailed Setup Guide

### Step 1: Create Staging Branch

```bash
# Create staging branch from main
git checkout main
git pull origin main
git checkout -b staging
git push origin staging
```

### Step 2: Set Up Hosting (Choose One)

#### Option A: Render.com (Recommended - Easiest)

1. **Go to Render Dashboard** (render.com)

2. **Create Staging Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Name: `cozmiclearning-staging`
   - Branch: `staging`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance Type: Free (for testing) or Starter ($7/month)
   
3. **Create Production Service:**
   - Repeat above steps
   - Name: `cozmiclearning-production`
   - Branch: `main`
   - Instance Type: Starter ($7/month recommended for live site)

4. **Create Databases:**
   - New + → PostgreSQL
   - Create two databases:
     - `cozmiclearning-staging-db`
     - `cozmiclearning-production-db`

5. **Link Databases to Services:**
   - In each web service, go to Environment
   - Add: `DATABASE_URL` = [your database internal URL]

6. **Configure Auto-Deploy:**
   - Staging: Auto-deploy ✅ (deploys immediately on push)
   - Production: Auto-deploy with manual approval ✅ (you click "Deploy" button)

#### Option B: Railway (Alternative)

1. **Create Project**
   - Connect GitHub repo
   - Create two deployments from same repo
   - Point to different branches

2. **Similar configuration** to Render above

#### Option C: Heroku

```bash
# Create apps
heroku create cozmiclearning-staging
heroku create cozmiclearning-production

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini -a cozmiclearning-staging
heroku addons:create heroku-postgresql:mini -a cozmiclearning-production

# Set up git remotes
git remote add staging https://git.heroku.com/cozmiclearning-staging.git
git remote add production https://git.heroku.com/cozmiclearning-production.git

# Deploy
git push staging staging:main  # Deploys staging branch
git push production main:main  # Deploys main branch
```

### Step 3: Configure Environment Variables

**For EACH service, add these environment variables:**

#### Staging Environment Variables
```
FLASK_ENV=staging
DATABASE_URL=[automatically set by database]
STRIPE_SECRET_KEY=sk_test_...  ← Use TEST keys!
STRIPE_PUBLISHABLE_KEY=pk_test_...  ← Use TEST keys!
OPENAI_API_KEY=sk-...
SECRET_KEY=[random string]
FLASK_APP=app.py
```

#### Production Environment Variables
```
FLASK_ENV=production
DATABASE_URL=[automatically set by database]
STRIPE_SECRET_KEY=sk_live_...  ← Use LIVE keys!
STRIPE_PUBLISHABLE_KEY=pk_live_...  ← Use LIVE keys!
OPENAI_API_KEY=sk-...
SECRET_KEY=[different random string]
FLASK_APP=app.py
```

### Step 4: Set Up Custom Domains

#### In Your Domain Registrar (GoDaddy, Namecheap, etc.)

**DNS Records:**
```
Type   Name    Value
A      @       [Production Server IP]
A      www     [Production Server IP]
A      test    [Staging Server IP]
```

#### In Render/Railway Dashboard
- Production service: Add custom domain `cozmiclearning.com` and `www.cozmiclearning.com`
- Staging service: Add custom domain `test.cozmiclearning.com`

---

## Your Daily Workflow

### Making Changes Safely

#### 1. Work on Staging
```bash
# Start on staging branch
git checkout staging
git pull origin staging

# Make your changes to code
# Edit files, add features, fix bugs

# Commit and push
git add -A
git commit -m "Add new Study Buddy feature"
git push origin staging
```

**Result:** Changes automatically deploy to `test.cozmiclearning.com`

#### 2. Test Thoroughly on Staging

Visit `test.cozmiclearning.com` and test:
- ✅ New feature works
- ✅ No errors in browser console (F12)
- ✅ Works on mobile
- ✅ All user roles work (student, parent, teacher)
- ✅ Database changes work (if any)
- ✅ Payments work (use Stripe test cards)

**Stripe Test Cards for Staging:**
```
Success: 4242 4242 4242 4242
Decline: 4000 0000 0000 0002
```

#### 3. Deploy to Production (When Ready)

```bash
# Switch to main branch
git checkout main
git pull origin main

# Merge staging into main
git merge staging

# Push to production
git push origin main
```

**If using Render with manual approval:**
- Go to Render dashboard
- See "Deploy main" notification
- Click "Deploy" button
- Monitor deployment progress

**Result:** Changes go live on `cozmiclearning.com`

### If You Need to Rollback

**Something broke on production? Quick fix:**

```bash
# Method 1: Revert the last commit
git checkout main
git revert HEAD
git push origin main

# Method 2: Use hosting dashboard
# Render: Click "Rollback to previous deploy"
# Heroku: heroku rollback -a cozmiclearning-production
```

---

## Database Migrations

### ALWAYS Test on Staging First!

#### Example: Adding Conversation System

**On Staging:**
```bash
# SSH into staging server or use Render shell
python add_conversation_system.py
# Test thoroughly on test.cozmiclearning.com
```

**On Production (after staging success):**
```bash
# SSH into production server
python add_conversation_system.py
# Verify on cozmiclearning.com
```

### Creating Backups Before Migrations

**Render:**
- Database → Settings → Create Manual Backup

**Heroku:**
```bash
heroku pg:backups:capture -a cozmiclearning-production
```

---

## Understanding the Two Databases

### Why Separate Databases?

**Staging Database:**
- Safe to experiment
- Can be wiped/reset
- Test data only
- Test Stripe payments

**Production Database:**
- Real user data
- Must be protected
- Live Stripe payments
- Backed up daily

### Seeding Test Data on Staging

```python
# create_test_data.py
from app import app, db
from models import Student, Teacher, Parent

with app.app_context():
    # Create test student
    student = Student(
        name="Test Student",
        email="test@example.com",
        grade=5
    )
    db.session.add(student)
    db.session.commit()
```

Run on staging only:
```bash
python create_test_data.py
```

---

## Monitoring & Alerts

### Set Up Basic Monitoring

#### 1. Uptime Monitoring (Free)
**UptimeRobot.com:**
- Monitor: `https://cozmiclearning.com`
- Check every: 5 minutes
- Alert via: Email, SMS

#### 2. Error Tracking (Free Tier)
**Sentry.io:**
```python
# Add to app.py
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

if os.getenv('FLASK_ENV') == 'production':
    sentry_sdk.init(
        dsn="your-sentry-dsn",
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0
    )
```

#### 3. Daily Health Check

Create a simple endpoint:
```python
# In app.py
@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "environment": os.getenv("FLASK_ENV"),
        "timestamp": datetime.now().isoformat()
    })
```

---

## Security Checklist

### Before Going Live

- [ ] Use different Stripe keys (test vs live)
- [ ] Use different SECRET_KEY for each environment
- [ ] Enable HTTPS on custom domains
- [ ] Set up daily database backups
- [ ] Add Sentry error tracking
- [ ] Test password reset flow
- [ ] Test payment flows with test cards (staging)
- [ ] Verify parent notifications work
- [ ] Check content moderation is active
- [ ] Review user data privacy settings

---

## Cost Breakdown

### Starting Out (Free/Minimal)
```
Render Free Tier:
- Staging: $0 (sleeps after 15 min inactive)
- Production: $7/month (always on)
- Staging DB: $0 (free 90 days, then $7/month)
- Production DB: $7/month
- Domain: $12/year

Total: ~$15-22/month + $12/year
```

### Growing (Recommended)
```
Render Starter:
- Staging: $7/month
- Production: $7/month  
- Staging DB: $7/month
- Production DB: $7/month
- Domain: $12/year
- Sentry: $0 (free tier)

Total: ~$28/month + $12/year = ~$40/month
```

---

## Common Scenarios

### Scenario 1: Hot Fix Needed

**Problem:** Production has a bug, needs immediate fix

```bash
# Fix on staging first (even for hot fixes!)
git checkout staging
# Fix the bug
git commit -am "Fix critical payment bug"
git push origin staging
# Test on test.cozmiclearning.com

# Deploy to production
git checkout main
git merge staging
git push origin main
```

### Scenario 2: Feature Not Ready

**Problem:** Pushed to staging but feature isn't ready for production

```bash
# Just don't merge to main yet!
# Keep working on staging
# Production stays stable

# When ready:
git checkout main
git merge staging
git push origin main
```

### Scenario 3: Need to Test Migration

```bash
# On staging
python new_migration.py
# Test thoroughly

# If it breaks something:
# 1. Fix the migration script
# 2. Reset staging database
# 3. Test again

# When perfect:
# Run on production
```

---

## Quick Reference

### Common Commands

```bash
# Check current branch
git branch

# Switch to staging
git checkout staging

# Switch to production
git checkout main

# See what's different between branches
git diff main staging

# Merge staging into main
git checkout main
git merge staging

# Undo last commit (before pushing)
git reset --soft HEAD~1

# See deployment logs (Render)
# Use dashboard → Service → Logs

# Access database (Render)
# Dashboard → Database → Connect
```

### Service URLs

After setup, you'll have:
- **Staging:** `https://test.cozmiclearning.com`
- **Production:** `https://cozmiclearning.com`
- **Staging DB:** `postgresql://...` (from Render)
- **Production DB:** `postgresql://...` (from Render)

---

## Next Steps

1. **Create staging branch** (5 minutes)
2. **Set up Render services** (20 minutes)
3. **Configure domains** (10 minutes, may take 24h to propagate)
4. **Test the workflow** (30 minutes)
5. **Set up monitoring** (15 minutes)

**Total Setup Time:** ~2 hours

---

## Getting Help

**If deployment fails:**
1. Check Render logs (Dashboard → Service → Logs)
2. Verify environment variables are set
3. Check database is connected
4. Verify requirements.txt has all dependencies

**If database migration fails:**
1. Check PostgreSQL vs SQLite syntax differences
2. Verify column/table names match
3. Test migration on staging first!

**If domain not working:**
1. DNS changes take up to 24 hours
2. Verify DNS records in registrar
3. Check custom domain settings in Render
4. Ensure SSL certificate is active

---

## Summary

**The Safe Development Cycle:**

```
1. Code on staging branch
   ↓
2. Push to staging
   ↓
3. Auto-deploys to test.cozmiclearning.com
   ↓
4. Test everything thoroughly
   ↓
5. Merge to main
   ↓
6. Push to main
   ↓
7. Deploy to cozmiclearning.com
   ↓
8. Monitor for issues
```

**This gives you:**
- ✅ Safe testing environment
- ✅ Can't accidentally break production
- ✅ Easy rollback if needed
- ✅ Professional workflow
- ✅ Peace of mind!
