from PyQt6.QtCore import QObject, QThread, pyqtSignal
from server.serv import Serv

class ServeurSignaux(QObject):
    #Cette classe définit les signaux que le serveur va emettre et que l'interface va écouter
    requete_recue = pyqtSignal(str)              # Envoie un texte (log)
    robot_ajoute = pyqtSignal(str)               # Envoie l'ID du nouveau robot
    robot_supprime = pyqtSignal(str)             # Envoie l'ID du robot supprimé
    score_mis_a_jour = pyqtSignal(str, int)      # Envoie l'ID du robot et son nouveau score
    pas_mis_a_jour = pyqtSignal(str, int)        #Envoie l'ID du robot et le nombre de pas restant


class ThreadServeur(QThread):
    #classe pour faire tourner le serveur dans un thread parralèlle 
    
    def __init__(self, chemin_battle, port):
        super().__init__()
        self.chemin_battle = chemin_battle
        self.port = port
        # On instancie les signaux ici pour pouvoir les passer au serveur
        self.signaux = ServeurSignaux() 
        #on instancie le serveur mais on ne le lance pas
        self.serveur = Serv(self.chemin_battle, self.port, self.signaux)

    def run(self):
        # Cette méthode s'exécute dans le thread quand on appellera .start()
        self.serveur.run()