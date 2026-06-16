from typing import Dict, Any, List

from modules.faculty.faculty_repo import FacultyRepository
from modules.faculty.faculty_models import FacultyDTO

class FacultyService:
    def __init__(self, faculty_repo: FacultyRepository) -> None:
        self.repo = faculty_repo

    def create(self, faculty: FacultyDTO) -> FacultyDTO:
        """Registers a new faculty"""
        self.repo.create(faculty)
        return faculty
    
    def get_all(self) -> List[Dict[str, Any]] | None:
        """Retrieves all faculties"""
        return self.repo.get_all()
    
    def update(self, faculty: FacultyDTO) -> FacultyDTO:
        """Updates a faculty by ID"""
        self.repo.update(faculty)
        return faculty