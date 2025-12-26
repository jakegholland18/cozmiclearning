#!/usr/bin/env python3
"""
Simple admin creator - pass credentials as arguments.

Usage:
    python create_admin_simple.py <username> <email> <password> "<full_name>"

Example:
    python create_admin_simple.py jake jake@example.com MyPass123 "Jake Holland"
"""

import os
import sys
os.environ['SKIP_STRIPE_CHECK'] = '1'

from app import app, db
from models import Admin
from werkzeug.security import generate_password_hash

def create_admin():
    if len(sys.argv) < 4:
        print("Usage: python create_admin_simple.py <username> <email> <password> [full_name]")
        print("Example: python create_admin_simple.py admin admin@example.com MyPass123 'Admin User'")
        return

    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    full_name = sys.argv[4] if len(sys.argv) > 4 else None

    with app.app_context():
        print("=" * 60)
        print("🔧 Creating Admin User")
        print("=" * 60)

        # Check if username already exists
        if Admin.query.filter_by(username=username).first():
            print(f"❌ Username '{username}' already exists")
            return

        # Check if email already exists
        if Admin.query.filter_by(email=email).first():
            print(f"❌ Email '{email}' already exists")
            return

        # Check if this is first admin
        existing_admins = Admin.query.count()
        is_super_admin = (existing_admins == 0)

        try:
            # Create admin user
            admin = Admin(
                username=username,
                email=email,
                full_name=full_name,
                password_hash=generate_password_hash(password),
                is_super_admin=is_super_admin,
                is_active=True
            )

            db.session.add(admin)
            db.session.commit()

            print("\n" + "=" * 60)
            print("✅ Admin account created successfully!")
            print("=" * 60)
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Full Name: {full_name or '(not set)'}")
            print(f"Super Admin: {'Yes' if is_super_admin else 'No'}")
            print("\n💡 Login at: /secret_admin_login")
            print("=" * 60)

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error creating admin: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_admin()
