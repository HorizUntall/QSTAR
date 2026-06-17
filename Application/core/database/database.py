import sqlite3
from pathlib import Path

DB_PATH = Path("C:/QSTAR/Data/attendance.db")

def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None: 
    with get_db() as conn:
        cursor = conn.cursor()

        # Student Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS student (
            id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            batch TEXT NOT NULL,
            sex TEXT NOT NULL 
        )""")

        # Faculty Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS faculty (
            id TEXT PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            sex TEXT NOT NULL
        )""")

        # Attendance Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            user_type TEXT NOT NULL,
            time_in TEXT NOT NULL,
            time_out TEXT
        )""")


        # --- PERFORMANCE INDEXES ---

        # Speeds up date filtering: "Today" queries and custom ranges
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_attendance_time_in
        ON attendance(time_in)
        """)

        # Speeds up table joins and user history lookups
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_attendance_user_id
        ON attendance(user_id, user_type)
        """)

        # Speeds up name-searching and alphabetical sorting for students
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_student_name
        ON student(last_name, first_name)
        """)

        # Speeds up name-searching and alphabetical sorting for faculty
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_faculty_name
        ON faculty(last_name, first_name)
        """)

        conn.commit()