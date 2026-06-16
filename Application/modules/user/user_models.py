from dataclasses import dataclass
from typing import Optional

from core.exceptions import BadRequestException
from core.shared.constants import SexEnum, UserTypeEnum

from modules.identity.qr_parser import validate_and_parse

@dataclass
class UserDTO:
    """Dataclass for User"""
    id: str
    first_name: str
    last_name: str
    sex: str

    user_type: str = None
    batch: Optional[str] = None

    def __post_init__(self) -> None:
        for field_name in ['id', 'first_name', 'last_name', 'sex']:
            val = getattr(self, field_name)
            if val is None or not isinstance(val, str):
                raise BadRequestException(message=f"Missing or invalid type for field: {field_name}")
            
        parsed = validate_and_parse(qr_data=self.id)
        self.id = parsed.id
        self.user_type = parsed.user_type

        # Batch is required for student
        if self.user_type == UserTypeEnum.STUDENT.value:
            if not self.batch or not isinstance(self.batch, str):
                raise BadRequestException(message="Batch is required for student users.")
            
        self.first_name = str(self.first_name).strip().title()
        self.last_name = str(self.last_name).strip().title()
        self.batch = str(self.batch).strip()
        self.sex = str(self.sex).strip().upper()

        if not self.batch.isdigit():
            raise BadRequestException(message="Invalid batch format")
        
        if self.sex not in [choice.value for choice in SexEnum]:
            raise BadRequestException(message="Invalid sex format")