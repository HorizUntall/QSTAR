from typing import Dict, Any

from core.exceptions import VersionFileNotFoundException
from modules.version.version_service import VersionService

class VersionController:
    def __init__(self, version_service: VersionService) -> None:
        self._service = version_service

    def get_version(self) -> Dict[str, Any]:
        try:
            return {
                "status": "success", 
                "message": "Version retrieved successfully",
                "data": {
                    "version": self._service.get_version()
                }
            }
        
        except VersionFileNotFoundException as e:
            return {
                "status": e.status,
                "message": e.message
            }