from typing import Dict, Any

import sqlite3
from webview import Window

from modules.scanner.qrscanner import QRCodeScanner
from modules.api.dataAPI import DataAPI
from modules.api.scannerAPI import ScannerAPI
from modules.api.auth.guard import GuardAPI
from modules.database.models import Student, Faculty, Attendance, DashboardFilters

"""
Note:
Only public methods can be accessed and called by the backend. 
The class Api is the main API and holds other API classes.
To call the main API: pywebview.api.method()

Names/Identifier of Private Methods and Variables start with an underscore(_)
"""


class Api:
    def __init__(self, qrscanner: QRCodeScanner, db_conn: sqlite3.Connection) -> None:
        self._window: Window | None = None
        self.scanner = ScannerAPI(qrscanner) # pywebview.api.scanner.method()
        self.data = DataAPI(db_conn) # pywebview.api.data.method()
        self._auth = GuardAPI() # pywebview.api.

    # Private
    def _setWindow(self, window_instance: Window) -> None:
        self._window = window_instance
        self.scanner._setWindow(self._window)


    # ========== Attendance & Homepage Functionalities ==========

    # Public
    def verifyAndProcessQR(self, qr_data: str) -> Dict[str, Any]:
        """This method processes the scanned QR Code"""
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

    # Private
    def _isValid(self, qr_data: str) -> bool:
        """Check if QR Code is Valid"""
        return True
    
    # Public
    def register_new_user(self, form_data: dict) -> Dict[str, Any]:
        success = self.data.create_user(
            user_id=form_data["id"],
            first_name=form_data["firstName"],
            last_name=form_data["lastName"],
            sex=form_data["sex"],
            user_type=form_data["type"],
            batch=form_data.get("batch") # Optional
        )
        return {"status": "success" if success else "error"}
    

    # ========== For Security and Navigation =========== 
    
    # Public
    def authenticate(self, input_pw: str) -> Dict[str, Any]:
        return self._auth.authenticate(input_pw)
    
    # Public
    def navigate_to(self, dest: str) -> Dict[str, Any]:
        return self._auth.navigate_to(dest)
    

    # ========== For Dashboard Functionalities ==========

    # Public
    def get_dashboard_data(self, filters_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Frontend calls this to populate the dashboard"""
        if not self._auth._isAuthorized:
            return {"status": "error", "message": "Unauthorized access."}
        
        filters = DashboardFilters(**filters_dict)
        topUsersLimit = 5
        num_batches = 6
        if "topUsersLimit" in filters_dict:
            topUsersLimit = filters_dict["topUsersLimit"]
        if "num_batches" in filters_dict:
            num_batches = filters_dict["num_batches"]
        
        return {"status": "success", "data": self.data._get_processed_dashboard_data(filters=filters, 
                                                                           topUsersLimit=topUsersLimit, 
                                                                           num_batches=num_batches)}
    
    # Public
    def get_attendance_history(self, filters_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Frontend calls this to populate attendance history"""
        # page -> Page index
        # page_size -> amount of rows/data in a single page

        if not self._auth._isAuthorized:
            return {"status": "error", "message": "Unauthorized access."}
        
        filters = DashboardFilters(**filters_dict)
        page = 1
        page_size = 100
        if "page" in filters_dict:
            page = filters_dict["page"]
        if "page_size" in filters_dict:
            page_size = filters_dict["page_size"]
        
        return {"status": "success", "data": self.data._get_processed_attendance_history(filters=filters,
                                                                                         page=page,
                                                                                         page_size=page_size)}
    
    # Public
    def get_registered_users(self, filters_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Frontend calls this to populate registered users list"""
        # page -> Page index
        # page_size -> amount of rows/data in a single page

        if not self._auth._isAuthorized:
            return {"status": "error", "message": "Unauthorized access."}
        
        filters = DashboardFilters(**filters_dict)
        page = 1
        page_size = 100
        if "page" in filters_dict:
            page = filters_dict["page"]
        if "page_size" in filters_dict:
            page_size = filters_dict["page_size"]
        
        return {"status": "success", "data": self.data._get_processed_registered_users(filters=filters,
                                                                                         page=page,
                                                                                         page_size=page_size)}

"""
IMPORTANT!!! HOW TO VERIFY IF STUDENT OR FACULTY. 
MIGHT BE WEIRD IF WHEN A STUDENT REGISTER, THEY CAN JUST LABEL THEMSELVES AS FACULTY
"""