from typing import List, Dict, Any

from core.exceptions import BadRequestException, UserNotRegisteredException

from modules.attendance.attendance_service import AttendanceService
from modules.attendance.attendance_models import ProcessedAttendanceResult

class AttendanceController:
    def __init__(self, attendance_service: AttendanceService) -> None:
        self._service = attendance_service

    # Public
    def get_today_attendance(self) -> Dict[str, Any]:
        """This endpoint returns a list of entries within today"""
        try:
            today_attendance = self._service.get_today_attendance()
            return {
                "status": "success",
                "message": "Today logs successfully retrieved.",
                "data": {
                    "today_attendance": today_attendance
                }
            }
        
        except Exception as e:
            return {"status": "error", "message": f"Error occured while retrieving today logs: {e}"}
    
    # Public
    def processScannedCode(self, qr_data: str) -> Dict[str, Any]:
        """This endpoint processes the scanned QR Code"""

        try:
            result = self._service.processCode(qr_data=qr_data)
            return {
                "status": "success",
                "message": "QR Code processed succesfully.",
                "action": result.action,
                "timestamp": result.timestamp
            }

        except UserNotRegisteredException as e:
            return {
                "status": e.status,
                "message": e.message,
                "meta": e.meta 
            }
        
        except BadRequestException as e:
            return {
                "status": e.status,
                "message": e.message
            }
        
        except Exception as e:
            return {"status": "error", "message": "An unexpected system error occured."}