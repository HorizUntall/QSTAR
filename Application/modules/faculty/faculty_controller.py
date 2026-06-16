from typing import Dict, Any, List

from core.exceptions import BridgeException

from modules.faculty.faculty_service import FacultyService
from modules.faculty.faculty_models import FacultyDTO

class FacultyController:
    def __init__(self, faculty_service: FacultyService) -> None:
        self._service = faculty_service

    # Public <-- Commented Out since not being used for now
    # DO NOT DELETE
    # def create_faculty(self, data: Dict[str, Any]) -> Dict[str, Any]:
    #     try:
    #         faculty_dto = FacultyDTO(**data)
    #         faculty = self._service.create(faculty=faculty_dto)
    #         return {
    #             "status": "success",
    #             "message": "Student registered successfully.",
    #             "data": {
    #                 "faculty": {
    #                     "id": faculty.id,
    #                     "first_name": faculty.first_name,
    #                     "last_name": faculty.last_name,
    #                     "sex": faculty.sex,
    #                 }
    #             }
    #         }           

    #     except TypeError as e:
    #          return {
    #         "status": "invalid",
    #         "message": f"Invalid request payload: {str(e)}"
    #     }

    #     except BridgeException as e:
    #         return {
    #             "status": e.status,
    #             "message": e.message,
    #             "meta": e.meta
    #         }

    # Public 
    def update_faculty(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            faculty_dto = FacultyDTO(**data)
            faculty = self._service.update(faculty=faculty_dto)
            return {
                "status": "success",
                "message": "Student registered successfully",
                "data": {
                    "student": {
                        "id": faculty.id,
                        "first_name": faculty.first_name,
                        "last_name": faculty.last_name,
                        "sex": faculty.sex,
                    }
                }
            }
        
        except TypeError as e:
            return {
            "status": "invalid",
            "message": f"Invalid request payload: {str(e)}"
        }

        except BridgeException as e:
            return {
                "status": e.status,
                "message": e.message,
                "meta": e.meta
            }
        
    # Public
    def get_all_faculty(self) -> List[Dict[str, Any]] | None:
        try:
            faculties = self._service.get_all()
            return {
                "status": "success",
                "message": "All faculties retrieved.",
                "data": {
                    "faculties": faculties
                }
            }
        
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error occured while retrieving all faculties: {e}"
            }