from typing import Dict, Any
from dataclasses import dataclass
from core.exceptions import BadRequestException

# def validate_and_parse(qr_data: str) -> Dict[str, Any]:
#     scanned_str = str(qr_data).strip()
#     print(scanned_str)

#     # If code is too short or too long
#     if len(scanned_str) < 5 or len(scanned_str) > 25:
#         return {"is_valid": False, "reason": f"Invalid length string. Received: '{qr_data}'"}
    
#     # Format must be X-Y-Z
#     parts = scanned_str.split('-')
#     if len(parts) < 2:
#         return {"is_valid": False, "reason": f"Malformed identifier layout: '{qr_data}'"}
    
#     stripped_str = scanned_str.replace('-', '')
    
#     # Rule A: Purely numbers and dashes = Student
#     if stripped_str.isdigit():
#         return {
#             "is_valid": True,
#             "user_type": "student",
#             "id": scanned_str
#         }
    
#     # Rule B: Contains letters = Faculty
#     elif any(char.isalpha() for char in stripped_str):
#         return {
#             "is_valid": True,
#             "user_type": "faculty",
#             "id": scanned_str
#         }
    
#     return {"is_valid": False, "reason": f"Unknown identifier type. Received: '{qr_data}'"}

@dataclass(frozen=True)
class ParsedQR:
    user_type: str
    cleaned_id: str