"""
app.py - Mobile Responsive GUI Interface for JARVIS Mobile
"""
import sys
import os

try:
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTextEdit, QLineEdit, QMessageBox
    )
    from PyQt5.QtCore import Qt
    from PyQt5.QtGui import QFont
    QT5 = True
except ImportError:
    from PyQt6.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QPushButton, QTextEdit, QLineEdit, QMessageBox
    )
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QFont
    QT5 = False

from mobile.services.background_service import JARVISBackgroundService
from mobile.banking_guard import BankingGuard
from config.settings import settings

class JARVISMobileWindow(QWidget):
    """JARVIS Mobile Interface."""

    def __init__(self):
        super().__init__()
        self.service = JARVISBackgroundService()
        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle("JARVIS Mobile Assistant")
        self.resize(380, 640) # Mobile Aspect Ratio
        self.setStyleSheet("""
            QWidget {
                background-color: #0d1117;
                color: #c9d1d9;
                font-family: 'Segoe UI', sans-serif;
            }
            QLabel#status_pill {
                background-color: rgba(35, 134, 54, 0.3);
                border: 1px solid #238636;
                border-radius: 12px;
                padding: 6px 14px;
                color: #3fb950;
                font-weight: bold;
            }
            QPushButton {
                background-color: #21262d;
                border: 1px solid #30363d;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton#toggle_svc_btn {
                background-color: #238636;
                color: white;
            }
        """)

        layout = QVBoxLayout(self)

        header = QLabel("📱 JARVIS Mobile")
        header.setFont(QFont("Segoe UI", 16, QFont.Bold if QT5 else QFont.Weight.Bold))
        header.setAlignment(Qt.AlignCenter if QT5 else Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #58a6ff; margin-top: 10px;")
        layout.addWidget(header)

        self.status_pill = QLabel("🟢 Background Service: ACTIVE")
        self.status_pill.setObjectName("status_pill")
        self.status_pill.setAlignment(Qt.AlignCenter if QT5 else Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_pill)

        sub_info = QLabel("Say 'Jarvis' anywhere on phone to activate voice commands.\n\n🛡️ Banking & Financial Apps Protection: ENABLED")
        sub_info.setWordWrap(True)
        sub_info.setStyleSheet("color: #8b949e; font-size: 12px; padding: 10px;")
        layout.addWidget(sub_info)

        self.chat_box = QTextEdit()
        self.chat_box.setReadOnly(True)
        layout.addWidget(self.chat_box, stretch=1)

        self.toggle_svc_btn = QPushButton("Stop Background Service")
        self.toggle_svc_btn.setObjectName("toggle_svc_btn")
        self.toggle_svc_btn.clicked.connect(self._toggle_service)
        layout.addWidget(self.toggle_svc_btn)

        # Start Background Service by default
        self.service.start_service()

    def _toggle_service(self):
        if self.service.is_running:
            self.service.stop_service()
            self.status_pill.setText("🔴 Background Service: STOPPED")
            self.status_pill.setStyleSheet("background-color: rgba(218, 54, 51, 0.3); border: 1px solid #da3633; color: #f85149;")
            self.toggle_svc_btn.setText("Start Background Service")
        else:
            self.service.start_service()
            self.status_pill.setText("🟢 Background Service: ACTIVE")
            self.status_pill.setStyleSheet("background-color: rgba(35, 134, 54, 0.3); border: 1px solid #238636; color: #3fb950;")
            self.toggle_svc_btn.setText("Stop Background Service")
