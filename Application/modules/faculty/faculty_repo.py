import sqlite3
from modules.faculty.faculty_models import FacultyDTO
from typing import List, Dict, Any

class FacultyRepository:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self.conn = db_conn

    def find_unique(self, faculty_id: str) -> FacultyDTO | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM faculty WHERE id = ?", (faculty_id,))
        row = cursor.fetchone()
        return FacultyDTO(**dict(row)) if row is not None else None
    
    def create(self, faculty: FacultyDTO) -> None:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO faculty (id, first_name, last_name, sex) VALUES (?, ?, ?, ?)",
            (faculty.id, faculty.first_name, faculty.last_name, faculty.sex)
        )
        self.conn.commit()

    def get_all(self) -> List[Dict[str, Any]] | None:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM faculty")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    
    def update(self, faculty: FacultyDTO) -> None:
        cursor = self.conn.cursor()
        cursor.execute("UPDATE faculty SET first_name = ?, last_name = ?, sex = ? WHERE id = ?", 
                       (faculty.first_name, faculty.last_name, faculty.sex, faculty.id))
        self.conn.commit()