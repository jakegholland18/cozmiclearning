#!/usr/bin/env python3
"""
Send Weekly Summary Emails
Run this script every Sunday to send weekly progress reports to parents

Usage:
    python3 send_weekly_summaries.py

Or schedule it with cron (every Sunday at 6pm):
    0 18 * * 0 cd /path/to/cozmiclearning && python3 send_weekly_summaries.py
"""

from app import app, mail
from modules.weekly_summary import send_all_weekly_summaries

if __name__ == '__main__':
    with app.app_context():
        print("📧 Sending weekly summary emails to parents...")
        print("=" * 60)

        stats = send_all_weekly_summaries(mail)

        print("\n" + "=" * 60)
        print("📊 Summary Results:")
        print(f"   Total parents: {stats['total']}")
        print(f"   ✅ Sent successfully: {stats['sent']}")
        print(f"   ❌ Failed: {stats['failed']}")
        print("=" * 60)

        if stats['sent'] > 0:
            print(f"\n✨ Successfully sent {stats['sent']} weekly summaries!")
        else:
            print("\n⚠️  No emails were sent. Check parent email preferences.")
