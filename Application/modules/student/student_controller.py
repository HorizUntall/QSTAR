from typing import Dict, Any

from core.exceptions import BridgeException

from modules.student.student_service import StudentService
from modules.student.student_models import StudentDTO

class StudentController:
    def __int__(self, student_service: StudentService) -> None:
        self._service = student_service

    # Public <-- Commented Out since not being used for now
    # DO NOT DELETE
    # def create_student(self, data: Dict[str, Any]) -> Dict[str, Any]:
    #     try:
    #         student_dto = StudentDTO(**data)
    #         student = self._service.create(student=student_dto)
    #         return {
    #             "status": "success",
    #             "message": "Student registered successfully.",
    #             "data": {
    #                 "student": {
    #                     "id": student.id,
    #                     "first_name": student.first_name,
    #                     "last_name": student.last_name,
    #                     "sex": student.sex,
    #                     "batch": student.batch
    #                 }
    #             }
    #         }
        
    #     except TypeError as e:
    #         return {
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
    def update_student(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            student_dto = StudentDTO(**data)
            student = self._service.update(student=student_dto)
            return {
                "status": "success",
                "message": "Student registered successfully",
                "data": {
                    "student": {
                        "id": student.id,
                        "first_name": student.first_name,
                        "last_name": student.last_name,
                        "sex": student.sex,
                        "batch": student.batch
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