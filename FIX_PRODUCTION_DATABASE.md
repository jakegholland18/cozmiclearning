# 🚨 Fix Production Database - Stripe Columns Missing

## Problem
Your site is showing "Houston, We Have a Problem!" (500 error) on all pages because the database is missing Stripe columns.

**Error:**
```
sqlalchemy.exc.OperationalError: no such column: students.stripe_customer_id
sqlalchemy.exc.OperationalError: no such column: teachers.stripe_customer_id
```

---

## ✅ Solution: Run Database Migration on Render

### Step 1: Open Render Shell

1. Go to https://dashboard.render.com
2. Click on your **cozmiclearning** web service
3. Click the **Shell** tab (top navigation)
4. Wait for the shell to connect

### Step 2: Run Migration Script

In the Render shell, copy and paste this command:

```bash
python add_stripe_columns_to_students.py
```

### Step 3: Verify Success

You should see output like this:

```
============================================================
  Stripe Columns Migration for All User Tables
============================================================

📋 Checking students table...
   📝 Adding column: stripe_customer_id (VARCHAR(255))
   ✅ Added stripe_customer_id
   📝 Adding column: stripe_subscription_id (VARCHAR(255))
   ✅ Added stripe_subscription_id

📋 Checking teachers table...
   📝 Adding column: stripe_customer_id (VARCHAR(255))
   ✅ Added stripe_customer_id
   📝 Adding column: stripe_subscription_id (VARCHAR(255))
   ✅ Added stripe_subscription_id

📋 Checking parents table...
   📝 Adding column: stripe_customer_id (VARCHAR(255))
   ✅ Added stripe_customer_id
   📝 Adding column: stripe_subscription_id (VARCHAR(255))
   ✅ Added stripe_subscription_id

============================================================
✅ Migration completed successfully!
============================================================
   Added 6 total column(s) across all tables
   Tables updated: students, teachers, parents
============================================================

✅ You can now run your app without the database error!
```

### Step 4: Restart Your Service (if needed)

Usually not needed, but if the site still shows errors:

1. In Render dashboard, go to **Manual Deploy**
2. Click **Clear build cache & deploy**

---

## 🎉 Your Site Should Work Now!

After running the migration:
- ✅ Login pages will work
- ✅ Admin panel will work
- ✅ All user dashboards will work
- ✅ No more 500 errors

---

## 📝 What This Migration Does

The script adds these columns to your database:

**To `students` table:**
- `stripe_customer_id` (VARCHAR 255)
- `stripe_subscription_id` (VARCHAR 255)

**To `teachers` table:**
- `stripe_customer_id` (VARCHAR 255)
- `stripe_subscription_id` (VARCHAR 255)

**To `parents` table:**
- `stripe_customer_id` (VARCHAR 255)
- `stripe_subscription_id` (VARCHAR 255)

These columns are needed for Stripe payment integration but were missing from your production database.

---

## ❓ Troubleshooting

### If the migration script doesn't exist:
The script should be there since it was just deployed, but if you get "file not found":

```bash
ls -la add_stripe_columns_to_students.py
```

If it's missing, the deployment might not have completed. Check the deployment logs.

### If you get "Database not found":
```bash
ls -la instance/cozmic.db
```

The database should exist in the `instance/` folder.

### If columns already exist:
The script will detect this and skip those columns:
```
✅ Stripe columns already exist in students table
```

This is safe - it means the migration was already run.

---

## 🚀 That's It!

Once the migration runs successfully, refresh your site and everything should work perfectly!
