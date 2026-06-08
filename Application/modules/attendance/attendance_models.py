from dataclasses import dataclass

# Currently not being used
@dataclass(slots=True)
class AttendanceDTO:
    """Dataclass for Attendance"""
    id: int
    user_id: str
    user_type: str
    time_in: str
    time_out: str