from dataclasses import dataclass
from typing import Optional

@dataclass
class DashboardFiltersDTO:
    """Dataclass to hold and transport filter states cleanly"""
    start_date: Optional[str] = None    # Format: 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'
    end_date: Optional[str] = None      # Format: 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'
    search_name: Optional[str] = None
    sex: Optional[str] = None           # 'M' or 'F'
    batch: Optional[str] = None         # e.g., '2024', '2025', or 'Faculty'