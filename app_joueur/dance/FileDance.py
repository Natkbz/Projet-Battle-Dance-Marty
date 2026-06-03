class FileDance:
    def __init__(self,path):
        self.file = open(path, 'r')
        self.movement = [] #format: [(dir1,step1),(dir2,step2)]
        self.colorDance = {} #format: {color1 : ([bras1, bras2],expr), color2 : (bras,expr)}
        self.decode()
    
    def close(self):
        self.file.close()
    
    def readLine(self):
        line = self.file.readline()
        return line.rstrip("\n")
    
    def decode(self):
        line = self.readLine()
        firstWord = line.split()[0]
        if(firstWord=="SEQ"):
            line = self.readLine()
            while(line!="ACT"):
                direction = line[-1]
                nb_step = line[:-1]
                self.movement.append((direction,nb_step))
                line = self.readLine()
            if(line=="ACT"):
                line = self.readLine()
                while(line!=""):
                    words = line.split()
                    color = words[0]
                    dance = []
                    expression = 0
                    for i in range(len(words)):
                        if(words[i][0]=="A"):
                            dance.append(words[i])
                        elif(words[i][0]=="X"):
                            expression = words[i]
                    self.colorDance[color] = (dance,expression)
                    line = self.readLine()
            else :                     
                print("Erreur lors du décodage du fichier: Pas de ACT")      
        else : 
            print("Erreur lors du décodage du fichier: Pas de SEQ")
            
    def getMvt(self):
        return self.movement
    
    def getColorDance(self):
        return self.colorDance