from dataclasses import dataclass

@dataclass(slots=True)
class Faculty:
    """Dataclass for Faculty"""
    id: str
    first_name: str
    last_name: str
    sex: str # 'M' or 'F'