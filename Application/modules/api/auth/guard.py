import hashlib
import webview
from pathlib import Path
from typing import Dict, Any

from modules.database.services.config_service import get_password

class GuardAPI:
    def __init__(self):
        self._isAuthorized = False
        self._protected_pages = set(["dashboard", "settings"])

        self._base_dir = Path(__file__).resolve().parent
        self._web_dir = self._base_dir / "web"

    # Public
    def authenticate(self, input_pw: str) -> Dict[str, Any]:
        input_hash = hashlib.sha256(input_pw.encode()).hexdigest
        self._isAuthorized = input_hash == get_password()
        if self._isAuthorized:
            return {"status": "success"}
        else:
            return {"status": "error", "message": "Incorrect credentials"}    
    
    # Public
    def navigate_to(self, dest: str) -> Dict[str, Any]:
        """Routes Pages"""
        if dest in self._protected_pages and not self._isAuthorized:
            return {"status": "error", "message": "Unauthorized access attempt logged."}
        
        # When exiting protected zones
        if dest not in self._protected_pages and self._isAuthorized:
            self._isAuthorized = False

        # Locate the file
        try:
            if dest == "index":
                dest = self._web_dir / "index.html"
            else:
                safe_name = Path(f"{dest}.html").name
                file_path = self._web_dir / "pages" / safe_name

            # Security Check: Force resolved path to stay strictly inside the /web dir
            if not file_path.resolve().is_relative_to(self.web_dir):
                return {"status": "error", "message": "Illegal file access path."}
            
            html_content = file_path.read_text(encoding="utf-8")
            return {"status": "success", "content": html_content, "page": dest}
        
        except FileNotFoundError:
            return {"status": "error", "message": "Page not found."}
        