from typing import Dict, Any

from core.exceptions import BridgeException

from modules.identity.qr_parser import ParsedQR, validate_and_parse

from modules.student.student_models import StudentDTO

from modules.faculty.faculty_models import FacultyDTO

from modules.user.user_models import UserDTO
from modules.user.user_service import UserService

class UserController:
    def __init__(self, user_service: UserService) -> None:
        self._service = UserService

    def register_new_user(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """This endpoint processes the user registration"""
        
        try:
            user_dto = UserDTO(**form_data)
            user: StudentDTO | FacultyDTO = self._service.register(user=user_dto)
            return {
                "status": "success",
                "message": f"User registration successful",
                "data": {
                    "id": user.id,
                    "user_type": user_dto.user_type
                }
            }

        except KeyError as e:
            return {"status": "error", "message": f"Invalid form data: {e}"}
        
        except BridgeException as e:
            return {
                "status": e.status,
                "message": e.message,
                "meta": e.meta
            }