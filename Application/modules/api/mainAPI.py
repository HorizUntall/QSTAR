from typing import Dict, Any

from webview import Window

from modules.scanner.qrscanner import QRCodeScanner
from modules.api.scannerAPI import ScannerAPI

from modules.student.student_models import StudentDTO
from modules.student.student_service import StudentService

from modules.faculty.faculty_models import FacultyDTO
from modules.faculty.faculty_service import FacultyService

from modules.attendance.attendance_models import AttendanceDTO
from modules.attendance.attendance_service import AttendanceService

from modules.dashboard.dashboard_models import DashboardFiltersDTO
from modules.dashboard.dashboard_service import DashboardService

from modules.auth.auth_service import AuthService
from modules.navigation.navigation_service import NavigationService

"""
Note:
Only public methods can be accessed and called by the frontend. 
The class Api is the main API and holds other API classes.
To call the main API: pywebview.api.method()

Names/Identifier of Private Methods and Variables start with an underscore(_)
"""


class Api:
    def __init__(self, qrscanner: QRCodeScanner, 
                 attendance_service: AttendanceService, 
                 student_service: StudentService, 
                 faculty_service: FacultyService,
                 dashboard_service: DashboardService,
                 auth_service: AuthService,
                 nav_service: NavigationService) -> None:
        
        self._window: Window | None = None
        self.scanner = ScannerAPI(qrscanner) # pywebview.api.scanner.method()

        self._attendance_service = attendance_service
        self._student_service = student_service
        self._faculty_service = faculty_service
        self._dashboard_service = dashboard_service
        self._auth_service = auth_service
        self.nav_service = nav_service

    # Private
    def _setWindow(self, window_instance: Window) -> None:
        self._window = window_instance
        self.scanner._setWindow(self._window)

    # ========== For Security and Navigation =========== 

    # Public
    def changePage(self, dest_page: str) -> Dict[str, Any]:
        return self.nav_service.get_page_layout(dest_page)
    
    # Public
    def loginAdmin(self, password: str) -> Dict[str, Any]:
        return self._auth_service.authenticate(input_pw=password)
    
    # Public
    def logoutAdmin(self) -> Dict[str, Any]:
        self._auth_service.logout()
        return {"status": "success"}

    # ========== Attendance & Homepage Functionalities ==========

    # Public
    def processScannedCode(self, qr_data: str) -> Dict[str, Any]:
        """This endpoint processes the scanned QR Code"""

        # If user code exists in the database, returns status="success", action, and timestamp
        # Otherwise, returns status="not_found", id, and user_type

        return self._attendance_service.verify_and_process_qr(qr_data=qr_data)
    
    # Public
    def register_new_user(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """This endpoint processes the user registration"""
        try:
            user_type = form_data["user_type"]

            # If user is student
            if user_type == "student":
                student = StudentDTO(
                    id=form_data["id"],
                    first_name=form_data["first_name"],
                    last_name=form_data["last_name"],
                    sex=form_data["sex"],
                    batch=form_data["batch"]
                )
                return self._student_service.create_student(student=student)

            # If user is faculty
            else:
                faculty = FacultyDTO(
                    id=form_data["id"],
                    first_name=form_data["first_name"],
                    last_name=form_data["last_name"],
                    sex=form_data["sex"],
                )
                return self._faculty_service.create_faculty(faculty=faculty)

        except KeyError:
            return {"status": "error", "message": "invalid form data"}
    
    # ========== For Dashboard Functionalities ==========

    # Public
    def get_dashboard_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Frontend calls this to populate the dashboard"""
        if not self._auth_service.is_admin():
            return {"status": "unauthorized", "message": "Access denied. Admin rights required."}
        
        filters_dict: Dict[str, Any] = form_data.get("filters", {})
        filters = DashboardFiltersDTO(
            start_date=filters_dict.get("start_date"),
            end_date=filters_dict.get("end_date"),
            search_name=filters_dict.get("search_name"),
            batch=filters_dict.get("batch"),
            sex=filters_dict.get("sex"),
        )
        topUsersLimit = form_data.get("topUsersLimit", 5)
        num_batches = form_data.get("num_batches", 6)
        
        return {"status": "success", 
                "data": self._dashboard_service.get_processed_dashboard_data(filters=filters, 
                                                                            topUsersLimit=topUsersLimit, 
                                                                            num_batches=num_batches)}

    # Public
    def get_attendance_history(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Frontend calls this to populate attendance history"""
        # page -> Page index
        # page_size -> amount of rows/data in a single page

        if not self._auth_service.is_admin():
            return {"status": "unauthorized", "message": "Access denied. Admin rights required."}
        
        filters_dict: Dict[str, Any] = form_data.get("filters", {})
        filters = DashboardFiltersDTO(
            start_date=filters_dict.get("start_date"),
            end_date=filters_dict.get("end_date"),
            search_name=filters_dict.get("search_name"),
            batch=filters_dict.get("batch"),
            sex=filters_dict.get("sex"),
        )
        page = form_data.get("page", 1)
        page_size = form_data.get("page_size", 100)
        
        return {"status": "success", 
                "data": self._dashboard_service.get_processed_attendance_history(filters=filters,
                                                                    page=page,
                                                                    page_size=page_size)}
    
    # Public
    def get_registered_users(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Frontend calls this to populate registered users list"""
        # page -> Page index
        # page_size -> amount of rows/data in a single page

        if not self._auth_service.is_admin():
            return {"status": "unauthorized", "message": "Access denied. Admin rights required."}
        
        filters_dict: Dict[str, Any] = form_data.get("filters", {})
        filters = DashboardFiltersDTO(
            start_date=filters_dict.get("start_date"),
            end_date=filters_dict.get("end_date"),
            search_name=filters_dict.get("search_name"),
            batch=filters_dict.get("batch"),
            sex=filters_dict.get("sex"),
        )
        page = form_data.get("page", 1)
        page_size = form_data.get("page_size", 100)
        
        return {"status": "success", 
                "data": self._dashboard_service.get_processed_registered_users(filters=filters,
                                                                page=page,
                                                                page_size=page_size)}