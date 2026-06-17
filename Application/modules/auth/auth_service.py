from core.security.security import verify_password
from core.exceptions import UnauthorizedException
from core.state import app_state

class AuthService:
    def login(self, password: str) -> bool:
        """Verifies the admin password"""
        if not verify_password(password):
            raise UnauthorizedException("Incorrect admin password")
        
        app_state.log_in()
        return True
    
    def logout(self) -> None:
        app_state.log_out()

    def is_authenticated(self) -> bool:
        return app_state.is_admin_logged_in