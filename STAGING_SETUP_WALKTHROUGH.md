# Staging Environment Setup - Step-by-Step Walkthrough

## What You'll Have When Done

- **test.cozmiclearning.com** - Your testing site (safe to break!)
- **cozmiclearning.com** - Your live site (protected)
- Separate databases for each
- Automatic deployments from Git branches

**Time needed:** 30-45 minutes

---

## Step 1: Create Staging Branch (5 minutes)

Open Terminal and navigate to your project:

```bash
cd /Users/tamara/Desktop/cozmiclearning

# Make sure you're on main and it's up to date
git checkout main
git pull origin main

# Create staging branch
git checkout -b staging

# Push it to GitHub
git push origin staging
```

**✅ Checkpoint:** You should now see "staging" branch on GitHub

---

## Step 2: Sign Up for Render.com (5 minutes)

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (easiest option)
4. Authorize Render to access your GitHub

**Why Render?**
- Free tier available
- Auto-deploys from GitHub
- PostgreSQL included
- Easy to use
- No credit card needed for free tier

---

## Step 3: Create Staging Web Service (10 minutes)

### 3.1: Create New Web Service

1. Click "New +" button → "Web Service"
2. Connect your `jakegholland18/cozmiclearning` repository
3. Click "Connect" next to it

### 3.2: Configure Staging Service

**Basic Settings:**
```
Name: cozmiclearning-staging
Region: Oregon (US West) or closest to you
Branch: staging  ⬅️ Important! Select "staging" not "main"
Root Directory: [leave blank]
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

**Instance Type:**
```
Free (for testing)
OR
Starter - $7/month (recommended - doesn't sleep)
```

### 3.3: Add Environment Variables

Click "Advanced" → "Add Environment Variable"

Add these one by one:

```
FLASK_ENV = staging

SECRET_KEY = [generate a random string - keep this secret!]

OPENAI_API_KEY = [your OpenAI key - same as production]

STRIPE_SECRET_KEY = sk_test_... [your TEST Stripe key]

STRIPE_PUBLISHABLE_KEY = pk_test_... [your TEST Stripe key]

FLASK_APP = app.py

SKIP_STRIPE_CHECK = 1
```

**How to generate SECRET_KEY:**
```python
# In Python terminal:
import secrets
print(secrets.token_hex(32))
# Copy the output
```

### 3.4: Create the Service

- Click "Create Web Service"
- Wait 5-10 minutes for deployment
- Watch the logs scroll by

**✅ Checkpoint:** You should see "Your service is live 🎉"

---

## Step 4: Create Staging Database (5 minutes)

### 4.1: Create PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Configure:

```
Name: cozmiclearning-staging-db
Database: cozmiclearning_staging
User: cozmiclearning_staging
Region: Same as your web service
PostgreSQL Version: 16
```

**Instance Type:**
```
Free (90 days free, then $7/month)
OR
Starter - $7/month (recommended for longer projects)
```

3. Click "Create Database"
4. Wait ~2 minutes for it to spin up

### 4.2: Link Database to Web Service

1. Go to your web service (cozmiclearning-staging)
2. Click "Environment" in left sidebar
3. Click "Add Environment Variable"
4. Add:

```
DATABASE_URL = [Click "Insert from Database" → select your staging DB → Internal Database URL]
```

5. Click "Save Changes"

**Your service will automatically redeploy!**

---

## Step 5: Run Database Migrations (10 minutes)

### Option A: Using Render Shell (Easiest)

1. Go to your web service
2. Click "Shell" in top right
3. Wait for terminal to connect
4. Run migrations:

```bash
# Check which migrations you need to run
ls *.py | grep -E "(add_|create_|migrate_)"

# Run them in order
python add_moderation_fields.py
python add_conversation_system.py

# Verify tables exist
python -c "from app import app, db; app.app_context().push(); print([table for table in db.metadata.tables])"
```

### Option B: Using Local Connection

1. Get database URL from Render dashboard
2. In your local terminal:

```bash
# Set DATABASE_URL temporarily
export DATABASE_URL="postgresql://[from-render-dashboard]"

# Run migrations
python add_moderation_fields.py
python add_conversation_system.py
```

**✅ Checkpoint:** Migrations should complete without errors

---

## Step 6: Create Production Web Service (10 minutes)

**Repeat Step 3, but:**

```
Name: cozmiclearning-production
Branch: main  ⬅️ Important! Use "main" this time
Instance Type: Starter - $7/month (recommended for live site)
```

**Environment Variables:**
```
FLASK_ENV = production  ⬅️ Different!

SECRET_KEY = [DIFFERENT random string than staging!]

OPENAI_API_KEY = [same as staging]

STRIPE_SECRET_KEY = sk_live_... [LIVE Stripe key]

STRIPE_PUBLISHABLE_KEY = pk_live_... [LIVE Stripe key]

FLASK_APP = app.py
```

**Important:**
- Use LIVE Stripe keys for production!
- Use DIFFERENT SECRET_KEY than staging!

---

## Step 7: Create Production Database (5 minutes)

Same as Step 4, but:

```
Name: cozmiclearning-production-db
Database: cozmiclearning_production
User: cozmiclearning_production
```

Link it to production web service, then run migrations.

---

## Step 8: Set Up Custom Domains (10 minutes)

### 8.1: Configure Staging Domain

1. Go to staging web service
2. Click "Settings" → "Custom Domains"
3. Click "Add Custom Domain"
4. Enter: `test.cozmiclearning.com`
5. Render will show you DNS records to add

### 8.2: Configure Production Domain

1. Go to production web service
2. Click "Settings" → "Custom Domains"
3. Add both:
   - `cozmiclearning.com`
   - `www.cozmiclearning.com`

### 8.3: Update DNS Records

Go to your domain registrar (GoDaddy, Namecheap, etc.)

**Add these DNS records:**

For **test.cozmiclearning.com** (staging):
```
Type: CNAME
Name: test
Value: [the hostname Render provides, e.g., cozmiclearning-staging.onrender.com]
TTL: Automatic
```

For **cozmiclearning.com** (production):
```
Type: CNAME
Name: www
Value: [the hostname Render provides]

Type: A
Name: @
Value: [the IP address Render provides]
```

**Note:** DNS changes can take up to 24 hours to propagate, but usually work within an hour.

---

## Step 9: Configure Auto-Deploy Settings

### For Staging (Auto-deploy immediately)

1. Go to staging web service
2. Settings → "Build & Deploy"
3. Auto-Deploy: **Yes** ✅
4. Branch: `staging`

**Result:** Every push to `staging` branch auto-deploys!

### For Production (Manual approval)

1. Go to production web service
2. Settings → "Build & Deploy"
3. Auto-Deploy: **Yes** ✅
4. ⚠️ But you'll manually click "Deploy" in dashboard for safety

**Result:** Push to `main` triggers build, but YOU click deploy button!

---

## Step 10: Test Your Setup (10 minutes)

### Test Staging

1. Make a small change:

```bash
git checkout staging
echo "# Test staging" >> README.md
git add README.md
git commit -m "Test staging deployment"
git push origin staging
```

2. Watch Render dashboard
3. Should auto-deploy in ~3 minutes
4. Visit `https://test.cozmiclearning.com` (or the Render URL if DNS not ready)

### Test Production

1. Merge to production:

```bash
git checkout main
git merge staging
git push origin main
```

2. Go to Render dashboard → production service
3. You'll see "Deploy main" notification
4. Click "Deploy" button
5. Watch deployment
6. Visit `https://cozmiclearning.com`

**✅ Success!** Both environments are live!

---

## Your New Workflow

### Making Changes

```bash
# 1. Work on staging
git checkout staging
# Make your changes

# 2. Commit and push
git add -A
git commit -m "Add new feature"
git push origin staging

# 3. Auto-deploys to test.cozmiclearning.com
# Wait 3-5 minutes

# 4. Test thoroughly on test.cozmiclearning.com
# - Click around
# - Test as student, parent, teacher
# - Check browser console for errors (F12)

# 5. If good, deploy to production
git checkout main
git merge staging
git push origin main

# 6. Go to Render dashboard
# Click "Deploy" on production service

# 7. Verify on cozmiclearning.com
```

---

## Troubleshooting

### Service won't start

**Check Render logs:**
1. Go to service
2. Click "Logs" tab
3. Look for error messages

**Common issues:**
- Missing environment variable
- Database not connected
- Wrong Python version
- Missing dependency in requirements.txt

**Fix:**
1. Add missing environment variable
2. Link database properly
3. Check `requirements.txt` is complete

### Database connection failed

**Check:**
1. Is DATABASE_URL set correctly?
2. Is database running? (Check database dashboard)
3. Did you select "Internal Database URL"?

**Fix:**
1. Go to Environment variables
2. Delete DATABASE_URL
3. Re-add using "Insert from Database"

### DNS not working

**Check:**
1. Did you add the CNAME/A records?
2. Waited at least 1 hour?
3. Using correct hostname from Render?

**Temporary fix:**
- Use the `.onrender.com` URL while DNS propagates

### Migration failed

**Check:**
1. Is database PostgreSQL (not SQLite)?
2. Does migration script have PostgreSQL syntax?
3. Do tables already exist?

**Fix:**
1. Use Render shell
2. Drop and recreate tables if needed
3. Re-run migration

---

## Quick Reference

### URLs After Setup

```
Staging Site: https://test.cozmiclearning.com
Production Site: https://cozmiclearning.com

Render Dashboard: https://dashboard.render.com
GitHub Repo: https://github.com/jakegholland18/cozmiclearning
```

### Important Commands

```bash
# Switch to staging
git checkout staging

# Switch to production
git checkout main

# Deploy staging (auto)
git push origin staging

# Deploy production (manual approval in Render)
git push origin main

# See current branch
git branch

# Run migrations on Render
# Go to service → Shell → run python migration.py
```

### Cost Summary

**Free Tier (Testing):**
- Staging web service: $0 (sleeps after 15 min)
- Staging database: $0 (free 90 days)
- Production web service: $7/month
- Production database: $7/month
- **Total: $14/month**

**Recommended Setup:**
- Staging web service: $7/month (no sleeping)
- Staging database: $7/month
- Production web service: $7/month
- Production database: $7/month
- **Total: $28/month**

---

## Next Steps

After setup is complete:

1. ✅ Read through `ERROR_PREVENTION_STRATEGY.md`
2. ✅ Set up Sentry error tracking
3. ✅ Set up UptimeRobot monitoring
4. ✅ Create test student accounts on staging
5. ✅ Test all critical flows on staging
6. ✅ Create database backup plan

---

## Getting Help

**If you get stuck:**

1. Check Render documentation: https://render.com/docs
2. Check your service logs in Render dashboard
3. Google the specific error message
4. Check GitHub Issues for render.com

**Common documentation:**
- https://render.com/docs/deploy-flask
- https://render.com/docs/databases
- https://render.com/docs/custom-domains

---

## Checklist

Use this to track your progress:

- [ ] Created staging branch
- [ ] Signed up for Render.com
- [ ] Created staging web service
- [ ] Added environment variables to staging
- [ ] Created staging database
- [ ] Linked database to staging service
- [ ] Ran migrations on staging database
- [ ] Created production web service
- [ ] Added environment variables to production
- [ ] Created production database
- [ ] Linked database to production service
- [ ] Ran migrations on production database
- [ ] Set up test.cozmiclearning.com domain
- [ ] Set up cozmiclearning.com domain
- [ ] Tested staging deployment
- [ ] Tested production deployment
- [ ] Verified both sites work

**When all checked:** You're ready to deploy safely! 🎉
