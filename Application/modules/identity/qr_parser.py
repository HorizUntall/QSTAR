from dataclasses import dataclass
from core.exceptions import BadRequestException
from core.shared.constants import UserTypeEnum

@dataclass(frozen=True)
class ParsedQR:
    user_type: str
    id: str

def validate_and_parse(qr_data: str) -> ParsedQR:
    scanned_str = str(qr_data).strip()

    # Length Validation
    if len(scanned_str) < 5 or len(scanned_str) > 25:
        raise BadRequestException(f"Invalid length string. Received: '{qr_data}'")
    
    # Format Validation
    parts = scanned_str.split('-')
    if len(parts) < 2:
        raise BadRequestException(f"Malformed identifier layout: {qr_data}")
    
    stripped_str = scanned_str.replace('-', '')

    # Rule A. Purely numbers and dashes = Student
    if stripped_str.isdigit():
        return ParsedQR(user_type=UserTypeEnum.STUDENT.value, id=scanned_str)
    
    # Rule B: Contains letters = Faculty
    if any(char.isalpha() for char in stripped_str):
        return ParsedQR(user_type=UserTypeEnum.FACULTY.value, id=scanned_str)
    
    raise BadRequestException(f"Unknown identifier type. Recieved: '{qr_data}'")