from typing import List, Dict, Any

from modules.attendance.attendance_service import AttendanceService

class AttendanceController:
    def __init__(self, attendance_service: AttendanceService) -> None:
        self._attendance_service = attendance_service

    # Public
    def get_today_attendance(self) -> List[Dict[str, Any]]:
        """This endpoint returns a list of entries within today"""
        return self._attendance_service.get_today_attendance()
    
    # Public
    def processScannedCode(self, qr_data: str) -> Dict[str, Any]:
        """This endpoint processes the scanned QR Code"""

        # If user code exists in the database, returns status="success", action, and timestamp
        # Otherwise, returns status="not_found", id, and user_type

        return self._attendance_service.verify_and_process_qr(qr_data=qr_data)