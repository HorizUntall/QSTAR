import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

import time
import webview

from modules.api import Api
from modules.scanner.qrscanner import QRCodeScanner
from modules.database.db_manager import DatabaseManager
from modules.attendance import attendance
from modules.verifier import verifier

# GLOBAL VARIABLES
APP_DIR : Path = Path(__file__).resolve().parent
ROOT_DIR : Path = APP_DIR.parent
LOG_DIR : Path = ROOT_DIR / "Data" / "logs" / "app.log"

def setup_logger():
    LOG_DIR.parent.mkdir(parents=True, exist_ok=True)
    handler = RotatingFileHandler(
        LOG_DIR,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    return logger
    

class QSTARApp:

    def __init__(self) -> None:
        self.indexPage: str = 'web/index.html'

        self.db = DatabaseManager()
        self.qrscanner = QRCodeScanner(attendance, vidSrc=2)

    def check_for_updates(self) -> None:
        ...

    def on_closing(self):
        print("Closing...")
        self.qrscanner.stop_scanning()
        self.qrscanner.cleanup()

    def run(self) -> None:
        api = Api(self.qrscanner, self.db)
        window = webview.create_window("QSTAR", self.indexPage, js_api=api)

        self.qrscanner.start_scanning()

        window.events.closing += self.on_closing
        webview.start()

if __name__ == "__main__":
    setup_logger()
    app = QSTARApp()
    app.run()