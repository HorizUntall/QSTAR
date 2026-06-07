from modules.faculty.faculty_repo import FacultyRepository

class FacultyService:
    def __init__(self, faculty_repo: FacultyRepository) -> None:
        self.repo = faculty_repo