import hashlib
from typing import Dict, Any
from modules.config.config import get_data

class AuthService:
    def __init__(self) -> None:
        # State management for admin session
        self._is_authorized = False

    def authenticate(self, input_pw: str) -> Dict[str, Any]:
        """Verifies the admin password hash."""
        input_hash = hashlib.sha256(input_pw.encode()).hexdigest()
        
        # Compare against config storage
        self._is_authorized = (input_hash == get_data(key="admin_password_hash"))
        
        if self._is_authorized:
            return {"status": "success", "message": "Authenticated successfully"}
        return {"status": "error", "message": "Incorrect credentials"}

    def logout(self) -> None:
        """Clears the authentication state."""
        self._is_authorized = False

    def is_admin(self) -> bool:
        """The Guard Check method used by other services/controllers."""
        return self._is_authorized