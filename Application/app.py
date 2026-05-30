import os
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
import webview

# GLOBAL VARIABLES
APP_DIR : Path = Path(__file__).resolve().parent
ROOT_DIR : Path = APP_DIR.parent()
LOG_DIR : Path = ROOT_DIR / "Data" / "logs"

LOG_DIR.parent

class Api:
    ...

class QSTARApp:

    def __init__(self) -> None:
        self.indexPage: str = 'web/index.html'

    def check_for_updates(self) -> None:
        ...

    def run(self):
        webview.create_window('QSTAR', self.indexPage, js_api=self)
        webview.start()



if __name__ == "__main__":
    app = QSTARApp()
    app.run()