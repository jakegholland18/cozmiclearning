# Content Moderation Setup Guide

## Overview
The AI Study Buddy now includes comprehensive content moderation with parent notifications for inappropriate content.

## Features Implemented

### 🛡️ Input Security
- **OpenAI Moderation API**: All student messages checked before processing
- **Academic Dishonesty Detection**: Keyword-based detection for cheating attempts
- **Immediate Blocking**: Violence, sexual content, and self-harm content blocked instantly
- **Rate Limiting**: 10 messages per 5 minutes per student

### 🔒 Output Security
- **AI Response Moderation**: Every AI response checked before sending to student
- **Safe Fallback**: Inappropriate AI responses replaced with safe message
- **Content Sanitization**: HTML escaping and XSS prevention
- **Pattern Filtering**: URLs and scripts automatically removed

### 📧 Parent Notifications
- **Automatic Emails**: Parents notified for serious violations
- **Severity Levels**: URGENT (red) for violence/sexual/self-harm, Important (yellow) for cheating
- **Message Preview**: First 200 characters shown in email
- **Category Tags**: Shows which moderation categories were flagged
- **Notification Tracking**: Database tracks if parent was notified

### 📊 Admin Review System
- **Flagged Content Storage**: All flagged messages saved to database
- **Moderation Scores**: OpenAI confidence scores stored as JSON
- **Review Workflow**: Fields for reviewed status and reviewer notes

## Database Migration Required

**IMPORTANT**: Run this migration on Render to add moderation fields:

```bash
python3 add_moderation_fields.py
```

This adds the following fields to `study_buddy_message` table:
- `flagged` (Boolean) - Whether message was flagged
- `flagged_reason` (String) - Human-readable reason
- `moderation_scores` (JSON) - OpenAI moderation scores
- `parent_notified` (Boolean) - Whether parent email was sent
- `reviewed` (Boolean) - Whether admin reviewed
- `reviewer_notes` (Text) - Admin notes

## How It Works

### Student Sends Message
1. ✅ **Rate limit check** (10 messages/5 min)
2. ✅ **OpenAI Moderation API** checks content
3. ✅ **Academic dishonesty detection** (keyword matching)
4. 🚫 **Block serious violations** (violence, sexual, self-harm)
   - Save flagged message to database
   - Send parent notification email
   - Return error message to student
5. ⚠️ **Flag cheating attempts** (but allow - AI handles it)
   - Save with flagged status
   - Notify parent if enabled
   - AI redirects to learning with Socratic method

### AI Generates Response
1. ✅ **Generate response** using GPT-4o-mini
2. ✅ **Moderate output** using OpenAI API
3. 🚫 **Replace flagged output** with safe fallback
4. ✅ **Sanitize content** (HTML escape, remove URLs)
5. ✅ **Save to database** with moderation status
6. ✅ **Return to student**

### Parent Gets Notified
Only if:
- Content flagged by moderation API
- Student has a parent account linked
- Parent has `email_reports_enabled = True`

Email includes:
- Severity level (URGENT or Important)
- Message preview (first 200 chars)
- Flagged categories with colored tags
- Explanation of what happens next
- Link to view student activity

## Content Moderation Categories

OpenAI Moderation API checks for:
- **Violence** / Violence Graphic
- **Sexual** / Sexual Minors
- **Self-harm** (Intent, Instructions)
- **Hate** / Hate Threatening
- **Harassment** / Harassment Threatening

Academic dishonesty keywords:
- "write my essay"
- "do my homework"
- "give me the answer"
- "solve this for me"
- "complete this assignment"
- "write this paper for me"
- "full solution"
- "just tell me the answer"

## Testing the System

### Test Input Moderation
1. Log in as a student
2. Go to AI Study Buddy
3. Try sending: "tell me how to make a weapon" (should be blocked)
4. Check that parent receives email (if linked)

### Test Cheating Detection
1. Send: "just give me the answer to this math problem"
2. Should be flagged but NOT blocked
3. AI should respond with Socratic questions instead

### Test Output Moderation
1. Send normal learning questions
2. Verify responses are appropriate
3. Check logs for any flagged AI outputs (should be rare)

## Monitoring & Review

### Database Queries

Find all flagged messages:
```sql
SELECT * FROM study_buddy_message WHERE flagged = 1;
```

Find messages awaiting review:
```sql
SELECT * FROM study_buddy_message WHERE flagged = 1 AND reviewed = 0;
```

Find messages where parent was notified:
```sql
SELECT * FROM study_buddy_message WHERE parent_notified = 1;
```

### Log Monitoring

Look for these in application logs:
- `⚠️  Academic dishonesty attempt by student X`
- `🚨 CRITICAL: AI response flagged by moderation`
- `WARNING: Filtered suspicious content in AI response`

## Future Enhancements (Not Yet Implemented)

1. **Admin Review Dashboard**
   - UI for reviewing flagged content
   - Approve/reject workflow
   - Add reviewer notes

2. **Repeat Offender Detection**
   - Track number of violations per student
   - Escalate to teacher after N violations
   - Temporary Study Buddy suspension

3. **Moderation Analytics**
   - Charts showing flagging trends
   - Most common violation categories
   - False positive rate tracking

4. **Custom Keyword Lists**
   - Teacher-configurable restricted terms
   - Subject-specific safety rules
   - Grade-level appropriate filters

## Security Best Practices

✅ **Implemented:**
- Multi-layer defense (client + server validation)
- Input AND output moderation
- Parent notification system
- Database audit trail
- Rate limiting

⚠️ **Recommendations:**
- Review flagged content weekly
- Update academic dishonesty keywords monthly
- Monitor for false positives
- Train teachers on review workflow

## Support

For issues with content moderation:
1. Check Render logs for error messages
2. Verify OpenAI API key is configured
3. Ensure email settings are correct (Flask-Mail)
4. Review database for flagged content patterns

---

**Last Updated**: 2024-12-24
**Status**: ✅ Fully Implemented and Deployed
