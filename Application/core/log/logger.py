import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

LOG_DIR: Path = Path("C:/QSTAR/Data/logs")
LOG_FILE: Path = LOG_DIR / "app.log"

def setup_logger():
    LOG_DIR.parent.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        LOG_DIR,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    return logger

