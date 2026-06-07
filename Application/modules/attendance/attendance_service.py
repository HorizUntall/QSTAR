from modules.attendance.attendance_repo import AttendanceRepository

class AttendanceService:
    def __init__(self, attendance_repo: AttendanceRepository) -> None:
        self.repo = attendance_repo