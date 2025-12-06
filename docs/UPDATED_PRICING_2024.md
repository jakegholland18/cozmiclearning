# CozmicLearning Updated Pricing Structure - December 2024

## 🎯 FINAL PRICING (Implemented)

---

## 👨‍🎓 STUDENT PLANS

| Plan | Monthly | Yearly | Annual Savings |
|------|---------|--------|----------------|
| **Basic** | $9.99 | $99 | $20 (17% off) |
| **Premium** | $14.99 | $149 | $30 (17% off) |

**Features:**
- Basic: 50 questions/day, 20 practice sessions/day, 1 PowerGrid/day
- Premium: 200 questions/day, 100 practice sessions/day, 5 PowerGrid/day

---

## 👨‍👩‍👧‍👦 PARENT PLANS

| Plan | Monthly | Yearly | Annual Savings |
|------|---------|--------|----------------|
| **Essentials** | $19.99 | $199 | $40 (17% off) |
| **Complete** | $29.99 | $299 | $60 (17% off) |

**Features:**
- Essentials: 2 students, 15 lesson plans/month, 10 PowerGrid/day
- Complete: 5 students, 50 lesson plans/month, 30 PowerGrid/day

---

## 👨‍🏫 TEACHER PLANS

| Plan | Monthly | Yearly | Annual Savings |
|------|---------|--------|----------------|
| **Classroom** | $29.99 | $299 | $60 (17% off) |
| **Complete** | $39.99 | $399 | $80 (17% off) |

**Features:**
- Classroom: 35 students, 25 lesson plans/month, 15 PowerGrid/day
- Complete: 150 students, 100 lesson plans/month, 50 PowerGrid/day

---

## 🏠 HOMESCHOOL PLANS

| Plan | Monthly | Yearly | Annual Savings |
|------|---------|--------|----------------|
| **Essentials** | $24.99 | $249 | $50 (17% off) |
| **Complete** | $34.99 | $349 | $70 (17% off) |

**Features:**
- Essentials: 2 students, 15 lesson plans/month, 10 PowerGrid/day, Biblical integration
- Complete: 5 students, 50 lesson plans/month, 30 PowerGrid/day, Biblical integration

---

## 📋 STRIPE PRODUCTS TO CREATE

### 1. Student Basic
- Monthly: $9.99/month → Price ID → `STRIPE_STUDENT_BASIC_MONTHLY`
- Yearly: $99/year → Price ID → `STRIPE_STUDENT_BASIC_YEARLY`

### 2. Student Premium
- Monthly: $14.99/month → Price ID → `STRIPE_STUDENT_PREMIUM_MONTHLY`
- Yearly: $149/year → Price ID → `STRIPE_STUDENT_PREMIUM_YEARLY`

### 3. Parent Essentials
- Monthly: $19.99/month → Price ID → `STRIPE_PARENT_BASIC_MONTHLY`
- Yearly: $199/year → Price ID → `STRIPE_PARENT_BASIC_YEARLY`

### 4. Parent Complete
- Monthly: $29.99/month → Price ID → `STRIPE_PARENT_PREMIUM_MONTHLY`
- Yearly: $299/year → Price ID → `STRIPE_PARENT_PREMIUM_YEARLY`

### 5. Teacher Classroom
- Monthly: $29.99/month → Price ID → `STRIPE_TEACHER_BASIC_MONTHLY`
- Yearly: $299/year → Price ID → `STRIPE_TEACHER_BASIC_YEARLY`

### 6. Teacher Complete
- Monthly: $39.99/month → Price ID → `STRIPE_TEACHER_PREMIUM_MONTHLY`
- Yearly: $399/year → Price ID → `STRIPE_TEACHER_PREMIUM_YEARLY`

### 7. Homeschool Essentials
- Monthly: $24.99/month → Price ID → `STRIPE_HOMESCHOOL_ESSENTIAL_MONTHLY`
- Yearly: $249/year → Price ID → `STRIPE_HOMESCHOOL_ESSENTIAL_YEARLY`

### 8. Homeschool Complete
- Monthly: $34.99/month → Price ID → `STRIPE_HOMESCHOOL_COMPLETE_MONTHLY`
- Yearly: $349/year → Price ID → `STRIPE_HOMESCHOOL_COMPLETE_YEARLY`

---

## ✅ FILES UPDATED WITH NEW PRICING

- ✅ `/website/templates/trial_expired.html` - Main payment selection page
- ⏳ `/website/templates/home.html` - Homepage pricing display
- ⏳ `/website/templates/homeschool_signup.html` - Homeschool signup page
- ⏳ Other marketing pages as needed

---

## 🎯 NEXT STEPS

1. **Create Stripe Products** (8 products, 16 prices total)
2. **Copy Price IDs** from Stripe dashboard
3. **Add to Render** as environment variables (16 total)
4. **Test Payment Flow** for each user type
5. **Update Marketing Materials** with new pricing

---

**Last Updated:** December 6, 2024
**Status:** PRICING UPDATED IN CODE - READY FOR STRIPE SETUP
