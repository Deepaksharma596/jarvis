"""
styles.py - Premium Dark Glassmorphism QSS Styling for JARVIS
"""

DARK_GLASS_QSS = """
/* Global Window Transparency & Styling */
QMainWindow {
    background: transparent;
}

QWidget#main_container {
    background-color: rgba(13, 17, 23, 0.88);
    border: 1px solid rgba(88, 166, 255, 0.25);
    border-radius: 16px;
    color: #c9d1d9;
    font-family: 'Segoe UI', 'Roboto', 'Outfit', sans-serif;
}

/* Custom TitleBar */
QWidget#title_bar {
    background-color: rgba(22, 27, 34, 0.75);
    border-top-left-radius: 16px;
    border-top-right-radius: 16px;
    border-bottom: 1px solid rgba(48, 54, 61, 0.6);
    padding: 4px 12px;
}

QLabel#title_label {
    color: #58a6ff;
    font-size: 15px;
    font-weight: 700;
}

QPushButton.title_btn {
    background: transparent;
    border: none;
    color: #8b949e;
    font-size: 14px;
    padding: 4px 8px;
    border-radius: 4px;
}

QPushButton.title_btn:hover {
    background-color: rgba(255, 255, 255, 0.1);
    color: #ffffff;
}

QPushButton#close_title_btn:hover {
    background-color: #da3633;
    color: #ffffff;
}

/* Group Boxes & Panels */
QGroupBox {
    border: 1px solid rgba(48, 54, 61, 0.7);
    border-radius: 12px;
    margin-top: 12px;
    padding-top: 10px;
    font-weight: bold;
    color: #58a6ff;
    background-color: rgba(22, 27, 34, 0.4);
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

/* Text Input & Log Area */
QTextEdit, QLineEdit {
    background-color: rgba(22, 27, 34, 0.7);
    border: 1px solid rgba(48, 54, 61, 0.8);
    border-radius: 10px;
    padding: 10px 14px;
    color: #f0f6fc;
    font-size: 14px;
    selection-background-color: #1f6feb;
}

QTextEdit:focus, QLineEdit:focus {
    border: 1px solid #58a6ff;
    background-color: rgba(22, 27, 34, 0.9);
}

/* Action Buttons */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #21262d, stop:1 #30363d);
    border: 1px solid rgba(88, 166, 255, 0.2);
    border-radius: 10px;
    padding: 8px 18px;
    color: #c9d1d9;
    font-weight: 600;
    font-size: 13px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #30363d, stop:1 #484f58);
    border-color: #58a6ff;
    color: #ffffff;
}

QPushButton:pressed {
    background-color: #161b22;
}

/* Glowing Mic Button */
QPushButton#mic_button {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #238636, stop:1 #2ea043);
    border-radius: 25px;
    color: #ffffff;
    font-size: 18px;
    border: 1px solid rgba(46, 160, 67, 0.5);
}

QPushButton#mic_button:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #2ea043, stop:1 #3fb950);
    border-color: #3fb950;
}

QPushButton#mic_button[listening="true"] {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #da3633, stop:1 #f85149);
    border-color: #f85149;
}

/* Emergency Stop Button */
QPushButton#stop_button {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b62324, stop:1 #da3633);
    color: #ffffff;
    border: 1px solid rgba(248, 81, 73, 0.4);
}

QPushButton#stop_button:hover {
    background: #f85149;
}

/* Plan Step List Widget */
QListWidget {
    background-color: rgba(22, 27, 34, 0.6);
    border: 1px solid rgba(48, 54, 61, 0.6);
    border-radius: 10px;
    padding: 6px;
}

QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid rgba(48, 54, 61, 0.4);
    border-radius: 6px;
    margin-bottom: 4px;
}

QListWidget::item:selected {
    background-color: rgba(31, 111, 235, 0.6);
    color: #ffffff;
}

/* Scrollbar Customization */
QScrollBar:vertical {
    background: rgba(13, 17, 23, 0.5);
    width: 8px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: rgba(88, 166, 255, 0.3);
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #58a6ff;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Dialog & Tab Bar */
QDialog {
    background-color: #0d1117;
    border-radius: 12px;
}

QTabBar::tab {
    background: rgba(22, 27, 34, 0.8);
    border: 1px solid #30363d;
    padding: 10px 18px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    color: #8b949e;
}

QTabBar::tab:selected {
    background: #21262d;
    color: #58a6ff;
    border-bottom: 2px solid #58a6ff;
}
"""
