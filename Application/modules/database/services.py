import logging
from datetime import datetime
from database.connection import get_db
import sqlite3
from database.models import Student, Faculty, Attendance

class StudentService:
    def __init__(self, db_connection: sqlite3.Connection) -> None:
        self.db = db_connection

    def find_unique(self, student_id: str) -> Student | None:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM student WHERE id = ?", (student_id,))
        row = cursor.fetchone()

        return Student(**dict(row)) if row is not None else None
    
    def create(self, student: Student) -> None:
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO student (id, first_name, last_name, batch, sex) VALUES (?, ?, ?, ?, ?)",
            (student.id, student.first_name, student.last_name, student.batch, student.sex)
        )
        self.db.commit()


class FacultyService:
    def __init__(self, db_connection: sqlite3.Connection) -> None:
        self.db = db_connection

    def find_unique(self, faculty_id: str) -> Faculty | None:
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM faculty WHERE id = ?", (faculty_id,))
        row = cursor.fetchone()
        return Faculty(**dict(row)) if row is not None else None
    
    def create(self, faculty: Faculty) -> None:
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO faculty (id, first_name, last_name, sex) VALUES (?, ?, ?, ?)",
            (faculty.id, faculty.first_name, faculty.last_name, faculty.sex)
        )
        self.db.commit()


class AttendanceService:
    def __init__(self, db_connection: sqlite3.Connection) -> None:
        self.db = db_connection

    def get_active_scan_today(self, user_id: str, today_date: str) -> int | None:
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT id FROM attendance
            WHERE user_id = ? AND time_in LIKE ? AND time_out IS NULL
            ORDER BY id DESC LIMIT 1
        """, (user_id, f"{today_date}%"))
        row = cursor.fetchone()
        return row["id"] if row is not None else None
    
    def check_in(self, user_id: str, user_type: str, current_time: str) -> None:
        cursor = self.db.cursor()
        cursor.execute(
            "INSERT INTO attendance (user_id, user_type, time_in) VALUES (?, ?, ?)",
            (user_id, user_type, current_time)
        )
        self.db.commit()

    def check_out(self, record_id: int, current_time: str) -> None:
        cursor = self.db.cursor()
        cursor.execute(
            "UPDATE attendance SET time_out = ? WHERE id = ?",
            (current_time, record_id)
        )
        self.db.commit()