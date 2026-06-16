class BridgeException(Exception):
    def __init__(self, status: str, message: str, meta: dict = None) -> None:
        self.status = status
        self.message = message
        self.meta = meta
        super().__init__(self.message)

class BadRequestException(BridgeException):
    """Equivalent to Error 400"""
    def __init__(self, message: str) -> None:
        super().__init__(status="invalid", message=message)

class NotFoundException(BridgeException):
    """Equivalent to Error 404"""
    def __init__(self, message: str, meta = None) -> None:
        super().__init__(status="not_found", message=message, meta=meta)

class UserNotRegisteredException(BridgeException):
    """Exception for when a user is not registered"""
    def __init__(self, message: str, meta = None) -> None:
        super().__init__(status="not_found", message=message, meta=meta)