import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

import time
import webview

from modules.api.mainAPI import Api
from modules.scanner.qrscanner import QRCodeScanner
from modules.config.logger import setup_logger

from modules.student.student_repo import StudentRepository
from modules.student.student_service import StudentService

from modules.faculty.faculty_repo import FacultyRepository
from modules.faculty.faculty_service import FacultyService

from modules.attendance.attendance_repo import AttendanceRepository
from modules.attendance.attendance_service import AttendanceService

from modules.dashboard.dashboard_repo import DashboardRepository
from modules.dashboard.dashboard_service import DashboardService

from modules.auth.auth_service import AuthService
from modules.navigation.navigation_service import NavigationService

from modules.database.connection import init_db, get_db 

class QSTARApp:

    def __init__(self) -> None:
        self.root_dir = Path(__file__).resolve().parent
        self.web_dir = self.root_dir / "web"
        self.indexPage = self.web_dir / "index.html"
        self.qrscanner = QRCodeScanner(vidSrc=2)

        try:
            init_db()
        except Exception as db_err:
            logging.critical(f"Database setup layer totally stalled execution: {db_err}")
            exit(1)

        db_conn = get_db()

        # Student Module
        self.student_repo = StudentRepository(db_conn=db_conn)
        self.student_service = StudentService(student_repo=self.student_repo)

        # Faculty Module
        self.faculty_repo = FacultyRepository(db_conn=db_conn)
        self.faculty_service = FacultyService(faculty_repo=self.faculty_repo)

        # Attendance Module
        self.attendance_repo = AttendanceRepository(db_conn=db_conn)
        self.attendance_service = AttendanceService(attendance_repo=self.attendance_repo,
                                                    student_repo=self.student_repo,
                                                    faculty_repo=self.faculty_repo)

        # Dashboard Module
        self.dashboard_repo = DashboardRepository(db_conn=db_conn)
        self.dashboard_service = DashboardService(dashboard_repo=self.dashboard_repo)

        # Auth Module
        self.auth_service = AuthService()

        # Navigation Module
        self.nav_service = NavigationService(web_dir=self.web_dir,
                                        auth_service=self.auth_service)

        # Load Main API
        self.api = Api(qrscanner=self.qrscanner,
                       attendance_service=self.attendance_service,
                       student_service=self.student_service,
                       faculty_service=self.faculty_service,
                       dashboard_service=self.dashboard_service,
                       auth_service=self.auth_service,
                       nav_service=self.nav_service)


    def check_for_updates(self) -> None:
        ...

    def on_closing(self):
        print("Closing...")
        self.qrscanner.stop_scanning()
        self.qrscanner.cleanup()

    def run(self) -> None:
        window = webview.create_window("QSTAR", url=str(self.indexPage), js_api=self.api)
        self.api._setWindow(window)
        self.qrscanner.start_scanning()

        window.events.closing += self.on_closing
        webview.start(debug=True)

if __name__ == "__main__":
    setup_logger()
    app = QSTARApp()
    app.run()