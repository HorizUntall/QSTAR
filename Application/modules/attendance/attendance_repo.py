import sqlite3

class AttendanceRepository:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self.conn = db_conn