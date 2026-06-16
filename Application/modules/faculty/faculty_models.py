from dataclasses import dataclass
from core.exceptions import BadRequestException
from core.shared.constants import SexEnum

@dataclass(slots=True)
class FacultyDTO:
    """Dataclass for Faculty"""
    id: str
    first_name: str
    last_name: str
    sex: str # 'M' or 'F'

    def __post_init__(self) -> None:

        # Guard against None or non-string values before processing
        for field_name in ['id', 'first_name', 'last_name', 'sex']:
            val = getattr(self, field_name)
            if val is None or not isinstance(val, str):
                raise BadRequestException(message=f"Missing or invalid type for field: {field_name}")

        self.id = str(self.id).strip()
        self.first_name = str(self.first_name).strip().title()
        self.last_name = str(self.last_name).strip().title()
        self.sex = str(self.sex).strip().upper()
        
        if self.sex not in [choice.value for choice in SexEnum]:
            raise BadRequestException(message="Invalid sex format")