from functools import wraps
from core.state import app_state
from core.exceptions import UnauthorizedException

def admin_required(func):
    """Blocks execution of a function if admin is not logged in"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            if not app_state.is_admin_logged_in:
                raise UnauthorizedException("Access denied. Admin login required.")
            
            # If authenticated, execute the actual API method
            return func(*args, **kwargs)
            
        except UnauthorizedException as e:
            # Catch the exception at the controller boundary and format for JS
            return {"status": "error", "message": str(e)}
            
    return wrapper