import hashlib
from typing import Dict, Any
from modules.config.config import get_data

class AuthService:
    def verify_admin_password(self, input_pw: str) -> bool:
        """Verifies the admin password"""