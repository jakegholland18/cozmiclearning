# Stripe Recurring Subscription Setup Guide

**Issue Identified:** Price IDs are set to "One time" instead of "Recurring"

**Error from Stripe API:**
```
You must provide at least one recurring price in `subscription` mode when using prices.
```

---

## ✅ How to Create Recurring Subscription Prices

### For Each Product (16 total):

1. **Go to Stripe Dashboard → Products**
2. **Click "Add product"** (or edit existing product)
3. **Fill in product details:**
   - Name: e.g., "Student Basic Plan"
   - Description: "Basic subscription for student users"

4. **Add a Price - IMPORTANT SETTINGS:**
   - ✅ **Pricing model:** Standard pricing
   - ✅ **Price:** Enter your amount (e.g., $9.99)
   - ✅ **Billing period:** **RECURRING** ← MUST SELECT THIS!
   - ✅ **Interval:** Monthly or Yearly (depending on the price)
   - ✅ **Usage type:** Licensed
   - ❌ **DO NOT select "One time"**

5. **Save and copy the Price ID**
   - Will look like: `price_xxxxxxxxxxxxx`

6. **Add to Render Environment Variables**
   - Go to Render Dashboard → Your Service → Environment
   - Add/Update the variable (see table below)

---

## 📋 All 16 Required Prices

### Student Plans (4 prices)

| Variable Name | Product | Billing | Type |
|--------------|---------|---------|------|
| `STRIPE_STUDENT_BASIC_MONTHLY` | Student Basic | Monthly | Recurring |
| `STRIPE_STUDENT_BASIC_YEARLY` | Student Basic | Yearly | Recurring |
| `STRIPE_STUDENT_PREMIUM_MONTHLY` | Student Premium | Monthly | Recurring |
| `STRIPE_STUDENT_PREMIUM_YEARLY` | Student Premium | Yearly | Recurring |

### Parent Plans (4 prices)

| Variable Name | Product | Billing | Type |
|--------------|---------|---------|------|
| `STRIPE_PARENT_BASIC_MONTHLY` | Parent Basic | Monthly | Recurring |
| `STRIPE_PARENT_BASIC_YEARLY` | Parent Basic | Yearly | Recurring |
| `STRIPE_PARENT_PREMIUM_MONTHLY` | Parent Premium | Monthly | Recurring |
| `STRIPE_PARENT_PREMIUM_YEARLY` | Parent Premium | Yearly | Recurring |

### Teacher Plans (4 prices)

| Variable Name | Product | Billing | Type |
|--------------|---------|---------|------|
| `STRIPE_TEACHER_BASIC_MONTHLY` | Teacher Basic | Monthly | Recurring |
| `STRIPE_TEACHER_BASIC_YEARLY` | Teacher Basic | Yearly | Recurring |
| `STRIPE_TEACHER_PREMIUM_MONTHLY` | Teacher Premium | Monthly | Recurring |
| `STRIPE_TEACHER_PREMIUM_YEARLY` | Teacher Premium | Yearly | Recurring |

### Homeschool Plans (4 prices)

| Variable Name | Product | Billing | Type |
|--------------|---------|---------|------|
| `STRIPE_HOMESCHOOL_ESSENTIAL_MONTHLY` | Homeschool Essential | Monthly | Recurring |
| `STRIPE_HOMESCHOOL_ESSENTIAL_YEARLY` | Homeschool Essential | Yearly | Recurring |
| `STRIPE_HOMESCHOOL_COMPLETE_MONTHLY` | Homeschool Complete | Monthly | Recurring |
| `STRIPE_HOMESCHOOL_COMPLETE_YEARLY` | Homeschool Complete | Yearly | Recurring |

---

## 🎯 Quick Setup (Start with 2 prices for testing)

Don't want to create all 16 right now? Start with these 2 for testing:

1. **STRIPE_STUDENT_BASIC_MONTHLY**
   - Product: "Student Basic Plan"
   - Price: $9.99
   - **Recurring:** Monthly ✅

2. **STRIPE_STUDENT_PREMIUM_MONTHLY**
   - Product: "Student Premium Plan"
   - Price: $14.99
   - **Recurring:** Monthly ✅

Test the payment flow with these 2, then add the rest later.

---

## 🔍 How to Check if a Price is Recurring

1. Go to Stripe Dashboard → Products
2. Click on a product
3. Look at the price details
4. Should say: **"$9.99 / month"** (recurring)
5. Should NOT say: **"$9.99"** (one-time)

### Example of CORRECT setup:
```
Product: Student Basic Plan
Price: $9.99 / month
Type: Recurring subscription
```

### Example of WRONG setup:
```
Product: Student Basic Plan
Price: $9.99
Type: One-time payment
```

---

## 🚨 Common Mistake

**Mistake:** Creating a "One-time" price
- This charges the customer once
- Does NOT create a subscription
- App needs RECURRING prices

**Fix:** Delete one-time price, create new recurring price

---

## ✅ Verification

After setting up prices, test the payment flow:

1. Visit https://cozmiclearning-1.onrender.com/trial_expired?role=student
2. Click "Choose Basic Monthly"
3. Should redirect to Stripe Checkout
4. Should NOT reload the same page

If it still reloads, check Render logs for errors.

---

## 📝 Stripe Dashboard Links

- **Products:** https://dashboard.stripe.com/products
- **Test Mode:** Use test mode for testing (toggle in top-right)
- **Live Mode:** Switch to live mode when ready for production

---

**Last Updated:** 2025-12-07
**Status:** Ready to create recurring subscription prices
