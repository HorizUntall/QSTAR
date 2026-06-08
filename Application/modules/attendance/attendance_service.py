from typing import Dict, Any, Tuple

from modules.student.student_models import StudentDTO
from modules.student.student_repo import StudentRepository

from modules.faculty.faculty_models import FacultyDTO
from modules.faculty.faculty_repo import FacultyRepository

from modules.attendance.attendance_repo import AttendanceRepository

class AttendanceService:
    def __init__(self, attendance_repo: AttendanceRepository, student_repo: StudentRepository, faculty_repo: FacultyRepository) -> None:
        self.attendance_repo = attendance_repo
        self.student_repo = student_repo
        self.faculty_repo = faculty_repo

    def verify_and_process_qr(self, qr_data: str) -> Dict[str, Any]:
        
        parsed = self.validate_and_parse(qr_data=qr_data)

        if not parsed["is_valid"]:
            return {"status": "invalid", "message": f"Scan Rejected: {parsed["reason"]}"}
        
        user: StudentDTO | FacultyDTO | None
        scanned_id: str = parsed["id"]
        user_type: str = parsed["user_type"]

        if user_type == "student":
            user = self.student_repo.find_unique(scanned_id)
        else:
            user = self.faculty_repo.find_unique(scanned_id)

        if not user:
            return {
                "status": "not_found",
                "id": scanned_id,
                "type": user_type,
            }
        
        

    def validate_and_parse(self, qr_data: str) -> Dict[str, Any]:
        scanned_str = str(qr_data).strip()

        # If code is too short or too long
        if len(scanned_str) < 5 or len(scanned_str) > 25:
            return {"is_valid": False, "reason": f"Invalid length string. Received: '{qr_data}'"}
        
        # Format must be X-Y-Z
        parts = scanned_str.split('-')
        if len(parts) < 2:
            return {"is_valid": False, "reason": f"Malformed identifier layout: '{qr_data}'"}
        
        stripped_str = scanned_str.replace('-', '')
        
        # Rule A: Purely numbers and dashes = Student
        if stripped_str.isdigit():
            return {
                "is_valid": True,
                "user_type": "student",
                "id": scanned_str
            }
        
        # Rule B: Contains letters = Faculty
        elif any(char.isalpha() for char in stripped_str):
            return {
                "is_valid": True,
                "user_type": "faculty",
                "id": scanned_str
            }
        
        return {"is_valid": False, "reason": "Unknown identifier type. Received: '{qr_data}'"}