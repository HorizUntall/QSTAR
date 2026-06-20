import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, Any
import os
from datetime import datetime

CONFIG_PATH = Path("C:/QSTAR/Data/config.json")

DEFAULT_CONFIG_BLUEPRINT = {
    "school_name": "Philippine Science High School - Zamboanga Peninsula Region Campus",
    "admin_key": None,
    "scrypt_salt": None,
    "scrypt_n": 16384,
    "scrypt_r": 8,
    "scrypt_p": 1,
    "last_updated": None
}

# 1. In-memory cache to avoid reading from the hard drive every single second
_config_cache: Dict[str, Any] = {}

def _generate_initial_config() -> Dict[str, Any]:
    """Generates the fresh default configuration values dynamically once."""
    config = DEFAULT_CONFIG_BLUEPRINT.copy()

    salt = os.urandom(16)
    default_password = "admin123".encode('utf-8')
    key = hashlib.scrypt(
        password=default_password, 
        salt=salt,
        n=config["scrypt_n"],
        r=config["scrypt_r"],
        p=config["scrypt_p"]
    )
    
    config["admin_key"] = key
    config["scrypt_salt"] = salt
    config["last_updated"] = datetime.now()
    return config

def _serialize_config(config_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Converts bytes and datetimes to JSON-serializable types."""
    serialized = config_dict.copy()
    
    if isinstance(serialized.get("admin_key"), bytes):
        serialized["admin_key"] = serialized["admin_key"].hex()
        
    if isinstance(serialized.get("scrypt_salt"), bytes):
        serialized["scrypt_salt"] = serialized["scrypt_salt"].hex()
        
    if isinstance(serialized.get("last_updated"), datetime):
        serialized["last_updated"] = serialized["last_updated"].isoformat()
        
    return serialized

def _deserialize_config(config_dict: Dict[str, Any]) -> Dict[str, Any]:
    """Converts hex strings and ISO datetimes back to bytes and datetimes."""
    deserialized = config_dict.copy()
    
    if "admin_key" in deserialized and isinstance(deserialized["admin_key"], str):
        deserialized["admin_key"] = bytes.fromhex(deserialized["admin_key"])
        
    if "scrypt_salt" in deserialized and isinstance(deserialized["scrypt_salt"], str):
        deserialized["scrypt_salt"] = bytes.fromhex(deserialized["scrypt_salt"])
        
    if "last_updated" in deserialized and isinstance(deserialized["last_updated"], str):
        try:
            deserialized["last_updated"] = datetime.fromisoformat(deserialized["last_updated"])
        except ValueError:
            pass

    return deserialized

def _load_config() -> Dict[str, Any]:
    global _config_cache
    
    # Return cache if we already read it during this run loop
    if _config_cache:
        return _config_cache

    if not CONFIG_PATH.is_file():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        _config_cache = _generate_initial_config()
        _save_config_file(_config_cache)
        return _config_cache

    try:
        with open(CONFIG_PATH, "r") as f:
            raw_data = json.load(f)
            _config_cache = _deserialize_config(raw_data)
            return _config_cache
    except Exception:
        logging.exception("Failed reading config file. Raising error to prevent password overwrites.")
        # 2. CRITICAL: Do NOT auto-generate a new password salt if the file merely has a syntax error! 
        # Raise an exception so the application safely stops instead of locking users out.
        raise RuntimeError("Configuration file is corrupted. Fix or backup and delete to reset.")

def _save_config_file(config: Dict[str, Any]) -> None:
    """Helper to safely write to the configuration file atomically."""
    temp_path = CONFIG_PATH.with_suffix(".tmp")
    try:
        with open(temp_path, "w") as f:
            json.dump(_serialize_config(config), f, indent=4)
        # Atomic replacement: prevents half-written files if power cuts or app crashes
        temp_path.replace(CONFIG_PATH)
    except Exception:
        if temp_path.is_file():
            temp_path.unlink()
        raise

def get_data(key: str) -> Any:
    config = _load_config()
    return config.get(key)

def change_data(key: str, val: Any) -> None:
    config = _load_config()
    config[key] = val
    config["last_updated"] = datetime.now()
    _save_config_file(config)