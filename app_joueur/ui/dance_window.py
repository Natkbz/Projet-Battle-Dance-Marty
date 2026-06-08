from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class DanceWindow(QMainWindow):

    def __init__(self, file_path: str, parent=None):
        super().__init__()
        self.file_path = file_path
        self.parent_window = parent
        self.server_connected = False

        self.setWindowTitle("Dance")
        self.setMinimumSize(600, 500)
        self.setWindowIcon(QIcon("app_joueur/assets/images/robot_icon.png"))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_widget.setLayout(outer_layout)

        # Carte principale
        card = QWidget()
        card.setObjectName("form_card")
        card.setFixedWidth(400)
        outer_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(10)
        card.setLayout(layout)

        # Titre
        heading = QLabel("Chorégraphie")
        heading.setAlignment(Qt.AlignmentFlag.AlignCenter)
        heading.setObjectName("heading")
        layout.addWidget(heading)

        # Nom du fichier importé
        file_name = file_path.split("/")[-1]
        file_label = QLabel(f"{file_name}")
        file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        file_label.setObjectName("subheading")
        layout.addWidget(file_label)

        layout.addSpacing(16)

        # Séparateur
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #e0eaf8;")
        layout.addWidget(sep)

        layout.addSpacing(8)

        # Connexion serveur
        server_label = QLabel("ADRESSE IP DU SERVEUR")
        server_label.setObjectName("input_label")
        layout.addWidget(server_label)

        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Ex : 192.168.1.10")
        layout.addWidget(self.ip_input)

        self.btn_connect_server = QPushButton("Se connecter au serveur")
        self.btn_connect_server.setObjectName("btn_primary")
        self.btn_connect_server.clicked.connect(self.on_connect_server)
        layout.addWidget(self.btn_connect_server)

        self.status_label = QLabel("Non connecté au serveur")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setObjectName("status")
        layout.addWidget(self.status_label)

        layout.addSpacing(16)

        # Bouton lancer chorégraphie (caché au départ)
        self.btn_launch = QPushButton("▶  Lancer la chorégraphie")
        self.btn_launch.setObjectName("btn_primary")
        self.btn_launch.clicked.connect(self.on_launch)
        self.btn_launch.setVisible(False)  # caché jusqu'à connexion serveur
        layout.addWidget(self.btn_launch)

    def on_connect_server(self):
        ip = self.ip_input.text().strip()

        # validation IP
        parts = ip.split(".")
        if len(parts) != 4 or any(not p.isdigit() or int(p) not in range(256) for p in parts):
            self._set_status("Adresse IP invalide", "status_error")
            return

        self._set_status("Connexion en cours...", "status")

        # simulé pour l'instant
        success = True

        if success:
            self.server_connected = True
            self._set_status(f"Connecté au serveur {ip} !", "status_ok")
            self.btn_launch.setVisible(True)  # on affiche le bouton
        else:
            self._set_status("Connexion au serveur échouée", "status_error")

    def on_launch(self):
        # test avec un print
        print(f"Lancement de la chorégraphie : {self.file_path}")

    def _set_status(self, message: str, style_name: str):
        self.status_label.setText(message)
        self.status_label.setObjectName(style_name)
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)
    
    def closeEvent(self):
        if self.parent_window:
            self.parent_window.show()
        event.accept() # marque un event comme traité donc pas de propragation
    
    