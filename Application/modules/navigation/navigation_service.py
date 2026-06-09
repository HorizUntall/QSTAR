from pathlib import Path
from typing import Dict, Any, Set

from modules.auth.auth_service import AuthService

class NavigationService:
    def __init__(self, web_dir: Path, auth_service: AuthService) -> None:
        self.auth_service = auth_service
        self._cache: Dict[str, Dict[str, str]] = {}
        self._secured_pages = set()

        views_dir = web_dir / "views"
        self._auto_discover_views(views_dir)

    def _auto_discover_views(self, views_dir: Path) -> None:
        if not views_dir.exists():
            return
        
        for js_file in views_dir.rglob("*.js"):
            page_name = js_file.stem

            relative_parts = js_file.relative_to(views_dir.parent).parts
            js_url = "./" + "/".join(relative_parts)

            self._cache[page_name] = {
                "tag": f"<app-{page_name}></app-{page_name}>",
                "script_url": js_url
            }

            # Security folders check
            if "admin" in js_file.parts:
                self._secured_pages.add(page_name)

    def get_page_layout(self, page_name: str) -> Dict[str, Any]:
        if page_name not in self._cache:
            return {"status": "error", "message": "Layout not found."}
        
        if page_name in self._secured_pages and not self.auth_service.is_admin():
            return {"status": "unauthorized", "message": "Access Denied."}
        
        return {
            "status": "success",
            "content": self._cache[page_name]["tag"],
            "script_url": self._cache[page_name]["script_url"]
        }