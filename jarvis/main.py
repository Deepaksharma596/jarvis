"""
main.py - Entry point launcher for JARVIS AI Desktop Voice Assistant (Supports PyQt5 & PyQt6)
"""
import sys
import os
import argparse
import logging

try:
    from PyQt5.QtWidgets import QApplication
except ImportError:
    from PyQt6.QtWidgets import QApplication

from config.settings import settings
from ui.app import JARVISMainWindow

def setup_logging(debug: bool = False):
    """Configure system logging."""
    log_dir = os.path.join(os.path.expanduser("~"), ".jarvis", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "jarvis.log")

    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    logging.info("Starting JARVIS AI Voice Assistant...")

def main():
    parser = argparse.ArgumentParser(description="JARVIS — AI Desktop Voice Assistant for Windows")
    parser.add_argument("--mock", action="store_true", help="Run in mock/simulation mode without executing real desktop actions.")
    parser.add_argument("--text", type=str, help="Process a single text command directly from CLI.")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug logging.")
    args = parser.parse_args()

    setup_logging(args.debug)

    if args.mock:
        settings.mock_mode = True
        logging.info("Mock mode forced via command line argument.")

    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS Voice Assistant")
    app.setQuitOnLastWindowClosed(False)

    window = JARVISMainWindow(mock_mode=args.mock)

    if args.text:
        window.show()
        window.input_line.setText(args.text)
        window._send_text_command()
    else:
        window.show()

    sys.exit(app.exec_() if hasattr(app, "exec_") else app.exec())

if __name__ == "__main__":
    main()
