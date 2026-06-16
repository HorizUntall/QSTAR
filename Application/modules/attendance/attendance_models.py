from dataclasses import dataclass
from typing import Optional

# Currently not being used
@dataclass(slots=True)
class ProcessedAttendanceResult:
    action: str
    timestamp: Optional[str] = None