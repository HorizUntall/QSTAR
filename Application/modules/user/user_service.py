from typing import Dict, Any

from core.shared.constants import UserTypeEnum

from modules.identity.qr_parser import ParsedQR, validate_and_parse

from modules.student.student_models import StudentDTO
from modules.student.student_service import StudentService

from modules.faculty.faculty_models import FacultyDTO
from modules.faculty.faculty_service import FacultyService

from modules.user.user_models import UserDTO

class UserService:
    def __init__(self, student_service: StudentService, faculty_service: FacultyService) -> None:
        self._student_service = student_service
        self._faculty_service = faculty_service

    def register(self, user: UserDTO) -> StudentDTO | FacultyDTO:
        """Orchestrates the registration process based on user type"""

        # Routing to the appropriate Domain Service
        if user.user_type == UserTypeEnum.STUDENT.value:
            student_dto = StudentDTO(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                sex=user.sex,
                batch=user.batch
            )
            return self._student_service.create(student=student_dto)
        
        else:
            faculty_dto = FacultyDTO(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                sex=user.sex
            )
            return self._faculty_service.create(faculty=faculty_dto)
