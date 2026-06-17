from typing import Dict, Any

from core.renderer.layout_service import LayoutService
from core.exceptions import ViewNotFoundException, UnauthorizedException

class LayoutController:
    def __init__(self, layout_service: LayoutService) -> None:
        self._layout_service = layout_service

    def changePage(self, page_name: str):
        try:
            layout = self._layout_service.get_page_layout(page_name=page_name)
            return {
                "status": "success",
                "content": layout["content"],
                "script_url": layout["script_url"]
            }
        
        except ViewNotFoundException as e:
            return {
                "status": "error", 
                "message": e.message
            }
        
        except UnauthorizedException as e:
            return {
                "status": "error",
                "message": e.message
            }
        
    def get_boot_assets(self) -> Dict[str, Any]:
        """Method for index.js to call at startup"""
        return {"status": "success", "css_files": self._layout_service.get_all_css()}