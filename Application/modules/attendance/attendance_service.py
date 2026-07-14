from typing import Dict, Any, Tuple
from datetime import datetime, timedelta

# from modules.shared.code_validate_and_parse import validate_and_parse
from core.exceptions import NotFoundException, UserNotRegisteredException
from core.shared.constants import UserTypeEnum

from modules.identity.qr_parser import ParsedQR, validate_and_parse

from modules.student.student_models import StudentDTO
from modules.student.student_repo import StudentRepository

from modules.faculty.faculty_models import FacultyDTO
from modules.faculty.faculty_repo import FacultyRepository

from modules.attendance.attendance_models import ProcessedAttendanceResult
from modules.attendance.attendance_repo import AttendanceRepository

import logging
from threading import Thread

logger = logging.getLogger()

class AttendanceService:
    def __init__(self, attendance_repo: AttendanceRepository, student_repo: StudentRepository, faculty_repo: FacultyRepository) -> None:
        self.attendance_repo = attendance_repo
        self.student_repo = student_repo
        self.faculty_repo = faculty_repo

        self.cutoff_time = 10 # temporary minutes available

    # def verify_and_process_qr(self, qr_data: str) -> Dict[str, Any]: 
    #     parsed = validate_and_parse(qr_data=qr_data)

    #     if not parsed["is_valid"]:
    #         return {"status": "invalid", "message": f"Scan Rejected: {parsed['reason']}"}
        
    #     user: StudentDTO | FacultyDTO | None
    #     scanned_id: str = parsed["id"]
    #     user_type: str = parsed["user_type"]

    #     if user_type == "student":
    #         user = self.student_repo.find_unique(scanned_id)
    #     else:
    #         user = self.faculty_repo.find_unique(scanned_id)

    #     if not user:
    #         return {
    #             "status": "not_found",
    #             "id": scanned_id,
    #             "user_type": user_type,
    #         }
        
    #     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     today_date = datetime.now().strftime("%Y-%m-%d")

    #     # Find the current active log where log out is null
    #     recordId = self.attendance_repo.find_active_in_record(user_id=user.id, date_prefix=today_date)
    #     if recordId is not None:
    #         self.attendance_repo.update_time_out(record_id=recordId, time_out=current_time)
    #         return {"status": "success", "action": "check_out", "timestamp": current_time}

    #     # If recordId is None, try to find the previous log
    #     # and check if the current log is within X minutes as the previous log out.
    #     # This will overwrite the previous logout
    #     recordId = self.attendance_repo.find_recent_out_record(user_id=user.id, cutoff_time=self.cutoff_time)
    #     if recordId is not None:
    #         self.attendance_repo.update_time_out(record_id=recordId, time_out=None)
    #         return {"status": "success", "action": "overwrite_checkout"}


    #     # If recordId is still None, then log a brand new entry as Check-In
    #     self.attendance_repo.insert_time_in(user_id=user.id, user_type=user_type, time_in=current_time)
    #     return {"status": "success", "action": "check_in", "timestamp": current_time}

    def processCode(self, qr_data: str) -> ProcessedAttendanceResult:
        parsed = validate_and_parse(qr_data=qr_data)

        user: StudentDTO | FacultyDTO | None
        scanned_id: str = parsed.id
        user_type: str = parsed.user_type

        if user_type == UserTypeEnum.STUDENT.value:
            user = self.student_repo.find_unique(scanned_id)
        else:
            user = self.faculty_repo.find_unique(scanned_id)

        if user is None:
            raise UserNotRegisteredException(
                message ="User ID not found",
                meta = {
                    "data": {
                        "id": parsed.id,
                        "user_type": parsed.user_type
                    }
                }
            )
        
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        today_date = now.strftime("%Y-%m-%d")
        
        # Find the current active log where log out is null
        recordId = self.attendance_repo.find_active_in_record(user_id=user.id, date_prefix=today_date)
        if recordId is not None:
            self.attendance_repo.update_time_out(record_id=recordId, time_out=current_time)
            return ProcessedAttendanceResult(action="check_out", timestamp=current_time)
        
        # If recordId is None, try to find the previous log
        # and check if the current log is within X minutes as the previous log out.
        # This will overwrite the previous logout

        cutoff_dt = now - timedelta(minutes=self.cutoff_time)
        dynamic_cutoff = cutoff_dt.strftime("%Y-%m-%d %H:%M:%S")

        recordId = self.attendance_repo.find_recent_out_record(user_id=user.id, cutoff_time=dynamic_cutoff)
        if recordId is not None:
            self.attendance_repo.update_time_out(record_id=recordId, time_out=None)
            return ProcessedAttendanceResult(action="overwrite_checkout")
        
        # If recordId is still None, then log a brand new entry as Check-In
        self.attendance_repo.insert_time_in(user_id=user.id, user_type=user_type, time_in=current_time)
        return ProcessedAttendanceResult(action="check_in")
        
    def get_today_attendance(self) -> list[Dict[str, Any]]:
        return self.attendance_repo.get_today_attendance()

    def run_stale_records_cleanup(self) -> None:
        """Spawns an isolated background worker thread to process daily auto-timeouts."""
        def worker():
            try:
                logger.info("AttendanceService: Executing system maintenance database check...")
                count = self.attendance_repo.auto_timeout_previous_days()
                if count > 0:
                    logger.info(f"AttendanceService: Force closed {count} stale active records from previous days at 17:00:00.")
            except Exception as err:
                logger.error(f"AttendanceService Lifecycle Error: Maintenance execution thread failed: {err}")

        # Execute as a daemon process so it instantly yields control if the UI window is killed
        maintenance_worker = Thread(target=worker, daemon=True)
        maintenance_worker.start()