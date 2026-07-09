import logging
from pathlib import Path
import watchfiles
from threading import Event, Thread
import sys
import numpy as np

import webview

# Core 
from core.database.database import init_db, get_db 
from core.log.logger import setup_logger
from core import version

from core.renderer.asset_service import AssetResolverService
from core.renderer.layout_service import LayoutService
from core.renderer.layout_controller import LayoutController

from core.api import API

# Modules
from modules.auth.auth_controller import AuthController
from modules.auth.auth_service import AuthService

from modules.student.student_repo import StudentRepository
from modules.student.student_service import StudentService
from modules.student.student_controller import StudentController

from modules.faculty.faculty_repo import FacultyRepository
from modules.faculty.faculty_service import FacultyService
from modules.faculty.faculty_controller import FacultyController

from modules.attendance.attendance_repo import AttendanceRepository
from modules.attendance.attendance_service import AttendanceService
from modules.attendance.attendance_controller import AttendanceController

from modules.user.user_service import UserService
from modules.user.user_controller import UserController

from modules.dashboard.dashboard_repo import DashboardRepository
from modules.dashboard.dashboard_service import DashboardService
from modules.dashboard.dashboard_controller import DashboardController

from modules.scanner.qrscanner import QRCodeScanner
from modules.scanner.scanner_controller import ScannerController

from modules.version.version_service import VersionService
from modules.version.version_controller import VersionController

class QSTARApp:

    def __init__(self, devMode=False) -> None:

        # Check if running as an Auto PY to EXE bundle
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            # In the EXE, sys._MEIPASS points directly to '_internal/' 
            # and all your assets (web, core, modules) live straight inside it.
            self.root_dir = Path(sys._MEIPASS)
            version.version_path = self.root_dir / "version.json"
        else:
            # Locally, __file__ is inside 'core/', so we go up two levels to reach the root project directory
            self.root_dir = Path(__file__).resolve().parent.parent
            version.version_path = self.root_dir / "version.json"

        self.web_dir = self.root_dir / "web"
        self.indexPage = self.web_dir / "index.html"
        self.qrscanner = QRCodeScanner()
        self.window: webview.Window | None = None

        """For Dev Mode Hot Reloading"""
        self.devMode = devMode
        self.stop_watcher_event = Event()  # Clean exit state trigger
        self.watcher_thread: Thread | None = None

        try:
            init_db()
        except Exception as db_err:
            logging.critical(f"Database setup layer totally stalled execution: {db_err}")
            exit(1)

        db_conn = get_db()

        # Student Module
        self.student_repo = StudentRepository(db_conn=db_conn)
        self.student_service = StudentService(student_repo=self.student_repo)
        self.student_controller = StudentController(student_service=self.student_service)

        # Faculty Module
        self.faculty_repo = FacultyRepository(db_conn=db_conn)
        self.faculty_service = FacultyService(faculty_repo=self.faculty_repo)
        self.faculty_controller = FacultyController(faculty_service=self.faculty_service)

        # Attendance Module
        self.attendance_repo = AttendanceRepository(db_conn=db_conn)
        self.attendance_service = AttendanceService(attendance_repo=self.attendance_repo,
                                                    student_repo=self.student_repo,
                                                    faculty_repo=self.faculty_repo)
        self.attendance_controller = AttendanceController(attendance_service=self.attendance_service)

        # User Module
        self.user_service = UserService(student_service=self.student_service,
                                        faculty_service=self.faculty_service)
        self.user_controller = UserController(user_service=self.user_service)

        # Dashboard Module
        self.dashboard_repo = DashboardRepository(db_conn=db_conn)
        self.dashboard_service = DashboardService(dashboard_repo=self.dashboard_repo)
        self.dashboard_controller = DashboardController(dashboard_service=self.dashboard_service)

        # Auth Module
        self.auth_service = AuthService()
        self.auth_controller = AuthController(auth_service=self.auth_service)

        # Scanner Module
        self.scanner_controller = ScannerController(qrscanner=self.qrscanner)

        # Layout Module (Core)
        self.asset_service = AssetResolverService(web_dir=self.web_dir)
        self.layout_service = LayoutService(asset_service=self.asset_service)
        self.layout_controller = LayoutController(layout_service=self.layout_service)

        # Version Module
        self.version_service = VersionService()
        self.version_controller = VersionController(version_service=self.version_service)

        # Load Main API
        self.api = API(
            layout_controller=self.layout_controller,
            student_controller=self.student_controller,
            faculty_controller=self.faculty_controller,
            attendance_controller=self.attendance_controller,
            user_controller=self.user_controller,
            dashboard_controller=self.dashboard_controller,
            scanner_controller=self.scanner_controller,
            auth_controller=self.auth_controller,
            version_controller=self.version_controller
        )

    def on_closing(self):
        print("Closing...")

        if self.devMode:
            print("[Dev Hot Reload] Stopping file watcher thread...")
            self.stop_watcher_event.set()

        self.qrscanner.stop_scanning()
        self.qrscanner.cleanup()

    def watch_and_reload(self) -> None:
        """Fires automatically on changes ONLY when devMode is active."""
        for change in watchfiles.watch(".", stop_event=self.stop_watcher_event):
            if self.window is not None:
                self.asset_service.initialize_manifest()
                self.window.evaluate_js("window.location.reload()")

    def run(self) -> None:
        self.window = webview.create_window("QSTAR", url=str(self.indexPage), js_api=self.api)
        self.api._setWindow(self.window)
        self.qrscanner.start_scanning()

        self.window.events.closing += self.on_closing

        if self.devMode:
            self.watcher_thread = Thread(target=self.watch_and_reload)
            self.watcher_thread.daemon = True
            self.watcher_thread.start()
            webview.start(debug=True)
        else:
            webview.start()