import sqlite3

class DataAPI:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self._db_conn = db_conn
    