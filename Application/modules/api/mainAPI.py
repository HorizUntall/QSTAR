from typing import Optional, List, Dict

import sqlite3
from webview import Window

from modules.scanner.qrscanner import QRCodeScanner
from modules.api.dataAPI import DataAPI
from modules.api.scannerAPI import ScannerAPI

class Api:
    def __init__(self, qrscanner: QRCodeScanner, db_conn: sqlite3.Connection) -> None:
        self._window: Window | None = None
        self.scanner = ScannerAPI(qrscanner)
        self.data = DataAPI(db_conn)

    def _setWindow(self, window_instance: Window) -> None:
        self._window = window_instance
        self.scanner._setWindow(self._window)

    def verifyAndProcessQR(self, qr_data: str) -> dict:
        scanned_string = str(qr_data).strip()

        if not self._isValid(scanned_string):
            return {"status": "invalid", "message": "Malformed QR Code skipped"}
        
        return {
                "status": "success"
            }

    def _isValid(self, qr_data: str) -> bool:
        return True