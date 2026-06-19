from core.app import QSTARApp
from core.log.logger import setup_logger

if __name__ == "__main__":
    setup_logger()
    app = QSTARApp(devMode=True)
    app.run()