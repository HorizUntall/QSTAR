from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class Student:
    """Dataclass for Student"""
    id: str
    first_name: str
    last_name: str
    batch: str
    sex: str # 'M' or 'F'

@dataclass(slots=True)
class Faculty:
    """Dataclass for Faculty"""
    id: str
    first_name: str
    last_name: str
    sex: str # 'M' or 'F'

@dataclass(slots=True)
class Attendance:
    """Dataclass for Attendance"""
    id: int
    user_id: str
    user_type: str
    time_in: str
    time_out: str

@dataclass
class DashboardFilters:
    """Dataclass to hold and transport filter states cleanly"""
    start_date: Optional[str] = None    # Format: 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'
    end_date: Optional[str] = None      # Format: 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'
    search_name: Optional[str] = None
    sex: Optional[str] = None           # 'M' or 'F'
    batch: Optional[str] = None         # e.g., '2024', '2025', or 'Faculty'