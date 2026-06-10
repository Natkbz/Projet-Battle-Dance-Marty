import os
from PyQt6.QtWidgets import (
    QFileDialog, QMainWindow, QPushButton, QWidget, QVBoxLayout, 
    QLabel, QTableWidget, QTableWidgetItem, QTextEdit, QAbstractItemView
)
from PyQt6.QtCore import Qt

class ServerWindow(QMainWindow):
    def __init__(self,thread_serveur):
        super().__init__()
        #initialisation du thread_server pour pouvoir lui transmettre des infos
        self.thread_serveur = thread_serveur
        
        #titre et taille de la fenêtre
        self.setWindowTitle("Tableau de Bord - Arbitre Battle")
        self.setMinimumSize(800, 600)

        # Widget central principal
        central_widget = QWidget()
        central_widget.setObjectName("serverWindowCentral")
        self.setCentralWidget(central_widget)

        # Layout vertical
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Label pour l'IP et le Port du serveur
        self.lbl_info_serveur = QLabel("Serveur hors ligne")
        self.lbl_info_serveur.setObjectName("lblInfoServeur") 
        self.lbl_info_serveur.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_info_serveur)
        
        #Bouton pour changer de fichier .battle -
        self.btn_change_battle = QPushButton("Changer de fichier .battle")
        self.btn_change_battle.setObjectName("btnChangeBattle")
        self.btn_change_battle.setMinimumHeight(35)
        self.btn_change_battle.clicked.connect(self.on_change_battle)
        layout.addWidget(self.btn_change_battle)
        
        # titre au dessus du tableau des Robots
        lbl_robots = QLabel("Robots connectés en direct")
        lbl_robots.setObjectName("lblRobots")
        layout.addWidget(lbl_robots)

        # Création du tableau à 2 colonnes (ID et Score)
        self.tableau_robots = QTableWidget(0, 2) #création tableau 0ligne et 2 colonne
        self.tableau_robots.setObjectName("tableauRobots")
        self.tableau_robots.setHorizontalHeaderLabels(["ID du Robot", "Score Final"])

        self.tableau_robots.horizontalHeader().setStretchLastSection(True) #force la colonne score a s'étirer
        self.tableau_robots.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) #on empeche de modifier la case en cliquant dessus
        self.tableau_robots.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection) #on empeche de selectionner une case en cliquant dessus 
        layout.addWidget(self.tableau_robots)

        # Console de Logs 
        lbl_logs = QLabel("Console des requêtes reçues")
        lbl_logs.setObjectName("lblLogs")
        layout.addWidget(lbl_logs)

        # Zone de texte typée "Console" ou on ne peut pas écrire mais scroll
        self.console = QTextEdit()
        self.console.setObjectName("consoleLogs")
        self.console.setReadOnly(True) 
        layout.addWidget(self.console)
    
    def set_server_info(self, ip, port):
        #Met à jour le texte de l'adresse IP
        self.lbl_info_serveur.setText(f"Serving at port : {port}, on IP : {ip}")
    
    def ajouter_log(self, message):
        #ajoute un message dans la console
        self.console.append(message)

    def ajouter_robot(self, robot_id):
        #ajoute un robot au tableau
        
        if self._trouver_ligne_robot(robot_id) != -1:
            #on ne peut pas ajouter un robot existant
            return

        #ajout d'une nouvelle ligne dans le tableau
        ligne = self.tableau_robots.rowCount()
        self.tableau_robots.insertRow(ligne)
        
        #ajout de l'id ds la première colonne de la nouvelle ligne
        item_id = QTableWidgetItem(robot_id)
        item_id.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tableau_robots.setItem(ligne, 0, item_id)
        
        #ajout du scrore dans la deuxième colonne de la nouvelle ligne
        item_score = QTableWidgetItem("0")
        item_score.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tableau_robots.setItem(ligne, 1, item_score)

    def supprimer_robot(self, robot_id):
        #on recup la ligne correspondant au robot et on le supprime
        ligne = self._trouver_ligne_robot(robot_id)
        if ligne != -1:
            #si on l'a trouvé
            self.tableau_robots.removeRow(ligne)

    def mettre_a_jour_score(self, robot_id, nouveau_score):
        #on change l'item score du robot en question
        ligne = self._trouver_ligne_robot(robot_id)
        if ligne != -1:
            #si on la trouver on change la deuxième colonne de la ligne du robot
            item_score = QTableWidgetItem(str(nouveau_score))
            item_score.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tableau_robots.setItem(ligne, 1, item_score)

    def _trouver_ligne_robot(self, robot_id):
        #cherche la ligne du robot 
        for ligne in range(self.tableau_robots.rowCount()):
            item = self.tableau_robots.item(ligne, 0)
            if item and item.text() == robot_id:
                return ligne
        return -1
    
    def on_change_battle(self):
        #Ouvre l'explorateur pour choisir un nouveau fichier et met à jour le serveur.
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Sélectionner un nouveau fichier de battle", 
            "", 
            "Fichiers Battle (*.battle)" 
        )
        
        if file_path:
            # Appel de la fonction du server pour lui donner le changement 
            self.thread_serveur.serveur.updateBattle(file_path)
            
            # ajout ds la console du changement de fichier
            nom_fichier = os.path.basename(file_path)
            self.ajouter_log(f"Nouveau fichier chargé : {nom_fichier}")