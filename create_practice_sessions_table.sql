-- Migration: Add practice_sessions table for tracking self-practice
-- Created: 2025-12-20

CREATE TABLE IF NOT EXISTS practice_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    subject VARCHAR(50),
    topic VARCHAR(200),
    grade_level VARCHAR(10),
    mode VARCHAR(20),
    total_questions INTEGER,
    questions_answered INTEGER DEFAULT 0,
    questions_correct INTEGER DEFAULT 0,
    score_percent FLOAT,
    time_spent_seconds INTEGER,
    completed BOOLEAN DEFAULT 0,
    practice_data_json TEXT,
    answers_json TEXT,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME,
    FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
);

-- Indices for performance
CREATE INDEX IF NOT EXISTS idx_practice_session_student_id ON practice_sessions (student_id);
CREATE INDEX IF NOT EXISTS idx_practice_session_started_at ON practice_sessions (started_at);
