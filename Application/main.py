from core.app import QSTARApp
from core.log.logger import setup_logger

if __name__ == "__main__":
    setup_logger()
    # We pass devMode=False since production deployments use the Launcher loop
    app = QSTARApp(devMode=True)
    app.run()