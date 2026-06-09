import logging
from pathlib import Path
import watchfiles
from threading import Event, Thread

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
from modules.config.asset_manifest_service import AssetManifestService

from modules.database.connection import init_db, get_db 

class QSTARApp:

    def __init__(self, devMode=False) -> None:
        self.root_dir = Path(__file__).resolve().parent
        self.web_dir = self.root_dir / "web"
        self.indexPage = self.web_dir / "index.html"
        self.qrscanner = QRCodeScanner(vidSrc=2)
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

        # Config Module
        self.asset_manifest_service = AssetManifestService(web_dir=self.web_dir)

        # Navigation Module
        self.nav_service = NavigationService(manifest_service=self.asset_manifest_service,
                                             auth_service=self.auth_service)

        # Load Main API
        self.api = Api(qrscanner=self.qrscanner,
                       attendance_service=self.attendance_service,
                       student_service=self.student_service,
                       faculty_service=self.faculty_service,
                       dashboard_service=self.dashboard_service,
                       auth_service=self.auth_service,
                       manifest_service=self.asset_manifest_service,
                       nav_service=self.nav_service)

    def check_for_updates(self) -> None:
        ...

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
                self.asset_manifest_service._generate_manifest()
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

if __name__ == "__main__":
    setup_logger()
    app = QSTARApp(devMode=True)
    app.run()