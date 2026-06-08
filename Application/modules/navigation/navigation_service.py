from pathlib import Path
from typing import Dict, Any, Set

from modules.auth.auth_service import AuthService

class NavigationService:
    def __init__(self, web_dir: Path, auth_service: AuthService) -> None:
        self.auth_service = auth_service

        # HTML Pages (!!!This must be updated when adding new pages !!!)
        self._file_map = {
            "homepage": web_dir / "pages" / "homepage.html",
            "registration": web_dir / "pages" / "registration.html",
            "login": web_dir / "pages" / "login.html",
            "dashboard": web_dir / "pages" / "dashboard.html",
            "settings": web_dir / "pages" / "settings.html",
            "about": web_dir / "pages" / "about.html"
        }

        # Admin-Only Pages. Name must match from file_map !!!
        self._admin_pages = set([
            "dashboard",
            "settings"
        ])

        # Cache. Read files into memory immediately on boot
        self._cache = {}
        for page_name, file_path in self._file_map.items():
            if file_path.exists():
                self._cache[page_name] = file_path.read_text(encoding="utf-8")

    def get_page_layout(self, page_name: str) -> Dict[str, Any]:
        if page_name not in self._cache:
            return {"status": "error", "message": "Layout not found."}
        
        if page_name in self._admin_pages and not self.auth_service.is_admin():
            return {"status": "unauthorized", "message": "Access Denied."}
        
        return {"status": "success", "content": self._cache[page_name]}