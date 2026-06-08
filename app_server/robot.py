class Robot():
    def __init__(self):
        self.score_final = 0
        self.id = 0
        self.nombreDePasRestants = 0

    def setId(self, id):
        self.id = id
        
    def setNbrDePasRestants(self, nbr):
        self.nombreDePasRestants = nbr
        
    def addToScore_final(self, point):
        self.score_final += point
        print("le score actuel est : ",self.score_final)
        
    def getScore_final(self):
        return self.score_final
    
    def decreaseNbrDePasRestants(self):
        self.nombreDePasRestants -= 1