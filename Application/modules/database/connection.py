import sqlite3
from pathlib import Path

DB_PATH = Path("C:/QSTAR/Data/attendance.db")

def get_db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
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

        conn.commit()