from pathlib import Path
from typing import List, Dict
import time

class AssetManifestService:
    def __init__(self, web_dir: Path) -> None:
        self.web_dir = web_dir
        self._view_scripts: Dict[str, str] = {}
        self._css_urls: List[str] = []

        self._generate_manifest()

    def _generate_manifest(self) -> None:
        """Crawls the web folder to map out static assets"""
        self._view_scripts.clear()
        self._css_urls.clear()

        # Generate a unique timestamp for launch session
        version = int(time.time())

        # Discover all CSS styles
        for css_file in self.web_dir.rglob("*.css"):
            # Ignore index.css at the root level
            if css_file.name == "index.css":
                continue

            rel_parts = css_file.relative_to(self.web_dir).parts
            self._css_urls.append("./" + "/".join(rel_parts) + f"?v={version}")

        # Discover all JS views
        views_dir = self.web_dir / "views"
        if views_dir.exists():
            for js_file in views_dir.rglob("*.js"):
                rel_parts = js_file.relative_to(self.web_dir).parts
                self._view_scripts[js_file.stem] = "./" + "/".join(rel_parts) + f"?v={version}"

    def get_all_css(self) -> List[str]:
        return self._css_urls
    
    def get_view_script(self, page_name: str) -> str:
        return self._view_scripts.get(page_name, "")

    def view_exists(self, page_name: str) -> bool:
        return page_name in self._view_scripts