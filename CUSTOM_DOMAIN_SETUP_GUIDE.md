# 🌐 Custom Domain Setup for CozmicLearning

**Goal**: Connect your custom domain (like cozmiclearning.com) to your Render website

**Current URL**: https://cozmiclearning-1.onrender.com
**Future URL**: https://cozmiclearning.com (or whatever domain you choose)

---

## 📋 QUICK OVERVIEW

**What You Need**:
1. A domain name (buy one if you don't have it yet)
2. Access to your domain registrar account
3. Access to your Render dashboard
4. 5-30 minutes

**Steps**:
1. Buy domain (if you don't have one)
2. Add custom domain in Render
3. Update DNS settings at your domain registrar
4. Wait for DNS propagation (5 minutes - 48 hours)
5. Enable HTTPS/SSL (automatic on Render)

**Cost**: $10-15/year for domain (Render hosting is what you're already paying)

---

## STEP 1: BUY A DOMAIN (If You Don't Have One)

### **Recommended Domain Registrars**:

**Option 1: Namecheap** ⭐ RECOMMENDED
- **Website**: namecheap.com
- **Cost**: $8-13/year for .com
- **Pros**: Cheap, easy to use, free WHOIS privacy, good support
- **Best For**: Most people

**Option 2: Google Domains** (Now Squarespace Domains)
- **Website**: domains.google (redirects to Squarespace)
- **Cost**: $12/year for .com
- **Pros**: Simple interface, integrated with Google services
- **Best For**: If you use Google Workspace

**Option 3: Cloudflare**
- **Website**: cloudflare.com
- **Cost**: At-cost pricing (~$10/year)
- **Pros**: Built-in CDN, best performance, advanced features
- **Best For**: If you want maximum speed/security

**Option 4: GoDaddy**
- **Cost**: $12-20/year (often more expensive)
- **Cons**: Aggressive upselling, more expensive renewals
- **Recommendation**: Use Namecheap or Cloudflare instead

---

### **Which Domain Name?**

**Options**:

**Option A: CozmicLearning.com** ⭐ RECOMMENDED
- Professional
- Matches your brand exactly
- Easy to remember
- Check availability: namecheap.com

**Option B: Variations if .com is taken**:
- CozmicLearning.org (for educational feel)
- CozmicLearning.io (modern/tech feel)
- GetCozmic.com (shorter, action-oriented)
- LearnCozmic.com
- CozmicEd.com

**Option C: Christian-focused variants**:
- CozmicChristianLearning.com
- FaithCozmic.com
- ChristianCozmic.com

---

### **How to Buy Domain (Namecheap Example)**:

**Step 1**: Go to namecheap.com

**Step 2**: Search for your desired domain
```
Search box: "cozmiclearning.com"
Click "Search"
```

**Step 3**: Check if available
- ✅ Available → Click "Add to Cart"
- ❌ Taken → Try variations (cozmiclearning.org, getcozmic.com, etc.)

**Step 4**: Cart & Checkout
- Domain: $8.88/year (or similar)
- WHOIS Privacy: FREE (auto-included)
- Auto-Renew: ON (recommended)
- SSL Certificate: NO NEED (Render provides free SSL)

**Step 5**: Create Account
- Enter email, password
- Complete payment

**Step 6**: Confirmation
- Check email for confirmation
- Domain is now yours!

**Time**: 5 minutes
**Cost**: ~$10/year

---

## STEP 2: ADD CUSTOM DOMAIN IN RENDER

### **Navigate to Render Dashboard**:

**Step 1**: Go to dashboard.render.com

**Step 2**: Log in with your credentials

**Step 3**: Click on your **CozmicLearning service** (from the list)

**Step 4**: Click **"Settings"** tab (top navigation)

**Step 5**: Scroll down to **"Custom Domains"** section

**Step 6**: Click **"Add Custom Domain"** button

---

### **Add Your Domain**:

**In the dialog box that appears**:

**Domain Name**: Enter your domain
```
Example: cozmiclearning.com
```

**Options**:

**Option A: With www**
- Add both: `cozmiclearning.com` AND `www.cozmiclearning.com`
- Render will redirect www → non-www automatically
- **Recommended**: Better for SEO, more professional

**Option B: Without www**
- Add only: `cozmiclearning.com`
- Simpler, modern approach

**My Recommendation**: Add BOTH, set main as non-www

**Step 7**: Click **"Add"** or **"Save"**

---

### **Get DNS Instructions from Render**:

After adding domain, Render will show you:

**For Apex Domain** (cozmiclearning.com):
```
Type: A
Name: @
Value: [Render's IP address - something like 216.24.57.1]
TTL: Automatic or 3600
```

**For www Subdomain** (www.cozmiclearning.com):
```
Type: CNAME
Name: www
Value: cozmiclearning-1.onrender.com
TTL: Automatic or 3600
```

**IMPORTANT**: Write these down or keep the Render page open - you'll need these values in the next step!

---

## STEP 3: UPDATE DNS SETTINGS AT YOUR DOMAIN REGISTRAR

### **Namecheap Instructions** (Most Common):

**Step 1**: Log in to namecheap.com

**Step 2**: Go to **Domain List** (left sidebar)

**Step 3**: Find your domain → Click **"Manage"**

**Step 4**: Click **"Advanced DNS"** tab

**Step 5**: Add/Edit DNS Records

---

### **DNS Records to Add**:

**Record 1 - Apex Domain (A Record)**:

Click **"Add New Record"**

```
Type: A Record
Host: @
Value: [Render's IP address from Step 2]
TTL: Automatic (or 3600)
```

Click **"Save Changes"** (green checkmark)

---

**Record 2 - www Subdomain (CNAME Record)**:

Click **"Add New Record"**

```
Type: CNAME Record
Host: www
Value: cozmiclearning-1.onrender.com
TTL: Automatic (or 3600)
```

Click **"Save Changes"**

---

**Remove Old Records** (if they exist):

Look for existing records with Host "@" or "www"

Common ones to DELETE:
- Namecheap Parking Page (A record pointing to their parking IP)
- Default CNAME records
- Old hosting records

**Only keep**:
- Your new A record (@)
- Your new CNAME record (www)
- Any email-related records (MX, TXT for email - don't delete these!)

---

### **Google Domains / Squarespace Domains**:

**Step 1**: Go to domains.google.com (redirects to Squarespace)

**Step 2**: Click your domain

**Step 3**: Click **"DNS"** in left sidebar

**Step 4**: Scroll to **"Custom records"**

**Step 5**: Add records:

**A Record**:
```
Host name: @
Type: A
TTL: 3600
Data: [Render's IP]
```

**CNAME Record**:
```
Host name: www
Type: CNAME
TTL: 3600
Data: cozmiclearning-1.onrender.com
```

**Step 6**: Click **"Save"**

---

### **Cloudflare Instructions**:

**Step 1**: Log in to cloudflare.com

**Step 2**: Click your domain

**Step 3**: Click **"DNS"** tab

**Step 4**: Click **"Add record"**

**A Record**:
```
Type: A
Name: @
IPv4 address: [Render's IP]
Proxy status: Proxied (orange cloud) ← TURN THIS ON
TTL: Auto
```

**CNAME Record**:
```
Type: CNAME
Name: www
Target: cozmiclearning-1.onrender.com
Proxy status: Proxied (orange cloud) ← TURN THIS ON
TTL: Auto
```

**Step 5**: Click **"Save"**

**Note**: Cloudflare's proxy (orange cloud) gives you free CDN + DDoS protection - recommended!

---

## STEP 4: WAIT FOR DNS PROPAGATION

### **What is DNS Propagation?**

When you change DNS records, it takes time for the entire internet to update.

**Timeline**:
- **Minimum**: 5-15 minutes (best case)
- **Typical**: 1-4 hours (most common)
- **Maximum**: 24-48 hours (worst case, rare)

**What to do**: Just wait. Check periodically.

---

### **How to Check if It's Working**:

**Method 1: Browser Test**
- Open incognito/private browser window
- Type: `https://cozmiclearning.com`
- If you see your site → SUCCESS! ✅
- If you see error → Wait longer, or check DNS records

**Method 2: DNS Checker Tool**
- Go to: whatsmydns.net
- Enter: `cozmiclearning.com`
- Select: `A` record type
- Click "Search"
- You should see Render's IP address appear globally (green checkmarks)

**Method 3: Command Line** (Mac/Linux)
```bash
dig cozmiclearning.com
# Look for Render's IP address in the ANSWER section
```

**Method 4: Windows Command Prompt**
```cmd
nslookup cozmiclearning.com
# Should show Render's IP address
```

---

## STEP 5: ENABLE HTTPS/SSL (Automatic)

### **Good News**: Render handles this automatically!

**What Happens**:
1. Once your domain points to Render (DNS propagated)
2. Render automatically provisions a free SSL certificate from Let's Encrypt
3. Your site is automatically available via HTTPS
4. HTTP requests automatically redirect to HTTPS

**Timeline**: Usually within 5-15 minutes after DNS propagates

**You'll know it's working when**:
- Browser shows padlock icon 🔒
- URL shows `https://cozmiclearning.com` (not http)
- No security warnings

**If SSL doesn't auto-enable**:
1. Check Render dashboard → Settings → Custom Domains
2. Look for your domain - should show "Active" with green checkmark
3. If shows "Pending" → Wait 10-30 more minutes
4. If shows "Failed" → Check DNS records are correct

---

## TROUBLESHOOTING

### **Problem 1: "This site can't be reached" or "DNS_PROBE_FINISHED_NXDOMAIN"**

**Cause**: DNS records not set up correctly or not propagated yet

**Fix**:
1. Double-check DNS records in your registrar
2. Make sure A record has correct Render IP
3. Make sure CNAME has correct Render URL
4. Wait 1-2 hours for propagation
5. Clear browser cache: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

---

### **Problem 2: "Your connection is not private" or SSL warning**

**Cause**: SSL certificate hasn't provisioned yet

**Fix**:
1. Wait 15-30 minutes after DNS propagates
2. Check Render dashboard - domain should show "Active"
3. If still not working after 1 hour → Contact Render support

---

### **Problem 3: Domain points to Render but shows wrong site**

**Cause**: Domain pointing to wrong Render service

**Fix**:
1. Render dashboard → Check which service domain is added to
2. Make sure it's added to "CozmicLearning" service, not a different one
3. Remove domain from wrong service, re-add to correct one

---

### **Problem 4: www works but non-www doesn't (or vice versa)**

**Cause**: Missing A record or CNAME record

**Fix**:
- For non-www (cozmiclearning.com): Need A record with host "@"
- For www (www.cozmiclearning.com): Need CNAME record with host "www"
- Add the missing record

---

### **Problem 5: DNS propagated but Render shows "Pending"**

**Cause**: Render waiting for DNS to fully propagate

**Fix**:
1. Wait 30 minutes
2. Check whatsmydns.net - make sure majority of locations show green
3. If still pending after 2 hours → Contact Render support

---

## COMPLETE CHECKLIST

### **Before You Start**:
- [ ] Domain name purchased (or you know which one to buy)
- [ ] Access to domain registrar account
- [ ] Access to Render dashboard
- [ ] Know your desired domain (cozmiclearning.com, etc.)

### **During Setup**:
- [ ] Added custom domain in Render
- [ ] Copied Render's A record IP address
- [ ] Copied Render's CNAME target
- [ ] Logged into domain registrar
- [ ] Added A record (@ → Render IP)
- [ ] Added CNAME record (www → Render URL)
- [ ] Removed old/conflicting DNS records
- [ ] Saved DNS changes

### **After Setup**:
- [ ] Waited for DNS propagation (1-4 hours)
- [ ] Tested domain in browser (incognito mode)
- [ ] Checked DNS with whatsmydns.net
- [ ] Confirmed HTTPS working (padlock icon)
- [ ] Tested both www and non-www versions
- [ ] Updated all marketing materials with new domain
- [ ] Updated Facebook/Google Ads with new URL
- [ ] Celebrated! 🎉

---

## ADDITIONAL CONFIGURATIONS

### **Email Setup** (Optional but Recommended)

**Problem**: You bought cozmiclearning.com but want email like contact@cozmiclearning.com

**Solutions**:

**Option 1: Google Workspace** (Recommended for business)
- **Cost**: $6/user/month
- **Features**: Professional email, Google Drive, Calendar, Docs
- **Setup**: workspace.google.com → Add domain → Follow DNS instructions
- **Email**: contact@cozmiclearning.com, support@cozmiclearning.com

**Option 2: Zoho Mail** (Free for small teams)
- **Cost**: FREE for up to 5 users
- **Features**: Email only (no Drive/Calendar)
- **Setup**: zoho.com/mail → Free plan → Add domain
- **Email**: contact@cozmiclearning.com

**Option 3: Email Forwarding** (Simplest, free)
- **Cost**: FREE
- **Features**: Forward cozmiclearning.com emails to your Gmail
- **Setup**:
  1. Namecheap Dashboard → Email Forwarding
  2. Create: contact@cozmiclearning.com → forwards to → yourpersonal@gmail.com
  3. You can reply from Gmail (will show your Gmail address)

**My Recommendation**: Start with Email Forwarding (free), upgrade to Google Workspace later if needed

---

### **Subdomain Setup** (Optional)

**Want**: blog.cozmiclearning.com, api.cozmiclearning.com, etc.

**Setup**:
1. Render dashboard → Add custom domain
2. Enter subdomain: `blog.cozmiclearning.com`
3. Get CNAME target from Render
4. Add CNAME record in DNS:
   ```
   Type: CNAME
   Host: blog
   Value: [Render's CNAME target]
   ```

**Use Cases**:
- `blog.cozmiclearning.com` - For blog/content
- `app.cozmiclearning.com` - For the main application
- `api.cozmiclearning.com` - For API server
- `docs.cozmiclearning.com` - For documentation

---

### **Domain Forwarding** (Optional)

**Want**: Automatically redirect www → non-www (or vice versa)

**Good News**: Render does this automatically!

**How it works**:
- If you add both `cozmiclearning.com` and `www.cozmiclearning.com`
- Render automatically redirects one to the other
- Default: Redirects www → non-www
- Professional and good for SEO

---

## COST BREAKDOWN

### **Annual Costs**:

**Domain Name**: $10-15/year
- Namecheap: ~$9-13/year
- Google Domains: ~$12/year
- Renewal usually slightly higher

**Render Hosting**: Already paying (no extra cost for custom domain)

**SSL Certificate**: FREE (Render provides via Let's Encrypt)

**Email** (Optional):
- Email Forwarding: FREE
- Zoho Mail: FREE (5 users)
- Google Workspace: $72/year ($6/month)

**Total Minimum**: $10-15/year (just domain)

---

## TIMELINE

### **Complete Setup Timeline**:

**Day 1 - Hour 1**: Buy domain (5 minutes)
**Day 1 - Hour 1**: Add to Render (5 minutes)
**Day 1 - Hour 1**: Update DNS (10 minutes)
**Day 1 - Hour 2-4**: Wait for DNS propagation
**Day 1 - Hour 4**: Site live on custom domain! ✅
**Day 1 - Hour 4-5**: SSL auto-enables
**Day 1 - Hour 5**: Fully working with HTTPS! 🎉

**Total Active Time**: 20 minutes
**Total Wait Time**: 4-24 hours (usually 4 hours)

---

## FINAL NOTES

### **Important Reminders**:

✅ **Keep domain auto-renew ON** - Don't let domain expire!
✅ **Keep login credentials safe** - Store domain registrar password securely
✅ **Enable 2FA** - On both Render and domain registrar accounts
✅ **Set calendar reminder** - 1 month before domain renewal (check pricing)
✅ **Update all marketing** - Change URLs in ads, social media, emails

### **After Going Live**:

**Update These**:
- [ ] Facebook Ads → New domain URL
- [ ] Instagram bio → New domain
- [ ] Google Ads → New domain
- [ ] Business cards (if you have them)
- [ ] Email signature
- [ ] Social media profiles
- [ ] Any print materials

**Monitor**:
- [ ] Google Analytics (update property URL if you set it up)
- [ ] Google Search Console (add new domain, verify)
- [ ] Facebook Pixel (verify still tracking)
- [ ] Stripe webhooks (update URLs if using webhooks)

---

## QUICK REFERENCE

### **DNS Records Cheat Sheet**:

**For Apex Domain** (cozmiclearning.com):
```
Type: A
Host: @ (or leave blank)
Value: [Render's IP - get from Render dashboard]
TTL: Automatic or 3600
```

**For www Subdomain**:
```
Type: CNAME
Host: www
Value: cozmiclearning-1.onrender.com (or whatever Render gives you)
TTL: Automatic or 3600
```

---

## NEED HELP?

### **Resources**:

**Render Documentation**:
- https://render.com/docs/custom-domains

**Domain Registrar Support**:
- Namecheap: Live chat (24/7)
- Google Domains: support.google.com/domains
- Cloudflare: Community forum or support ticket

**DNS Checker**:
- whatsmydns.net
- dnschecker.org

**SSL Checker**:
- ssllabs.com/ssltest

---

## 🎉 READY TO GO LIVE?

**Your action items**:

**TODAY** (20 minutes):
1. Decide on domain name (cozmiclearning.com?)
2. Buy domain from Namecheap
3. Add domain in Render dashboard
4. Update DNS records at Namecheap
5. Wait

**TOMORROW** (5 minutes):
1. Check if domain is working
2. Verify HTTPS is enabled
3. Test signup flow on new domain
4. Update marketing materials

**You'll go from**:
https://cozmiclearning-1.onrender.com
**to**
https://cozmiclearning.com

**Professional. Memorable. Ready for launch.** 🚀

Want me to walk you through any specific step in more detail?
