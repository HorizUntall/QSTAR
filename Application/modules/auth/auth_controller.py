from typing import Dict, Any

from core.exceptions import UnauthorizedException
from modules.auth.auth_service import AuthService

class AuthController:
    def __init__(self, auth_service: AuthService) -> None:
        self._service = auth_service

    # Public
    def login(self, password: str) -> Dict[str, Any]:
        try:
            self._service.login(password)
            return {"status": "success", "message": "Logged in successfully"}
        except UnauthorizedException as e:
            return {"status": "error", "message": e.message}

    # Public 
    def logout(self) -> Dict[str, Any]:
        self._service.logout()
        return {"status": "success"}

    # Public
    def get_status(self):
        return {"is_authenticated": self._service.is_authenticated()}