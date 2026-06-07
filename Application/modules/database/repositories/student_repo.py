import sqlite3
from typing import Tuple
from modules.database.models import Student

class StudentRepository:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self.conn = db_conn

    def find_unique(self, student_id: str) -> Tuple[Student | None, str | None]:
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
