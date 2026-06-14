from typing import Dict, Any
from pathlib import Path
from webview import Window
from tkinter import filedialog, Tk

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
from modules.config.asset_manifest_service import AssetManifestService

from modules.export.export_service import ExportService
from modules.email.email_service import EmailService

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
                 manifest_service: AssetManifestService,
                 nav_service: NavigationService) -> None:
        
        self._window: Window | None = None
        self.scanner = ScannerAPI(qrscanner) # pywebview.api.scanner.method()

        self._manifest = manifest_service
        self._attendance_service = attendance_service
        self._student_service = student_service
        self._faculty_service = faculty_service
        self._dashboard_service = dashboard_service
        self._auth_service = auth_service
        self._nav_service = nav_service

    # Private
    def _setWindow(self, window_instance: Window) -> None:
        self._window = window_instance
        self.scanner._setWindow(self._window)

    # Public
    def get_boot_assets(self) -> Dict[str, Any]:
        """Method for index.js to call at startup"""
        return {"css_files": self._manifest.get_all_css()}

    # ========== For Security and Navigation =========== 

    # Public
    def changePage(self, dest_page: str) -> Dict[str, Any]:
        return self._nav_service.get_page_layout(dest_page)
    
    # Public
    def loginAdmin(self, password: str) -> Dict[str, Any]:
        return self._auth_service.authenticate(input_pw=password)
    
    # Public
    def logoutAdmin(self) -> Dict[str, Any]:
        self._auth_service.logout()
        return {"status": "success"}

    # ========== Attendance & Homepage Functionalities ==========

    # Public
    def get_today_attendance(self) -> list[Dict[str, Any]]:
        """This endpoint returns a list of entries within today"""
        return self._attendance_service.get_today_attendance()

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
    
    # Public
    def trigger_data_export(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Frontend calls this to generate and route PDF/Excel exports"""
        if not self._auth_service.is_admin():
            return {"status": "unauthorized", "message": "Access denied. Admin rights required."}
        
        try:
            # 1. Map the frontend filters to your DashboardFiltersDTO
            filters_dict: Dict[str, Any] = form_data.get("filters", {})
            filters = DashboardFiltersDTO(
                start_date=filters_dict.get("start_date"),
                end_date=filters_dict.get("end_date"),
                search_name=filters_dict.get("search_name"),
                batch=filters_dict.get("batch"),
                sex=filters_dict.get("sex"),
            )

            # 2. Fetch the Data 
            MAX_RECORDS = 1000000 
            
            history_res = self._dashboard_service.get_processed_attendance_history(
                filters=filters, page=1, page_size=MAX_RECORDS
            )
            
            users_res = self._dashboard_service.get_processed_registered_users(
                filters=filters, page=1, page_size=MAX_RECORDS
            )

            # 3. Clean and Split the Data for the Excel Tabs
            all_users = users_res.get("data", [])
            students = [u for u in all_users if u.get("user_type") == "student"]
            faculty = [u for u in all_users if u.get("user_type") == "faculty"]

            db_data = {
                'history': history_res.get("data", []),
                'users': students,
                'faculty': faculty
            }

            # 4. Generate the Binary Files in-memory
            # Fetch the actual dashboard aggregate data for the PDF charts
            dashboard_res = self._dashboard_service.get_processed_dashboard_data(
                filters=filters, topUsersLimit=5, num_batches=6
            )

            excel_bytes = ExportService.generate_excel(db_data)
            
            # Pass the backend data instead of frontend base64 images
            pdf_bytes = ExportService.generate_pdf(
                dashboard_data=dashboard_res,
                start_date=filters.start_date,
                end_date=filters.end_date
            )

            export_method = form_data.get('export_method')

            # 5. Route the generated files based on user choice
            if export_method == 'email':
                target_email = form_data.get('target_email')
                if not target_email:
                    return {"status": "error", "message": "Email address is required."}
                
                EmailService.send_export_email(target_email, excel_bytes, pdf_bytes)
                return {"status": "success", "message": "Email sent successfully."}

            elif export_method == 'local':
                # Open native folder selection dialog (hidden main tkinter window)
                root = Tk()
                root.withdraw() 
                root.attributes('-topmost', True) 
                
                folder_path = filedialog.askdirectory(title="Select Folder to Save Export Files")
                root.destroy()
                
                if not folder_path:
                    return {"status": "error", "message": "Save cancelled by user."}

                target_dir = Path(folder_path)
                
                excel_file = target_dir / "Library_Data_Export.xlsx"
                pdf_file = target_dir / "Library_Dashboard_Summary.pdf"
                
                # pathlib allows us to write bytes directly without context managers
                excel_file.write_bytes(excel_bytes)
                pdf_file.write_bytes(pdf_bytes)

                return {"status": "success", "message": "Files saved locally."}
            
            else:
                return {"status": "error", "message": "Invalid export method selected."}

        except Exception as e:
            # Catching generic errors to prevent pywebview from silently crashing on bridge failures
            return {"status": "error", "message": f"Export failed: {str(e)}"}