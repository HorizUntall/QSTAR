from typing import Dict, Any

from core.exceptions import UnauthorizedException, PasswordMismatchException
from modules.auth.auth_service import AuthService
from modules.auth.decorators import admin_required

class AuthController:
    def __init__(self, auth_service: AuthService) -> None:
        self._service = auth_service

    # Public
    def login(self, password: str) -> Dict[str, Any]:
        try:
            self._service.login(password)
            return {"status": "success", "message": "Logged in successfully"}
        except UnauthorizedException as e:
            return {"status": e.status, "message": e.message }

    # Public 
    def logout(self) -> Dict[str, Any]:
        self._service.logout()
        return {"status": "success"}

    # Public
    def get_status(self):
        return {"is_authenticated": self._service.is_authenticated()}
    
    # Public
    @admin_required
    def change_password(self, curr_pw, new_pw, new_repeat_pw) -> Dict[str, Any]:
        try:
            self._service.change_password(curr_pass=curr_pw, new_pass=new_pw, new_repeat_pass=new_repeat_pw)
            return {"status": "success", "message": "Changed password successfully"}

        except PasswordMismatchException as e:
            return {"status": e.status, "message": e.message}
        
        except UnauthorizedException as e:
            return {"status": e.status, "message": e.message}