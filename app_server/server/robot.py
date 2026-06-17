class Robot():
    def __init__(self):
        self.score_final = 0
        self.id = 0
        self.nombreDePasRestants = 0

    def setId(self, id):
        self.id = id
        
    def setNbrDePasRestants(self, nbr):
        self.nombreDePasRestants = nbr
        
    def setScore(self, score):
        self.score_final = score
        
    def addToScore_final(self, point):
        self.score_final += point
        
    def getScore_final(self):
        return self.score_final
    
    def decreaseNbrDePasRestants(self):
        self.nombreDePasRestants -= 1
        
    def getNbrDePasRestants(self):
        return self.nombreDePasRestants
    
    def setRegles(self, regles_du_serveur):
        # On enregistre une copie des regles si jamais le fichier est changer pdt la battle
        self.regles = regles_du_serveur.copy()
        
    def getRegles(self):
        return self.regles