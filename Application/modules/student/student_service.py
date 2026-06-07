from modules.student.student_repo import StudentRepository

class StudentService:
    def __init__(self, student_repo: StudentRepository) -> None:
        self.repo = student_repo