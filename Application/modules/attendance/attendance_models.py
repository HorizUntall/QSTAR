from dataclasses import dataclass

@dataclass(slots=True)
class Attendance:
    """Dataclass for Attendance"""
    id: int
    user_id: str
    user_type: str
    time_in: str
    time_out: str