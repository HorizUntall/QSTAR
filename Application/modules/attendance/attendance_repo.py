import sqlite3
from typing import Dict, Any

class AttendanceRepository:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self.conn = db_conn

    def find_active_in_record(self, user_id: str, date_prefix: str) -> int | None:
        """Finds the latest record where the user timed in today but hasn't timed out."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id FROM attendance
            WHERE user_id = ? AND time_in LIKE ? AND time_out IS NULL
            ORDER BY id DESC LIMIT 1
        """, (user_id, f"{date_prefix}%"))
        row = cursor.fetchone()
        return row["id"] if row is not None else None

    def find_recent_out_record(self, user_id: str, cutoff_time: str) -> int | None:
        """Finds if a user timed out recently after a specific cutoff timestamp."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id FROM attendance
            WHERE user_id = ?
            AND time_out IS NOT NULL
            AND time_out >= ?
            ORDER BY time_out DESC 
            LIMIT 1
        """, (user_id, cutoff_time))
        row = cursor.fetchone()
        return row["id"] if row is not None else None

    def insert_time_in(self, user_id: str, user_type: str, time_in: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO attendance (user_id, user_type, time_in) VALUES (?, ?, ?)",
            (user_id, user_type, time_in)
        )
        self.conn.commit()

    def update_time_out(self, record_id: int, time_out: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE attendance SET time_out = ? WHERE id = ?",
            (time_out, record_id)
        )
        self.conn.commit()

    def get_today_attendance(self) -> list[Dict[str, Any]]:
        query = """
        WITH CombinedUsers AS (
            SELECT id, first_name, last_name, 'student' AS user_type FROM student
            UNION ALL
            SELECT id, first_name, last_name,  'faculty' as user_type FROM faculty
        )
        SELECT 
            u.first_name, u.last_name, a.time_in, a.time_out
        FROM attendance a
        INNER JOIN CombinedUsers u ON a.user_id = u.id AND a.user_type = u.user_type
        WHERE a.time_in >= DATE('now', 'start of day', 'localtime')
            AND a.time_in < DATE('now', 'start of day', '+1 day', '+1 day')
        ORDER BY a.time_in DESC;
        """

        cursor = self.conn.cursor()
        cursor.execute(query)

        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]