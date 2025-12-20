-- Database Migration: Add Security Columns to All User Tables
-- Adds failed_login_attempts and account_locked_until to students, teachers, AND parents tables
-- Compatible with PostgreSQL

-- Add security columns to STUDENTS table
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'students' AND column_name = 'failed_login_attempts'
    ) THEN
        ALTER TABLE students ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;
        RAISE NOTICE 'Added failed_login_attempts column to students';
    ELSE
        RAISE NOTICE 'students.failed_login_attempts already exists';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'students' AND column_name = 'account_locked_until'
    ) THEN
        ALTER TABLE students ADD COLUMN account_locked_until TIMESTAMP;
        RAISE NOTICE 'Added account_locked_until column to students';
    ELSE
        RAISE NOTICE 'students.account_locked_until already exists';
    END IF;
END $$;

-- Add security columns to TEACHERS table
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'teachers' AND column_name = 'failed_login_attempts'
    ) THEN
        ALTER TABLE teachers ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;
        RAISE NOTICE 'Added failed_login_attempts column to teachers';
    ELSE
        RAISE NOTICE 'teachers.failed_login_attempts already exists';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'teachers' AND column_name = 'account_locked_until'
    ) THEN
        ALTER TABLE teachers ADD COLUMN account_locked_until TIMESTAMP;
        RAISE NOTICE 'Added account_locked_until column to teachers';
    ELSE
        RAISE NOTICE 'teachers.account_locked_until already exists';
    END IF;
END $$;

-- Add security columns to PARENTS table
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'parents' AND column_name = 'failed_login_attempts'
    ) THEN
        ALTER TABLE parents ADD COLUMN failed_login_attempts INTEGER DEFAULT 0;
        RAISE NOTICE 'Added failed_login_attempts column to parents';
    ELSE
        RAISE NOTICE 'parents.failed_login_attempts already exists';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'parents' AND column_name = 'account_locked_until'
    ) THEN
        ALTER TABLE parents ADD COLUMN account_locked_until TIMESTAMP;
        RAISE NOTICE 'Added account_locked_until column to parents';
    ELSE
        RAISE NOTICE 'parents.account_locked_until already exists';
    END IF;
END $$;

-- Verify columns were added
SELECT 'students' as table_name, column_name, data_type
FROM information_schema.columns
WHERE table_name = 'students'
AND column_name IN ('failed_login_attempts', 'account_locked_until')
UNION ALL
SELECT 'teachers' as table_name, column_name, data_type
FROM information_schema.columns
WHERE table_name = 'teachers'
AND column_name IN ('failed_login_attempts', 'account_locked_until')
UNION ALL
SELECT 'parents' as table_name, column_name, data_type
FROM information_schema.columns
WHERE table_name = 'parents'
AND column_name IN ('failed_login_attempts', 'account_locked_until')
ORDER BY table_name, column_name;
