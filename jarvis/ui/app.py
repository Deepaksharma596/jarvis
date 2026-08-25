"""
app.py - Translucent Glassmorphism PyQt Desktop Application GUI for JARVIS
"""
import sys
import threading
import logging

try:
    from PyQt5.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
        QLineEdit, QPushButton, QLabel, QListWidget, QListWidgetItem,
        QSplitter, QMessageBox, QApplication, QShortcut
    )
    from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread, QEventLoop, QPoint
    from PyQt5.QtGui import QFont, QKeySequence
    QT5 = True
except ImportError:
    from PyQt6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
        QLineEdit, QPushButton, QLabel, QListWidget, QListWidgetItem,
        QSplitter, QMessageBox, QApplication, QShortcut
    )
    from PyQt6.QtCore import Qt, pyqtSignal, QObject, QThread, QEventLoop, QPoint
    from PyQt6.QtGui import QFont, QKeySequence
    QT5 = False

from config.settings import settings
from config.constants import EMERGENCY_STOP_HOTKEY
from core.agent import JARVISAgent
from voice.text_to_speech import tts_engine
from voice.speech_to_text import stt_engine
from voice.wake_word import WakeWordDetector
from ui.styles import DARK_GLASS_QSS
from ui.components import AvatarStatusWidget, ConfirmationDialog
from ui.settings_dialog import SettingsDialog
from ui.tray import SystemTrayManager

class AgentWorkerSignals(QObject):
    status_changed = pyqtSignal(str)
    message_received = pyqtSignal(str, str) # sender, text
    plan_created = pyqtSignal(dict)
    confirmation_requested = pyqtSignal(str, dict, str)
    finished = pyqtSignal(str)

class CustomTitleBar(QWidget):
    """Sleek Frameless Window Glass TitleBar with window dragging and window controls."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("title_bar")
        self.parent_window = parent
        self.drag_position = QPoint()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)

        title_label = QLabel("🤖 JARVIS AI Assistant")
        title_label.setObjectName("title_label")

        bold_font = QFont.Bold if QT5 else QFont.Weight.Bold
        title_label.setFont(QFont("Segoe UI", 11, bold_font))

        self.min_btn = QPushButton("─")
        self.min_btn.setProperty("class", "title_btn")
        self.min_btn.setFixedSize(30, 26)
        self.min_btn.clicked.connect(self.parent_window.showMinimized)

        self.max_btn = QPushButton("▢")
        self.max_btn.setProperty("class", "title_btn")
        self.max_btn.setFixedSize(30, 26)
        self.max_btn.clicked.connect(self._toggle_maximize)

        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("close_title_btn")
        self.close_btn.setFixedSize(30, 26)
        self.close_btn.clicked.connect(self.parent_window.close)

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(self.min_btn)
        layout.addWidget(self.max_btn)
        layout.addWidget(self.close_btn)

    def _toggle_maximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
        else:
            self.parent_window.showMaximized()

    def mousePressEvent(self, event):
        left_button = Qt.LeftButton if QT5 else Qt.MouseButton.LeftButton
        if event.button() == left_button:
            self.drag_position = event.globalPos() - self.parent_window.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        left_button = Qt.LeftButton if QT5 else Qt.MouseButton.LeftButton
        if event.buttons() == left_button:
            self.parent_window.move(event.globalPos() - self.drag_position)
            event.accept()

class JARVISMainWindow(QMainWindow):
    """Main Translucent Glassmorphism Desktop Window for JARVIS."""

    confirmation_response_signal = pyqtSignal(bool)

    def __init__(self, mock_mode: bool = False):
        super().__init__()
        self.mock_mode = mock_mode
        if mock_mode:
            settings.mock_mode = True

        self.agent = JARVISAgent()
        self.signals = AgentWorkerSignals()

        # Transparent Window Attributes
        self.setAttribute(Qt.WA_TranslucentBackground)
        frameless = (Qt.FramelessWindowHint | Qt.WindowSystemMenuHint | Qt.WindowMinMaxButtonsHint) if QT5 else (Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowSystemMenuHint | Qt.WindowType.WindowMinMaxButtonsHint)
        self.setWindowFlags(frameless)

        self._init_ui()
        self._init_tray()
        self._init_emergency_stop()
        self._init_signals()

        # Start Wake Word Listener
        self.wake_detector = WakeWordDetector(on_wake_detected=self._on_wake_word_triggered)
        if settings.wake_word_enabled and not mock_mode:
            self.wake_detector.start()

    def _init_ui(self):
        self.setWindowTitle("JARVIS — AI Desktop Voice Assistant")
        self.resize(1020, 700)
        self.setStyleSheet(DARK_GLASS_QSS)

        align_center = Qt.AlignCenter if QT5 else Qt.AlignmentFlag.AlignCenter
        horiz_orient = Qt.Horizontal if QT5 else Qt.Orientation.Horizontal
        bold_font = QFont.Bold if QT5 else QFont.Weight.Bold

        # Central Translucent Container Card
        self.main_container = QWidget()
        self.main_container.setObjectName("main_container")
        container_layout = QVBoxLayout(self.main_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Custom TitleBar
        self.title_bar = CustomTitleBar(self)
        container_layout.addWidget(self.title_bar)

        # Body Layout
        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(16, 12, 16, 16)

        # Left Panel: Avatar + Controls + Chat
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Action Bar (Settings & Emergency Stop)
        action_bar = QHBoxLayout()
        self.settings_btn = QPushButton("⚙️ Settings")
        self.settings_btn.clicked.connect(self._open_settings)

        self.stop_btn = QPushButton("⏹️ Emergency Stop")
        self.stop_btn.setObjectName("stop_button")
        self.stop_btn.setToolTip(f"Global Emergency Stop ({EMERGENCY_STOP_HOTKEY.upper()})")
        self.stop_btn.clicked.connect(self._trigger_emergency_stop)

        action_bar.addStretch()
        action_bar.addWidget(self.settings_btn)
        action_bar.addWidget(self.stop_btn)
        left_layout.addLayout(action_bar)

        # Glowing Avatar Widget
        self.avatar_widget = AvatarStatusWidget()
        left_layout.addWidget(self.avatar_widget, alignment=align_center)

        # Conversation Log
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        left_layout.addWidget(self.chat_display, stretch=1)

        # Input Row
        input_layout = QHBoxLayout()
        self.mic_btn = QPushButton("🎙️")
        self.mic_btn.setObjectName("mic_button")
        self.mic_btn.setFixedSize(50, 50)
        self.mic_btn.clicked.connect(self._toggle_voice_input)

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Type a command (e.g. 'Send Rahul a WhatsApp message saying I'll reach at 7')...")
        self.input_line.returnPressed.connect(self._send_text_command)

        self.send_btn = QPushButton("Send")
        self.send_btn.setFixedHeight(46)
        self.send_btn.clicked.connect(self._send_text_command)

        input_layout.addWidget(self.mic_btn)
        input_layout.addWidget(self.input_line, stretch=1)
        input_layout.addWidget(self.send_btn)
        left_layout.addLayout(input_layout)

        # Right Panel: Task Plan Step List
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_panel.setMinimumWidth(310)

        plan_title = QLabel("📋 Execution Plan Steps")
        plan_title.setFont(QFont("Segoe UI", 12, bold_font))
        plan_title.setStyleSheet("color: #8b949e;")
        right_layout.addWidget(plan_title)

        self.plan_list_widget = QListWidget()
        right_layout.addWidget(self.plan_list_widget, stretch=1)

        splitter = QSplitter(horiz_orient)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([690, 310])

        body_layout.addWidget(splitter)
        container_layout.addWidget(body_widget, stretch=1)

        self.setCentralWidget(self.main_container)

    def _init_tray(self):
        self.tray_manager = SystemTrayManager(self)
        self.tray_manager.open_requested.connect(self.showNormal)
        self.tray_manager.voice_requested.connect(self._toggle_voice_input)
        self.tray_manager.settings_requested.connect(self._open_settings)
        self.tray_manager.exit_requested.connect(QApplication.quit)

    def _init_emergency_stop(self):
        self.emergency_shortcut = QShortcut(QKeySequence("Ctrl+Shift+Esc"), self)
        self.emergency_shortcut.activated.connect(self._trigger_emergency_stop)

    def _init_signals(self):
        self.signals.status_changed.connect(self.avatar_widget.set_status)
        self.signals.message_received.connect(self._append_message)
        self.signals.plan_created.connect(self._update_plan_view)
        self.signals.confirmation_requested.connect(self._prompt_user_confirmation)

    def _append_message(self, sender: str, text: str):
        is_user = "User" in sender
        bg_color = "rgba(31, 111, 235, 0.25)" if is_user else "rgba(46, 160, 67, 0.2)"
        border_color = "rgba(88, 166, 255, 0.4)" if is_user else "rgba(63, 185, 80, 0.4)"
        color_tag = "#58a6ff" if is_user else "#3fb950"
        
        formatted = f'<div style="margin-bottom:10px; padding:10px 14px; background-color:{bg_color}; border:1px solid {border_color}; border-radius:10px;"><b style="color:{color_tag};">{sender}:</b> <span style="color:#f0f6fc;">{text}</span></div>'
        self.chat_display.append(formatted)

    def _update_plan_view(self, plan_dict: dict):
        self.plan_list_widget.clear()
        steps = plan_dict.get("steps", [])
        for step in steps:
            st = step.get("status", "pending")
            icon = "⏳" if st == "pending" else "🔄" if st == "in_progress" else "✅" if st == "completed" else "❌"
            txt = f"{icon} Step {step.get('step_number')}: {step.get('description')}"
            item = QListWidgetItem(txt)
            self.plan_list_widget.addItem(item)

    def _send_text_command(self):
        text = self.input_line.text().strip()
        if not text:
            return
        self.input_line.clear()
        self._append_message("User", text)
        self._process_command_async(text)

    def _toggle_voice_input(self):
        self.mic_btn.setProperty("listening", "true")
        self.mic_btn.setStyle(self.mic_btn.style())
        self.signals.status_changed.emit("Listening...")

        def _voice_thread():
            transcription = stt_engine.listen_and_transcribe(timeout=5.0)
            self.mic_btn.setProperty("listening", "false")
            self.mic_btn.setStyle(self.mic_btn.style())
            if transcription:
                self.signals.message_received.emit("User (Voice)", transcription)
                self._process_command_async(transcription)
            else:
                self.signals.status_changed.emit("Idle")

        threading.Thread(target=_voice_thread, daemon=True).start()

    def _on_wake_word_triggered(self):
        self.tray_manager.show_notification("JARVIS Awakened", "Listening for your voice command...")
        self._toggle_voice_input()

    def _process_command_async(self, command_text: str):
        self.signals.status_changed.emit("Thinking...")

        def _worker():
            def confirmation_cb(action_name: str, details: dict, prompt_msg: str) -> bool:
                self.signals.status_changed.emit("Waiting for confirmation...")
                self.signals.confirmation_requested.emit(action_name, details, prompt_msg)
                
                loop = QEventLoop()
                response = [False]
                def _on_res(val):
                    response[0] = val
                    loop.quit()
                self.confirmation_response_signal.connect(_on_res)
                loop.exec()
                return response[0]

            response_text, task_plan = self.agent.process_request(command_text, confirmation_cb)
            if task_plan:
                self.signals.plan_created.emit(task_plan.to_dict())

            self.signals.message_received.emit("JARVIS", response_text)
            self.signals.status_changed.emit("Completed")
            
            tts_engine.speak(response_text)

        threading.Thread(target=_worker, daemon=True).start()

    def _prompt_user_confirmation(self, action_name: str, details: dict, prompt_msg: str):
        dialog = ConfirmationDialog(action_name, str(details), prompt_msg, self)
        dialog.exec()
        self.confirmation_response_signal.emit(dialog.user_approved)

    def _trigger_emergency_stop(self):
        tts_engine.stop()
        self.signals.status_changed.emit("Emergency Stop Activated!")
        self.tray_manager.show_notification("EMERGENCY STOP", "All automations and speech halted immediately.")
        QMessageBox.warning(self, "Emergency Stop", "Emergency stop triggered! All mouse, keyboard, and AI executions halted.")

    def _open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec()

    def closeEvent(self, event):
        """Minimize to System Tray on close instead of exiting completely."""
        if self.tray_manager.tray_icon.isVisible():
            self.hide()
            self.tray_manager.show_notification("JARVIS Minimized", "Running in system tray.")
            event.ignore()
        else:
            event.accept()
