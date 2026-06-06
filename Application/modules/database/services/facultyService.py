import sqlite3
from modules.database.models import Faculty

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