import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt

class FileWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration de l'Arbitre")
        self.setMinimumSize(800, 600)
        
        self.chemin_battle = ""

        #Création du widget central 
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        # Création du Layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Titre tout en haut
        self.title_label = QLabel("Lancement du serveur arbitre")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Bouton de recherche de fichier
        self.btn_browse = QPushButton("Choisir un fichier .battle")
        self.btn_browse.setObjectName("btnBrowse") 
        self.btn_browse.setMinimumHeight(45)
        self.btn_browse.clicked.connect(self.on_browse)
        layout.addWidget(self.btn_browse)

        # Label discret
        self.file_label = QLabel("")
        self.file_label.setObjectName("fileLabel")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.file_label)

        # 6. Bouton "Lancer le serveur"
        self.btn_start = QPushButton("Lancer le serveur")
        self.btn_start.setObjectName("btnStart") 
        self.btn_start.setMinimumHeight(45)
        self.btn_start.clicked.connect(self.on_start)
        self.btn_start.hide() 
        layout.addWidget(self.btn_start)

    def on_browse(self):
        """Ouvre l'explorateur filtré UNIQUEMENT sur les fichiers .battle."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner le fichier de battle", 
            "", 
            "Fichiers Battle (*.battle)" 
        )
        
        if file_path:
            self.chemin_battle = file_path
            nom_fichier = os.path.basename(file_path)
            self.file_label.setText(f"Fichier chargé : {nom_fichier}")
            self.btn_start.show()

    def on_start(self):
        """Se déclenche au clic sur 'Lancer le serveur'."""
        if not self.chemin_battle or not os.path.isfile(self.chemin_battle):
            self.file_label.setText("Erreur : Fichier introuvable.")
            return

        # Création de MainWindow
        print("lancement du serveur")