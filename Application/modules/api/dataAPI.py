import logging
import sqlite3
from datetime import datetime
from modules.database.models import Student, Faculty, Attendance
from modules.database.services import StudentService, FacultyService, AttendanceService
from modules.database.config_service import verify_admin_password

class DataAPI:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self._studentService = StudentService(db_conn)
        self._facultyService = FacultyService(db_conn)
        self._attendanceService = AttendanceService(db_conn)

        self.minutes = 10 # temporary minutes variable
    
    def find_unique(self, id: str) -> tuple[Student | Faculty | None, str | None] | None:
        user, user_type = self._studentService.find_unique(id)
        if user is not None:
            return user, user_type
        
        user, user_type = self._facultyService.find_unique(id)
        return user, user_type
    
    def register_scan(self, user_id: str, user_type: str) -> dict | None:
        """Processes scanning events. It resolves if action must be Check-In or Check-Out"""
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            today_date = datetime.now().strftime("%Y-%m-%d")

            # Find the current active log where log out is null
            recordId = self._attendanceService.get_active_scan_today(user_id, today_date)
            
            # If recordId is None, try to find the previous log 
            # and check if the current log is within X minutes as the previous log out
            recordId = self._attendanceService.get_active_scan_within_window(user_id, current_time, self.minutes)

            # recordId is still None. Thus, log brand new entry as Check-In
            if recordId is None:
                self._attendanceService.check_in(user_id, user_type, current_time)
                return {"action": "check_in", "timestamp": current_time}
            
            # Otherwise, update open track to Check-Out
            else:
                self._attendanceService.check_out(recordId, current_time)
                return {"action": "check_out", "timestamp": current_time}

        except Exception:
            logging.exception(f"Attendance writing error occurred targeting target user: {user_id}")
            return None
        
    def create_user(self, user_id: str, first_name: str, last_name: str, sex: str, user_type: str, batch: str = None) -> bool:
        try:
            if user_type == "student":
                user = Student(user_id, first_name, last_name, batch, sex)
                self._studentService.create(user)
                return True

            elif user_type == "faculty":
                user = Faculty(user_id, first_name, last_name, sex)
                self._facultyService.create(user)
                return True
            
            return False
        except Exception:
            logging.exception(f"Failed writing new profile data for: {user_id}")
            return False
        
    def _verify_admin(self, input_pw: str):
        return verify_admin_password(input_pw)
    
    def _get_sensitive_data(self):
        ...
