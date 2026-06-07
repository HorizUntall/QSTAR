from dataclasses import dataclass

@dataclass(slots=True)
class Student:
    """Dataclass for Student"""
    id: str
    first_name: str
    last_name: str
    batch: str
    sex: str # 'M' or 'F'