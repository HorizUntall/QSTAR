import logging
import sqlite3
from datetime import datetime
from modules.database.models import Student, Faculty, Attendance
from modules.database.services import StudentService, FacultyService, AttendanceService

class DataAPI:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self.studentService = StudentService(db_conn)
        self.facultyService = FacultyService(db_conn)
        self.attendanceService = AttendanceService(db_conn)
    
    def find_unique(self, id: str) -> Student | Faculty | None:
        user = self.studentService.find_unique(id)
        if user is not None:
            return user
        
        user = self.facultyService.find_unique(id)
        return user
    
    def register_scan(self, user_id: str, user_type: str) -> dict | None:
        """Processes scanning events. It resolves if action must be Check-In or Check-Out"""
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            today_date = datetime.now().strftime("%Y-%m-%d")

            recordId = self.attendanceService.get_active_scan_today(user_id, today_date)

            # userId is None. Thus, log brand new entry as Check-In
            if recordId is None:
                self.attendanceService.check_in(user_id, user_type, current_time)
                return {"action": "check_in", "timestamp": current_time}
            
            # Otherwise, update open track to Check-Out
            else:
                self.attendanceService.check_out(recordId, current_time)
                return {"action": "check_out", "timestamp": current_time}

        
        except Exception:
            logging.exception(f"Attendance writing error occurred targeting target user: {user_id}")
            return None