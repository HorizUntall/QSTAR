from webview import Window

# Importing all controllers/endpoints
from core.renderer.layout_controller import LayoutController

from modules.student.student_controller import StudentController
from modules.faculty.faculty_controller import FacultyController
from modules.attendance.attendance_controller import AttendanceController
from modules.user.user_controller import UserController
from modules.dashboard.dashboard_controller import DashboardController
from modules.scanner.scanner_controller import ScannerController
from modules.auth.auth_controller import AuthController
from modules.version.version_controller import VersionController
from modules.email.email_controller import EmailController
from modules.bug_report.bug_report_controller import BugReportController

class API:
    def __init__(self,
                 layout_controller: LayoutController,
                 student_controller: StudentController,
                 faculty_controller: FacultyController,
                 attendance_controller: AttendanceController,
                 user_controller: UserController,
                 dashboard_controller: DashboardController,
                 scanner_controller: ScannerController,
                 auth_controller: AuthController,
                 version_controller: VersionController,
                 email_controller: EmailController,
                 bug_report_controller: BugReportController) -> None:
        
        self._window: Window | None = None
        
        self.layout = layout_controller
        self.student = student_controller
        self.faculty = faculty_controller
        self.attendance = attendance_controller
        self.user = user_controller
        self.dashboard = dashboard_controller
        self.scanner = scanner_controller
        self.auth = auth_controller
        self.version = version_controller
        self.email = email_controller
        self.bug_report = bug_report_controller
    
    # Private
    def _setWindow(self, window_instance: Window) -> None:
        self._window = window_instance
        self.scanner._setWindow(self._window)