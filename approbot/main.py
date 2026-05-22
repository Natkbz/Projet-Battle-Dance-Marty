import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QFont

# classe MainWindow qui hérite de QMainWindow 
# et qui permet de personnaliser les fenêtres 
# qu'on affichent à l'utiilsateur 
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NDDance")
        self.setMinimumSize(800,600)
        self.setWindowIcon(QIcon("approbot/assets/images/robot_icon.png")) # icône de la fenêtre (à définir)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal pour centrer tous les éléments 
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_widget.setLayout(main_layout)
        
        # Conteneur de largeur limitée
        container = QWidget()
        container.setFixedWidth(400)
        container.setObjectName("container")
        main_layout.addWidget(container)
        
        # Layout du conteneur
        layout = QVBoxLayout()
        layout.setSpacing(12)
        container.setLayout(layout)
        
        heading = QLabel("Connectez vous à un robot")
        heading.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        heading.setObjectName("heading")
        
        subheading = QLabel("Entrer l'adresse IP du robot")
        subheading.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        subheading.setObjectName("subheading")

        self.ip = QLineEdit()
        self.ip.setPlaceholderText("Ex: 192.168.1.42")

        # Label de statut (vide au départ)
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.status_label.setObjectName("status")

        # Bouton connexion
        self.btn_connect = QPushButton("Se connecter")
        self.btn_connect.clicked.connect(self.submit)
        
        layout.addWidget(heading)
        layout.addWidget(subheading)
        layout.addSpacing(20)
        layout.addWidget(QLabel("Adresse IP :"))
        layout.addWidget(self.ip)
        layout.addWidget(self.status_label)
        layout.addWidget(self.btn_connect)

    def submit(self):
        ip = self.ip.text().strip()
        
        # Vérifie si l'ip rentré est bien au format ipv4
        ip_parts = ip.split(".")
        if len(ip_parts) == 4 and all(p.isdigit() and 0 <= int(p) <= 255 for p in ip_parts):
            self.status_label.setText(f"Connexion à {ip}...")
            self.status_label.setObjectName("status_ok")
            # appeler vraie connexion au Marty plus tard
        else:
            self.status_label.setText(f"Adresse IP invalide")
            self.status_label.setObjectName("status_error")
            
        # Forcer le rechargement du style après changement d'objectName
        self.status_label.style().unpolish(self.status_label)
        self.status_label.style().polish(self.status_label)

app = QApplication(sys.argv)
with open("approbot/styles/robot-connection.qss", "r") as f:
    app.setStyleSheet(f.read())
window = MainWindow()
window.show()
sys.exit(app.exec())


