import argparse
from core.app import QSTARApp
from core.log.logger import setup_logger

def parse_args():
    parser = argparse.ArgumentParser(description="Run the QSTAR Application")

    # Creates --dev and --no-dev flags
    parser.add_argument(
        "--dev",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Enable or disable devMode (e.g., --dev or --no-dev). By default, devMode is set to False"
    )

    return parser.parse_args()

if __name__ == "__main__":
    setup_logger()

    args = parse_args()

    # We pass devMode=False since production deployments use the Launcher loop
    app = QSTARApp(devMode=args.dev)
    app.run()