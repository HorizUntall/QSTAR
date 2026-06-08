from typing import Dict, Any

from modules.shared.constants import SexEnum
from modules.student.student_repo import StudentRepository
from modules.student.student_models import StudentDTO

class StudentService:
    def __init__(self, student_repo: StudentRepository) -> None:
        self.repo = student_repo

    def create_student(self, student: StudentDTO) -> Dict[str, Any]:
        """Registers a new student"""
        # Handle student first and last name
        student.first_name = student.first_name.strip().title()
        student.last_name = student.last_name.strip().title()

        # Handle student sex
        normalized_sex = student.sex.strip().upper()
        if normalized_sex not in [choice.value for choice in SexEnum]:
            return {
                "status": "error",
                "message": f"Validation failed: Sex must be either 'M' or 'F'. Received: '{student.sex}'"
            } 
        student.sex = normalized_sex

        # Handle student batch
        normalized_batch = str(student.batch).strip()
        if not normalized_batch.isdigit():
            return {
                "status": "error",
                "message": f"Validation failed: Batch must be a valid number. Received: '{student.batch}'"
            }
        student.batch = normalized_batch

        self.repo.create(student)
        return {"status": "success", "message": "Student registered successfully."}