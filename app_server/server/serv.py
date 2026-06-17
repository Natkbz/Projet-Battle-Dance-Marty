import http.server
import socket
from server.robot import Robot
from server.handler import Handler

class Serv():
    port = 8080
    nombreDePasBattle = 0
    chemin_battle = ""
    liste_robots = []
    
    def __init__(self, chemin_battle, port,signaux):
        self.port = port
        self.chemin_battle = chemin_battle
        
        #definition de signaux pour que handler les utilise
        self.signaux = signaux
        
        self.charger_regles_battle(self.chemin_battle)
    
    def charger_regles_battle(self, chemin):
        """Lit le fichier .battle une seule fois et le stocke en mémoire."""
        self.regles_points = {}#format {color:{arm:ptn,arm,ptn,amr+arm:ptn,exp:ptn}}
        with open(chemin, "r", encoding="utf-8") as f:
            lignes = f.readlines()
            
            # Le nombre de pas est le dernier mot de la première ligne
            premiere_ligne = lignes[0].strip().split(" ")
            self.nombreDePasBattle = str(premiere_ligne[-1])
            
            # Construction du dictionnaire de règles
            couleur_actuelle = ""
            for ligne in lignes[1:]:
                ligne = ligne.strip()
                if not ligne: 
                    continue
                
                # Détection d'une couleur (ex: [N])
                if ligne.startswith("[") and ligne.endswith("]"):
                    couleur_actuelle = ligne[1:-1]
                    self.regles_points[couleur_actuelle] = {}
                
                # Détection d'une règle (ex: ALB,ARB=-1)
                elif "=" in ligne and couleur_actuelle:
                    gauche, droite = ligne.split("=")
                    points = int(droite)
                    elements = gauche.split(",")
                    for element in elements:
                        self.regles_points[couleur_actuelle][element] = points
    
    def getIpServer(self):
        """hostname = socket.gethostname()
        ip_locale = socket.gethostbyname(hostname)
        
        return ip_locale"""
        try:
            # On crée un socket fictif
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            # on simule une connexion vers le routeur des robots.
            s.connect(("192.168.1.254", 80)) 
            
            ip_locale = s.getsockname()[0]
            s.close()
            return ip_locale
        except Exception as e:
            print(f"Erreur de détection d'IP : {e}")
            # Fallback local
            return "127.0.0.1"
    
    def updateBattle(self, newChemin):
        #on change de .battle donc on récupère à nouveau les regles
        self.chemin_battle = newChemin
        self.charger_regles_battle(self.chemin_battle)

    def run(self) :

        server = http.server.HTTPServer((self.getIpServer(), self.port), Handler)
        server.serv_instance = self
        print("serving at port :", self.port, " on ip : ", self.getIpServer())
        server.serve_forever()

    def recherche_robot(self, id):
        for i in range(len(self.liste_robots)):
            if(self.liste_robots[i].id == id):
                return self.liste_robots[i]
        exception = Exception("Robot non trouvé")
        raise exception
            
    def supprimer_robot(self, id):
        for i in range(len(self.liste_robots)):
            if(self.liste_robots[i].id == id):
                self.liste_robots.pop(i)
                
    def ajouter_robot(self, robot):
        self.liste_robots.append(robot)
        
    def getNombreDePasBattle(self):
        return str(self.nombreDePasBattle)
    
    def calculPoint(self, col, arm, exp,regle_du_robot):
        res = 0
        
        # Si la couleur n'existe pas dans le fichier, on retourne 0
        if col not in regle_du_robot:
            return "0"
            
        regles = regle_du_robot[col]
        
        # 1. Calcul des points de l'expression
        if exp in regles:
            res += regles[exp]
            print(f"exp ({exp}) rapporte {regles[exp]} points")
            
        # 2. Calcul des points des arm
        if "+" in arm and arm in regles:
            res += regles[arm]
            print(f"Combinaison complète ({arm}) rapporte {regles[arm]} points")
            

        # On découpe la chaîne si jamais c'était un +
        sous_armes = arm.split("+")
        for a in sous_armes:
            if a in regles:
                res += regles[a]
                print(f"Arme individuelle ({a}) rapporte {regles[a]} points")
                    
        return str(res)
                    