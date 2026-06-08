from dance.FileDance import FileDance
from robot.MartyContext import MartyContext
from client.APIClient import Client
class MartyDance:
    def __init__(self,path,marty_,ip):
        self.marty = marty_
        self.file_dance = FileDance(path)
        self.move = self.file_dance.getMvt()
        self.colorDance = self.file_dance.getColorDance()
        self.client = Client(ip,8080)
    
    def test_fichier(self):
        if not self.move:
            return False
        if not self.colorDance:
            return False
        return True
        
    def test_connection(self):
        connected = self.client.testConnection()
        if(connected):
            self.id = self.client.getId()
        return connected
    
    def dance(self):
        self.nb_move = int(self.client.start(self.id))
        self.adjust_nb_move()
        for i in range(self.nb_move):
            print("mouvement ",i)
            self.execute_mouvement(i)
            self.marty.normal(1500)
            self.check_color()
        return self.client.getScore(self.id)
            
    def adjust_nb_move(self):
        if(len(self.move)>self.nb_move):
            self.move= self.move[:self.nb_move]
        else:
            for i in range(self.nb_move-len(self.move)):
                self.move.append(self.move[i])
                
                
    def execute_mouvement(self,n_move):
        self.marty.move_foot(self.move[n_move][0], int(self.move[n_move][1]))
        
    def check_color(self):
        color = self.marty.getColor()
        print(color)
        if color in self.colorDance:
            bras = self.colorDance[color][0]
            expressionToDo = self.colorDance[color][1]
            for i in range(len(bras)):
                self.marty.move_arm(bras[i])
            self.marty.expression(expressionToDo)
            arm = "+".join(bras)
            self.client.sendStep(self.id,color,arm,expressionToDo)