# Complete Stripe Integration Guide

## Current Status

Your Stripe integration is **partially functional**:
- ✅ Checkout sessions work
- ✅ Webhook endpoint exists
- ✅ Payment processing works
- ❌ Customer tracking not implemented (missing `stripe_customer_id`)
- ❌ Subscription cancellation doesn't sync with Stripe
- ❌ Webhook handlers incomplete (can't find users by customer_id)

**To fully functionalize Stripe, you need to:**
1. Add `stripe_customer_id` and `stripe_subscription_id` to database
2. Store these IDs when subscriptions are created
3. Update cancel subscription routes to cancel in Stripe
4. Complete webhook handlers to find users by customer_id

---

## What You Need to Do

### Step 1: Add Database Migration

Add two new fields to your models to track Stripe customers:

**File: `models.py`**

Find the `Parent`, `Student`, and `Teacher` models and add:

```python
# In Parent model (around line 38):
stripe_customer_id = db.Column(db.String(255), nullable=True)
stripe_subscription_id = db.Column(db.String(255), nullable=True)

# In Teacher model (around line 70):
stripe_customer_id = db.Column(db.String(255), nullable=True)
stripe_subscription_id = db.Column(db.String(255), nullable=True)

# In Student model (around line 110):
stripe_customer_id = db.Column(db.String(255), nullable=True)
stripe_subscription_id = db.Column(db.String(255), nullable=True)
```

### Step 2: Create Migration Script

**File: `add_stripe_ids.py`** (new file in project root)

```python
"""
Add stripe_customer_id and stripe_subscription_id to all user models
Run this ONCE after deploying the model changes
"""

import sqlite3
import os

def get_db_path():
    """Find the database file"""
    possible_paths = [
        'instance/cozmiclearning.db',
        'persistent_db/cozmiclearning.db',
        '/opt/render/project/src/instance/cozmiclearning.db',
        '/opt/render/project/src/persistent_db/cozmiclearning.db',
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    if 'DB_PATH' in os.environ:
        return os.environ['DB_PATH']

    return None

def add_stripe_columns():
    """Add stripe_customer_id and stripe_subscription_id columns"""
    db_path = get_db_path()

    if not db_path:
        print("❌ Database not found")
        return False

    print(f"📁 Database: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        tables = ['parents', 'teachers', 'students']

        for table in tables:
            print(f"\n📋 Migrating {table} table...")

            # Check if columns already exist
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [col[1] for col in cursor.fetchall()]

            if 'stripe_customer_id' not in columns:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN stripe_customer_id VARCHAR(255)")
                print(f"  ✅ Added stripe_customer_id to {table}")
            else:
                print(f"  ⏭️  stripe_customer_id already exists in {table}")

            if 'stripe_subscription_id' not in columns:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN stripe_subscription_id VARCHAR(255)")
                print(f"  ✅ Added stripe_subscription_id to {table}")
            else:
                print(f"  ⏭️  stripe_subscription_id already exists in {table}")

        conn.commit()
        print("\n✅ Migration complete!")
        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        conn.rollback()
        return False

    finally:
        conn.close()

if __name__ == "__main__":
    add_stripe_columns()
```

### Step 3: Update Stripe Checkout to Save Customer/Subscription IDs

**File: `app.py`**

Find the `handle_checkout_completed` function (around line 2845) and update it:

```python
def handle_checkout_completed(session_obj):
    """Activate subscription when checkout is completed."""
    try:
        metadata = session_obj.get('metadata', {})
        role = metadata.get('role')
        user_id = metadata.get('user_id')

        # Get Stripe customer and subscription IDs
        customer_id = session_obj.get('customer')
        subscription_id = session_obj.get('subscription')

        if role == "student":
            user = Student.query.get(user_id)
        elif role == "parent":
            user = Parent.query.get(user_id)
        elif role == "teacher":
            user = Teacher.query.get(user_id)
        else:
            logging.error(f"Unknown role in webhook: {role}")
            return

        if user:
            user.subscription_active = True
            user.trial_end = None
            user.stripe_customer_id = customer_id  # NEW
            user.stripe_subscription_id = subscription_id  # NEW

            success, error = safe_commit()  # Use safe commit
            if success:
                logging.info(f"Activated subscription for {role} {user_id}")
            else:
                logging.error(f"Failed to save subscription: {error}")
    except Exception as e:
        logging.error(f"Error in handle_checkout_completed: {e}")
```

### Step 4: Update Cancel Subscription Routes to Cancel in Stripe

**File: `app.py`**

Find the cancel subscription routes (around line 2917) and update them:

```python
@app.route("/student/cancel-subscription", methods=["GET", "POST"])
def student_cancel_subscription():
    """Cancel student subscription"""
    if "student_id" not in session:
        return redirect("/student/login")

    student_id = session["student_id"]
    student = Student.query.get(student_id)

    if not student:
        flash("Student not found.", "error")
        return redirect("/student/dashboard")

    if request.method == "POST":
        reason = request.form.get("reason", "No reason provided")
        feedback = request.form.get("feedback", "")

        app.logger.info(f"Student {student_id} canceled subscription. Reason: {reason}")

        # Cancel in Stripe if subscription ID exists
        if student.stripe_subscription_id:
            try:
                stripe.Subscription.delete(student.stripe_subscription_id)
                app.logger.info(f"Canceled Stripe subscription: {student.stripe_subscription_id}")
            except Exception as e:
                app.logger.error(f"Failed to cancel Stripe subscription: {e}")
                flash("Error canceling subscription in Stripe. Please contact support.", "error")
                return redirect("/student/cancel-subscription")

        # Deactivate subscription locally
        student.subscription_active = False
        student.plan = "free"
        student.stripe_subscription_id = None  # Clear subscription ID

        success, error = safe_commit()

        if success:
            flash("Your subscription has been canceled. You now have a free account.", "info")
            return redirect("/student/dashboard")
        else:
            flash("Error canceling subscription. Please contact support.", "error")
            return redirect("/student/cancel-subscription")

    return render_template("cancel_subscription.html",
                         user_type="student",
                         user=student)
```

**Repeat for parent, teacher, and homeschool routes** with the same Stripe cancellation logic.

### Step 5: Complete Webhook Handlers

**File: `app.py`**

Update the webhook handlers to find users by customer_id:

```python
def handle_subscription_canceled(subscription):
    """Deactivate user account when subscription is canceled."""
    try:
        customer_id = subscription.get('customer')

        # Find user by Stripe customer ID
        user = (Student.query.filter_by(stripe_customer_id=customer_id).first() or
                Parent.query.filter_by(stripe_customer_id=customer_id).first() or
                Teacher.query.filter_by(stripe_customer_id=customer_id).first())

        if user:
            user.subscription_active = False
            user.plan = "free"
            user.stripe_subscription_id = None

            success, error = safe_commit()
            if success:
                logging.info(f"Deactivated subscription for customer {customer_id}")
            else:
                logging.error(f"Failed to deactivate subscription: {error}")
        else:
            logging.warning(f"No user found for customer {customer_id}")

    except Exception as e:
        logging.error(f"Error in handle_subscription_canceled: {e}")


def handle_subscription_updated(subscription):
    """Handle subscription updates (plan changes, renewals)."""
    try:
        customer_id = subscription.get('customer')
        status = subscription.get('status')

        # Find user by Stripe customer ID
        user = (Student.query.filter_by(stripe_customer_id=customer_id).first() or
                Parent.query.filter_by(stripe_customer_id=customer_id).first() or
                Teacher.query.filter_by(stripe_customer_id=customer_id).first())

        if user:
            # Update subscription status
            if status == 'active':
                user.subscription_active = True
            elif status in ['canceled', 'unpaid', 'incomplete_expired']:
                user.subscription_active = False

            success, error = safe_commit()
            if success:
                logging.info(f"Updated subscription for customer {customer_id}: {status}")
            else:
                logging.error(f"Failed to update subscription: {error}")
        else:
            logging.warning(f"No user found for customer {customer_id}")

    except Exception as e:
        logging.error(f"Error in handle_subscription_updated: {e}")


def handle_payment_failed(invoice):
    """Handle failed payment (send email, grace period, etc)."""
    try:
        customer_id = invoice.get('customer')
        amount_due = invoice.get('amount_due') / 100  # Convert cents to dollars

        # Find user by Stripe customer ID
        user = (Student.query.filter_by(stripe_customer_id=customer_id).first() or
                Parent.query.filter_by(stripe_customer_id=customer_id).first() or
                Teacher.query.filter_by(stripe_customer_id=customer_id).first())

        if user:
            logging.warning(f"Payment failed for {user.email}: ${amount_due}")
            # TODO: Send email notification
            # TODO: Set grace period before deactivating
        else:
            logging.warning(f"Payment failed for unknown customer {customer_id}")

    except Exception as e:
        logging.error(f"Error in handle_payment_failed: {e}")
```

---

## Implementation Checklist

### Phase 1: Database Setup (Local)
- [ ] Add `stripe_customer_id` and `stripe_subscription_id` to models.py
- [ ] Create `add_stripe_ids.py` migration script
- [ ] Run migration locally: `python3 add_stripe_ids.py`
- [ ] Verify columns exist in database

### Phase 2: Code Updates (Local)
- [ ] Update `handle_checkout_completed` to save Stripe IDs
- [ ] Update all 4 cancel subscription routes to cancel in Stripe
- [ ] Update `handle_subscription_canceled` to find users by customer_id
- [ ] Update `handle_subscription_updated` to find users by customer_id
- [ ] Update `handle_payment_failed` to find users by customer_id
- [ ] Test locally with Stripe test mode

### Phase 3: Production Deployment
- [ ] Commit and push all changes
- [ ] Wait for Render auto-deploy
- [ ] Run migration on production: Add to render.yaml buildCommand OR use admin endpoint
- [ ] Test with Stripe test mode in production

### Phase 4: Stripe Dashboard Setup
- [ ] Configure webhook endpoint in Stripe
- [ ] Add webhook URL: `https://cozmiclearning-1.onrender.com/stripe-webhook`
- [ ] Enable events: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`
- [ ] Copy webhook signing secret to Render env vars

### Phase 5: Testing
- [ ] Test new subscription creation (verify IDs saved)
- [ ] Test subscription cancellation (verify canceled in Stripe)
- [ ] Test webhook: Cancel in Stripe dashboard (verify user deactivated)
- [ ] Test webhook: Update subscription status (verify user updated)

---

## Quick Start (Copy-Paste Implementation)

### 1. Add to models.py (in each user model):

```python
stripe_customer_id = db.Column(db.String(255), nullable=True)
stripe_subscription_id = db.Column(db.String(255), nullable=True)
```

### 2. Create add_stripe_ids.py:

Use the script provided above.

### 3. Run locally:

```bash
python3 add_stripe_ids.py
```

### 4. Add to render.yaml buildCommand:

```yaml
buildCommand: |
  pip install --upgrade pip
  pip install -r requirements.txt
  python3 fix_production_db.py
  python3 init_arcade_enhancements.py
  python3 add_stripe_ids.py  # NEW
```

### 5. Update app.py:

Replace the 3 webhook handlers with the updated versions above.

Update all 4 cancel subscription routes to include Stripe cancellation.

### 6. Setup Stripe Webhook:

1. Go to Stripe Dashboard → Developers → Webhooks
2. Click "Add endpoint"
3. Endpoint URL: `https://cozmiclearning-1.onrender.com/stripe-webhook`
4. Select events:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_failed`
5. Copy "Signing secret" (starts with `whsec_...`)
6. Add to Render environment: `STRIPE_WEBHOOK_SECRET`

---

## Benefits of Full Integration

### Before (Current):
- ❌ Canceling in app doesn't cancel in Stripe
- ❌ Customer still charged after canceling
- ❌ Webhooks can't find users (missing customer_id)
- ❌ Subscription updates in Stripe don't sync to app
- ❌ Can't track which Stripe customer owns which account

### After (Full Integration):
- ✅ Canceling in app cancels in Stripe automatically
- ✅ No more charges after cancellation
- ✅ Webhooks work perfectly (can find users)
- ✅ Stripe subscription changes sync to app instantly
- ✅ Full customer tracking for support/analytics
- ✅ Handles payment failures gracefully
- ✅ Professional, reliable subscription management

---

## Testing with Stripe Test Mode

### Test Card Numbers:

**Success:**
- `4242 4242 4242 4242` - Visa (success)
- Any future expiry (e.g., 12/34)
- Any 3-digit CVC (e.g., 123)
- Any ZIP code

**Decline:**
- `4000 0000 0000 0002` - Card declined
- `4000 0000 0000 9995` - Insufficient funds

### Test Webhooks:

1. Use Stripe CLI: `stripe listen --forward-to localhost:5000/stripe-webhook`
2. Or use Stripe Dashboard → Webhooks → "Send test webhook"

---

## Important Notes

1. **Always test in Test Mode first** - Don't use live keys until fully tested
2. **Webhook secret is required** - Stripe webhook verification will fail without it
3. **Customer ID is unique** - Each user gets one Stripe customer ID
4. **Subscription ID changes** - When user cancels/resubscribes, new subscription ID
5. **Don't delete customer records** - Keep for billing history

---

## Need Help?

**Stuck on implementation?** Let me know which step you're on and I can:
1. Write the complete code for you
2. Update all files automatically
3. Create the migration scripts
4. Test the integration

**Ready to implement?** Just say "implement full Stripe integration" and I'll do it all!
