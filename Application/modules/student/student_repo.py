import sqlite3
from typing import Tuple
from modules.student.student_models import StudentDTO

class StudentRepository:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self.conn = db_conn

    def find_unique(self, student_id: str) -> StudentDTO | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM student WHERE id = ?", (student_id,))
        row = cursor.fetchone()

        return StudentDTO(**dict(row)) if row is not None else None

    def create(self, student: StudentDTO) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO student (id, first_name, last_name, batch, sex) VALUES (?, ?, ?, ?, ?)",
            (student.id, student.first_name, student.last_name, student.batch, student.sex)
        )
        self.conn.commit()

    def update(self, student: StudentDTO) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "UDPATE student SET first_name = ?, last_name = ?, batch = ?, sex = ? WHERE id = ?",
            (student.first_name, student.last_name, student.batch, student.sex, student.id)
        )
        self.conn.commit()