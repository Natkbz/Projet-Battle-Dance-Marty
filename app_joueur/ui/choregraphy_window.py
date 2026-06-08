from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QTimer

class EyesWidget(QWidget):
    
    def __init__(self, color="#6395EE"):
        super().__init__()
        self.setFixedSize(220, 100)
        self.eye_color = color

    def set_color(self, color: str):
        self.eye_color = color
        self.update()  # force le redessin

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._draw_eye(painter, 20, 10)
        self._draw_eye(painter, 120, 10)

    def _draw_eye(self, painter, x, y):
        size = 80
        painter.setBrush(QColor("#e8f0ff"))
        painter.setPen(QColor(self.eye_color))
        painter.drawEllipse(x, y, size, size)
        pupil_size = 48
        px = x + (size - pupil_size) // 2
        py = y + (size - pupil_size) // 2
        painter.setBrush(QColor(self.eye_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(px, py, pupil_size, pupil_size)
        painter.setBrush(QColor(255, 255, 255, 140))
        painter.drawEllipse(x + 52, y + 14, 16, 16)

class ChoregraphyWindow(QMainWindow):

    def __init__(self, file_path: str, marty, marty_dance_, parent=None):
        super().__init__()
        self.file_path = file_path
        self.marty = marty
        self.marty_dance = marty_dance_
        print(self.marty_dance, marty_dance_)
        self.parent_window = parent
        self.is_running = False

        self.setWindowTitle("Chorégraphie en cours")
        self.setMinimumSize(500, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        central_widget.setLayout(layout)

        # Yeux de Marty
        self.eyes = EyesWidget(color="#6395EE")
        layout.addWidget(self.eyes, alignment=Qt.AlignmentFlag.AlignCenter)

        # Statut
        self.status_label = QLabel("Prêt à lancer")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName("heading")
        layout.addWidget(self.status_label)

        # Nom du fichier
        file_name = file_path.split("/")[-1]
        file_label = QLabel(f"{file_name}")
        file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_label.setObjectName("subheading")
        layout.addWidget(file_label)

        # Bouton lancer
        self.btn_start = QPushButton("▶  Lancer")
        self.btn_start.setObjectName("btn_primary")
        self.btn_start.clicked.connect(self.on_start)
        layout.addWidget(self.btn_start)

    def on_start(self):
        self.is_running = True
        self.eyes.set_color("#6395EE")  # bleu = en cours
        self.status_label.setText("Chorégraphie en cours...")
        self.btn_start.setVisible(False)
        
        score = self.marty_dance.dance()
        
        self.status_label.setText(f"Score : {score}/100")
        self.eyes.set_color("#88CFA8")  # Vert = terminé
        self.btn_start.setVisible(True)
        
    def _return_to_control(self):
        self.close()
        if self.parent_window:
            self.parent_window.show()

    def closeEvent(self, event):
        if self.parent_window:
            self.parent_window.show()
        event.accept()