import json
from pathlib import Path
from core.exceptions import VersionFileNotFoundException
import logging

version_path: Path | None = None

def get_app_version() -> str:
    if version_path is None:
        raise VersionFileNotFoundException("version path not initialized")
    
    try:
        with open(version_path, "r") as f:
            data = json.load(f)
            return data["version"]
    except Exception as e:
        logging.exception("Failed reading the version file.", e)
        raise VersionFileNotFoundException