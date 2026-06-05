import json
import hashlib
import logging
from pathlib import Path

CONFIG_PATH = Path("C:/QSTAR/Data/config.json")

# Default fallback settings (Default Password: "admin123")
DEFAULT_CONFIG = {
    "school_name": "High School Campus",
    "academic_year": "2025-2026",
    "admin_password_hash": "240aa35473d06c11d1e4602a76d3125a0d341b52a4cf535b91b8d27d73f4e24c"
}

def load_config() -> dict[str, str]:
    if not CONFIG_PATH.is_file():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception:
        logging.exception("Failed reading config file")
        return DEFAULT_CONFIG

def verify_admin_password(input_pw: str) -> bool:
    config = load_config()
    input_hash = hashlib.sha256(input_pw.encode()).hexdigest()
    return input_hash == config["admin_password_hash"]