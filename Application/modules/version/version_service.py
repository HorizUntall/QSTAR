from core.version import get_app_version

class VersionService:
    def __init__(self) -> None:
        pass

    def get_version(self) -> str:
        return get_app_version()