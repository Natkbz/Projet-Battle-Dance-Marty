import sys
from PyQt6.QtWidgets import (
    QMainWindow, QLineEdit, QLabel,
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QFont, QPainter, QColor
from robot.MartyContext import MartyContext
from ui.control_window import ControlWindow


# widget = tout élément visible à l'écran (bouton, label etc...)
# layout = gestionnaire invisible pour organiser les widgets

class EyesWidget(QWidget):
    """Widget qui dessine les yeux de Marty en CSS/QPainter."""

    def __init__(self):
        super().__init__()
        self.setFixedSize(220, 100)

    # méthode héritée de QWidget
    # appellée automatiquement chaque fois qu'il faut redessiner le widget (ouverture, redimensionnnement, de la fenêtre)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) # lissage des bords

        # oeil gauche
        self._draw_eye(painter, 20, 10)
        # oeil droit
        self._draw_eye(painter, 120, 10)

    def _draw_eye(self, painter, x, y):
        size = 80
        
        # fond de l'oeil
        painter.setBrush(QColor("#e8f0ff"))
        painter.setPen(QColor("#6395EE"))
        painter.drawEllipse(x, y, size, size)

        # pupille
        pupil_size = 48
        px = x + (size - pupil_size) // 2 # centrer la pupille dans l'oeil
        py = y + (size - pupil_size) // 2
        painter.setBrush(QColor("#6395EE"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(px, py, pupil_size, pupil_size)

        # reflet
        painter.setBrush(QColor(255, 255, 255, 140))
        painter.drawEllipse(x + 52, y + 14, 16, 16)

class ConnectionWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("NDDance")
        self.setMinimumSize(800, 600)
        self.setWindowIcon(QIcon("approbot/assets/images/robot_icon.png"))

        self.marty = None # instance de la classe pour contrôler le robot

        # widget central (fond)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # layout principal (vertical) contenant les yeux, marty-nddance, la carte blanche
        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_widget.setLayout(outer_layout)

        # yeux de Marty
        self.eyes = EyesWidget()
        outer_layout.addWidget(self.eyes, alignment=Qt.AlignmentFlag.AlignCenter)

        # label "Marty · NDDance"
        app_label = QLabel("MARTY · NDDANCE")
        app_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_label.setStyleSheet("color: #90B8D6; font-size: 10px; letter-spacing: 3px;")
        outer_layout.addWidget(app_label)
        outer_layout.addSpacing(16)

        # carte blanche du formulaire
        form_card = QWidget()
        form_card.setObjectName("form_card")
        form_card.setFixedWidth(360)
        outer_layout.addWidget(form_card, alignment=Qt.AlignmentFlag.AlignCenter)

        # layout intérieur de la carte
        layout = QVBoxLayout()
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(8)
        form_card.setLayout(layout)

        # titre
        heading = QLabel("Connexion au robot")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setObjectName("heading")

        # sous-titre
        subheading = QLabel("Entrez l'adresse IP de votre Marty")
        subheading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subheading.setObjectName("subheading")

        # label champ IP
        input_label = QLabel("ADRESSE IP")
        input_label.setObjectName("input_label")

        # champ IP
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Ex : 192.168.1.42")

        # label statut
        self.status_label = QLabel("Non connecté")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName("status")

        # bouton connexion
        self.btn_connect = QPushButton("Se connecter")
        self.btn_connect.setObjectName("btn_primary")
        self.btn_connect.clicked.connect(self.on_connect)

        # séparateur "ou"
        or_layout = QHBoxLayout()
        line_left = QFrame()    
        line_left.setFrameShape(QFrame.Shape.HLine) # widget pour afficher une ligne horizontale
        line_left.setStyleSheet("color: #e0eaf8;")
        or_label = QLabel("ou")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        or_label.setStyleSheet("color: #aabbcc; font-size: 11px;")
        line_right = QFrame()
        line_right.setFrameShape(QFrame.Shape.HLine)
        line_right.setStyleSheet("color: #e0eaf8;")
        or_layout.addWidget(line_left)
        or_layout.addWidget(or_label)
        or_layout.addWidget(line_right)

        # bouton secondaire recherche automatique
        self.btn_auto = QPushButton("Recherche automatique")
        self.btn_auto.setObjectName("btn_secondary")
        self.btn_auto.clicked.connect(self.on_auto_search)

        # ajout de tous les éléments dans la carte (ordre de haut en bas)
        layout.addWidget(heading)
        layout.addWidget(subheading)
        layout.addSpacing(16)
        layout.addWidget(input_label)
        layout.addWidget(self.ip_input)
        layout.addSpacing(4)
        layout.addWidget(self.btn_connect)
        layout.addLayout(or_layout)
        layout.addWidget(self.btn_auto)
        layout.addSpacing(8)
        layout.addWidget(self.status_label)

    def on_connect(self):
        ip = self.ip_input.text().strip()

        # validation du format IPv4
        parts = ip.split(".")
        if len(parts) != 4 or any(not p.isdigit() or int(p) not in range(256) for p in parts):
            self._set_status("Adresse IP invalide", "status_error")
            return

        self._set_status("Connexion en cours...", "status")
        self.marty = MartyContext(ip)
        success = self.marty.connect()
        #self.marty = MartyContext(ip)
        #self.marty.marty = None
        #success = True

        if success:
            self._set_status(f"Connecté à {ip} !", "status_ok")
            self.marty.CalibrateColor()
            self._open_control_window()
        else:
            self._set_status("Connexion échouée", "status_error")

    def on_auto_search(self):
        # a implémenter plus tard (idée : nslookup)
        self._set_status("Recherche en cours...", "status")

    def _set_status(self, message: str, style_name: str):
        """Met à jour le label de statut et son style."""
        self.status_label.setText(message) # change le texte affiché par le label
        self.status_label.setObjectName(style_name) # change le nom du label pour que le qss lui applique un style différent
        # PyQt6 ne recharge pas automatiquement le style quand on change l'objectName
        self.status_label.style().unpolish(self.status_label) # dit a qt : oublie le style actuel de ce widget
        self.status_label.style().polish(self.status_label) # recalcule et applique le nouveau style

    def _open_control_window(self):
        self.control_window = ControlWindow(self.marty)
        self.control_window.show()
        self.hide()