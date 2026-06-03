from typing import Optional, List, Dict

from .scanner.qrscanner import QRCodeScanner
from .database.db_manager import DatabaseManager

class Api:
    def __init__(self, qrscanner: QRCodeScanner, db: DatabaseManager):
        
        self._scanner = qrscanner
        self.db = db

    # -------------------------------------------------------
    # CAMERA / SCANNER ENDPOINTS
    # -------------------------------------------------------

    def fetch_frame(self) -> str:
        if not self._scanner.update_frames:
            return ""
        
        b64frame = self._scanner.fetch_frame()
        if not b64frame:
            return ""
        
        return f"data:image/jpeg;base64,{b64frame}"

    def pause_camera(self) -> None: 
        self._scanner.stop_scanning()

    def resume_camera(self) -> None:
        self._scanner.start_scanning()

    
    # -------------------------------------------------------
    # DATABASE / CRUD ENDPOINTS
    # -------------------------------------------------------