import logging
from datetime import datetime, timedelta
from modules.database.connection import get_db
import sqlite3
from modules.database.models import Student, Faculty, Attendance

class StudentService:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self.conn = db_conn

    def find_unique(self, student_id: str) -> tuple[Student | None, str | None]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM student WHERE id = ?", (student_id,))
        row = cursor.fetchone()

        return (Student(**dict(row)), "student") if row is not None else (None, None)
    
    def create(self, student: Student) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO student (id, first_name, last_name, batch, sex) VALUES (?, ?, ?, ?, ?)",
            (student.id, student.first_name, student.last_name, student.batch, student.sex)
        )
        self.conn.commit()


class FacultyService:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self.conn = db_conn

    def find_unique(self, faculty_id: str) -> tuple[Faculty | None, str | None]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM faculty WHERE id = ?", (faculty_id,))
        row = cursor.fetchone()
        return (Faculty(**dict(row)), "faculty") if row is not None else (None, None)
    
    def create(self, faculty: Faculty) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO faculty (id, first_name, last_name, sex) VALUES (?, ?, ?, ?)",
            (faculty.id, faculty.first_name, faculty.last_name, faculty.sex)
        )
        self.conn.commit()


class AttendanceService:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self.conn = db_conn

    def get_active_scan_today(self, user_id: str, today_date: str,) -> int | None:
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id FROM attendance
            WHERE user_id = ? AND time_in LIKE ? AND time_out IS NULL
            ORDER BY id DESC LIMIT 1
        """, (user_id, f"{today_date}%"))
        row = cursor.fetchone()
        return row["id"] if row is not None else None
    
    def get_active_scan_within_window(self, user_id: str, current_time: str, minutes: int = 10) -> int | None:
        time_format = "%Y-%m-%d %H:%M:%S"

        # Convert the passed current time string back to a datetime object to do math
        current_dt = datetime.strptime(current_time, time_format)

        # Calculate the cutoff time based on the passed time
        cutoff_time = (current_dt - timedelta(minutes=minutes)).strftime(time_format)
        
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
    
    def check_in(self, user_id: str, user_type: str, current_time) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO attendance (user_id, user_type, time_in) VALUES (?, ?, ?)",
            (user_id, user_type, current_time)
        )
        self.conn.commit()

    def check_out(self, record_id: int, current_time: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE attendance SET time_out = ? WHERE id = ?",
            (current_time, record_id)
        )
        self.conn.commit()