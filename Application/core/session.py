class SessionManager:
    def __init__(self) -> None:
        self._is_admin_authenticated: bool = False

    def set_admin_authenticated(self, status: bool) -> None:
        self._is_admin_authenticated = status

    def is_admin(self) -> bool:
        return self._is_admin_authenticated
    
    def clear(self) -> None:
        self._is_admin_authenticated = False