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
        
        f = open(chemin_battle)
        #le nombre de pas est le deuxième mot de la premère ligne du .battle
        line = f.readline()
        tab = line.split(" ")
        self.nombreDePasBattle = str(tab[1])
        f.close()
        
    def getIpServer(self):
        hostname = socket.gethostname()
        ip_locale = socket.gethostbyname(hostname)
        
        return ip_locale
    
    def updateBattle(self, newChemin):
        #on change de .battle donc on récupère à nouveau le nombre de pas
        self.chemin_battle = newChemin
        
        f = open(newChemin)
        line = f.readline()
        tab = line.split(" ")
        self.nombreDePasBattle = str(tab[1])
        f.close()

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
                
    def calculPoint(self, col, arm, exp):
        res = 0
        
        f = open(self.chemin_battle)
        
        while(True):
            line = f.readline()
            if(line == f"[{col}]" or line == f"[{col}]\n"):
                break
            elif(line == "" or line == "\n"):
                return str(res)
            
        nextLine = f.readline()
        
        while(nextLine[0] != "["):
            splitEgal = nextLine.split("=")
            splitVirgule = splitEgal[0].split(",")
            for i in range(0, len(splitVirgule)):
                if(exp == splitVirgule[i]):
                    res += int(splitEgal[1])
                    print("exp")
                if(len(arm) > 4):
                    if(arm == splitVirgule[i]):
                        res += int(splitEgal[1])
                        print("a+b = a+b")
                    elif(arm[0:3] == splitVirgule[i]):
                        res += int(splitEgal[1])
                        print("a+b = a")
                    elif(arm[4::] == splitVirgule[i]):
                        res += int(splitEgal[1])
                        print(f"a+b = b")
                else:
                    if(arm == splitVirgule[i]):
                        res += int(splitEgal[1])
                        print("arm")
            nextLine = f.readline()
            if(nextLine == "" or nextLine == "\n"):
                return str(res)
        
        f.close()
        return str(res)