# Phase 1 Testing Guide
**Date:** 2025-12-07
**Site:** https://cozmiclearning-1.onrender.com

---

## 🎯 **What Phase 1 Fixed**

1. ✅ Environment variable validation (prevents bad deploys)
2. ✅ Session key safety (no more KeyError crashes)
3. ✅ Database migrations (arcade columns auto-added)
4. ✅ Parent model fix (subscription_tier → plan)

---

## ⚡ **Quick Tests (5-10 Minutes)**

### **Test 1: Homepage Loads**
- [ ] Visit https://cozmiclearning-1.onrender.com
- [ ] Page loads without errors
- [ ] No "Houston, We Have a Problem" error page

**Expected:** Homepage displays correctly

---

### **Test 2: Student Login & Dashboard**
- [ ] Click "Student Login" or visit https://cozmiclearning-1.onrender.com/student/login
- [ ] Login with existing student account (or create new one)
- [ ] Dashboard loads successfully
- [ ] See XP, tokens, level displayed
- [ ] No crashes when viewing stats

**Expected:** Dashboard shows student info without crashes

**Tests Phase 1 Fix:** Session variables use safe `.get()` - won't crash if session incomplete

---

### **Test 3: Ask a Question**
- [ ] From student dashboard, click on any subject
- [ ] Type a question (e.g., "What is photosynthesis?")
- [ ] Click submit
- [ ] AI response appears
- [ ] XP and tokens increase

**Expected:** Question answered, XP/tokens update correctly

**Tests Phase 1 Fix:** Session XP/token updates use safe assignment patterns

---

### **Test 4: Play Arcade Game**
- [ ] Click "Arcade" from student dashboard
- [ ] Select any game (e.g., Speed Math)
- [ ] Choose difficulty (easy/medium/hard)
- [ ] Play through a few questions
- [ ] Complete the game
- [ ] See results screen with score

**Expected:** Game works, results display, no database column errors

**Tests Phase 1 Fix:** Arcade columns (difficulty, game_mode) exist in database

---

### **Test 5: Admin Mode**
- [ ] Visit https://cozmiclearning-1.onrender.com/secret_admin_login
- [ ] Enter admin password (check your ADMIN_PASSWORD env var, or try default)
- [ ] Should redirect to admin dashboard
- [ ] Try switching views (Student/Parent/Teacher/Homeschool)
- [ ] Verify you can access each view

**Expected:** Admin login works, view switching works, admin powers preserved

**Tests Phase 1 Fix:** Admin session handling, no KeyError crashes

---

## 📋 **Detailed Tests (20-30 Minutes)**

### **Test 6: Parent Account**
- [ ] Logout from student account
- [ ] Visit https://cozmiclearning-1.onrender.com/parent/login
- [ ] Login as parent (or create new parent account)
- [ ] Parent dashboard loads
- [ ] Click "My Students"
- [ ] Click "Lesson Plans"
- [ ] Click "Analytics"
- [ ] No 404 errors on any page

**Expected:** All parent pages load without 404 errors

**Tests Phase 1 Fix:** Parent sidebar links fixed (no more /parent/progress 404)

---

### **Test 7: Teacher Account**
- [ ] Logout
- [ ] Visit https://cozmiclearning-1.onrender.com/teacher/login
- [ ] Login as teacher (or create new account)
- [ ] Teacher dashboard loads
- [ ] Try creating a class
- [ ] Try creating an assignment
- [ ] View class roster

**Expected:** Teacher features work, no crashes

---

### **Test 8: Session Persistence**
- [ ] Login as student
- [ ] Navigate to different pages (subjects, arcade, profile)
- [ ] Open site in new tab
- [ ] Verify still logged in
- [ ] Close browser completely
- [ ] Reopen and visit site
- [ ] Should still be logged in (7-day session)

**Expected:** Sessions persist across tabs and browser restarts

**Tests Phase 1 Fix:** Session handling is robust

---

### **Test 9: Clear Session (Stress Test)**
- [ ] Login as student
- [ ] Open browser developer tools (F12)
- [ ] Go to "Application" tab → "Cookies"
- [ ] Delete all cookies for cozmiclearning-1.onrender.com
- [ ] Try navigating to dashboard
- [ ] Should redirect to login (not crash)

**Expected:** Graceful redirect to login, no crash

**Tests Phase 1 Fix:** Session.get() handles missing session gracefully

---

### **Test 10: Multiple Account Types**
- [ ] Login as student in one browser (e.g., Chrome)
- [ ] Login as parent in another browser (e.g., Firefox)
- [ ] Login as teacher in incognito window
- [ ] All should work simultaneously without conflicts

**Expected:** Multiple user types can use site at same time

---

## 🚨 **Error Scenarios to Test**

### **Test 11: Invalid Login**
- [ ] Try logging in with wrong password
- [ ] Should see error message
- [ ] Try logging in with non-existent email
- [ ] Should see error message
- [ ] No crashes, just clear error messages

**Expected:** Clear error messages, no crashes

---

### **Test 12: Database Edge Cases**
- [ ] Create a new student account
- [ ] Ask 10 questions rapidly
- [ ] Play 3 arcade games back-to-back
- [ ] No database lock errors
- [ ] No "database is locked" messages

**Expected:** Multiple operations succeed without database errors

**Tests Phase 1 Fix:** While safe_commit() not widely used yet, basic operations should work

---

## 📊 **What to Look For**

### **✅ Good Signs:**
- Pages load quickly
- No "Houston, We Have a Problem" errors
- No blank pages
- XP and tokens update correctly
- Session persists across page loads
- Error messages are clear and helpful

### **🚨 Red Flags:**
- Blank pages or 500 errors
- "KeyError" in browser console
- "NoneType has no attribute" errors
- Session logs you out randomly
- Database lock errors
- Arcade games fail to load

---

## 🔍 **Where to Check for Errors**

### **In Browser:**
1. Open Developer Tools (F12)
2. Check "Console" tab for JavaScript errors
3. Check "Network" tab for failed API calls (red entries)

### **In Render Dashboard:**
1. Go to https://dashboard.render.com
2. Click your service → "Logs" tab
3. Look for red error messages
4. Watch for patterns (same error repeating)

### **Common Error Patterns:**

**Before Phase 1 (Should NOT see these anymore):**
```
KeyError: 'character'
KeyError: 'xp'
AttributeError: 'NoneType' object has no attribute 'email'
no such column: game_sessions.game_mode
```

**After Phase 1 (Should see these instead):**
```
✅ All required environment variables are set
✅ Added column game_sessions.game_mode
✅ Database OK - all required columns exist
```

---

## 📝 **Testing Checklist**

### **Critical (Must Test):**
- [ ] Homepage loads
- [ ] Student login works
- [ ] Ask a question (OpenAI API)
- [ ] Play arcade game (database columns)
- [ ] Admin login works

### **Important (Should Test):**
- [ ] Parent dashboard
- [ ] Teacher dashboard
- [ ] Session persistence
- [ ] Multiple users simultaneously
- [ ] Clear session doesn't crash

### **Optional (Nice to Test):**
- [ ] Signup flow
- [ ] Password reset
- [ ] Profile updates
- [ ] Practice missions
- [ ] PowerGrid study guides

---

## 🎯 **Success Criteria**

Phase 1 is successful if:

1. ✅ **No crashes** when navigating the site
2. ✅ **No KeyError** or session-related errors
3. ✅ **Arcade games work** (columns exist)
4. ✅ **Admin mode works** (no login issues)
5. ✅ **Sessions persist** across page loads
6. ✅ **Error messages are clear** (not blank pages)

---

## 📊 **Report Template**

After testing, note:

### **What Worked:**
- Homepage: ✅
- Student login: ✅
- Questions: ✅
- Arcade: ✅
- Admin: ✅

### **What Had Issues:**
- [List any errors or problems]

### **Browser Console Errors:**
- [Any JavaScript errors]

### **Render Log Errors:**
- [Any Python/server errors]

---

## ⏱️ **Testing Time Estimates**

- **Quick Tests (1-5):** 5-10 minutes
- **Detailed Tests (6-10):** 20-30 minutes
- **Error Scenarios (11-12):** 10 minutes
- **Total:** 35-50 minutes for comprehensive testing

---

## 🚀 **After Testing**

### **If Everything Works:**
- ✅ Phase 1 is successful!
- ✅ Let it run in production for 24-48 hours
- ✅ Monitor logs for any new errors
- ✅ Then consider Phase 2

### **If You Find Issues:**
- 🐛 Note the specific error
- 📋 Share the error message or screenshot
- 🔍 Check Render logs for details
- 💬 Let me know and I'll fix it immediately

---

## 💡 **Tips**

1. **Test in order** - Quick tests first, then detailed
2. **Use different browsers** - Chrome, Firefox, Safari
3. **Test on mobile** - Responsive design should work
4. **Don't rush** - Take time to click around
5. **Check logs** - Errors might not show in UI
6. **Try edge cases** - Rapid clicks, long inputs, etc.

---

## 📞 **Need Help?**

If you encounter any errors during testing:
1. Take a screenshot
2. Copy the error message from browser console
3. Copy error from Render logs
4. Share with me - I'll fix immediately!

---

**Last Updated:** 2025-12-07
**Status:** Ready for Testing
