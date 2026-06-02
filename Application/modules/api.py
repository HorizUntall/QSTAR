from typing import Optional, List, Dict

from .scanner.qrscanner import QRCodeScanner
from .database.db_manager import DatabaseManager

class Api:
    def __init__(self, qrscanner: QRCodeScanner, db: DatabaseManager):
        ...
        # self.qrscanner = qrscanner
        # self.db = db

    # -------------------------------------------------------
    # CAMERA / SCANNER ENDPOINTS
    # -------------------------------------------------------
    # def pause_camera(self) -> None: 
    #     self.qrscanner.stop_scanning()

    # def resume_camera(self) -> None:
    #     self.qrscanner.start_scanning()

    
    # -------------------------------------------------------
    # DATABASE / CRUD ENDPOINTS
    # -------------------------------------------------------