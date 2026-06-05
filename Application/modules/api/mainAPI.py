from typing import Optional, List, Dict

import sqlite3
from webview import Window

from modules.scanner.qrscanner import QRCodeScanner
from modules.api.dataAPI import DataAPI
from modules.api.scannerAPI import ScannerAPI
from modules.database.models import Student, Faculty, Attendance

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
        
        # Check profiles data
        user: Student | Faculty | None
        user_type: str | None
        user, user_type = self.data.find_unique(scanned_string)

        if user is None:
            return {"status": "not_found", "id": scanned_string}
        
        # Log attendance event
        result = self.data.register_scan(scanned_string, user_type)
        if result:
            return {
                "status": "success",
                "action": result["action"],
                "name": f"{user.first_name} {user.last_name}",
                "type": user_type,
                "time": result["timestamp"]
            }
        return {"status": "error", "message": "Database write failure execution event."}

    # Check if QR Code is Valid
    def _isValid(self, qr_data: str) -> bool:
        return True
    
    def register_new_user(self, form_data: dict) -> dict:
        success = self.data.create_user(
            user_id=form_data["id"],
            first_name=form_data["firstName"],
            last_name=form_data["lastName"],
            sex=form_data["sex"],
            batch=form_data.get("batch") # Optional
        )
        return {"status": "success" if success else "error"}
    
    def access_dashboard(self, password_input) -> dict:
        if self.data._verify_admin(password_input):
            return {"status": "granted"}
        return {"status": "denied", "message": "Incorred access credentials."}