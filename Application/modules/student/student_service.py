from modules.student.student_repo import StudentRepository
from modules.student.student_models import StudentDTO

class StudentService:
    def __init__(self, student_repo: StudentRepository) -> None:
        self.repo = student_repo

    def create(self, student: StudentDTO) -> StudentDTO:
        """Registers a new student"""
        self.repo.create(student)
        return student
    
    def update(self, student: StudentDTO) -> StudentDTO:
        """Updates a student by ID"""
        self.repo.update(student)
        return student