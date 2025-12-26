#!/usr/bin/env python3
"""
Create your first admin user account.

This script creates a new admin user with a secure hashed password.
Run this after adding the admins table to create your first admin account.
"""

import os
import getpass
os.environ['SKIP_STRIPE_CHECK'] = '1'

from app import app, db
from models import Admin
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        print("=" * 60)
        print("🔧 Create First Admin User")
        print("=" * 60)

        # Check if any admins exist
        existing_admins = Admin.query.count()
        if existing_admins > 0:
            print(f"\n⚠️  {existing_admins} admin(s) already exist in the database.")
            response = input("Do you want to create another admin? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("Cancelled.")
                return

        print("\nEnter details for the new admin account:")
        print("(This admin will have full system access)")

        # Get admin details
        username = input("\nUsername: ").strip()
        if not username:
            print("❌ Username is required")
            return

        # Check if username already exists
        if Admin.query.filter_by(username=username).first():
            print(f"❌ Username '{username}' already exists")
            return

        email = input("Email: ").strip()
        if not email:
            print("❌ Email is required")
            return

        # Check if email already exists
        if Admin.query.filter_by(email=email).first():
            print(f"❌ Email '{email}' already exists")
            return

        full_name = input("Full Name (optional): ").strip()

        # Get password securely
        while True:
            password = getpass.getpass("Password (will be hidden): ")
            if len(password) < 8:
                print("❌ Password must be at least 8 characters long")
                continue

            password_confirm = getpass.getpass("Confirm Password: ")
            if password != password_confirm:
                print("❌ Passwords don't match. Try again.")
                continue

            break

        # Ask if super admin (only for first admin or by confirmation)
        is_super_admin = False
        if existing_admins == 0:
            print("\nThis will be the first admin account (Super Admin by default)")
            is_super_admin = True
        else:
            response = input("\nMake this a Super Admin? (can manage other admins) (yes/no): ").strip().lower()
            is_super_admin = response in ['yes', 'y']

        try:
            # Create admin user
            admin = Admin(
                username=username,
                email=email,
                full_name=full_name if full_name else None,
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
            print("\n💡 You can now login at:")
            print("   /secret_admin_login")
            print("\n🔒 Security features enabled:")
            print("   - Password is securely hashed")
            print("   - Account locks after 5 failed attempts")
            print("   - Login attempts are tracked")
            print("=" * 60)

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error creating admin: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_admin()
