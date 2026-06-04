import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

import time
import webview

from modules.api.mainAPI import Api
from modules.scanner.qrscanner import QRCodeScanner
from modules.config.logger import setup_logger

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

        self.db_conn = get_db()

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