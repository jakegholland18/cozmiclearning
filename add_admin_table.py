#!/usr/bin/env python3
"""
Database migration to add admin users table.

This migration:
1. Creates admins table for secure admin authentication
2. Replaces hardcoded ADMIN_PASSWORD with database-backed admin users
3. Supports multiple admin users with hashed passwords
4. Includes security features: account lockout, login tracking

Run this to enable database-based admin authentication.
"""

import os
os.environ['SKIP_STRIPE_CHECK'] = '1'

from app import app, db
from sqlalchemy import text

def add_admin_table():
    with app.app_context():
        print("🔧 Adding admin users table...")

        try:
            # Check database type
            db_url = db.engine.url.drivername
            is_postgres = 'postgresql' in db_url

            print(f"\n📋 Database type: {db_url}")

            with db.engine.connect() as conn:
                if is_postgres:
                    # PostgreSQL version
                    print("\n📋 Creating admins table (PostgreSQL)...")

                    conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS admins (
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(50) UNIQUE NOT NULL,
                            email VARCHAR(120) UNIQUE NOT NULL,
                            password_hash VARCHAR(255) NOT NULL,

                            -- Admin metadata
                            full_name VARCHAR(120),
                            is_active BOOLEAN DEFAULT TRUE,
                            is_super_admin BOOLEAN DEFAULT FALSE,

                            -- Security tracking
                            last_login TIMESTAMP,
                            last_login_ip VARCHAR(45),
                            failed_login_attempts INTEGER DEFAULT 0,
                            locked_until TIMESTAMP,

                            -- Timestamps
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            created_by INTEGER REFERENCES admins(id),
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """))

                else:
                    # SQLite version
                    print("\n📋 Creating admins table (SQLite)...")

                    conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS admins (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username VARCHAR(50) UNIQUE NOT NULL,
                            email VARCHAR(120) UNIQUE NOT NULL,
                            password_hash VARCHAR(255) NOT NULL,

                            -- Admin metadata
                            full_name VARCHAR(120),
                            is_active BOOLEAN DEFAULT 1,
                            is_super_admin BOOLEAN DEFAULT 0,

                            -- Security tracking
                            last_login TIMESTAMP,
                            last_login_ip VARCHAR(45),
                            failed_login_attempts INTEGER DEFAULT 0,
                            locked_until TIMESTAMP,

                            -- Timestamps
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            created_by INTEGER REFERENCES admins(id),
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """))

                print("  ✓ Created admins table")

                # Create indexes
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_admin_email
                    ON admins(email)
                """))
                conn.execute(text("""
                    CREATE INDEX IF NOT EXISTS idx_admin_username
                    ON admins(username)
                """))
                print("  ✓ Created indexes on admins table")

                conn.commit()

            print("\n✅ Admin users table created successfully!")
            print("\n🎉 New features enabled:")
            print("  - Database-backed admin authentication")
            print("  - Multiple admin users support")
            print("  - Secure password hashing")
            print("  - Account lockout after failed attempts")
            print("  - Login tracking and audit trail")
            print("\n💡 Next steps:")
            print("  1. Run: python create_first_admin.py")
            print("  2. Create your first admin account")
            print("  3. Remove ADMIN_PASSWORD from environment variables")

        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    add_admin_table()
