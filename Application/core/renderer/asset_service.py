# core/renderer/asset_manifest.py
from pathlib import Path
import time
from typing import List, Dict

class AssetResolverService:
    def __init__(self, web_dir: Path) -> None:
        self.web_dir = web_dir
        self._view_scripts: Dict[str, str] = {}
        self._css_urls: List[str] = []
        
        self.initialize_manifest()

    def initialize_manifest(self) -> None:
        """Crawls the web folder to map out static assets (POSIX compliant)."""
        self._view_scripts.clear()
        self._css_urls.clear()

        # Cache-busting timestamp for the application session
        version = int(time.time())
        query_string = f"?v={version}"

        # 1. Discover CSS Stylesheets
        index_style: str | None = None
        for css_file in self.web_dir.rglob("*.css"):
            # .as_posix() guarantees forward slashes (/) even on Windows
            rel_path = css_file.relative_to(self.web_dir).as_posix()
            asset_url = f"./{rel_path}{query_string}"

            if css_file.name == "index.css":
                index_style = asset_url
            else:
                self._css_urls.append(asset_url)

        # Ensure index.css is always injected first in the DOM cascade
        if index_style:
            self._css_urls.insert(0, index_style)

        # 2. Discover JavaScript Views
        views_dir = self.web_dir / "views"
        if views_dir.exists():
            for js_file in views_dir.rglob("*.js"):
                rel_path = js_file.relative_to(self.web_dir).as_posix()
                # Store by view name (e.g., 'dashboard' -> './views/dashboard.js?v=123')
                self._view_scripts[js_file.stem] = f"./{rel_path}{query_string}"

    def get_all_css(self) -> List[str]:
        return self._css_urls
    
    def resolve_view_script(self, page_name: str) -> str:
        """NestJS naming pattern: 'resolve' sounds intentional for an asset locator"""
        return self._view_scripts.get(page_name, "")

    def has_view(self, page_name: str) -> bool:
        return page_name in self._view_scripts