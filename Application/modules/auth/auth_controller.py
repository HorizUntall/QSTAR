from typing import Dict, Any
from core.session import SessionManager
from modules.auth.auth_service import AuthService

class AuthController:
    def __init__(self, auth_service: AuthService, session_manager: SessionManager) -> None:
        self._auth_service = auth_service
        self._session_manager = session_manager

    def login_admin(self, password: str) -> Dict[str, Any]:
        """Bridge endpoint: window.pywebview.api.auth.login_admin()"""
        if not password:
            return {"status": "error", "message": "Password cannot be empty."}
        
        is_valid = self._auth_service.verify_admin_password(input_pw=password)

        if is_valid:
            self._session_manager.set_admin_authenticated(True)
            return {"status": "success", "message": "Authenticated successfully"}
        
        return {"status": "error", "message": "Incorrect password."}
    
    def logout(self, admin) -> Dict[str, Any]:
        """Bridge endpoint: window.pywebview.api.auth.logout_admin()"""
        self._session_manager.clear()
        return {"status": "success", "message": "Logged out successfully."}