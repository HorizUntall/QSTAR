import logging
import sqlite3
from datetime import datetime
from typing import Tuple, Dict, Any

from modules.database.models import Student, Faculty, Attendance, DashboardFilters
from modules.database.services.studentService import StudentService
from modules.database.services.facultyService import FacultyService
from modules.database.services.attendanceService import AttendanceService
from modules.database.services.dashboardService import DashboardService
from modules.database.services.config_service import verify_admin_password

class DataAPI:
    def __init__(self, db_conn: sqlite3.Connection) -> None:
        self._studentService = StudentService(db_conn)
        self._facultyService = FacultyService(db_conn)
        self._attendanceService = AttendanceService(db_conn)
        self._dashboardService = DashboardService(db_conn)

        self.minutes = 10 # temporary minutes variable
    
    # Public
    def find_unique(self, id: str) -> Tuple[Student | Faculty | None, str | None] | None:
        """Returns the user details if user exists in the database"""
        user, user_type = self._studentService.find_unique(id)
        if user is not None:
            return user, user_type
        
        user, user_type = self._facultyService.find_unique(id)
        return user, user_type
    
    # Public
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

    # Public 
    def create_user(self, user_id: str, first_name: str, last_name: str, sex: str, user_type: str, batch: str = None) -> bool:
        """Creates a new user (Faculty/Student)"""
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

    # Private 
    def _verify_admin(self, input_pw: str) -> bool:
        return verify_admin_password(input_pw)
    
    # Private
    def _get_processed_dashboard_data(self, filters: DashboardFilters, topUsersLimit: int = 5, num_batches: int = 6) -> Dict[str, Any]:
        """Returns processed dashboard data using the filters"""

        return {
            "visits_vs_time": self._dashboardService.get_library_visits_vs_time(filters=filters),
            "top_goers": self._dashboardService.get_top_library_goers(filters=filters, limit=topUsersLimit),
            "batch_visits": self._dashboardService.get_visits_per_batch(filters=filters, num_batches=num_batches),
            "gender": self._dashboardService.get_gender_development(filters=filters),
            "kpis": self._dashboardService.get_kpis(filters=filters)   
        }
    
    # Private
    def _get_processed_attendance_history(self, filters: DashboardFilters, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """Returns processed attendance history using the filters"""

        return self._dashboardService.get_attendance_history(filters=filters, page=page, page_size=page_size)
    
    # Private
    def _get_processed_registered_users(self, filters: DashboardFilters, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
        """Returns processed registerd users list using the filters"""

        return self._dashboardService.get_registered_users(filters=filters, page=page, page_size=page_size)