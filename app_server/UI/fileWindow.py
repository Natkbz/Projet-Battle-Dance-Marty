import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog
)
from PyQt6.QtCore import Qt
from UI.serverWindow import ServerWindow
from server.network_thread import ThreadServeur

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

        # Label où on écrira le nom du fichier chargé
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
        #Ouvre l'explorateur filtré UNIQUEMENT sur les fichiers .battle.
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner le fichier de battle", 
            "", 
            "Fichiers Battle (*.battle)" 
        )
        
        if file_path:
            self.chemin_battle = file_path
            #récupération du nom du fichier à partir du chemin
            nom_fichier = os.path.basename(file_path)
            #on affiche le nom du fichier chargé
            self.file_label.setText(f"Fichier chargé : {nom_fichier}")
            #on peut afficher le bouton pour lancer le serveur
            self.btn_start.show()

    def on_start(self):
        #Se déclenche au clic sur 'Lancer le serveur'. On lance alors le serveur et l'interface graphique en les reliant via les signaux
        if not self.chemin_battle or not os.path.isfile(self.chemin_battle):
            self.file_label.setText("Erreur : Fichier introuvable.")
            return

        print("lancement du serveur...")
        # Création du serveur en arrière-plan
        port = 8080
        self.thread_serveur = ThreadServeur(self.chemin_battle, port)
        #Création de la fenêtre du tableau de bord
        self.server_window = ServerWindow(self.thread_serveur)
        #on recup l'ip et on l'affiche sur l'interface
        ip_locale = self.thread_serveur.serveur.getIpServer()
        self.server_window.set_server_info(ip_locale, port)
        
        # On relie les signaux du serveur aux méthode de la fenêtre
        self.thread_serveur.signaux.requete_recue.connect(self.server_window.ajouter_log)
        self.thread_serveur.signaux.robot_ajoute.connect(self.server_window.ajouter_robot)
        self.thread_serveur.signaux.robot_supprime.connect(self.server_window.supprimer_robot)
        self.thread_serveur.signaux.score_mis_a_jour.connect(self.server_window.mettre_a_jour_score)
        
        # Lancement du serveur dans un thread
        self.thread_serveur.start()
        
        # On ajoute des  messages dans la console pour annoncé le lancement du serveur
        self.server_window.ajouter_log("################################################")
        self.server_window.ajouter_log(f"Fichier de battle chargé : {self.chemin_battle}")
        self.server_window.ajouter_log(f"Serveur arbitre en écoute sur le port {port}...")
        self.server_window.ajouter_log("################################################\n")
        
        #Affichage du tableau de bord et fermeture de la fenêtre de config
        self.server_window.show()
        self.hide()