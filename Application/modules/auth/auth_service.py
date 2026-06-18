from core.security.security import verify_password, change_pass
from core.exceptions import UnauthorizedException, PasswordMismatchException
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
    
    def change_password(self, curr_pass, new_pass, new_repeat_pass) -> None:
        if new_pass != new_repeat_pass:
            raise PasswordMismatchException("The password confirmation does not match")
        
        if not verify_password(curr_pass):
            raise UnauthorizedException("Incorrect admin password")
        
        change_pass(new_pass)