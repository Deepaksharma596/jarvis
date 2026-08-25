"""
tray.py - Windows System Tray Integration for JARVIS (Supports PyQt5 & PyQt6)
"""
try:
    from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
    from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
    from PyQt5.QtCore import pyqtSignal, QObject
    QT5 = True
except ImportError:
    from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
    from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor
    from PyQt6.QtCore import pyqtSignal, QObject
    QT5 = False

def create_default_tray_icon() -> QIcon:
    """Generate default tray icon pixmap."""
    pixmap = QPixmap(32, 32)
    pixmap.fill(QColor(0, 0, 0, 0))
    painter = QPainter(pixmap)
    antialiasing = QPainter.Antialiasing if QT5 else QPainter.RenderHint.Antialiasing
    painter.setRenderHint(antialiasing)
    painter.setBrush(QColor(88, 166, 255))
    painter.setPen(QColor(240, 246, 252))
    painter.drawEllipse(2, 2, 28, 28)
    painter.end()
    return QIcon(pixmap)

class SystemTrayManager(QObject):
    """Manages Windows System Tray icon, menu actions, and minimize-to-tray logic."""

    open_requested = pyqtSignal()
    voice_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    exit_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tray_icon = QSystemTrayIcon(create_default_tray_icon(), parent)
        self.tray_icon.setToolTip("JARVIS AI Voice Assistant")

        # Tray Context Menu
        menu = QMenu()
        open_action = menu.addAction("Open JARVIS")
        open_action.triggered.connect(self.open_requested.emit)

        voice_action = menu.addAction("Start Voice Mode")
        voice_action.triggered.connect(self.voice_requested.emit)

        settings_action = menu.addAction("Settings")
        settings_action.triggered.connect(self.settings_requested.emit)

        menu.addSeparator()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.exit_requested.emit)

        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self._on_activated)
        self.tray_icon.show()

    def _on_activated(self, reason):
        trig = QSystemTrayIcon.Trigger if QT5 else QSystemTrayIcon.ActivationReason.Trigger
        dbl = QSystemTrayIcon.DoubleClick if QT5 else QSystemTrayIcon.ActivationReason.DoubleClick
        if reason == trig or reason == dbl:
            self.open_requested.emit()

    def show_notification(self, title: str, message: str):
        """Display Windows system tray balloon notification."""
        icon = QSystemTrayIcon.Information if QT5 else QSystemTrayIcon.MessageIcon.Information
        self.tray_icon.showMessage(title, message, icon, 3000)
