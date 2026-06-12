from typing import Dict, Any

from modules.shared.constants import SexEnum
from modules.faculty.faculty_repo import FacultyRepository
from modules.faculty.faculty_models import FacultyDTO

class FacultyService:
    def __init__(self, faculty_repo: FacultyRepository) -> None:
        self.repo = faculty_repo

    def create_faculty(self, faculty: FacultyDTO) -> Dict[str, Any]:
        # Handle faculty first and last name
        faculty.first_name = faculty.first_name.strip().title()
        faculty.last_name = faculty.last_name.strip().title()

        # Handle faculty sex
        normalized_sex = faculty.sex.strip().upper()
        if normalized_sex not in [choice.value for choice in SexEnum]:
            return {
                "status": "error",
                "message": f"Validation failed: Sex must be either 'M' or 'F'. Received: '{faculty.sex}'"
            } 
        faculty.sex = normalized_sex

        self.repo.create(faculty)
        return {"status": "success", "message": "Faculty registered successfully."}