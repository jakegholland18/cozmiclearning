# Stripe Integration - Next Steps

## ✅ What's Been Completed

All code for Stripe payment integration has been implemented and pushed to GitHub:

1. **Subscription Enforcement**
   - Trial expiration checks on all dashboards
   - Automatic redirect to upgrade page when trial expires
   - Protected all AI features (questions, deep study, practice)

2. **Payment Flow**
   - Stripe Checkout integration for all 16 plan types
   - Success page that activates subscriptions
   - Webhook handler for subscription lifecycle events

3. **User Experience**
   - Beautiful trial_expired.html page with role-specific pricing
   - Trial countdown displayed on dashboards
   - Clear upgrade prompts throughout app

4. **Documentation**
   - Complete STRIPE_SETUP.md guide
   - Step-by-step instructions for Stripe configuration
   - Test card information and troubleshooting

---

## 🔧 Manual Setup Required (Do This Next)

### 1. Create Stripe Account
- Go to https://stripe.com and sign up
- Complete business verification (required for live payments)

### 2. Create Products in Stripe Dashboard
You need to create **16 subscription products** in Stripe:

**Students:**
- Basic Monthly: $7.99/month → Get Price ID
- Basic Yearly: $85/year → Get Price ID
- Premium Monthly: $12.99/month → Get Price ID
- Premium Yearly: $140/year → Get Price ID

**Parents:**
- Basic Monthly: $9.99/month → Get Price ID
- Basic Yearly: $75/year → Get Price ID
- Premium Monthly: $15.99/month → Get Price ID
- Premium Yearly: $160/year → Get Price ID

**Teachers:**
- Basic Monthly: $15.99/month → Get Price ID
- Basic Yearly: $170/year → Get Price ID
- Premium Monthly: $25.99/month → Get Price ID
- Premium Yearly: $280/year → Get Price ID

**Homeschool:**
- Essential Monthly: $19.99/month → Get Price ID
- Essential Yearly: $215/year → Get Price ID
- Complete Monthly: $29.99/month → Get Price ID
- Complete Yearly: $320/year → Get Price ID

**How to create products:**
1. In Stripe Dashboard, go to **Products**
2. Click **Add product**
3. Fill in name, price, and billing period
4. Click **Save**
5. **Copy the Price ID** (starts with `price_...`)

### 3. Add Environment Variables to Render

Go to your Render dashboard and add these environment variables to your web service:

```
STRIPE_SECRET_KEY=sk_test_... (from Stripe Dashboard → Developers → API keys)
STRIPE_PUBLISHABLE_KEY=pk_test_... (from Stripe Dashboard → Developers → API keys)

STRIPE_STUDENT_BASIC_MONTHLY=price_... (from step 2)
STRIPE_STUDENT_BASIC_YEARLY=price_...
STRIPE_STUDENT_PREMIUM_MONTHLY=price_...
STRIPE_STUDENT_PREMIUM_YEARLY=price_...
STRIPE_PARENT_BASIC_MONTHLY=price_...
STRIPE_PARENT_BASIC_YEARLY=price_...
STRIPE_PARENT_PREMIUM_MONTHLY=price_...
STRIPE_PARENT_PREMIUM_YEARLY=price_...
STRIPE_TEACHER_BASIC_MONTHLY=price_...
STRIPE_TEACHER_BASIC_YEARLY=price_...
STRIPE_TEACHER_PREMIUM_MONTHLY=price_...
STRIPE_TEACHER_PREMIUM_YEARLY=price_...
STRIPE_HOMESCHOOL_ESSENTIAL_MONTHLY=price_...
STRIPE_HOMESCHOOL_ESSENTIAL_YEARLY=price_...
STRIPE_HOMESCHOOL_COMPLETE_MONTHLY=price_...
STRIPE_HOMESCHOOL_COMPLETE_YEARLY=price_...
```

### 4. Set Up Webhook

1. In Stripe Dashboard, go to **Developers** → **Webhooks**
2. Click **Add endpoint**
3. Enter URL: `https://your-app.onrender.com/stripe-webhook`
4. Select these events:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_failed`
5. Click **Add endpoint**
6. Copy the **Signing secret** (starts with `whsec_...`)
7. Add to Render environment variables:
   ```
   STRIPE_WEBHOOK_SECRET=whsec_...
   ```

### 5. Test the Integration

**Using Test Mode (Recommended First):**
1. Make sure you're using test API keys
2. Create a new student account
3. Wait 7 days OR manually update database:
   ```sql
   UPDATE students SET trial_end = '2024-01-01' WHERE id = X;
   ```
4. Visit dashboard - should redirect to trial_expired page
5. Click a plan button
6. Use test card: `4242 4242 4242 4242`
7. Complete checkout
8. Verify subscription is activated

**Test Cards:**
- Success: `4242 4242 4242 4242`
- 3D Secure: `4000 0025 0000 3155`
- Declined: `4000 0000 0000 9995`

---

## 📋 Testing Checklist

- [ ] Stripe account created and verified
- [ ] All 16 products created in Stripe
- [ ] All Price IDs copied and saved
- [ ] Stripe API keys added to Render
- [ ] All 16 Price ID environment variables added to Render
- [ ] Webhook endpoint configured
- [ ] Webhook signing secret added to Render
- [ ] Test signup with trial expiration
- [ ] Test payment flow with test card
- [ ] Verify subscription activation
- [ ] Test webhook events (check Render logs)

---

## 🚀 Going Live

When ready for production:

1. **Switch to Live Mode** in Stripe Dashboard
2. Recreate all 16 products in **Live mode**
3. Update environment variables with **live** API keys and Price IDs
4. Update webhook endpoint to use live mode
5. Test with real payment (can refund after)
6. Monitor first few transactions closely

---

## 📚 Resources

- **Setup Guide**: See `STRIPE_SETUP.md` for detailed instructions
- **Stripe Dashboard**: https://dashboard.stripe.com
- **Stripe Docs**: https://stripe.com/docs
- **Stripe Testing**: https://stripe.com/docs/testing

---

## 🆘 Need Help?

If you get stuck:
1. Check STRIPE_SETUP.md for detailed troubleshooting
2. Verify all environment variables are set correctly
3. Check Render logs for error messages
4. Check Stripe Dashboard → Developers → Webhooks for failed events
5. Use Stripe test mode first before going live

---

## Current Status

✅ Code is ready and deployed
✅ Database supports subscriptions
✅ UI/UX is complete
⏳ Waiting for Stripe configuration
⏳ Waiting for environment variables

**Estimated time to complete manual setup:** 30-45 minutes
