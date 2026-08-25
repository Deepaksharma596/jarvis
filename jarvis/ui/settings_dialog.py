"""
settings_dialog.py - Configuration Settings Dialog for JARVIS (Supports PyQt5 & PyQt6)
"""
try:
    from PyQt5.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
        QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton, QMessageBox
    )
    QT5 = True
except ImportError:
    from PyQt6.QtWidgets import (
        QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
        QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton, QMessageBox
    )
    QT5 = False

from config.settings import settings
from security.credentials import CredentialManager

class SettingsDialog(QDialog):
    """GUI Tabbed Settings Dialog for JARVIS."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("JARVIS Settings & Configuration")
        self.resize(520, 420)

        layout = QVBoxLayout(self)
        self.tabs = QTabWidget()

        # Tab 1: AI Provider & Credentials
        ai_tab = QWidget()
        ai_layout = QVBoxLayout(ai_tab)
        
        ai_layout.addWidget(QLabel("AI Provider:"))
        self.ai_provider_combo = QComboBox()
        self.ai_provider_combo.addItems(["gemini", "openai", "ollama", "mock"])
        self.ai_provider_combo.setCurrentText(settings.ai_provider)
        ai_layout.addWidget(self.ai_provider_combo)

        ai_layout.addWidget(QLabel("Gemini API Key:"))
        self.gemini_key_input = QLineEdit()
        pwd_mode = QLineEdit.Password if QT5 else QLineEdit.EchoMode.Password
        self.gemini_key_input.setEchoMode(pwd_mode)
        self.gemini_key_input.setText(CredentialManager.get_credential("GEMINI_API_KEY"))
        ai_layout.addWidget(self.gemini_key_input)

        ai_layout.addWidget(QLabel("OpenAI API Key:"))
        self.openai_key_input = QLineEdit()
        self.openai_key_input.setEchoMode(pwd_mode)
        self.openai_key_input.setText(CredentialManager.get_credential("OPENAI_API_KEY"))
        ai_layout.addWidget(self.openai_key_input)

        ai_layout.addStretch()
        self.tabs.addTab(ai_tab, "AI & Models")

        # Tab 2: Voice & Wake Word
        voice_tab = QWidget()
        voice_layout = QVBoxLayout(voice_tab)

        self.wake_word_cb = QCheckBox("Enable Wake Word Detection")
        self.wake_word_cb.setChecked(settings.wake_word_enabled)
        voice_layout.addWidget(self.wake_word_cb)

        voice_layout.addWidget(QLabel("Wake Word:"))
        self.wake_word_input = QLineEdit(settings.wake_word)
        voice_layout.addWidget(self.wake_word_input)

        voice_layout.addWidget(QLabel("TTS Voice:"))
        self.voice_combo = QComboBox()
        self.voice_combo.addItems(["en-US-AriaNeural", "en-US-GuyNeural", "hi-IN-SwaraNeural", "hi-IN-MadhurNeural"])
        self.voice_combo.setCurrentText(settings.tts_voice)
        voice_layout.addWidget(self.voice_combo)

        voice_layout.addStretch()
        self.tabs.addTab(voice_tab, "Voice & Audio")

        # Tab 3: Security & Confirmation
        sec_tab = QWidget()
        sec_layout = QVBoxLayout(sec_tab)

        sec_layout.addWidget(QLabel("Confirmation Mode:"))
        self.conf_mode_combo = QComboBox()
        self.conf_mode_combo.addItems(["STRICT", "BALANCED", "TRUSTED"])
        self.conf_mode_combo.setCurrentText(settings.confirmation_mode)
        sec_layout.addWidget(self.conf_mode_combo)

        sec_layout.addWidget(QLabel("Trusted Contacts (comma separated):"))
        self.trusted_contacts_input = QLineEdit(", ".join(settings.trusted_contacts))
        sec_layout.addWidget(self.trusted_contacts_input)

        sec_layout.addStretch()
        self.tabs.addTab(sec_tab, "Safety & Permissions")

        layout.addWidget(self.tabs)

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save Settings")
        save_btn.setStyleSheet("background-color: #238636; color: white;")
        save_btn.clicked.connect(self._save)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def _save(self):
        settings.ai_provider = self.ai_provider_combo.currentText()
        settings.wake_word_enabled = self.wake_word_cb.isChecked()
        settings.wake_word = self.wake_word_input.text().strip()
        settings.tts_voice = self.voice_combo.currentText()
        settings.confirmation_mode = self.conf_mode_combo.currentText()
        
        contacts = [c.strip() for c in self.trusted_contacts_input.text().split(",") if c.strip()]
        settings.trusted_contacts = contacts
        settings.save()

        if self.gemini_key_input.text():
            CredentialManager.set_credential("GEMINI_API_KEY", self.gemini_key_input.text().strip())
        if self.openai_key_input.text():
            CredentialManager.set_credential("OPENAI_API_KEY", self.openai_key_input.text().strip())

        QMessageBox.information(self, "Settings Saved", "JARVIS settings have been updated successfully.")
        self.accept()
