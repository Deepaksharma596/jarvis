"""
main.py - Mobile Entry Point for JARVIS Mobile Assistant
"""
import sys
import os

# Add parent jarvis folder to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PyQt5.QtWidgets import QApplication
from mobile.app import JARVISMobileWindow
from config.settings import settings

def main():
    if "--mock" in sys.argv:
        settings.mock_mode = True

    app = QApplication(sys.argv)
    window = JARVISMobileWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
