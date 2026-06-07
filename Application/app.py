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

from modules.database.connection import init_db, get_db 

class QSTARApp:

    def __init__(self) -> None:
        self.indexPage: str = 'web/index.html'
        self.qrscanner = QRCodeScanner(vidSrc=2)

        try:
            init_db()
        except Exception as db_err:
            logging.critical(f"Database setup layer totally stalled execution: {db_err}")
            exit(1)

        db_conn = get_db()

        # Student Module
        student_repo = StudentRepository(db_conn=db_conn)
        student_service = StudentService(student_repo=student_repo)

        # Faculty Module
        faculty_repo = FacultyRepository(db_conn=db_conn)
        faculty_service = FacultyService(faculty_repo=faculty_repo)

        # Attendance Module
        attendance_repo = AttendanceRepository(db_conn=db_conn)
        attendance_service = AttendanceService(attendance_repo=attendance_repo)

        # Dashboard Module
        dashboard_repo = DashboardRepository(db_conn=db_conn)
        dashboard_service = DashboardService(dashboard_repo=dashboard_repo)

        # Load Main API
        self.api = Api(self.qrscanner)


    def check_for_updates(self) -> None:
        ...

    def on_closing(self):
        print("Closing...")
        self.qrscanner.stop_scanning()
        self.qrscanner.cleanup()

    def run(self) -> None:
        api = Api(self.qrscanner, self.db_conn)
        window = webview.create_window("QSTAR", self.indexPage, js_api=api)
        api._setWindow(window)
        self.qrscanner.start_scanning()

        window.events.closing += self.on_closing
        webview.start(debug=True)

if __name__ == "__main__":
    setup_logger()
    app = QSTARApp()
    app.run()