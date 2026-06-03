from dataclasses import dataclass

@dataclass(slots=True)
class Student:
    id: str
    first_name: str
    last_name: str
    batch: str
    sex: str

@dataclass(slots=True)
class Faculty:
    id: str
    first_name: str
    last_name: str
    sex: str

@dataclass(slots=True)
class Attendance:
    id: int
    user_id: str
    user_type: str
    time_in: str
    time_out: str