from pathlib import Path
from typing import Dict, Any, Set

from modules.auth.auth_service import AuthService
from modules.config.asset_manifest_service import AssetManifestService

class NavigationService:
    def __init__(self, manifest_service: AssetManifestService, auth_service: AuthService) -> None:
        self._manifest = manifest_service
        self.auth_service = auth_service

    def get_page_layout(self, page_name: str) -> Dict[str, Any]:
        if not self._manifest.view_exists(page_name=page_name):
            return {"status": "error", "message": f"Layout view '{page_name}' not found."}
        
        script_url = self._manifest.get_view_script(page_name=page_name)

        if "/_admin/" in script_url and not self.auth_service.is_admin():
            return {"status": "unauthorized", "message": "Access Denied. Admin clearance required."}
        
        return {
            "status": "success",
            "content": f"<app-{page_name}></app-{page_name}>",
            "script_url": script_url
        }