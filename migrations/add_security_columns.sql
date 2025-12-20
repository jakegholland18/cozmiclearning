-- Database Migration: Add Security Columns
-- Adds failed_login_attempts and account_locked_until to students table
-- Compatible with PostgreSQL and SQLite

-- For PostgreSQL:
-- Run with: psql -U username -d database_name -f add_security_columns.sql

-- For SQLite:
-- Run with: sqlite3 persistent_db/cozmiclearning.db < add_security_columns.sql

-- Add failed_login_attempts column (if not exists)
-- PostgreSQL version
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'students' AND column_name = 'failed_login_attempts'
    ) THEN
        ALTER TABLE students ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;
        RAISE NOTICE 'Added failed_login_attempts column';
    ELSE
        RAISE NOTICE 'failed_login_attempts column already exists';
    END IF;
END $$;

-- Add account_locked_until column (if not exists)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'students' AND column_name = 'account_locked_until'
    ) THEN
        ALTER TABLE students ADD COLUMN account_locked_until TIMESTAMP;
        RAISE NOTICE 'Added account_locked_until column';
    ELSE
        RAISE NOTICE 'account_locked_until column already exists';
    END IF;
END $$;

-- SQLite version (uncomment if using SQLite)
-- Note: SQLite doesn't support IF NOT EXISTS for ALTER TABLE
-- Check if columns exist first using: PRAGMA table_info(students);

-- ALTER TABLE students ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;
-- ALTER TABLE students ADD COLUMN account_locked_until TIMESTAMP;
