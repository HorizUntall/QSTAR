from typing import List
from core.exceptions import ViewNotFoundException, UnauthorizedException
from core.renderer.asset_service import AssetResolverService
from core.state import app_state

class LayoutService:
    def __init__(self, asset_service: AssetResolverService) -> None:
        self.asset_service = asset_service
        
    def get_page_layout(self, page_name: str) -> str:
        if not self.asset_service.has_view(page_name=page_name):
            raise ViewNotFoundException(f"{page_name} view is not found.")
        
        script_url = self.asset_service.resolve_view_script(page_name=page_name)

        if "/_admin/" in script_url and not app_state.is_admin_logged_in:
            raise UnauthorizedException("Access Denied. Admin clearance required.")
        
        # Auto Log out when going to non-admin pages
        if "/_admin" not in script_url:
            app_state.log_out()

        return {
            "content": f"<app-{page_name}></app-{page_name}>",
            "script_url": script_url
        }
    
    def get_all_css(self) -> List[str]:
        return self.asset_service.get_all_css()