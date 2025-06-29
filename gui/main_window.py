import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton
)
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from gui.gatekeeper_response_generator import generate_gatekeeper_response
from world_state_updater import update_world_state

BG_PATH = os.path.join(os.path.dirname(__file__), "assets", "mythic_gate_bg.jpg")

class BackgroundWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.bg_pixmap = QPixmap(image_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)
        scaled_pix = self.bg_pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        x = (self.width() - scaled_pix.width()) // 2
        y = (self.height() - scaled_pix.height()) // 2
        painter.drawPixmap(x, y, scaled_pix)

class GatekeeperGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Approach the Gate")

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        self.setFixedSize(screen.width(), screen.height())

        # Set background widget as central widget of QMainWindow
        self.background = BackgroundWidget(BG_PATH)
        self.setCentralWidget(self.background)

        text_box_style = """
            QTextEdit {
                background-color: rgba(0, 0, 0, 160);
                color: #f8f8f8;
                font-family: 'EB Garamond', serif;
                font-size: 18px;
                border: 2px solid #999;
                border-radius: 10px;
                padding: 10px;
            }
        """

        self.world_state_box = QTextEdit()
        self.world_state_box.setReadOnly(True)
        self.world_state_box.setStyleSheet(text_box_style)

        self.gatekeeper_box = QTextEdit()
        self.gatekeeper_box.setReadOnly(True)
        self.gatekeeper_box.setStyleSheet(text_box_style)

        self.user_input_box = QTextEdit()
        self.user_input_box.setPlaceholderText("Speak to the Gatekeeper...")
        self.user_input_box.setStyleSheet(text_box_style)

        self.submit_btn = QPushButton("Define Actions")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: #fff;
                font-size: 18px;
                font-weight: bold;
                padding: 12px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        self.submit_btn.clicked.connect(self.process_input)

        layout = QVBoxLayout(self.background)
        layout.setSpacing(30)
        layout.setContentsMargins(100, 100, 100, 100)
        layout.addWidget(self.world_state_box)
        layout.addWidget(self.gatekeeper_box)
        layout.addWidget(self.user_input_box)
        layout.addWidget(self.submit_btn)

    def process_input(self):
        user_text = self.user_input_box.toPlainText().strip()
        if not user_text:
            return

        self.user_input_box.clear()

        # Call your actual LLM-based functions here
        gate_response = generate_gatekeeper_response(user_text)
        world_update = update_world_state(user_text)

        # Append responses to text boxes
        self.gatekeeper_box.append(f"Gatekeeper: {gate_response}")
    self.world_state_box.append(f"World State: {world_update}")

def run_app():
    app = QApplication(sys.argv)
    gui = GatekeeperGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_app()

