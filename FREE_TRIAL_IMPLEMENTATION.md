# Free Trial System Implementation Plan

## Overview
This document outlines the complete free trial system for CozmicLearning, replacing the permanent free tier with a 14-day free trial that converts to paid.

## Current Status
✅ Database fields already exist (`trial_start`, `trial_end`, `subscription_active`)
⚠️ Trial logic needs to be implemented
⚠️ Trial enforcement needs to be added
⚠️ UI indicators need to be added

---

## 1. Trial Configuration

### Trial Settings
```python
TRIAL_DAYS = 14  # 14-day free trial
GRACE_PERIOD_DAYS = 3  # 3 days after trial before hard block
REQUIRE_CREDIT_CARD = True  # Require card upfront (reduces fraud)
```

### User Types & Trials
| User Type | Trial Length | Credit Card Required | Full Access |
|-----------|--------------|---------------------|-------------|
| Student | 14 days | Optional | ✅ Yes |
| Parent | 14 days | Yes (if premium) | ✅ Yes |
| Teacher | 14 days | Yes | ✅ Yes |

---

## 2. Trial Lifecycle

### Phase 1: Trial Sign Up
**When:** User creates new account
**Action:**
1. Set `trial_start = now()`
2. Set `trial_end = now() + 14 days`
3. Set `subscription_active = False` (trial is not subscription)
4. Set `plan = "trial"` or `plan = "premium_trial"`
5. If credit card required: collect payment method (don't charge)

**Code Location:** `/student/signup`, `/parent/signup`, `/teacher/signup`

### Phase 2: Active Trial
**When:** `now() < trial_end`
**Action:**
- Full access to all features
- Show "X days left in trial" banner
- Send reminder emails at days 7, 3, 1
- Allow upgrade to paid anytime

**Code Location:** All authenticated routes (middleware check)

### Phase 3: Trial Expired (Grace Period)
**When:** `trial_end < now() < trial_end + 3 days`
**Action:**
- Show urgent upgrade prompts
- Limit access to read-only mode
- Send "Trial Expired" emails daily
- Still allow login to upgrade

**Code Location:** Dashboard routes

### Phase 4: Hard Block
**When:** `now() > trial_end + 3 days AND subscription_active = False`
**Action:**
- Redirect all pages to upgrade page
- Block all features except billing
- Show account suspended message
- Final email: "Account Suspended"

**Code Location:** Auth middleware

### Phase 5: Conversion to Paid
**When:** User subscribes during or after trial
**Action:**
1. Charge payment method via Stripe
2. Set `subscription_active = True`
3. Set `plan = "basic"/"premium"/"pro"`
4. Clear trial fields or keep for analytics
5. Send "Welcome to Paid" email

**Code Location:** `/subscribe` endpoint

---

## 3. Database Schema (Already Exists!)

### Parent Model
```python
trial_start = db.Column(db.DateTime)  # When trial started
trial_end = db.Column(db.DateTime)    # When trial ends
subscription_active = db.Column(db.Boolean, default=False)  # Paid status
plan = db.Column(db.String(50))  # "trial", "basic", "premium"
stripe_customer_id = db.Column(db.String(255))
stripe_subscription_id = db.Column(db.String(255))
```

### Teacher & Student Models
Same fields as Parent model above.

---

## 4. Helper Functions to Build

### Trial Status Checker
```python
def get_trial_status(user):
    """
    Returns trial status for a user.

    Returns:
        {
            "status": "active" | "expired_grace" | "expired_hard" | "paid",
            "days_remaining": int,
            "trial_end_date": datetime,
            "can_access": bool,
            "message": str
        }
    """
    from datetime import datetime, timedelta

    now = datetime.utcnow()

    # Already paid
    if user.subscription_active:
        return {
            "status": "paid",
            "days_remaining": None,
            "trial_end_date": None,
            "can_access": True,
            "message": "Active subscription"
        }

    # No trial set up (shouldn't happen with new signups)
    if not user.trial_start or not user.trial_end:
        return {
            "status": "no_trial",
            "days_remaining": 0,
            "trial_end_date": None,
            "can_access": False,
            "message": "No trial configured"
        }

    days_remaining = (user.trial_end - now).days
    grace_period_end = user.trial_end + timedelta(days=3)

    # Active trial
    if now < user.trial_end:
        return {
            "status": "active",
            "days_remaining": days_remaining,
            "trial_end_date": user.trial_end,
            "can_access": True,
            "message": f"{days_remaining} days left in your free trial"
        }

    # Grace period (soft block)
    elif now < grace_period_end:
        return {
            "status": "expired_grace",
            "days_remaining": 0,
            "trial_end_date": user.trial_end,
            "can_access": True,  # Limited access
            "message": "Your trial has expired. Upgrade to continue."
        }

    # Hard block
    else:
        return {
            "status": "expired_hard",
            "days_remaining": 0,
            "trial_end_date": user.trial_end,
            "can_access": False,
            "message": "Your account has been suspended. Please upgrade."
        }
```

### Trial Access Decorator
```python
from functools import wraps
from flask import redirect, flash

def trial_required(f):
    """
    Decorator to check if user has active trial or paid subscription.
    Redirects to upgrade page if trial expired.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()  # Your existing function
        if not user:
            return redirect("/login")

        status = get_trial_status(user)

        # Hard block - force upgrade
        if status["status"] == "expired_hard":
            flash(status["message"], "error")
            return redirect("/upgrade")

        # Grace period - show warning but allow access
        if status["status"] == "expired_grace":
            flash(status["message"], "warning")

        return f(*args, **kwargs)

    return decorated_function
```

---

## 5. UI Components to Add

### Trial Banner (All Pages)
```html
{% if trial_status.status == "active" and trial_status.days_remaining <= 3 %}
<div class="trial-banner trial-ending">
    ⏰ Only {{ trial_status.days_remaining }} days left in your trial!
    <a href="/upgrade">Upgrade Now</a>
</div>
{% elif trial_status.status == "expired_grace" %}
<div class="trial-banner trial-expired">
    ⚠️ Your trial has expired. <a href="/upgrade">Upgrade to continue</a>
</div>
{% endif %}
```

### Dashboard Trial Widget
```html
<div class="trial-widget">
    <h3>Free Trial Status</h3>
    {% if trial_status.status == "active" %}
        <p>{{ trial_status.days_remaining }} days remaining</p>
        <div class="trial-progress-bar">
            <div class="progress" style="width: {{ (trial_status.days_remaining / 14 * 100)|int }}%"></div>
        </div>
        <a href="/upgrade" class="btn btn-upgrade">Upgrade Now</a>
    {% elif trial_status.status == "paid" %}
        <p>✅ Active Subscription</p>
        <p>Plan: {{ current_user.plan|title }}</p>
    {% else %}
        <p>❌ Trial Expired</p>
        <a href="/upgrade" class="btn btn-primary">Upgrade to Continue</a>
    {% endif %}
</div>
```

---

## 6. Routes to Create/Modify

### New Routes Needed
- `GET /upgrade` - Upgrade page with pricing
- `POST /subscribe` - Handle Stripe subscription
- `GET /trial-expired` - Upgrade-only page for hard blocked users

### Routes to Modify (Add Trial Check)
- `/dashboard` - Add trial banner
- `/practice` - Check trial status
- `/teacher/dashboard` - Add trial status
- `/parent_dashboard` - Add trial widget
- All feature routes - Add `@trial_required` decorator

---

## 7. Stripe Integration

### Subscription Flow
1. **Collect Payment Method** (during signup or trial)
2. **Create Stripe Customer** (`stripe.Customer.create()`)
3. **Save customer ID** (`user.stripe_customer_id`)
4. **On upgrade:** Create subscription (`stripe.Subscription.create()`)
5. **Save subscription ID** (`user.stripe_subscription_id`)
6. **Set** `subscription_active = True`

### Webhook Handling (Critical!)
```python
@app.route("/stripe-webhook", methods=["POST"])
def stripe_webhook():
    """
    Handle Stripe events:
    - subscription.created
    - subscription.updated
    - subscription.deleted (cancellation)
    - invoice.payment_failed
    """
    # Verify webhook signature
    # Update user subscription_active based on event
    # Send confirmation emails
```

---

## 8. Email Notifications

### Trial Reminder Emails
| Day | Subject | Content |
|-----|---------|---------|
| Day 7 | "1 Week Left in Your Trial" | Highlight features, show upgrade link |
| Day 3 | "3 Days Left - Don't Lose Access!" | Urgency, pricing reminder |
| Day 1 | "Last Day of Your Free Trial" | Final reminder, easy upgrade CTA |
| Day 0 | "Your Trial Has Ended" | Grace period info, upgrade required |
| Day 3 (after) | "Account Suspended" | Final warning, data retention info |

### Implementation
```python
def send_trial_reminder_emails():
    """
    Cron job to send trial reminders.
    Run daily at 9am.
    """
    from datetime import datetime, timedelta

    now = datetime.utcnow()

    # Users with 7 days left
    users_day_7 = User.query.filter(
        User.trial_end == now + timedelta(days=7),
        User.subscription_active == False
    ).all()

    for user in users_day_7:
        send_email(
            to=user.email,
            subject="1 Week Left in Your CozmicLearning Trial",
            template="trial_7days.html",
            user=user
        )

    # Repeat for day 3, day 1, day 0, day 3 after
```

---

## 9. Analytics & Metrics

### Key Metrics to Track
- Trial signup conversion rate (signups → credit card added)
- Trial to paid conversion rate (trial users → paying users)
- Churn during grace period
- Average time to upgrade
- Revenue per trial user

### Database Logging
```python
class TrialEvent(db.Model):
    """Log trial lifecycle events for analytics"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_type = db.Column(db.String(20))  # student/parent/teacher
    event_type = db.Column(db.String(50))  # trial_started, trial_expired, upgraded, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

---

## 10. Implementation Checklist

### Phase 1: Core Trial Logic (Week 1)
- [x] Database fields already exist
- [ ] Create `get_trial_status()` helper function
- [ ] Create `@trial_required` decorator
- [ ] Update signup flows to set trial dates
- [ ] Test trial lifecycle manually

### Phase 2: UI Indicators (Week 1)
- [ ] Add trial banner component
- [ ] Add trial widget to dashboards
- [ ] Create upgrade page with pricing
- [ ] Add trial countdown timers
- [ ] Test UI on all user types

### Phase 3: Access Control (Week 2)
- [ ] Add `@trial_required` to all protected routes
- [ ] Implement grace period logic
- [ ] Implement hard block logic
- [ ] Create trial-expired page
- [ ] Test access restrictions

### Phase 4: Stripe Integration (Week 2)
- [ ] Set up Stripe account (already done?)
- [ ] Create subscription products in Stripe
- [ ] Build subscription creation flow
- [ ] Add webhook handler
- [ ] Test payment flow end-to-end

### Phase 5: Email Automation (Week 3)
- [ ] Create email templates
- [ ] Set up cron job for reminders
- [ ] Test email sending
- [ ] Monitor delivery rates

### Phase 6: Analytics & Monitoring (Week 3)
- [ ] Add trial event logging
- [ ] Create admin analytics dashboard
- [ ] Set up conversion tracking
- [ ] Monitor trial-to-paid rates

---

## 11. Testing Scenarios

### Manual Test Cases
1. **Sign up** → Verify trial_start and trial_end set correctly
2. **Access during trial** → Full access works
3. **Trial countdown** → Banner shows correct days remaining
4. **Upgrade during trial** → Subscription activates, trial cleared
5. **Let trial expire** → Grace period activates
6. **Wait 3 days after expiry** → Hard block activates
7. **Try to access features** → Redirects to upgrade page
8. **Upgrade after expiry** → Access restored immediately

### Automated Test Cases (Optional)
```python
def test_trial_lifecycle():
    # Create user with trial
    user = create_test_user(trial=True)
    assert user.trial_end == user.trial_start + timedelta(days=14)

    # Test active trial
    status = get_trial_status(user)
    assert status["status"] == "active"
    assert status["can_access"] == True

    # Simulate trial expiry
    user.trial_end = datetime.utcnow() - timedelta(days=1)
    status = get_trial_status(user)
    assert status["status"] == "expired_grace"

    # Simulate hard block
    user.trial_end = datetime.utcnow() - timedelta(days=5)
    status = get_trial_status(user)
    assert status["status"] == "expired_hard"
    assert status["can_access"] == False
```

---

## 12. Migration Plan (Existing Users)

### For Current Free Users
**Option 1: Grandfather Existing Users**
- Keep existing free users on free plan forever
- Only new signups get trial

**Option 2: Convert to Trial**
- Email all free users: "You're getting a premium upgrade!"
- Give them 30-day trial instead of 14
- Require upgrade after trial

**Option 3: Hybrid**
- Active users (logged in last 30 days): 30-day trial
- Inactive users: Convert to trial on next login
- Very old accounts (>1 year): Keep free as goodwill

### Migration Code
```python
def migrate_free_to_trial():
    """One-time migration script"""
    from datetime import datetime, timedelta

    free_users = Student.query.filter_by(plan="free", subscription_active=False).all()

    for user in free_users:
        # Option: Give 30-day trial to existing users
        user.trial_start = datetime.utcnow()
        user.trial_end = datetime.utcnow() + timedelta(days=30)
        user.plan = "premium_trial"
        db.session.add(user)

        # Send email notification
        send_email(
            to=user.email,
            subject="You've Been Upgraded!",
            template="free_to_trial.html",
            user=user
        )

    db.session.commit()
```

---

## Summary

**What You'll Have:**
✅ 14-day free trial for all new users
✅ Full access during trial
✅ Automatic trial tracking
✅ Trial expiration with grace period
✅ Hard block after grace period
✅ Stripe integration for upgrades
✅ Email reminders at key milestones
✅ Analytics to track conversions

**Estimated Build Time:** 2-3 weeks full implementation
**Complexity:** Medium (Stripe integration is the tricky part)
**Revenue Impact:** High (converts free users to paid customers)

---

## Next Steps

1. **Review this plan** - Does this match your vision?
2. **Prioritize phases** - What to build first?
3. **Start with Phase 1** - Core trial logic and UI
4. **Test thoroughly** - Don't launch broken billing!

Ready to start building? Let me know which phase you want to tackle first!
