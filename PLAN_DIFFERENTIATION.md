# Plan Differentiation Implementation

## Student Pricing Structure

### Basic Plan - $7.99/month ($85/year)
- Access to all 11 subjects
- **100 questions per month limit**
- Basic practice missions
- 7-day free trial

### Premium Plan - $12.99/month ($140/year)  
- **Unlimited questions**
- All differentiation modes
- Advanced analytics
- 7-day free trial

**Note:** Parent and Teacher pricing remains separate:
- Parent/Teacher Basic: $9.99/mo ($75/yr) - up to 3 students
- Parent/Teacher Premium: $15.99/mo ($160/yr) - unlimited students

## Implementation Details

### Usage Tracking System
**Location:** `app.py` lines 520-560

Three new helper functions:
1. **`check_monthly_reset()`** - Automatically resets question counter on first day of each month
2. **`check_question_limit()`** - Returns (allowed, remaining, limit) tuple for plan enforcement
3. **`increment_question_count()`** - Tracks each question asked by Basic plan students

**Session tracking:**
- `questions_this_month`: Integer counter of questions asked
- `month_start`: Date string tracking when current month started

### Plan Enforcement Points
All AI question endpoints now check limits before responding:

1. **`/subject` POST route** (line 2940)
   - Checks limit before generating subject-specific answers
   - Redirects to `/plans` if limit exceeded
   - Increments counter after successful response

2. **`/followup_message` POST route** (line 2987)
   - Checks limit for deep study follow-up questions
   - Returns JSON error with `upgrade_required: true` if exceeded
   - Increments counter after response

3. **`/deep_study_message` POST route** (line 3017)
   - Checks limit for PowerGrid chat messages
   - Returns JSON error if limit exceeded
   - Increments counter after response

### Dashboard Display
**Location:** `website/templates/dashboard.html` lines 258-282

Students on Basic plan see:
- **Usage counter** in stats grid (e.g., "45/100")
- **Orange border** on Questions stat when under 20 remaining
- **Warning banner** when under 10 questions remaining with upgrade link

### Plan Rules
1. **Premium students:** Unlimited questions (limit = infinity)
2. **Trial period students:** Unlimited during 7-day trial (regardless of plan selected)
3. **Parent-linked students:** Inherit parent's plan; no individual limits enforced
4. **Standalone students:** Subject to their own plan limits

### Monthly Reset Logic
- Runs automatically on every `init_user()` call
- Compares `session['month_start']` to current month's first day
- Resets counter to 0 if new month detected
- Updates `month_start` to current month

## User Experience Flow

### Basic Plan Student Journey
1. **Sign up** → Select Basic plan ($7.99/mo)
2. **Trial period** → 7 days unlimited access
3. **After trial** → 100 questions/month limit enforced
4. **Dashboard** → Usage counter visible (e.g., "23/100")
5. **Near limit** → Orange warning appears (<20 remaining)
6. **Hit limit** → Redirected to `/plans` with upgrade message
7. **Next month** → Counter auto-resets to 0

### Premium Plan Student Journey
1. **Sign up** → Select Premium plan ($12.99/mo)
2. **No limits** → Unlimited questions forever
3. **Dashboard** → No usage counter shown

### Parent-Linked Student Journey
1. **Parent creates account** → Selects parent plan (Basic/Premium)
2. **Student added** → Inherits parent subscription
3. **No individual limits** → Parent plan covers all their students
4. **Parent plan limits** → Basic parents limited to 3 students total

## Testing Checklist

- [ ] Basic standalone student hits 100 question limit
- [ ] Premium standalone student has unlimited access
- [ ] Trial period student has unlimited during first 7 days
- [ ] Counter resets automatically on month change
- [ ] Dashboard shows correct usage for Basic students
- [ ] Dashboard hides usage for Premium students
- [ ] Parent-linked students unaffected by individual limits
- [ ] Error messages display correctly when limit hit
- [ ] Upgrade link redirects to `/plans` page
- [ ] Monthly reset preserves other session data

## Future Enhancements

### Potential Additional Differentiators
1. **Practice mission complexity:** Basic gets standard difficulty, Premium gets adaptive/mastery modes
2. **Response depth:** Basic gets concise answers, Premium gets detailed explanations
3. **Analytics access:** Basic gets basic stats, Premium gets full analytics dashboard
4. **Character unlocks:** Basic gets default characters, Premium unlocks all characters
5. **PDF exports:** Basic limited, Premium unlimited PowerGrid study guides

### Analytics Dashboard
Track and display:
- Questions asked per subject
- Usage trends over time
- Most active learning times
- Subject distribution
- Engagement metrics

### Upgrade Prompts
- Show plan comparison modal when hitting limit
- Highlight Premium benefits contextually
- Offer upgrade discount for high-usage Basic users
- Email reminders when approaching limit (if email preferences allow)
