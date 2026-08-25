"""
components.py - Premium Custom Qt UI Components for JARVIS (Supports PyQt5 & PyQt6)
"""
import math
try:
    from PyQt5.QtWidgets import (
        QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
        QDialog, QTextEdit, QListWidget, QListWidgetItem
    )
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QRectF
    from PyQt5.QtGui import QPainter, QColor, QBrush, QPen, QFont, QConicalGradient, QRadialGradient
    QT5 = True
except ImportError:
    from PyQt6.QtWidgets import (
        QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton,
        QDialog, QTextEdit, QListWidget, QListWidgetItem
    )
    from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRectF
    from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont, QConicalGradient, QRadialGradient
    QT5 = False

class AvatarStatusWidget(QWidget):
    """Futuristic glowing animated avatar indicating assistant state with concentric pulse & arcs."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(160, 160)
        self.status_text = "Idle"
        self.glow_color = QColor(88, 166, 255) # Neon Cyan Blue default
        self.angle = 0
        self.pulse = 0.0
        self.pulse_dir = 0.05

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(30)

    def set_status(self, status: str):
        self.status_text = status
        st_lower = status.lower()
        if "listen" in st_lower:
            self.glow_color = QColor(63, 185, 80) # Glowing Green
        elif "think" in st_lower:
            self.glow_color = QColor(188, 140, 255) # Glowing Purple/Violet
        elif "confirm" in st_lower or "wait" in st_lower:
            self.glow_color = QColor(227, 179, 65) # Glowing Amber/Gold
        elif "execut" in st_lower or "open" in st_lower or "send" in st_lower:
            self.glow_color = QColor(88, 166, 255) # Neon Cyan
        elif "error" in st_lower or "fail" in st_lower:
            self.glow_color = QColor(248, 81, 73) # Glowing Red
        else:
            self.glow_color = QColor(88, 166, 255)
        self.update()

    def _animate(self):
        self.angle = (self.angle + 4) % 360
        self.pulse += self.pulse_dir
        if self.pulse > 1.0 or self.pulse < 0.0:
            self.pulse_dir = -self.pulse_dir
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        antialiasing = QPainter.Antialiasing if QT5 else QPainter.RenderHint.Antialiasing
        align_center = Qt.AlignCenter if QT5 else Qt.AlignmentFlag.AlignCenter

        painter.setRenderHint(antialiasing)

        w, h = self.width(), self.height()
        cx, cy = w // 2, (h // 2) - 10
        base_r = min(w, h) // 4

        # 1. Radial Background Glow
        radial = QRadialGradient(cx, cy, base_r * 2)
        c_glow = QColor(self.glow_color)
        c_glow.setAlpha(int(40 + 30 * self.pulse))
        radial.setColorAt(0, c_glow)
        radial.setColorAt(1, QColor(13, 17, 23, 0))
        painter.setBrush(QBrush(radial))
        painter.setPen(Qt.NoPen if QT5 else Qt.PenStyle.NoPen)
        painter.drawEllipse(cx - base_r * 2, cy - base_r * 2, base_r * 4, base_r * 4)

        # 2. Spinning Outer Arc
        pen_arc = QPen(self.glow_color, 3)
        pen_arc.setCapStyle(Qt.RoundCap if QT5 else Qt.PenCapStyle.RoundCap)
        painter.setPen(pen_arc)
        arc_rect = QRectF(cx - base_r - 12, cy - base_r - 12, (base_r + 12) * 2, (base_r + 12) * 2)
        painter.drawArc(arc_rect, int(-self.angle * 16), 120 * 16)
        painter.drawArc(arc_rect, int((-self.angle + 180) * 16), 90 * 16)

        # 3. Inner Pulsing Core
        core_r = base_r + int(4 * self.pulse)
        painter.setPen(Qt.NoPen if QT5 else Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.glow_color))
        painter.drawEllipse(cx - core_r, cy - core_r, core_r * 2, core_r * 2)

        # 4. Status Text Pill
        pill_w, pill_h = 130, 26
        pill_rect = QRectF(cx - pill_w // 2, h - 34, pill_w, pill_h)
        painter.setBrush(QBrush(QColor(22, 27, 34, 210)))
        pen_pill = QPen(self.glow_color, 1)
        painter.setPen(pen_pill)
        painter.drawRoundedRect(pill_rect, 13, 13)

        painter.setPen(QColor(240, 246, 252))
        font = QFont("Segoe UI", 9, QFont.Bold if QT5 else QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(pill_rect, align_center, self.status_text)

class ConfirmationDialog(QDialog):
    """User prompt modal asking for confirmation before executing high-impact actions."""

    def __init__(self, action_name: str, details: str, prompt_text: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("JARVIS Safety Authorization")
        self.resize(440, 230)
        self.user_approved = False

        layout = QVBoxLayout(self)

        title = QLabel(f"⚠️ Action Authorization: {action_name}")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #e3b341;")
        layout.addWidget(title)

        msg = QLabel(prompt_text)
        msg.setWordWrap(True)
        msg.setStyleSheet("font-size: 14px; color: #c9d1d9;")
        layout.addWidget(msg)

        details_box = QTextEdit()
        details_box.setReadOnly(True)
        details_box.setPlainText(str(details))
        details_box.setMaximumHeight(70)
        layout.addWidget(details_box)

        btn_layout = QHBoxLayout()
        approve_btn = QPushButton("Authorize & Send")
        approve_btn.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #238636, stop:1 #2ea043); color: white;")
        approve_btn.clicked.connect(self._approve)

        deny_btn = QPushButton("Deny Action")
        deny_btn.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b62324, stop:1 #da3633); color: white;")
        deny_btn.clicked.connect(self._deny)

        btn_layout.addWidget(approve_btn)
        btn_layout.addWidget(deny_btn)
        layout.addLayout(btn_layout)

    def _approve(self):
        self.user_approved = True
        self.accept()

    def _deny(self):
        self.user_approved = False
        self.reject()
